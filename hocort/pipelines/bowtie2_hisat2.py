from argparse import ArgumentParser
import time
import os

from hocort.pipelines.pipeline import Pipeline
from hocort.pipelines.bowtie2 import Bowtie2
from hocort.pipelines.hisat2 import HISAT2


class Bowtie2HISAT2(Pipeline):
    def __init__(self, dir=None):
        super().__init__(__file__, dir=dir)

    def run(self, bt2_idx, hs2_idx, seq1, out1, seq2=None, out2=None, threads=1, intermediary='SAM', hcfilter='f'):
        self.debug_log_args(self.run.__name__, locals())
        self.logger.info(f'Starting pipeline: {self.__class__.__name__}')
        start_time = time.time()
        temp1 = f'{self.temp_dir.name}/temp1.fastq'
        temp2 = None if seq2 == None else f'{self.temp_dir.name}/temp2.fastq'
        returncode = Bowtie2().run(bt2_idx, seq1, temp1, seq2=seq2, out2=temp2, mode='end-to-end', threads=threads, intermediary=intermediary, hcfilter=hcfilter)
        if returncode != 0:
            self.logger.error('Pipeline was terminated')
            return 1
        returncode = HISAT2().run(hs2_idx, temp1, out1, seq2=temp2, out2=out2, threads=threads, intermediary=intermediary, hcfilter=hcfilter)
        if returncode != 0:
            self.logger.error('Pipeline was terminated')
            return 1
        end_time = time.time()
        self.logger.info(f'Pipeline {self.__class__.__name__} run time: {end_time - start_time} seconds')
        return 0

    def interface(self, args):
        parser = ArgumentParser(
            description=f'{self.__class__.__name__} pipeline',
            usage=f'hocort {self.__class__.__name__} [-h] [--threads <int>] [--intermediary <format>] [--host_contam_filter <bool>] --bowtie2_index <idx> --hisat2_index <idx> -i <fastq_1> [<fastq_2>] -o <fastq_1> [<fastq_2>]'
        )
        parser.add_argument(
            '-b',
            '--bowtie2_index',
            required=True,
            type=str,
            metavar=('<idx>'),
            help='str: path to Bowtie2 index (required)'
        )
        parser.add_argument(
            '-s',
            '--hisat2_index',
            required=True,
            type=str,
            metavar=('<idx>'),
            help='str: path to HISAT2 index (required)'
        )
        parser.add_argument(
            '-i',
            '--input',
            required=True,
            type=str,
            nargs=('+'),
            metavar=('<fastq_1>', '<fastq_2>'),
            help='str: path to sequence files, max 2 (required)'
        )
        parser.add_argument(
            '-o',
            '--output',
            required=True,
            type=str,
            nargs=('+'),
            metavar=('<fastq_1>', '<fastq_2>'),
            help='str: path to output files, max 2 (required)'
        )
        parser.add_argument(
            '-t',
            '--threads',
            required=False,
            type=int,
            metavar=('<int>'),
            default=os.cpu_count(),
            help='int: number of threads (default: max available on machine)'
        )
        parser.add_argument(
            '-r',
            '--intermediary',
            choices=['SAM', 'BAM'],
            default='SAM',
            help='str: intermediary step output format (default: SAM)'
        )
        parser.add_argument(
            '-f',
            '--host_contam_filter',
            choices=['t', 'f'],
            default='f',
            help='str: set to true to keep host sequences, false to keep everything besides host sequences (default: f)'
        )
        parsed = parser.parse_args(args=args)

        bt2_idx = parsed.bowtie2_index
        hs2_idx = parsed.hisat2_index
        seq = parsed.input
        out = parsed.output
        threads = parsed.threads if parsed.threads else 1
        intermediary = parsed.intermediary
        hcfilter = parsed.host_contam_filter

        seq1 = seq[0]
        seq2 = None if len(seq) < 2 else seq[1]
        out1 = out[0]
        out2 = None if len(out) < 2 else out[1]

        self.run(bt2_idx, hs2_idx, seq1, out1, seq2=seq2, out2=out2, threads=threads, intermediary=intermediary, hcfilter=hcfilter)
