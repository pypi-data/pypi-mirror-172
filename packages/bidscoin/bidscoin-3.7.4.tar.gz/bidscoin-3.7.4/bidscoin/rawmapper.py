#!/usr/bin/env python3
"""
Maps out the values of a dicom attribute of all subjects in the sourcefolder, saves the result in a
mapper-file and, optionally, uses the dicom values to rename the sub-/ses-id's of the subfolders. This
latter option can be used, e.g. when an alternative subject id was entered in the [Additional info]
field during subject registration at the scanner console (i.e. this data is stored in the dicom
attribute named 'PatientComments')
"""

import re
import warnings
import shutil
from pathlib import Path
try:
    from bidscoin import bidscoin, bids
except ImportError:
    import bidscoin, bids         # This should work if bidscoin was not pip-installed


def rawmapper(rawfolder, outfolder: Path=Path(), sessions: tuple=(), rename: bool=False, force: bool=False, dicomfield: tuple=('PatientComments',), wildcard: str='*', subprefix: str='sub-', sesprefix: str='ses-', dryrun: bool=False) -> None:
    """
    :param rawfolder:   The root folder-name of the sub/ses/data/file tree containing the source data files
    :param outfolder:   The name of the folder where the mapping-file is saved (default = sourcefolder)
    :param sessions:    Space separated list of selected sub-#/ses-# names / folders to be processed. Otherwise all sessions in the bidsfolder will be selected
    :param rename:      Flag for renaming the sub-subid folders to sub-dicomfield
    :param force:       Flag to rename the directories, even if the target-directory already exists
    :param dicomfield:  The names of the dicomfields that are mapped (/ renamed to sub-dcmval/ses-dcmval)
    :param wildcard:    The Unix style pathname pattern expansion that is used by glob to select the series from which the dicomfield is being mapped
    :param subprefix:   The prefix common for all source subject-folders
    :param sesprefix:   The prefix common for all source session-folders
    :param dryrun:      Flag for dry-running renaming the sub-subid folders
    :return:            Nothing
    """

    # Input checking
    rawfolder = Path(rawfolder).resolve()
    if not outfolder:
        outfolder = rawfolder
        print(f"Outfolder: {outfolder}")
    outfolder = Path(outfolder).resolve()

    # Write the header of the mapper logfile
    mapperfile = outfolder/f"rawmapper_{'_'.join(dicomfield)}.tsv"
    if not dryrun:
        if rename and not mapperfile.is_file():     # Write the header once
            mapperfile.write_text('subid\tsesid\tnewsubid\tnewsesid\n')
        else:                                       # Write the header once
            mapperfile.write_text('subid\tsesid\tseriesname\t{}\n'.format('\t'.join(dicomfield)))

    # Map the sessions in the sourcefolder
    if not sessions:
        sessions = list(rawfolder.glob(f"{subprefix}*/{sesprefix}*"))
        if not sessions:
            sessions = list(rawfolder.glob(f"{subprefix}*"))        # Try without session-subfolders
    else:
        sessions = [sessionitem for session in sessions for sessionitem in rawfolder.glob(session)]
    sessions = [session for session in sessions if session.is_dir()]

    # Loop over the selected sessions in the sourcefolder
    for session in sessions:

        # Get the subject and session identifiers from the sub/ses session folder
        datasource   = bids.DataSource(session/'dum.my', subprefix=subprefix, sesprefix=sesprefix)
        subid, sesid = datasource.subid_sesid()
        subid = subid.replace('sub-', subprefix)
        sesid = sesid.replace('ses-', sesprefix)

        # Parse the new subject and session identifiers from the dicomfield
        series = bidscoin.lsdirs(session, wildcard)
        if not series:
            series    = Path()
            dicomfile = bids.get_dicomfile(session)     # Try and see if there is a DICOM file in the root of the session folder
        else:
            series    = series[0]                       # NB: Assumes the first folder contains a dicom file and that all folders give the same info
            dicomfile = bids.get_dicomfile(series)      # Try and see if there is a DICOM file in the root of the session folder
        dcmval = ''
        for dcmfield in dicomfield:
            dcmval = dcmval + '/' + str(bids.get_dicomfield(dcmfield, dicomfile))
        dcmval = dcmval[1:]

        # Rename the session subfolder in the sourcefolder and print & save this info
        if rename:

            # Get the new subid and sesid
            if not dcmval or dcmval=='None':
                warnings.warn(f"Skipping renaming because the dicom-field was empty for: {session}")
                continue
            else:
                if '/' in dcmval:               # Allow for different sub/ses delimiters that could be entered at the console (i.e. in PatientComments)
                    delim = '/'
                elif '\\' in dcmval:
                    delim = '\\'
                else:
                    delim = '\r\n'
                newsubsesid = [val for val in dcmval.split(delim) if val]   # Skip empty lines / entries
                newsubid    = subprefix + bids.cleanup_value(re.sub(f'^{subprefix}', '', newsubsesid[0]))
                if newsubid==subprefix or newsubid==subprefix+'None':
                    newsubid = subid
                    warnings.warn(f"Could not rename {subid} because the dicom-field was empty for: {session}")
                if len(newsubsesid)==1:
                    newsesid = sesid
                elif len(newsubsesid)==2:
                    newsesid = sesprefix + bids.cleanup_value(re.sub(f'^{sesprefix}', '', newsubsesid[1]))
                else:
                    warnings.warn(f"Skipping renaming of {session} because the dicom-field '{dcmval}' could not be parsed into [subid, sesid]")
                    continue
                if newsesid==sesprefix or newsesid==subprefix+'None':
                    newsesid = sesid
                    warnings.warn(f"Could not rename {sesid} because the dicom-field was empty for: {session}")

            # Save the dicomfield / sub-ses mapping in the mapper logfile and rename the session subfolder (but skip if it already exists)
            newsession = rawfolder/newsubid/newsesid
            print(f"{session} -> {newsession}")
            if newsession == session:
                continue
            if not force and (newsession.is_dir() or newsession.is_file()):
                warnings.warn(f"{newsession} already exists, skipping renaming of {session} (you can use the '-c' option to override this)")
            elif not dryrun:
                with mapperfile.open('a') as fid:
                    fid.write(f"{subid}\t{sesid}\t{newsubid}\t{newsesid}\n")
                if newsession.is_dir():
                    for item in session.iterdir():
                        shutil.move(item, newsession/item.name)
                    session.rmdir()
                else:
                    shutil.move(session, newsession)

        # Print & save the dicom values in the mapper logfile
        else:
            print('{}/{}/{}\t-> {}'.format(subid, sesid, series.name, '\t'.join(dcmval.split('/'))))
            if not dryrun:
                with mapperfile.open('a') as fid:
                    fid.write('{}\t{}\t{}\t{}\n'.format(subid, sesid, series.name, '\t'.join(dcmval.split('/'))))


def main():
    """Console script usage"""

    # Parse the input arguments and run the rawmapper(args)
    import argparse
    import textwrap

    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter): pass

    parser = argparse.ArgumentParser(formatter_class=CustomFormatter,
                                     description=textwrap.dedent(__doc__),
                                     epilog='examples:\n' 
                                            '  rawmapper /project/3022026.01/raw/\n'
                                            '  rawmapper /project/3022026.01/raw -d AcquisitionDate\n' 
                                            '  rawmapper /project/3022026.01/raw -s sub-100/ses-mri01 sub-126/ses-mri01\n'
                                            '  rawmapper /project/3022026.01/raw -r -d ManufacturerModelName AcquisitionDate --dryrun\n' 
                                            '  rawmapper raw/ -r -s sub-1*/* sub-2*/ses-mri01 --dryrun\n'
                                            '  rawmapper -d EchoTime -w *fMRI* /project/3022026.01/raw\n ')
    parser.add_argument('sourcefolder',     help='The source folder with the raw data in sub-#/ses-#/series organisation')
    parser.add_argument('-s','--sessions',  help='Space separated list of selected sub-#/ses-# names / folders to be processed. Otherwise all sessions in the bidsfolder will be selected', nargs='+')
    parser.add_argument('-f','--field',     help='The fieldname(s) of the dicom attribute(s) used to rename or map the subid/sesid foldernames', default=['PatientComments'], nargs='+')
    parser.add_argument('-w','--wildcard',  help='The Unix style pathname pattern expansion that is used to select the series from which the dicomfield is being mapped (can contain wildcards)', default='*')
    parser.add_argument('-o','--outfolder', help='The mapper-file is normally saved in sourcefolder or, when using this option, in outfolder')
    parser.add_argument('-r','--rename',    help='If this flag is given sub-subid/ses-sesid directories in the sourcefolder will be renamed to sub-dcmval/ses-dcmval', action='store_true')
    parser.add_argument('-c','--clobber',   help='Flag to rename the directories, even if the target-directory already exists', action='store_true')
    parser.add_argument('-n','--subprefix', help='The prefix common for all the source subject-folders', default='sub-')
    parser.add_argument('-m','--sesprefix', help='The prefix common for all the source session-folders', default='ses-')
    parser.add_argument('-d','--dryrun',    help='Add this flag to dryrun (test) the mapping or renaming of the sub-subid/ses-sesid directories (i.e. nothing is stored on disk and directory names are not actually changed))', action='store_true')
    args = parser.parse_args()

    rawmapper(rawfolder  = args.sourcefolder,
              outfolder  = args.outfolder,
              sessions   = args.sessions,
              rename     = args.rename,
              force      = args.clobber,
              dicomfield = args.field,
              wildcard   = args.wildcard,
              subprefix  = args.subprefix,
              sesprefix  = args.sesprefix,
              dryrun     = args.dryrun)


if __name__ == "__main__":
    main()
