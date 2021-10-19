from hocort.pipelines.pipeline import Pipeline

from hocort.aligners.bowtie2 import Bowtie2
from hocort.parse.sam import SAM
from hocort.parse.bam import BAM
from hocort.parse.bed import BED
from hocort.parse.fastq import FastQ

from argparse import ArgumentParser
import multiprocessing
import time


class Bowtie2(Pipeline):
    def __init__(self):
        super().__init__(__file__)

    def run(self, idx, seq1, out1, out2=None, seq2=None, intermediary='SAM', include='f', mode='local', threads=multiprocessing.cpu_count()):
        if seq2 and not out2:
            self.logger.error('Invalid input: sequence2 without output2')
            return None
        if out2 and not seq2:
            self.logger.error('Invalid input: output2 without sequence2')
            return None

        if mode == 'local':
            options = ['--local', '--very-fast-local', '--score-min G,21,9']
        elif mode == 'end-to-end':
            options = ['--end-to-end', '--sensitive', '--score-min L,-0.4,-0.4']
        else:
            self.logger.error(f'Invalid mode: {mode}')

        self.logger.debug(f'seq1: {seq1}')
        self.logger.debug(f'seq2: {seq2}')
        self.logger.debug(f'mode: {mode}')
        self.logger.debug(f'intermediary: {intermediary}')

        self.logger.info('Starting pipeline')
        start_time = time.time()

        bowtie2_output = f'{self.temp_dir.name}/output'

        add_slash=False
        if seq2: add_slash = True
        mapq = 0
        seq_ids_output = f'{self.temp_dir.name}/removed.list'
        query_names = []

        self.logger.info('Aligning reads with Bowtie2')
        if intermediary == 'BAM':
            returncode, stdout, stderr = Bowtie2.align_bam(idx, seq1, bowtie2_output, seq2=seq2, threads=threads, options=options)
            print('\n', stderr[0])
            print('\n', stderr[1])
            self.logger.info('Extracting sequence ids')
            query_names = BAM.extract_ids(bowtie2_output, mapping_quality=mapq, add_slash=add_slash)
        else:
            returncode, stdout, stderr = Bowtie2.align_sam(idx, seq1, bowtie2_output, seq2=seq2, threads=threads, options=options)
            print('\n', stderr)
            self.logger.info('Extracting sequence ids')
            query_names = SAM.extract_ids(bowtie2_output, mapping_quality=mapq, add_slash=add_slash)

        with open(seq_ids_output, 'w') as f:
            for query in query_names:
                f.write(f'{query}\n')

        # REMOVE FILTERED READS FROM ORIGINAL FASTQ FILES
        self.logger.info('Removing reads from input fastq file 1')
        returncode, stdout, stderr = FastQ.filter_by_id(seq1, out1, seq_ids_output, include=include)

        if seq2 is not None:
            self.logger.info('Removing reads from input fastq file 2')
            returncode, stdout, stderr = FastQ.filter_by_id(seq2, out2, seq_ids_output, include=include)

        end_time = time.time()
        self.logger.info(f'Pipeline run time: {end_time - start_time} seconds')

    def interface(self, args):
        parser = ArgumentParser(
            description='Bowtie2 pipeline',
            usage=f'hocort {self.__class__.__name__} positional_arguments [options]'
        )
        parser.add_argument(
            '-x',
            required=True,
            type=str,
            metavar=('<idx>'),
            help='str: path to bowtie2 index'
        )
        parser.add_argument(
            '-i',
            required=True,
            type=str,
            nargs=('+'),
            metavar=('<seq1>', '<seq2>'),
            help='str: path to sequence files, max 2'
        )
        parser.add_argument(
            '-o',
            required=True,
            type=str,
            nargs=('+'),
            metavar=('<out1>', '<out2>'),
            help='str: path to output files, max 2'
        )
        parser.add_argument(
            '-t',
            required=False,
            type=int,
            metavar=('INT'),
            help='int: number of threads, default is max available on machine'
        )
        parser.add_argument(
            '--intermediary',
            choices=['SAM', 'BAM'],
            default='SAM',
            help='str: intermediary step output format, default is SAM'
        )
        parser.add_argument(
            '--mode',
            choices=['local', 'end-to-end'],
            default='local',
            help='str: operation mode, default is local'
        )
        parser.add_argument(
            '--include',
            choices=['t', 'f'],
            default='f',
            help='str: set to true to include the filtered sequences, false to exclude'
        )
        parsed = parser.parse_args(args=args)

        idx = parsed.x
        seq = parsed.i
        out = parsed.o
        threads = parsed.t
        intermediary = parsed.intermediary
        mode = parsed.mode
        include = parsed.include

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

        self.run(idx, seq1, out1, out2=out2, seq2=seq2, intermediary=intermediary, include=include, threads=threads, mode=mode)
