import pysam
import hocort.execute as exe
import subprocess

class FastQ:
    # input:  bam
    # output: fastq
    def convert_bam(bam_path, output_path, options=[]):
        cmd = ['samtools', 'fastq', bam_path] + options

        returncode, result = exe.execute(cmd, out_file=output_path)
        return returncode, result

    # input:  fastq
    # output: fastq
    # filter: fastq
    def filter_by_id(input_path, output_path, filter_path, options=[]):
        # filterbyname.sh in=SRR3733117.1.fastq out=filtered.fastq names=removed.fastq include=f ow=t
        cmd = ['filterbyname.sh', f'in={input_path}', f'out={output_path}', f'names={filter_path}', 'include=f', 'ow=t'] + options

        returncode, result = exe.execute(cmd)
        return returncode, result

    # seqtk subseq in.fq name.lst > out.fq
    def filter_by_id1(input_path, output_path, filter_path, options=[]):
        pass
