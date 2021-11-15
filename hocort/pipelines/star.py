from argparse import ArgumentParser
import time
import os

from hocort.pipelines.pipeline import Pipeline
from hocort.aligners.star import STAR as star
from hocort.parse.sam import SAM
from hocort.parse.bam import BAM
from hocort.parse.fastq import FastQ


class STAR(Pipeline):
    def __init__(self, dir=None):
        super().__init__(__file__, dir=dir)

    def run(self, idx, seq1, out1, seq2=None, out2=None, intermediary='SAM', hcfilter='f', threads=1, mapq=0, options=[]):
        self.debug_log_args(self.run.__name__, locals())

        self.logger.info(f'Starting pipeline: {self.__class__.__name__}')
        start_time = time.time()

        if len(options) > 0:
            options = options
        else:
            options = []

        add_slash=False
        if seq2: add_slash = True
        query_names = []
        output_path = f'{self.temp_dir.name}/'

        self.logger.info('Aligning reads with STAR')
        if intermediary == 'BAM':
            returncode, stdout, stderr = star.align_bam(idx, seq1, output_path, seq2=seq2, threads=threads, options=options)
            self.logger.info('\n' + stderr[0])
            if returncode[0] != 0:
                self.logger.error('Pipeline was terminated')
                return 1
            self.logger.info('Extracting sequence ids')
            output_file = f'{self.temp_dir.name}/Aligned.out.bam'
            query_names = BAM.extract_ids(output_file, mapping_quality=mapq, threads=threads, add_slash=add_slash)
        else:
            returncode, stdout, stderr = star.align_sam(idx, seq1, output_path, seq2=seq2, threads=threads, options=options)
            self.logger.info('\n' + stderr[0])
            if returncode[0] != 0:
                self.logger.error('Pipeline was terminated')
                return 1
            self.logger.info('Extracting sequence ids')
            output_file = f'{self.temp_dir.name}/Aligned.out.sam'
            query_names = SAM.extract_ids(output_file, mapping_quality=mapq, threads=threads, add_slash=add_slash)

        # REMOVE FILTERED READS FROM ORIGINAL FASTQ FILES
        returncode = self.filter(query_names, seq1, out1, seq2=seq2, out2=out2, hcfilter=hcfilter)
        if returncode != 0:
            self.logger.error('Pipeline was terminated')
            return 1

        end_time = time.time()
        self.logger.info(f'Pipeline {self.__class__.__name__} run time: {end_time - start_time} seconds')
        return 0

    def interface(self, args):
        parser = ArgumentParser(
            description=f'{self.__class__.__name__} pipeline',
            usage=f'hocort {self.__class__.__name__} [-h] [--threads <int>] [--intermediary <format>] [--host_contam_filter <bool>] -x <idx> -i <seq1> [<seq2>] -o <out1> [<out2>]'
        )
        parser.add_argument(
            '-x',
            '--index',
            required=True,
            type=str,
            metavar=('<idx>'),
            help='str: path to STAR index (required)'
        )
        parser.add_argument(
            '-i',
            '--input',
            required=True,
            type=str,
            nargs=('+'),
            metavar=('<seq1>', '<seq2>'),
            help='str: path to sequence files, max 2 (required)'
        )
        parser.add_argument(
            '-o',
            '--output',
            required=True,
            type=str,
            nargs=('+'),
            metavar=('<out1>', '<out2>'),
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

        idx = parsed.index
        seq = parsed.input
        out = parsed.output
        threads = parsed.threads if parsed.threads else 1
        intermediary = parsed.intermediary
        hcfilter = parsed.host_contam_filter

        seq1 = seq[0]
        seq2 = None if len(seq) < 2 else seq[1]
        out1 = out[0]
        out2 = None if len(out) < 2 else out[1]

        self.run(idx, seq1, out1, out2=out2, seq2=seq2, intermediary=intermediary, hcfilter=hcfilter, threads=threads)
