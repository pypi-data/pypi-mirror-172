#!/usr/bin/env python3
"""
BIDScoin is a toolkit to convert and organize raw data-sets according to the Brain Imaging Data Structure (BIDS)

The basic workflow is to run these two tools:

  $ bidsmapper sourcefolder bidsfolder        # This produces a study bidsmap and launches a GUI
  $ bidscoiner sourcefolder bidsfolder        # This converts your data to BIDS according to the study bidsmap

For more documentation see: https://bidscoin.readthedocs.io
"""

import argparse
import textwrap
import tarfile
import shutil
import sys
import logging
import coloredlogs
import inspect
import subprocess
import urllib.request
import json
from PyQt5.QtWidgets import QApplication, QPushButton
from tqdm import tqdm
from pathlib import Path
from functools import lru_cache
from importlib.util import spec_from_file_location, module_from_spec
from importlib.metadata import entry_points
from typing import Tuple, Union, List
from ruamel.yaml import YAML
yaml = YAML()

# Define the default paths
tutorialurl      = 'https://surfdrive.surf.nl/files/index.php/s/HTxdUbykBZm2cYM/download'
bidscoinfolder   = Path(__file__).parent
schemafolder     = bidscoinfolder/'schema'
heuristicsfolder = bidscoinfolder/'heuristics'
pluginfolder     = bidscoinfolder/'plugins'
bidsmap_template = heuristicsfolder/'bidsmap_dccn.yaml'

LOGGER           = logging.getLogger(__name__)


class TqdmUpTo(tqdm):

    def update_to(self, b=1, bsize=1, tsize=None):
        """
        Adds a tqdm progress bar to urllib.request.urlretrieve()
        https://gist.github.com/leimao/37ff6e990b3226c2c9670a2cd1e4a6f5

        :param b:       Number of blocks transferred so far [default: 1].
        :param bsize:   Size of each block (in tqdm units) [default: 1].
        :param tsize:   Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize


def setup_logging(log_file: Path=Path(), debug: bool=False):
    """
    Setup the logging

    :param log_file:    Name of the logfile
    :param debug:       Set log level to DEBUG if debug==True
    :return:
     """

    # Get the root logger
    logger = logging.getLogger()

    # Set the format and logging level
    if debug:
        fmt = '%(asctime)s - %(name)s - %(levelname)s | %(message)s'
        logger.setLevel(logging.DEBUG)
    else:
        fmt = '%(asctime)s - %(levelname)s | %(message)s'
        logger.setLevel(logging.INFO)
    datefmt   = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    # Set & add the streamhandler and add some color to those boring terminal logs! :-)
    coloredlogs.install(level=logger.level, fmt=fmt, datefmt=datefmt)

    if not log_file.name:
        return

    # Set & add the log filehandler
    log_file.parent.mkdir(parents=True, exist_ok=True)      # Create the log dir if it does not exist
    loghandler = logging.FileHandler(log_file)
    loghandler.setLevel(logging.DEBUG)
    loghandler.setFormatter(formatter)
    loghandler.set_name('loghandler')
    logger.addHandler(loghandler)

    # Set & add the error / warnings filehandler
    error_file = log_file.with_suffix('.errors')            # Derive the name of the error logfile from the normal log_file
    errorhandler = logging.FileHandler(error_file, mode='w')
    errorhandler.setLevel(logging.WARNING)
    errorhandler.setFormatter(formatter)
    errorhandler.set_name('errorhandler')
    logger.addHandler(errorhandler)


def version(check: bool=False) -> Union[str, Tuple]:
    """
    Reads the BIDSCOIN version from the VERSION.TXT file and from pypi

    :param check:   Check if the current version is up-to-date
    :return:        The version number or (version number, checking message) if check=True
    """

    localversion = (bidscoinfolder/'version.txt').read_text().strip()

    # Check pypi for the latest version number
    if check:
        try:
            stream      = urllib.request.urlopen('https://pypi.org/pypi/bidscoin/json').read()
            pypiversion = json.loads(stream)['info']['version']
        except Exception as pypierror:
            LOGGER.info(f"Checking BIDScoin version on https://pypi.org/pypi/bidscoin failed:\n{pypierror}")
            return localversion, "(Could not check for new BIDScoin versions)"
        if localversion != pypiversion:
            return localversion, f"NB: Your BIDScoin version is NOT up-to-date: {localversion} -> {pypiversion}"
        else:
            return localversion, "Your BIDScoin version is up-to-date :-)"

    return localversion


def bidsversion() -> str:
    """
    Reads the BIDS version from the BIDSVERSION.TXT file

    :return:    The BIDS version number
    """

    return (bidscoinfolder/'bidsversion.txt').read_text().strip()


def reporterrors() -> None:
    """
    Summarized the warning and errors from the logfile

    :return:
    """

    # Find the filehandlers and report the errors and warnings
    for filehandler in logging.getLogger().handlers:
        if filehandler.name == 'errorhandler':

            errorfile = Path(filehandler.baseFilename)
            if errorfile.stat().st_size:
                LOGGER.info(f"The following BIDScoin errors and warnings were reported:\n\n{40 * '>'}\n{errorfile.read_text()}{40 * '<'}\n")

            else:
                LOGGER.info(f'No BIDScoin errors or warnings were reported')
                LOGGER.info('')

        elif filehandler.name == 'loghandler':
            logfile = Path(filehandler.baseFilename)

    # Final message
    if 'logfile' in locals():
        LOGGER.info(f"For the complete log see: {logfile}\n"
                    f"NB: Files in {logfile.parent} may contain privacy sensitive information, e.g. pathnames in logfiles and provenance data samples")


def run_command(command: str) -> bool:
    """
    Runs a command in a shell using subprocess.run(command, ..)

    :param command: The command that is executed
    :return:        True if the command was successfully executed (no errors), False otherwise
    """

    LOGGER.info(f"Running: {command}")
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)          # TODO: investigate shell=False and capture_output=True for python 3.7
    if process.stderr.decode() or process.returncode != 0:
        LOGGER.error(f"Failed to run:\n{command}\nErrorcode {process.returncode}:\n{process.stdout.decode()}\n{process.stderr.decode()}")
        return False
    else:
        LOGGER.info(f"Output:\n{process.stdout.decode()}")

    return True


def lsdirs(folder: Path, wildcard: str='*') -> List[Path]:
    """
    Gets all directories in a folder, ignores files

    :param folder:      The full pathname of the folder
    :param wildcard:    Simple (glob.glob) shell-style wildcards. Foldernames starting with a dot are considered hidden and will be skipped. Use '**/wildcard for recursive search'
    :return:            A list with all directories in the folder
    """

    return [fname for fname in sorted(folder.glob(wildcard)) if fname.is_dir() and not fname.name.startswith('.')]


def list_executables(show: bool=False) -> list:
    """
    :return:                Nothing
    """

    if show:
        LOGGER.info('Executable BIDScoin tools:')

    scripts = []
    for script in entry_points()['console_scripts']:
        if script.value.startswith('bidscoin'):
            scripts.append(script.name)
            if show:
                LOGGER.info(f"- {script.name}")

    return scripts


def list_plugins(show: bool=False) -> List[Path]:
    """
    :param show: Print the installed plugins if True
    :return:     List of the installed plugins
    """

    if show:
        LOGGER.info('Installed BIDScoin plugins:')

    plugins = []
    for plugin in (bidscoinfolder/'plugins').glob('*.py'):
        if plugin.stem != '__init__':
            plugins.append(plugin)
            if show:
                LOGGER.info(f"- {plugin.stem}")

    return plugins


def install_plugins(plugins: Tuple[Path]=()) -> Union[bool, None]:
    """
    Installs plugins in the plugins folder and adds their Options and data format section to the default template bidsmap

    :param plugins: Fullpath filenames of the plugins that need to be installed
    :return:        True if the installation was successful and False if it failed
    """

    if not plugins:
        return

    # Load the default template bidsmap
    with open(bidsmap_template, 'r') as stream:
        template = yaml.load(stream)

    # Install the plugins
    success = True
    for plugin in plugins:
        plugin = Path(plugin)
        LOGGER.info(f"Installing: '{plugin}'")

        # Copy the plugin to the plugins folder
        try:
            shutil.copyfile(plugin, bidscoinfolder/'plugins'/plugin.with_suffix('.py').name)
        except IOError as install_failure:
            LOGGER.error(f"{install_failure}\nFailed to install: '{plugin.name}' in '{bidscoinfolder/'plugins'}'")
            success = False
            continue
        module = import_plugin(plugin, ('bidsmapper_plugin', 'bidscoiner_plugin'))
        if not module:
            LOGGER.error(f"Import failure, please re-install a valid version of '{plugin.name}'")
            success = False
            continue

        # Add the Options and data format section to the default template bidsmap
        if 'OPTIONS' in dir(module) or 'BIDSMAP' in dir(module):
            if 'OPTIONS' in dir(module):
                LOGGER.info(f"Adding default {plugin.name} bidsmap options to the {bidsmap_template.stem} template")
                template['Options']['plugins'][plugin.stem] = module.OPTIONS
            if 'BIDSMAP' in dir(module):
                for key, value in module.BIDSMAP.items():
                    LOGGER.info(f"Adding default {key} bidsmappings to the {bidsmap_template.stem} template")
                    template[key] = value
            with open(bidsmap_template, 'w') as stream:
                yaml.dump(template, stream)

    return success


def uninstall_plugins(plugins: Tuple[str]=(), wipe: bool=True) -> Union[bool, None]:
    """
    Uninstalls plugins in the plugins folder and removes their Options and data format section from the default template bidsmap

    :param plugins: Fullpath filenames of the plugins that need to be uninstalled
    :param wipe:    Removes the plugin bidsmapping section if True
    :return:        True if the de-installation was successful, else False
    """

    if not plugins:
        return

    # Load the default template bidsmap
    with open(bidsmap_template, 'r') as stream:
        template = yaml.load(stream)

    # Uninstall the plugins
    success = True
    for plugin in plugins:

        plugin = (bidscoinfolder/'plugins'/plugin).with_suffix('.py')
        if not plugin.is_file():
            LOGGER.error(f"Plugin {plugin.stem} not found''")
            success = False
            continue

        module = import_plugin(plugin, ('bidsmapper_plugin', 'bidscoiner_plugin'))
        if not module:
            LOGGER.error(f"Import failure of '{plugin.stem}'")
            success = False
            continue

        # Remove the Options and data format section from the default template bidsmap
        if 'OPTIONS' in dir(module) or 'BIDSMAP' in dir(module):
            if 'OPTIONS' in dir(module):
                LOGGER.info(f"Removing default {plugin.stem} bidsmap options from the {bidsmap_template.stem} template")
                template['Options']['plugins'].pop(plugin.stem, None)
            if wipe and 'BIDSMAP' in dir(module):
                for key, value in module.BIDSMAP.items():
                    LOGGER.info(f"Removing default {key} bidsmappings from the {bidsmap_template.stem} template")
                    template.pop(key, None)
            with open(bidsmap_template, 'w') as stream:
                yaml.dump(template, stream)

        # Remove the plugin from the plugins folder
        try:
            LOGGER.info(f"Uninstalling: '{plugin.stem}'")
            plugin.unlink()
        except IOError as uninstall_error:
            LOGGER.info(f"Failed to uninstall: '{plugin}'\n{uninstall_error}")
            success = False

    return success


@lru_cache()
def import_plugin(plugin: Union[Path,str], functions: tuple=()) -> module_from_spec:
    """
    Imports the plugin if it contains any of the specified functions

    :param plugin:      Name of the plugin in the bidscoin "plugins" folder or the fullpath name
    :param functions:   List of functions of which at least one of them should be present in the plugin
    :return:            The imported plugin-module
    """

    if not plugin:
        return

    # Get the full path to the plugin-module
    plugin = Path(plugin).with_suffix('.py')
    if len(plugin.parents) == 1:
        plugin = pluginfolder/plugin

    # See if we can find the plug-in
    if not plugin.is_file():
        LOGGER.error(f"Could not find plugin: '{plugin}'")
        return

    # Load the plugin-module
    LOGGER.debug(f"Importing plugin: '{plugin}'")
    try:
        spec   = spec_from_file_location('bidscoin.plugin.' + plugin.stem, plugin)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        functionsfound = []
        for function in functions:
            if function not in dir(module):
                LOGGER.debug(f"Could not find '{function}' in the '{plugin}' plugin")
            elif not callable(getattr(module, function)):
                LOGGER.error(f"'The {function}' attribute in the '{plugin}' plugin is not callable")
            else:
                functionsfound.append(function)

        if functions and not functionsfound:
            LOGGER.info(f"Plugin '{plugin}' does not contain {functions} functions")
        else:
            return module

    except Exception as pluginerror:
        LOGGER.error(f"Could not import {plugin}:\n{pluginerror}")


def test_plugin(plugin: Union[Path,str], options: dict) -> bool:
    """
    Performs import tests of the plug-in

    :param plugin:  The name of the plugin that is being tested
    :param options: A dictionary with the plugin options, e.g. taken from the bidsmap['Options']['plugins'][plugin.stem]
    :return:        True if the plugin generated the expected result, False if there was a plug-in error
    """

    if not plugin:
        return False

    LOGGER.info(f"--------- Testing the '{plugin}' plugin ---------")

    # First test to see if we can import the plugin
    module = import_plugin(plugin, ('bidsmapper_plugin','bidscoiner_plugin'))
    if inspect.ismodule(module):
        LOGGER.info(f"Succesfully imported '{plugin}'")
    else:
        return False

    # Then run the plugin's own 'test' routine (if implemented)
    if 'test' in dir(module) and callable(getattr(module, 'test')):
        try:
            return module.test(options)
        except Exception as pluginerror:
            LOGGER.error(f"Could not run {plugin}.test(options):\n{pluginerror}")
            return False

    return True


def test_bidscoin(bidsmapfile: Union[Path,dict], options: dict=None, testplugins: bool=True, testgui: bool=True):
    """
    Performs a bidscoin installation test

    :param bidsmapfile: The bidsmap or the full pathname / basename of the bidsmap yaml-file
    :param options:     The bidscoin options. If empty, the default options are used
    :return:            True if the test was successful
    """

    if not bidsmapfile:
        return

    LOGGER.info('--------- Testing the BIDScoin tools and settings ---------')

    # Test loading the template bidsmap
    success = True
    if isinstance(bidsmapfile, (str, Path)):
        try:
            try:                    # Include the import in the test + moving the import to the top of this module will cause circular import issues
                from bidscoin import bids
            except ImportError:
                import bids         # This should work if bidscoin was not pip-installed

            bidsmap, _ = bids.load_bidsmap(Path(bidsmapfile))
            if not options:
                options = bidsmap['Options']
        except Exception as bidsmaperror:
            LOGGER.error(f'{bidsmaperror}')
            success = False
    else:
        if not options:
            options = bidsmapfile['Options']

    # Test PyQt
    if testgui:
        LOGGER.info('Testing the PyQt GUI setup:')
        try:
            app = QApplication(sys.argv)
            window = QPushButton('Minimal GUI test: OK')
            window.show()
            QApplication.quit()
            LOGGER.info('The GUI seems to work OK')
        except Exception as pyqterror:
            LOGGER.error(f"The installed PyQt version does not seem to work for your system:\n{pyqterror}")
            success = False

    # Test the DRMAA configuration (used by pydeface only)
    try:
        import pydeface
        LOGGER.info('Testing the DRMAA setup:')
        try:
            import drmaa
            LOGGER.info('The DRMAA library was successfully imported')
        except (RuntimeError, OSError, FileNotFoundError, ModuleNotFoundError, ImportError) as drmaaerror:
            LOGGER.warning(f"The DRMAA library could not be imported. This is OK if you want to run pydeface locally and not use the option to distribute jobs on a compute cluster\n{drmaaerror}")
    except ModuleNotFoundError:
        pass

    # Show an overview of the bidscoin tools. TODO: test the entry points?
    if options and not options.get('plugins'):
        LOGGER.warning('No plugins found in the bidsmap (BIDScoin will likely not do anything)')
    list_executables(True)

    # Test the plugins
    if testplugins:

        # Show an overview of the plugins and show the test results
        list_plugins(True)
        for plugin in (bidscoinfolder/'plugins').glob('*.py'):
            if plugin.stem != '__init__':
                success = test_plugin(plugin.stem, options['plugins'].get(plugin.stem,{}) if options else {}) and success

    return success


def pulltutorialdata(tutorialfolder: str) -> None:
    """
    Download and unzip tutorial.tar.gz file

    :param tutorialfolder:  The full pathname of the target folder in which the tutorial data will be downloaded
    :return:
    """

    if not tutorialfolder:
        return

    tutorialfolder = Path(tutorialfolder).resolve()
    tutorialtargz  = tutorialfolder/'bidscointutorial.tar.gz'
    tutorialfolder.mkdir(parents=True, exist_ok=True)

    # Download the data
    LOGGER.info(f"Downloading the tutorial dataset...")
    with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=tutorialtargz.name) as t:
        urllib.request.urlretrieve(tutorialurl, tutorialtargz, reporthook=t.update_to)  # NB: Much faster than requests.get(url, stream=True). In case of ssl certificate issues use: with urllib.request.urlopen(tutorialurl, context=ssl.SSLContext()) as data, open(tutorialtargz, 'wb') as targz_fid: shutil.copyfileobj(data, targz_fid)

    # Unzip the data in the target folder
    LOGGER.info(f"Unzipping the downloaded data in: {tutorialfolder}")
    with tarfile.open(tutorialtargz, 'r') as targz_fid:
        for member in tqdm(iterable=targz_fid.getmembers(), total=len(targz_fid.getmembers()), leave=False):
            targz_fid.extract(member, tutorialfolder)
    tutorialtargz.unlink()
    LOGGER.info(f"Done")


def main():
    """Console script usage"""

    setup_logging()
    localversion, versionmessage = version(check=True)

    # Parse the input arguments and run bidscoiner(args)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent(__doc__),
                                     epilog='examples:\n'
                                            '  bidscoin -l\n'
                                            '  bidscoin -d data/bidscoin_tutorial\n'
                                            '  bidscoin -t\n'
                                            '  bidscoin -t my_template_bidsmap\n'
                                            '  bidscoin -i python/project/my_plugin.py downloads/handy_plugin.py\n ')
    parser.add_argument('-l', '--list',      help='List all bidscoin tools', action='store_true')
    parser.add_argument('-p', '--plugins',   help='List all installed plugins', action='store_true')
    parser.add_argument('-i', '--install',   help='A list of bidscoin plugins to install', nargs='+')
    parser.add_argument('-u', '--uninstall', help='A list of bidscoin plugins to uninstall', nargs='+')
    parser.add_argument('-d', '--download',  help='Download folder. If given, tutorial MRI data will be downloaded here')
    parser.add_argument('-t', '--test',      help='Test the bidscoin installation and template bidsmap', nargs='?', const=bidsmap_template)
    parser.add_argument('-v', '--version',   help='Show the installed version and check for updates', action='version', version=f"BIDS-version:\t\t{bidsversion()}\nBIDScoin-version:\t{localversion}, {versionmessage}")
    if len(sys.argv) == 1:
        parser.print_help()
        return
    args = parser.parse_args()

    list_executables(show=args.list)
    list_plugins(show=args.plugins)
    uninstall_plugins(plugins=args.uninstall)
    install_plugins(plugins=args.install)
    pulltutorialdata(tutorialfolder=args.download)
    test_bidscoin(bidsmapfile=args.test)


if __name__ == "__main__":
    main()
