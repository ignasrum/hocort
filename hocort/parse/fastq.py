import pysam
import hocort.execute as exe
import subprocess

class FastQ:
    # input:  bam
    # output: fastq
    def convert_bam(bam_path, output_path, options=[]):
        log = open(output_path, 'a')
        log.flush()

        executable = ['samtools']
        parameters = [f'fastq {bam_path}'] + options
        parameters = ['fastq', bam_path] + options

        result, returncode = exe.execute(executable, parameters, stdout=log, stderr=log)
        return result, returncode

    # input:  fastq
    # output: fastq
    # filter: fastq
    def filter_by_id(input_path, output_path, filter_path, options=[]):
        # filterbyname.sh in=SRR3733117.1.fastq out=filtered.fastq names=removed.fastq include=f ow=t
        executable = ['filterbyname.sh']
        parameters = [f'in={input_path} out={output_path} names={filter_path} include=f ow=t'] + options

        result, returncode = exe.execute(executable, parameters)
        return result, returncode

    # seqtk subseq in.fq name.lst > out.fq
    def filter_by_id1(input_path, output_path, filter_path, options=[]):
        pass
