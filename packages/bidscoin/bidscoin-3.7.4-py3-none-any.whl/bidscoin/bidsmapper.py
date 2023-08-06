#!/usr/bin/env python3
"""
The bidsmapper scans your source data repository to identify different data types by matching
them against the run-items in the template bidsmap. Once a match is found, a mapping to BIDS
output data types is made and the run-item is added to the study bidsmap. You can check and edit
these generated bids-mappings to your needs with the (automatically launched) bidseditor. Re-run
the bidsmapper whenever something was changed in your data acquisition protocol and edit the new
data type to your needs (your existing bidsmap will be re-used).

The bidsmapper uses plugins, as stored in the bidsmap['Options'], to do the actual work
"""

# Global imports (plugin modules may be imported when needed)
import argparse
import textwrap
import copy
import logging
import sys
import shutil
import re
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from pathlib import Path
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMessageBox
try:
    from bidscoin import bidscoin, bids, bidseditor
except ImportError:
    import bidscoin, bids, bidseditor         # This should work if bidscoin was not pip-installed


localversion, versionmessage = bidscoin.version(check=True)


def bidsmapper(rawfolder: str, bidsfolder: str, bidsmapfile: str, templatefile: str, plugins: list, subprefix: str, sesprefix: str, store: bool=False, noedit: bool=False, force: bool=False) -> None:
    """
    Main function that processes all the subjects and session in the sourcefolder
    and that generates a maximally filled-in bidsmap.yaml file in bidsfolder/code/bidscoin.
    Folders in sourcefolder are assumed to contain a single dataset.

    :param rawfolder:       The root folder-name of the sub/ses/data/file tree containing the source data files
    :param bidsfolder:      The name of the BIDS root folder
    :param bidsmapfile:     The name of the bidsmap YAML-file
    :param templatefile:    The name of the bidsmap template YAML-file
    :param plugins:         Optional list of plugins that should be used (overrules the list in the study/template bidsmaps)
    :param subprefix:       The prefix common for all source subject-folders
    :param sesprefix:       The prefix common for all source session-folders
    :param store:           If True, the provenance samples will be stored
    :param noedit:          The bidseditor will not be launched if True
    :param force:           If True, the previous bidsmap and logfiles will be deleted
    :return:
    """

    # Input checking
    rawfolder      = Path(rawfolder).resolve()
    bidsfolder     = Path(bidsfolder).resolve()
    bidsmapfile    = Path(bidsmapfile)
    templatefile   = Path(templatefile)
    bidscoinfolder = bidsfolder/'code'/'bidscoin'
    metasubprefix  = [char for char in subprefix or '' if char in ('^', '$', '+', '{', '}', '[', ']', '\\', '|', '(', ')')]
    metasesprefix  = [char for char in sesprefix or '' if char in ('^', '$', '+', '{', '}', '[', ']', '\\', '|', '(', ')')]

    # Start logging
    if force:
        (bidscoinfolder/'bidsmapper.log').unlink(missing_ok=True)
    bidscoin.setup_logging(bidscoinfolder/'bidsmapper.log')
    LOGGER.info('')
    LOGGER.info('-------------- START BIDSmapper ------------')
    LOGGER.info(f">>> bidsmapper sourcefolder={rawfolder} bidsfolder={bidsfolder} bidsmap={bidsmapfile} "
                f"template={templatefile} plugins={plugins} subprefix={subprefix} sesprefix={sesprefix} store={store} force={force}")
    if metasubprefix:
        LOGGER.warning(f"Regular expression metacharacters {metasubprefix} found in {subprefix}, this may cause errors later on...")
    if metasesprefix:
        LOGGER.warning(f"Regular expression metacharacters {metasesprefix} found in {sesprefix}, this may cause errors later on...")

    # Get the heuristics for filling the new bidsmap
    bidsmap_old, bidsmapfile = bids.load_bidsmap(bidsmapfile,  bidscoinfolder, plugins)
    template, _              = bids.load_bidsmap(templatefile, bidscoinfolder, plugins)

    # Create the new bidsmap as a copy / bidsmap skeleton with no datatype entries (i.e. bidsmap with empty lists)
    if force:
        bidsmapfile.unlink(missing_ok=True)
        bidsmap_old = {}
    if bidsmap_old:
        bidsmap_new = copy.deepcopy(bidsmap_old)
    else:
        bidsmap_new = copy.deepcopy(template)
    template['Options'] = bidsmap_new['Options']                # Always use the options of the new bidsmap
    bidscoindatatypes   = bidsmap_new['Options']['bidscoin'].get('datatypes',[])
    unknowndatatypes    = bidsmap_new['Options']['bidscoin'].get('unknowntypes',[])
    ignoredatatypes     = bidsmap_new['Options']['bidscoin'].get('ignoretypes',[])
    for dataformat in bidsmap_new:
        if dataformat in ('Options','PlugIns'): continue        # Handle legacy bidsmaps (-> 'PlugIns')
        for datatype in bidscoindatatypes + unknowndatatypes + ignoredatatypes:
            if bidsmap_new[dataformat].get(datatype):
                bidsmap_new[dataformat][datatype] = None

    # Store/retrieve the empty or user-defined sub-/ses-prefix
    subprefix, sesprefix = setprefix(bidsmap_new, subprefix, sesprefix, rawfolder)

    # Start with an empty skeleton if we didn't have an old bidsmap
    if not bidsmap_old:
        bidsmap_old = copy.deepcopy(bidsmap_new)
        bidsmapfile = bidscoinfolder/'bidsmap.yaml'

    # Import the data scanning plugins
    plugins = [bidscoin.import_plugin(plugin, ('bidsmapper_plugin',)) for plugin in bidsmap_new['Options']['plugins']]
    plugins = [plugin for plugin in plugins if plugin]          # Filter the empty items from the list
    if not plugins:
        LOGGER.warning(f"The plugins listed in your bidsmap['Options'] did not have a usable `bidsmapper_plugin` function, nothing to do")
        LOGGER.info('-------------- FINISHED! ------------')
        LOGGER.info('')
        return

    # Loop over all subjects and sessions and built up the bidsmap entries
    subjects = bidscoin.lsdirs(rawfolder, (subprefix if subprefix!='*' else '') + '*')
    if not subjects:
        LOGGER.warning(f'No subjects found in: {rawfolder/subprefix}*')
    with logging_redirect_tqdm():
        for n, subject in enumerate(tqdm(subjects, unit='subject', leave=False), 1):

            sessions = bidscoin.lsdirs(subject, (sesprefix if sesprefix!='*' else '') + '*')
            if not sessions or (subject/'DICOMDIR').is_file():
                sessions = [subject]
            for session in sessions:

                LOGGER.info(f"Mapping: {session} (subject {n}/{len(subjects)})")

                # Unpack the data in a temporary folder if it is tarballed/zipped and/or contains a DICOMDIR file
                sesfolders, unpacked = bids.unpack(session)
                for sesfolder in sesfolders:
                    if store:
                        store = {'source': sesfolder.parent.parent.parent.parent if unpacked else rawfolder.parent, 'target': bidscoinfolder/'provenance'}
                    else:
                        store = {}

                    # Run the bidsmapper plugins
                    for module in plugins:
                        LOGGER.info(f"Executing plugin: {Path(module.__file__).name} -> {sesfolder}")
                        module.bidsmapper_plugin(sesfolder, bidsmap_new, bidsmap_old, template, store)

                    # Clean-up the temporary unpacked data
                    if unpacked:
                        shutil.rmtree(sesfolder)

    # Save the new study bidsmap in the bidscoinfolder or launch the bidseditor UI_MainWindow
    if noedit:
        bids.save_bidsmap(bidsmapfile, bidsmap_new)

    else:
        LOGGER.info('Opening the bidseditor')
        app = QApplication(sys.argv)
        app.setApplicationName(f"{bidsmapfile} - BIDS editor {localversion}")

        mainwin = bidseditor.MainWindow(bidsfolder, bidsmap_new, template)
        mainwin.show()

        messagebox = QMessageBox(mainwin)
        messagebox.setText(f"The bidsmapper has finished scanning {rawfolder}\n\n"
                           f"Please carefully check all the different BIDS output names "
                           f"and BIDScoin options and (re)edit them to your needs.\n\n"
                           f"You can always redo this step later by re-running the "
                           f"bidsmapper or by just running the bidseditor tool\n\n"
                           f"{versionmessage}")
        messagebox.setWindowTitle('About the BIDS-mapping workflow')
        messagebox.setIconPixmap(QtGui.QPixmap(str(bidseditor.BIDSCOIN_LOGO)).scaled(150, 150, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        messagebox.setWindowFlags(messagebox.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint)
        messagebox.show()

        app.exec()

    LOGGER.info('-------------- FINISHED! -------------------')
    LOGGER.info('')

    bidscoin.reporterrors()


def setprefix(bidsmap: dict, subprefix: str, sesprefix: str, rawfolder: Path) -> tuple:
    """
    Set the prefix in the Options, subject, session and in all the run['datasource'] objects

    :param bidsmap:     The bidsmap with the data
    :param subprefix:   The subprefix (take value from bidsmap if empty)
    :param sesprefix:   The sesprefix (take value from bidsmap if empty)
    :param rawfolder:   The root folder-name of the sub/ses/data/file tree containing the source data files
    :return:            A (subprefix, sesprefix) tuple
    """

    oldsubprefix = bidsmap['Options']['bidscoin'].get('subprefix','')
    oldsesprefix = bidsmap['Options']['bidscoin'].get('sesprefix','')
    if not subprefix:
        subprefix = oldsubprefix                                # Use the default value from the bidsmap
    if not sesprefix:
        sesprefix = oldsesprefix                                # Use the default value from the bidsmap
    bidsmap['Options']['bidscoin']['subprefix'] = subprefix
    bidsmap['Options']['bidscoin']['sesprefix'] = sesprefix

    # Replace the glob wildcards with the regexp wildcards
    oldresubprefix = oldsubprefix.replace('*', '.*').replace('?', '.')
    oldresesprefix = oldsesprefix.replace('*', '.*').replace('?', '.')
    resubprefix    = subprefix.replace('*', '' if subprefix=='*' else '.*').replace('?', '.')
    resesprefix    = sesprefix.replace('*', '' if sesprefix=='*' else '.*').replace('?', '.')
    for dataformat in bidsmap:
        if not bidsmap[dataformat] or dataformat=='Options': continue
        if bidsmap[dataformat]['subject'].startswith('<<filepath:'):
            if oldresubprefix:
                bidsmap[dataformat]['subject'] = bidsmap[dataformat]['subject'].replace(oldresubprefix, resubprefix)
            else:
                LOGGER.warning(f"Could not update the bidsmap subject label expression: {bidsmap[dataformat]['subject']}")
            if not bidsmap[dataformat]['subject'].startswith(f"<<filepath:.*/{rawfolder.name}"):    # NB: Don't prepend the fullpath of rawfolder because of potential data unpacking in /tmp
                bidsmap[dataformat]['subject'] = bidsmap[dataformat]['subject'].replace('<<filepath:', f"<<filepath:.*/{rawfolder.name}")
        if bidsmap[dataformat]['session'].startswith('<<filepath:'):
            if oldresesprefix:
                bidsmap[dataformat]['session'] = bidsmap[dataformat]['session'].replace(oldresubprefix, resubprefix).replace(oldresesprefix, resesprefix)
            else:
                LOGGER.warning(f"Could not update the bidsmap session label expression: {bidsmap[dataformat]['session']}")
            if not bidsmap[dataformat]['session'].startswith(f"<<filepath:.*/{rawfolder.name}"):
                bidsmap[dataformat]['session'] = bidsmap[dataformat]['session'].replace('<<filepath:', f"<<filepath:.*/{rawfolder.name}")
        for datatype in bidsmap[dataformat]:
            if not isinstance(bidsmap[dataformat][datatype], list): continue
            for run in bidsmap[dataformat][datatype]:
                run['datasource'].subprefix = subprefix
                run['datasource'].sesprefix = sesprefix

    return subprefix, sesprefix


def main():
    """Console script usage"""

    # Parse the input arguments and run bidsmapper(args)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent(__doc__),
                                     epilog='examples:\n'
                                            '  bidsmapper /project/foo/raw /project/foo/bids\n'
                                            '  bidsmapper /project/foo/raw /project/foo/bids -t bidsmap_dccn\n'
                                            '  bidsmapper /project/foo/raw /project/foo/bids -p nibabel2bids\n ')
    parser.add_argument('sourcefolder',       help='The study root folder containing the raw source data folders')
    parser.add_argument('bidsfolder',         help='The destination folder with the (future) bids data and the bidsfolder/code/bidscoin/bidsmap.yaml output file')
    parser.add_argument('-b','--bidsmap',     help='The study bidsmap file with the mapping heuristics. If the bidsmap filename is relative (i.e. no "/" in the name) then it is assumed to be located in bidsfolder/code/bidscoin. Default: bidsmap.yaml', default='bidsmap.yaml')
    parser.add_argument('-t','--template',    help='The bidsmap template file with the default heuristics (this could be provided by your institute). If the bidsmap filename is relative (i.e. no "/" in the name) then it is assumed to be located in bidsfolder/code/bidscoin. Default: bidsmap_dccn.yaml', default=bidscoin.bidsmap_template)
    parser.add_argument('-p','--plugins',     help='List of plugins to be used (with default options, overrules the plugin list in the study/template bidsmaps)', nargs='+', default=[])
    parser.add_argument('-n','--subprefix',   help="The prefix common for all the source subject-folders (e.g. 'Pt' is the subprefix if subject folders are named 'Pt018', 'Pt019', ...). Use '*' when your subject folders do not have a prefix. Default: the value of the study or template bidsmap, e.g. 'sub-'")
    parser.add_argument('-m','--sesprefix',   help="The prefix common for all the source session-folders (e.g. 'M_' is the subprefix if session folders are named 'M_pre', 'M_post', ...). Use '*' when your session folders do not have a prefix. Default: the value of the study or template bidsmap, e.g. 'ses-'")
    parser.add_argument('-s','--store',       help="Flag to store provenance data samples in the bidsfolder/'code'/'provenance' folder (useful for inspecting e.g. zipped or transfered datasets)", action='store_true')
    parser.add_argument('-a','--automated',   help="Flag to save the automatically generated bidsmap to disk and without interactively tweaking it with the bidseditor", action='store_true')
    parser.add_argument('-f','--force',       help='Flag to discard the previously saved bidsmap and logfile', action='store_true')
    parser.add_argument('-v','--version',     help='Show the installed version and check for updates', action='version', version=f'BIDS-version:\t\t{bidscoin.bidsversion()}\nBIDScoin-version:\t{localversion}, {versionmessage}')
    args = parser.parse_args()

    bidsmapper(rawfolder    = args.sourcefolder,
               bidsfolder   = args.bidsfolder,
               bidsmapfile  = args.bidsmap,
               templatefile = args.template,
               plugins      = args.plugins,
               subprefix    = args.subprefix,
               sesprefix    = args.sesprefix,
               store        = args.store,
               noedit       = args.automated,
               force        = args.force)


if __name__ == "__main__":
    LOGGER = logging.getLogger(f"bidscoin.{Path(__file__).stem}")
    main()

else:
    LOGGER = logging.getLogger(__name__)
