from argparse import ArgumentParser
from argparse import Action

import hocort.pipelines
import sys
import inspect

pipelines = {}
i = 0
for pipeline in dir(hocort.pipelines):
    if pipeline[0] != '_':
        m = getattr(hocort.pipelines, pipeline)
        if inspect.isclass(m):
            pipelines[i] = m
            i += 1

class ListAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print('Available pipelines:')
        for pipeline in pipelines:
            print(f'    {pipeline}: {pipelines[pipeline]}')
        parser.exit()

def main():
    parser = ArgumentParser(description='HoCoRT')

    parser.add_argument('pipeline', type=int,
                        help='int: id of pipeline to run')
    parser.add_argument('sequence_path', type=str,
                        help='str: path to sequence file')
    parser.add_argument('output_path', type=str,
                        help='str: path to output file')
    parser.add_argument('-l', action=ListAction, nargs=0,
                        help='bool: list all pipelines')

    args = parser.parse_args()
    print(args)
    pipeline = args.pipeline
    seq = args.sequence_path
    out = args.output_path

    try:
        idx = 'grch38_1kgmaj_snvindels_bt2/grch38_1kgmaj_snvindels'
        pipelines[pipeline]().run(idx, seq, out)
    except Exception as e:
        print(e)
