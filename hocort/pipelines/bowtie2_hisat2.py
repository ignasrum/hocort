from hocort.pipelines.pipeline import Pipeline

from hocort.pipelines.bowtie2 import Bowtie2
from hocort.pipelines.hisat2 import HISAT2

from argparse import ArgumentParser
import time

class Bowtie2HISAT2(Pipeline):
    def __init__(self):
        super().__init__(__file__)

    def run(self, bt2_idx, hs2_idx, seq1, out1, seq2=None, out2=None):
        self.logger.info(f'Starting pipeline: {self.__class__.__name__}')
        start_time = time.time()
        temp1 = f'{self.temp_dir.name}/temp1.fastq'
        temp2 = f'{self.temp_dir.name}/temp2.fastq'
        Bowtie2().run(bt2_idx, seq1, temp1, seq2=seq2, out2=temp2)
        HISAT2().run(hs2_idx, temp1, out1, seq2=temp2, out2=out2)
        end_time = time.time()
        self.logger.info(f'Pipeline {self.__class__.__name__} run time: {end_time - start_time} seconds')

    def interface(self, args):
        parser = ArgumentParser(
            description='Bowtie2 pipeline',
            usage=f'hocort {self.__class__.__name__} positional_arguments [options]'
        )
        parser.add_argument(
            '-bt2_idx',
            '--bowtie2_index',
            required=True,
            type=str,
            metavar=('<idx>'),
            help='str: path to bowtie2 index'
        )
        parser.add_argument(
            '-hs2_idx',
            '--hisat2_index',
            required=True,
            type=str,
            metavar=('<idx>'),
            help='str: path to hisat2 index'
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
        parsed = parser.parse_args(args=args)

        bt2_idx = parsed.bowtie2_index
        hs2_idx = parsed.hisat2_index
        seq = parsed.input
        out = parsed.output

        seq1 = seq[0]
        seq2 = None
        out1 = out[0]
        out2 = None

        try:
            seq2 = seq[1]
        except:
            self.logger.info('Sequence file 2 path was not provided')

        try:
            out2 = out[1]
        except:
            self.logger.info('Output file 2 path was not provided')

        self.run(bt2_idx, hs2_idx, seq1, out1, seq2=seq2, out2=out2)
