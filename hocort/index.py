"""
Index generation helper tool for HoCoRT.

"""
import sys
import inspect
import os

import hocort.aligners
import hocort.classifiers
import hocort.version as version
from hocort.logger import Logger
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

def print_version():
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
        print_version=print_version,
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

    parsed = parser.parse_args()
    tool = parsed.tool
    ref = parsed.input
    out = parsed.output
    threads = parsed.threads if parsed.threads else 1
    debug = parsed.debug

    logger = Logger(__file__, debug)
    logger.debug(str(parsed))

    s = os.path.split(out)
    out_dir = s[0]
    basename = s[1]
    if basename == '' or basename == out:
        logger.error(f'No basename was given (dir/basename): {basename}')
        sys.exit(1)
    if not os.path.isdir(out_dir):
        logger.error(f'Output path does not exist: {out}')
        sys.exit(1)

    try:
        tool_build_index = None
        if tool in aligners.keys():
            tool_build_index = aligners[tool].build_index
        elif tool in classifiers.keys():
            tool_build_index = classifiers[tool].build_index
        else:
            logger.error(f'Invalid tool: {tool}')
            sys.exit(1)
        logger.info(f'Building index with {tool}')
        returncode = tool_build_index(out, ref, threads=threads)
        logger.info(f'Process exited with returncode: {returncode}')
        sys.exit(returncode)
    except Exception as e:
        logger.error(e)
        sys.exit(1)
