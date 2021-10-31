import pysam
import hocort.execute as exe
import subprocess

class FastQ:
    # input:  bam
    # output: fastq
    def convert_bam(bam_path, output_path, options=[]):
        cmd = ['samtools', 'fastq', bam_path] + options

        return exe.execute(cmd, out_file=output_path)

    # input:  fastq
    # output: fastq
    # filter: fastq
    def filter_by_id(input_path, output_path, filter_path, include='f', options=[]):
        # filterbyname.sh in=SRR3733117.1.fastq out=filtered.fastq names=removed.fastq include=f ow=t
        cmd = ['filterbyname.sh', f'in={input_path}', f'out={output_path}', f'names={filter_path}', f'include={include}', 'ow=t'] + options

        return exe.execute(cmd)
