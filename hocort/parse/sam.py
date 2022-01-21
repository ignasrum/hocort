import pysam

class SAM:
    """
    SAM parsing and processing class.

    """
    def select(input_path=None, output_path=None, threads=1, hcfilter=False):
        # select reads based on mapq and output sam
        cmd = ['samtools', 'view', '--threads', f'{threads}', '-h']
        if hcfilter:
            cmd += ['-F', '12', '-f', '1']
        else:
            cmd += ['-f', '13']
        if input_path:
            pass
        if output_path:
            pass

        return [cmd]

    def sam_to_fastq(input_path=None, out1=None, out2=None, threads=1, hcfilter=False):
        cmd = ['samtools', 'fastq', '--threads', f'{threads}', '-N']
        if hcfilter:
            cmd += ['-F', '12', '-f', '1']
        else:
            cmd += ['-f', '13']
        cmd += ['-1', out1, '-2', out2, '-']

        return [cmd]
