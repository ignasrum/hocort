"""
Command line user interface for HoCoRT.

"""
from argparse import ArgumentParser
from argparse import Action
import sys
import inspect
import logging

import hocort.pipelines
import hocort.version as version

# Gets available pipelines from hocort.pipelines
pipelines = {}
for pipeline in dir(hocort.pipelines):
    if pipeline[0] != '_':
        m = getattr(hocort.pipelines, pipeline)
        if inspect.isclass(m):
            pipelines[pipeline] = m


class HelpAction(Action):
    """
    Called when '-h' or '--help' flags are given.

    """
    def __call__(self, parser, namespace, values, option_string=None):
        """
        If a pipeline is selected, its interface is called with the '-h' flag.
        Otherwise, the help message of this interface is printed together with the
        names of pipelines available in hocort.pipelines module.

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
        pipeline = namespace.pipeline
        if pipeline != None:
            pipeline_interface = pipelines[pipeline]().interface
            pipeline_interface(['-h'])
        else:
            parser.print_help()

        print('\nAvailable pipelines:')
        for pipeline in pipelines:
            print(f'    {pipeline}')
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
    Main function for user interface. Parses arguments and starts a pipeline if one is selected.

    Returns
    -------
    None

    """
    parser = ArgumentParser(
        prog='HoCoRT',
        description='HoCoRT: A Host Contamination Removal Tool',
        usage='hocort [pipeline] [options]',
        add_help=False
    )
    parser.add_argument(
        'pipeline',
        type=str,
        help='str: pipeline to run'
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

    args, unknown_args = parser.parse_known_args()
    pipeline = args.pipeline
    debug = args.debug

    logger = logging.getLogger(__file__)
    log_level = logging.INFO
    if debug: log_level = logging.DEBUG
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s - %(name)s', level=log_level)

    logger.debug(str(args))

    try:
        if pipeline not in pipelines.keys():
            logger.error(f'Invalid pipeline: {pipeline}')
            return
        pipeline_interface = pipelines[pipeline]().interface
        pipeline_interface(unknown_args)
    except Exception as e:
        logger.error(e)
