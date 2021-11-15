from argparse import ArgumentParser
from argparse import Action
import hocort.pipelines
import sys
import inspect
import logging


pipelines = {}
for pipeline in dir(hocort.pipelines):
    if pipeline[0] != '_':
        m = getattr(hocort.pipelines, pipeline)
        if inspect.isclass(m):
            pipelines[pipeline] = m

class HelpAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
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

def main():
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
        action='store_true',
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
