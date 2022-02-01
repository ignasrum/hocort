"""
Index generation helper tool for HoCoRT.

"""
import sys
import inspect
import os

import hocort.aligners
import hocort.classifiers
import hocort.version as version
import hocort.logging
from hocort.parser import ArgParser

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

def extra_help():
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
    Main function for the user interface. Parses arguments and builds an index if an aligner is selected.

    Returns
    -------
    None

    """
    parser = ArgParser(
        extra_help=extra_help,
        version_info=version_info,
        prog='HoCoRT',
        description='HoCoRT: A Host Contamination Removal Tool',
        usage='hocort-index tool -i <fasta> -o <path> [options]'
    )
    parser.add_argument(
        'tool',
        type=str,
        help='str: tool to generate index for (required)'
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
    args, unknown_args = parser.parse_known_args()
    tool = args.tool
    debug = args.debug
    quiet = args.quiet
    log_file = args.log_file

    logger = hocort.logging.configure_logger(__file__, debug=debug, quiet=quiet, filename=log_file)
    logger.debug(str(args))

    interface = None
    if tool in aligners.keys():
        interface = aligners[tool]().index_interface
    elif tool in classifiers.keys():
        interface = classifiers[tool]().index_interface
    else:
        logger.error(f'Invalid tool: {tool}')
        sys.exit(1)
    returncode = interface(unknown_args)
    logger.warning(f'Process exited with returncode: {returncode}')
    sys.exit(returncode)
