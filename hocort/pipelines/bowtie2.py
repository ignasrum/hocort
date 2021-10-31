from hocort.pipelines.pipeline import Pipeline

from hocort.aligners.bowtie2 import Bowtie2 as bt2
from hocort.parse.sam import SAM
from hocort.parse.bam import BAM
from hocort.parse.fastq import FastQ

from argparse import ArgumentParser
import time
import os


class Bowtie2(Pipeline):
    def __init__(self):
        super().__init__(__file__)

    def run(self, idx, seq1, out1, out2=None, seq2=None, intermediary='SAM', hcfilter='f', mode='local', threads=1, options=[]):
        if len(options) > 0:
            options = options
        elif mode == 'local':
            options = ['--local', '--very-fast-local', '--score-min G,21,9']
        elif mode == 'end-to-end':
            options = ['--end-to-end', '--sensitive', '--score-min L,-0.4,-0.4']
        else:
            self.logger.error(f'Invalid mode: {mode}')

        self.logger.debug(f'seq1: {seq1}')
        self.logger.debug(f'seq2: {seq2}')
        self.logger.debug(f'mode: {mode}')
        self.logger.debug(f'threads: {threads}')
        self.logger.debug(f'intermediary: {intermediary}')

        self.logger.info(f'Starting pipeline: {self.__class__.__name__}')
        start_time = time.time()

        bowtie2_output = f'{self.temp_dir.name}/output'

        add_slash=False
        if seq2: add_slash = True
        mapq = 0
        query_names = []

        self.logger.info('Aligning reads with Bowtie2')
        if intermediary == 'BAM':
            returncode, stdout, stderr = bt2.align_bam(idx, seq1, bowtie2_output, seq2=seq2, threads=threads, options=options)
            print('\n', stderr[0])
            print('\n', stderr[1])
            if returncode[0] != 0: return returncode, stdout, stderr
            self.logger.info('Extracting sequence ids')
            query_names = BAM.extract_ids(bowtie2_output, mapping_quality=mapq, add_slash=add_slash)
        else:
            returncode, stdout, stderr = bt2.align_sam(idx, seq1, bowtie2_output, seq2=seq2, threads=threads, options=options)
            print('\n', stderr[0])
            if returncode[0] != 0: return returncode, stdout, stderr
            self.logger.info('Extracting sequence ids')
            query_names = SAM.extract_ids(bowtie2_output, mapping_quality=mapq, add_slash=add_slash)

        # REMOVE FILTERED READS FROM ORIGINAL FASTQ FILES
        self.filter(query_names, seq1, out1, seq2=seq2, out2=out2, hcfilter=hcfilter)

        end_time = time.time()
        self.logger.info(f'Pipeline {self.__class__.__name__} run time: {end_time - start_time} seconds')
        return returncode, stdout, stderr

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
            help='str: path to bowtie2 index'
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
            '-inter',
            '--intermediary',
            choices=['SAM', 'BAM'],
            default='SAM',
            help='str: intermediary step output format, default is SAM'
        )
        parser.add_argument(
            '-m',
            '--mode',
            choices=['local', 'end-to-end'],
            default='local',
            help='str: operation mode, default is local'
        )
        parser.add_argument(
            '-hcfilter',
            '--host_contam_filter',
            choices=['t', 'f'],
            default='f',
            help='str: set to true to keep host sequences, false to keep everything besides host sequences'
        )
        parsed = parser.parse_args(args=args)

        idx = parsed.index
        seq = parsed.input
        out = parsed.output
        threads = parsed.threads if parsed.threads else 1
        intermediary = parsed.intermediary
        mode = parsed.mode
        hcfilter = parsed.host_contam_filter

        seq1 = seq[0]
        seq2 = None if len(seq) < 2 else seq[1]
        out1 = out[0]
        out2 = None if len(out) < 2 else out[1]

        self.run(idx, seq1, out1, out2=out2, seq2=seq2, intermediary=intermediary, hcfilter=hcfilter, threads=threads, mode=mode)
