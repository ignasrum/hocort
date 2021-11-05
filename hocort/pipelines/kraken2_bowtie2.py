from hocort.pipelines.pipeline import Pipeline

from hocort.pipelines.bowtie2 import Bowtie2
from hocort.pipelines.kraken2 import Kraken2

from argparse import ArgumentParser
import time
import os

class Kraken2Bowtie2(Pipeline):
    def __init__(self, dir=None):
        super().__init__(__file__, dir=dir)

    def run(self, bt2_idx, kr2_idx, seq1, out1, seq2=None, out2=None, threads=1, hcfilter='f'):
        self.logger.info(f'Starting pipeline: {self.__class__.__name__}')
        start_time = time.time()

        kr2_out = self.temp_dir.name
        returncode = Kraken2().run(kr2_idx, seq1, kr2_out, seq2=seq2, threads=threads)
        if returncode != 0:
            self.logger.error('Pipeline was terminated')
            return 1

        # add hcfilter as option
        temp1 = f'{self.temp_dir.name}/unclass_1.fq'
        temp2 = None if seq2 == None else f'{self.temp_dir.name}/unclass_2.fq'

        returncode = Bowtie2().run(bt2_idx, temp1, out1, seq2=temp2, out2=out2, mode='end-to-end', threads=threads, hcfilter=hcfilter)
        if returncode != 0:
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
            '-bt2_idx',
            '--bowtie2_index',
            required=True,
            type=str,
            metavar=('<idx>'),
            help='str: path to Bowtie2 index'
        )
        parser.add_argument(
            '-kr2_idx',
            '--kraken2_index',
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
            nargs=('+'),
            metavar=('<out1>', '<out2>'),
            help='str: path to output files, max 2'
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
        parser.add_argument(
            '-hcfilter',
            '--host_contam_filter',
            choices=['t', 'f'],
            default='f',
            help='str: set to true to keep host sequences, false to keep everything besides host sequences'
        )
        parsed = parser.parse_args(args=args)

        bt2_idx = parsed.bowtie2_index
        kr2_idx = parsed.kraken2_index
        seq = parsed.input
        out = parsed.output
        threads = parsed.threads if parsed.threads else 1
        hcfilter = parsed.host_contam_filter

        seq1 = seq[0]
        seq2 = None if len(seq) < 2 else seq[1]
        out1 = out[0]
        out2 = None if len(out) < 2 else out[1]

        self.run(bt2_idx, kr2_idx, seq1, out1, seq2=seq2, out2=out2, threads=threads, hcfilter=hcfilter)
