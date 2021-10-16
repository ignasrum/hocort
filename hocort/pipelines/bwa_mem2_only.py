from hocort.pipelines.pipeline import Pipeline

from hocort.aligners.bwa_mem2 import BWA_MEM2
from hocort.pipelines.human_host import HumanHost
from hocort.parse.sam import SAM
from hocort.parse.bam import BAM
from hocort.parse.bed import BED
from hocort.parse.fastq import FastQ

from argparse import ArgumentParser
import time


class BWA_MEM2_Only(Pipeline):
    def __init__(self):
        super().__init__(__file__)

    def run(self, idx, seq, out):
        # awk '($5 >= 42)' output1.sam | wc -l

        self.logger.info('Starting pipeline')
        start_time = time.time()
        # MAP READS TO INDEX
        bwa_mem2_output = f'{self.temp_dir.name}/output.sam'
        options = []
        self.logger.info('Aligning reads with BWA-MEM2')
        result, returncode = BWA_MEM2.align(idx, seq, bwa_mem2_output, options=options)

        # COUNT NUMBER OF READS WITH CERTAIN MAPPING QUALITY
        query_names = SAM.count_reads(bwa_mem2_output, 42)
        queries = len(query_names)
        self.logger.info(f'Reads with at least 42 mapping quality: {queries}')

        # FILTER MAPPED READS BASED ON MAPPING QUALITY
        sam_remove_output = f'{self.temp_dir.name}/removed.bam'
        self.logger.info('Filtering reads')
        result, returncode = SAM.remove(bwa_mem2_output, sam_remove_output, 42)

        # CONVERT BAM TO BED
        bam_to_bed_output = f'{self.temp_dir.name}/removed.bed'
        self.logger.info('Converting BAM to BED')
        result, returncode = BAM.bam_to_bed(sam_remove_output, bam_to_bed_output)

        # awk '{ print $4 }' in.bed
        # EXTRACT SEQUENCE IDS FROM BED
        seq_ids_output = f'{self.temp_dir.name}/removed.list'
        self.logger.info('Extracting sequence ids')
        result, returncode = BED.extract_sequence_ids(bam_to_bed_output, seq_ids_output)

        # REMOVE FILTERED READS FROM ORIGINAL FASTQ FILE
        self.logger.info('Removing reads from input fastq file')
        result, returncode = FastQ.filter_by_id(seq, out, seq_ids_output)

        end_time = time.time()
        self.logger.info(f'Pipeline run time: {end_time - start_time}')

    def interface(self, args):
        parser = ArgumentParser(
            description='BWA_MEM2 pipeline',
            usage=f'hocort {self.__class__.__name__} positional_arguments [options]'
        )
        parser.add_argument('bwa_mem2_index_path', type=str,
                            help='str: path to bwa_mem2 index')
        parser.add_argument('sequence_path', type=str,
                            help='str: path to sequence file')
        parser.add_argument('output_path', type=str,
                            help='str: path to output file')
        parsed = parser.parse_args(args=args)

        idx = parsed.bwa_mem2_index_path
        seq = parsed.sequence_path
        out = parsed.output_path

        self.run(idx, seq, out)
