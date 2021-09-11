from hocort.pipelines.pipeline import Pipeline

from hocort.aligners.bowtie2 import Bowtie2
from hocort.pipelines.human_host import HumanHost
from hocort.parse.sam import SAM
from hocort.parse.bam import BAM
from hocort.parse.bed import BED
from hocort.parse.fastq import FastQ

class HumanBowtie2(Pipeline):
    def __init__(self):
        super().__init__()

    def run(self, idx, seq, out):
        # awk '($5 >= 42)' output1.sam | wc -l

        # MAP READS TO INDEX
        bowtie2_output = f'{self.temp_dir.name}/output.sam'
        options = ['--quiet']
        result, returncode = Bowtie2.align(idx, seq, bowtie2_output, options=options)
        for line in result:
            print(line.strip('\n'))

        # COUNT NUMBER OF READS WITH CERTAIN MAPPING QUALITY
        query_names = SAM.count_reads(bowtie2_output, 42)
        queries = len(query_names)
        print(f'Reads with at least 42 mapping quality: {queries}')

        # FILTER MAPPED READS BASED ON MAPPING QUALITY
        sam_remove_output = f'{self.temp_dir.name}/removed.bam'
        result, returncode = SAM.remove(bowtie2_output, sam_remove_output, 42)
        for line in result:
            print(line.strip('\n'))

        # CONVERT BAM TO BED
        bam_to_bed_output = f'{self.temp_dir.name}/removed.bed'
        result, returncode = BAM.bam_to_bed(sam_remove_output, bam_to_bed_output)
        for line in result:
            print(line.strip('\n'))

        # awk '{ print $4 }' in.bed
        # EXTRACT SEQUENCE IDS FROM BED
        seq_ids_output = f'{self.temp_dir.name}/removed.list'
        result, returncode = BED.extract_sequence_ids(bam_to_bed_output, seq_ids_output)
        for line in result:
            print(line.strip('\n'))

        # REMOVE FILTERED READS FROM ORIGINAL FASTQ FILE
        result, returncode = FastQ.filter_by_id(seq, out, seq_ids_output)
        for line in result:
            print(line.strip('\n'))
