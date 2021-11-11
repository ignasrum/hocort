from hocort.pipelines.pipeline import Pipeline
from hocort.classifiers.kraken2 import Kraken2 as kr2
from hocort.parse.sam import SAM
from hocort.parse.bam import BAM
from hocort.parse.fastq import FastQ
from argparse import ArgumentParser
import time
import os


class Kraken2(Pipeline):
    def __init__(self, dir=None):
        super().__init__(__file__, dir=dir)

    def run(self, idx, seq1, out, seq2=None, threads=1, options=[]):
        self.logger.debug(f'seq1: {seq1}')
        self.logger.debug(f'seq2: {seq2}')

        if len(options) > 0:
            options = options
        else:
            options = []

        self.logger.info(f'Starting pipeline: {self.__class__.__name__}')
        start_time = time.time()

        class_base = 'class'
        unclass_base = 'unclass'
        if seq2:
            class_out = f'{out}/{class_base}#.fq'
            unclass_out = f'{out}/{unclass_base}#.fq'
        else:
            class_out = f'{out}/{class_base}_1.fq'
            unclass_out = f'{out}/{unclass_base}_1.fq'

        if len(options) > 0:
            options = options
        else:
            options = []

        self.logger.info('Classifying reads with Kraken2')
        returncode, stdout, stderr = kr2.classify(idx, seq1, class_out, unclass_out, seq2=seq2, threads=threads, options=options)
        self.logger.info('\n' + stderr[0])
        if returncode[0] != 0:
            self.logger.error('Pipeline was terminated')
            return 1

        end_time = time.time()
        self.logger.info(f'Pipeline {self.__class__.__name__} run time: {end_time - start_time} seconds')
        return 0

    def interface(self, args):
        parser = ArgumentParser(
            description=f'{self.__class__.__name__} pipeline',
            usage=f'hocort {self.__class__.__name__} positional_arguments [options]'
        )
        parser.add_argument(
            '-x',
            '--index',
            required=True,
            type=str,
            metavar=('<idx>'),
            help='str: path to Kraken2 index'
        )
        parser.add_argument(
            '-i',
            '--input',
            required=True,
            type=str,
            nargs=('+'),
            metavar=('<seq1>', '<seq2>'),
            help='str: path to sequence files, max 2'
        )
        parser.add_argument(
            '-o',
            '--output',
            required=True,
            type=str,
            metavar=('<out>'),
            help='str: output path'
        )
        parser.add_argument(
            '-t',
            '--threads',
            required=False,
            type=int,
            metavar=('INT'),
            default=os.cpu_count(),
            help='int: number of threads, default is max available on machine'
        )
        parsed = parser.parse_args(args=args)

        idx = parsed.index
        seq = parsed.input
        out = parsed.output
        threads = parsed.threads if parsed.threads else 1

        seq1 = seq[0]
        seq2 = None if len(seq) < 2 else seq[1]

        self.run(idx, seq1, out, seq2=seq2, threads=threads)
