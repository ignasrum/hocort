"""
Command line user interface for HoCoRT.

"""
from argparse import Action
import sys
import inspect

import hocort.aligners
import hocort.classifiers
import hocort.pipelines
import hocort.version as version
import hocort.logging
from hocort.parser import ArgParser
import hocort.dependencies as dep


# check external dependencies
if not dep.check_external_dependencies():
    sys.exit(1)

# Gets available aligners from hocort.aligners
aligners = {}
for aligner in dir(hocort.aligners):
    if aligner[0] != '_':
        m = getattr(hocort.aligners, aligner)
        if inspect.isclass(m):
            aligners[aligner] = m

# Gets available classifiers from hocort.classifiers
classifiers = {}
for classifier in dir(hocort.classifiers):
    if classifier[0] != '_':
        m = getattr(hocort.classifiers, classifier)
        if inspect.isclass(m):
            classifiers[classifier] = m

# Gets available pipelines from hocort.pipelines
pipelines = {}
for pipeline in dir(hocort.pipelines):
    if pipeline[0] != '_':
        m = getattr(hocort.pipelines, pipeline)
        if inspect.isclass(m):
            pipelines[pipeline] = m

class HelpActionMap(Action):
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

class HelpActionIndex(Action):
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
        tool = namespace.tool
        if tool != None:
            if tool in aligners:
                tool_interface = aligners[tool]().index_interface
                tool_interface(['-h'])
            if tool in classifiers:
                tool_interface = classifiers[tool]().index_interface
                tool_interface(['-h'])
        else:
            parser.print_help()
        parser.exit()

def extra_help_map():
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

def extra_help_index():
    """
    Returns string containing some help information about available tools.

    Returns
    -------
    message : str
        Message containing information about available tools.

    """
    message = '\nAvailable tools:'
    for aligner in aligners:
        message += f'\n    {aligner}'
    for classifier in classifiers:
        message += f'\n    {classifier}'
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
        version_info=version_info,
        prog='HoCoRT',
        description='HoCoRT: A Host Contamination Removal Tool',
        usage='hocort [subcommand] [options]'
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
        '-l',
        '--log-file',
        type=str,
        help='str: path to log file'
    )
    subparsers = parser.add_subparsers(
        dest='subcommand',
        title='available subcommands',
        metavar='subcommand',
        required=True
    )
    # map subcommand
    parser_map = subparsers.add_parser(
        'clean',
        prog='HoCoRT',
        description='HoCoRT: A Host Contamination Removal Tool',
        usage='hocort map [pipeline] [options]',
        extra_help=extra_help_map,
        help='Map reads to reference and remove contamination',
        add_help=False
    )
    parser_map.add_argument(
        'pipeline',
        type=str,
        help='str: pipeline to run (required)'
    )
    parser_map.add_argument(
        '-h',
        '--help',
        action=HelpActionMap,
        nargs=0,
        help='flag: print help'
    )
    # index subcommand
    parser_index = subparsers.add_parser(
        'index',
        prog='HoCoRT',
        description='HoCoRT: A Host Contamination Removal Tool',
        usage='hocort index [tool] [options]',
        extra_help=extra_help_index,
        help='Build index/-es for supported tools',
        add_help=False
    )
    parser_index.add_argument(
        'tool',
        type=str,
        help='str: tool to generate index for (required)'
    )
    parser_index.add_argument(
        '-h',
        '--help',
        action=HelpActionIndex,
        nargs=0,
        help='flag: print help'
    )

    args, unknown_args = parser.parse_known_args()
    cmd = args.subcommand
    debug = args.debug
    quiet = args.quiet
    log_file = args.log_file
    logger = hocort.logging.configure_logger(__file__, debug=debug, quiet=quiet, filename=log_file)
    logger.debug(str(args))

    if cmd == 'clean' and args.pipeline:
        if args.pipeline not in pipelines.keys():
            logger.error(f'Invalid pipeline: {args.pipeline}')
            sys.exit(1)
        pipeline_interface = pipelines[args.pipeline]().interface
        returncode = pipeline_interface(unknown_args)
        logger.warning(f'Pipeline exited with returncode: {returncode}')
        sys.exit(returncode)
    if cmd == 'index' and args.tool:
        interface = None
        if args.tool in aligners.keys():
            interface = aligners[args.tool]().index_interface
        elif args.tool in classifiers.keys():
            interface = classifiers[args.tool]().index_interface
        else:
            logger.error(f'Invalid tool: {args.tool}')
            sys.exit(1)
        returncode = interface(unknown_args)
        logger.warning(f'Process exited with returncode: {returncode}')
        sys.exit(returncode)
