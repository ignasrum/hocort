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
        print('HoCoRT Help:\n')
        parser.print_help()
        pipeline = namespace.pipeline
        if pipeline != None:
            print('\nPipeline Help:\n')
            pipeline_interface = pipelines[pipeline]().interface
            pipeline_interface(['-h'])
        parser.exit()

class ListAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print('Available pipelines:')
        for pipeline in pipelines:
            print(f'    {pipeline}')
        parser.exit()

def main():
    parser = ArgumentParser(description='HoCoRT', add_help=False)

    parser.add_argument('pipeline', type=str,
                        help='str: pipeline to run')
    parser.add_argument('-l', action=ListAction, nargs=0,
                        help='flag: list all pipelines')
    parser.add_argument('-v', action='count', default=0,
                        help='flag: verbose output')
    parser.add_argument('-h', action=HelpAction, nargs=0,
                        help='flag: print help')

    args, unknown_args = parser.parse_known_args()
    pipeline = args.pipeline
    verbose = True if args.v > 0 else False

    logger = logging.getLogger(__file__)
    log_level = logging.INFO
    if verbose > 0: log_level = logging.DEBUG
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
