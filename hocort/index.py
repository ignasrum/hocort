"""
Index generation helper tool for HoCoRT.

"""
from argparse import ArgumentParser
from argparse import Action
import sys
import inspect
import logging
import os

import hocort.aligners
import hocort.version as version

# Gets available aligners from hocort.aligners
aligners = {}
for aligner in dir(hocort.aligners):
    if aligner[0] != '_':
        m = getattr(hocort.aligners, aligner)
        if inspect.isclass(m):
            aligners[aligner] = m


class HelpAction(Action):
    """
    Called when '-h' or '--help' flags are given.

    """
    def __call__(self, parser, namespace, values, option_string=None):
        """
        The help message of this interface is printed together with the
        names of aligners available in hocort.aligners module.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            The object which contains this action.
        namespace : argparse.Namespace
            The argparse.Namespace object returned by parse_args().
        values : list
            The command-line arguments with any type conversion applied.
        option_string : string
            The option string which was used to invoke this action.

        Returns
        -------
        None

        """
        parser.print_help()

        print('\nAvailable aligners:')
        for aligner in aligners:
            print(f'    {aligner}')
        parser.exit()

class VersionAction(Action):
    """
    Called when '-v' or '--version' flags are given.

    """
    def __call__(self, parser, namespace, values, option_string=None):
        """
        When HoCoRT is ran with the '-v' or '--version' flags,
        the __version__ and __last_modified attributes from hocort.version are written to the command line.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            The object which contains this action.
        namespace : argparse.Namespace
            The argparse.Namespace object returned by parse_args().
        values : list
            The command-line arguments with any type conversion applied.
        option_string : string
            The option string which was used to invoke this action.

        Returns
        -------
        None

        """
        print(f'Version: {version.__version__}')
        print(f'Last modified: {version.__last_modified__}')
        parser.exit()

def main():
    """
    Main function for the user interface. Parses arguments and builds an index if an aligner is selected.

    Returns
    -------
    None

    """
    parser = ArgumentParser(
        prog='HoCoRT',
        description='HoCoRT: A Host Contamination Removal Tool',
        usage='hocort-index aligner -i <fasta> -o <path> [options]',
        add_help=False
    )
    parser.add_argument(
        'aligner',
        type=str,
        help='str: aligner to generate index for (required)'
    )
    parser.add_argument(
        '-i',
        '--input',
        required=True,
        type=str,
        metavar=('<fasta>'),
        help='str: path to reference genome fasta (required)'
    )
    parser.add_argument(
        '-o',
        '--output',
        required=True,
        type=str,
        metavar=('<path>'),
        help='str: path to output (required)'
    )
    parser.add_argument(
        '-t',
        '--threads',
        required=False,
        type=int,
        metavar=('<int>'),
        default=os.cpu_count(),
        help='int: max number of threads (default: max available on machine)'
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='flag: verbose output'
    )
    parser.add_argument(
        '-v',
        '--version',
        action=VersionAction,
        nargs=0,
        help='flag: print version'
    )
    parser.add_argument(
        '-h',
        '--help',
        action=HelpAction,
        nargs=0,
        help='flag: print help'
    )

    parsed = parser.parse_args()
    aligner = parsed.aligner
    ref = parsed.input
    out = parsed.output
    threads = parsed.threads if parsed.threads else 1
    debug = parsed.debug

    logger = logging.getLogger(__file__)
    log_level = logging.INFO
    if debug: log_level = logging.DEBUG
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s - %(name)s', level=log_level)

    logger.debug(str(parsed))

    if not os.path.isdir(out):
        logger.error(f'Output path does not exist: {out}')
        return 1

    try:
        if aligner not in aligners.keys():
            logger.error(f'Invalid aligner: {aligner}')
            return
        aligner_build_index = aligners[aligner].build_index
        logger.info(f'Building index with {aligner}')
        returncode, stdout, stderr = aligner_build_index(out, ref, threads=threads)
        logger.info(f'{stdout}')
        logger.info(f'{stderr}')
        logger.info(f'Process exited with returncode: {returncode}')
    except Exception as e:
        logger.error(e)
