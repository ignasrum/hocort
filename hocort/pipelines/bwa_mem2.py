from hocort.pipelines.pipeline import Pipeline

from hocort.aligners.bwa_mem2 import BWA_MEM2 as BWA_MEM2_mapper
from hocort.parse.sam import SAM
from hocort.parse.bam import BAM
from hocort.parse.bed import BED
from hocort.parse.fastq import FastQ

from argparse import ArgumentParser
import multiprocessing
import time


class BWA_MEM2(Pipeline):
    def __init__(self):
        super().__init__(__file__)

    def run(self, idx, seq1, out1, out2=None, seq2=None, intermediary='SAM', include='f', threads=multiprocessing.cpu_count()):
        # awk '($5 >= 42)' output1.sam | wc -l

        self.logger.info('Starting pipeline')
        start_time = time.time()
        # MAP READS TO INDEX
        bwa_mem2_output = f'{self.temp_dir.name}/output.sam'
        options = ['-O 20,20', '-E 6,6', '-L 2,2']

        include=False
        add_slash=False
        if seq2: add_slash = True
        mapq = 0
        seq_ids_output = f'{self.temp_dir.name}/removed.list'
        query_names = []

        self.logger.info('Aligning reads with BWA-MEM2')
        returncode, stdout, stderr = BWA_MEM2_mapper.align(idx, seq1, bwa_mem2_output, seq2=seq2, threads=threads, options=options)
        print('\n', stderr)
        self.logger.info('Extracting sequence ids')
        query_names = SAM.extract_ids(bwa_mem2_output, mapping_quality=mapq, add_slash=add_slash)

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
            description=f'{self.__class__.__name__} pipeline',
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
        parsed = parser.parse_args(args=args)

        idx = parsed.x
        seq = parsed.i
        out = parsed.o
        threads = parsed.t

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

        self.run(idx, seq1, out1, out2=out2, seq2=seq2, threads=threads)
