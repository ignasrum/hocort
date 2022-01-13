"""
Command line user interface for HoCoRT.

"""
from argparse import Action
import sys
import inspect

import hocort.pipelines
import hocort.version as version
from hocort.logger import Logger
from hocort.parser import ArgParser


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

        parser.exit()

def extra_help():
    """
    Returns string containing some help information about available pipelines.

    Returns
    -------
    message : str
        Message containing information about available pipelines.

    """
    message = '\nAvailable pipelines:'
    for pipeline in pipelines:
        message += f'\n    {pipeline}'
    message += '\n'
    return message

def version_info():
    """
    Returns string containing version information.

    Returns
    -------
    message : str
        Message containing version information.

    """
    message = f'Version: {version.__version__}'
    message += f'\nLast modified: {version.__last_modified__}'
    return message

def main():
    """
    Main function for user interface. Parses arguments and starts a pipeline if one is selected.

    Returns
    -------
    None

    """
    parser = ArgParser(
        extra_help=extra_help,
        version_info=version_info,
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
        '-q',
        '--quiet',
        action='store_true',
        help='flag: quiet output (overrides -d/--debug)'
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
    quiet = args.quiet

    logger = Logger(__file__, debug=debug, quiet=quiet)
    logger.debug(str(args))

    if pipeline not in pipelines.keys():
        logger.error(f'Invalid pipeline: {pipeline}')
        sys.exit(1)
    pipeline_interface = pipelines[pipeline]().interface
    pipeline_interface(unknown_args)
