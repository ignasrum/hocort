import pysam

class SAM:
    """
    SAM parsing and processing class.

    """
    def select(input_path=None, output_path=None, paired=True, threads=1, hcfilter=False):
        cmd = ['samtools', 'view', '--threads', f'{threads}', '-h']
        if paired:
            if hcfilter:
                cmd += ['-F', '12', '-f', '1']
            else:
                cmd += ['-f', '13']
        else:
            if hcfilter:
                cmd += ['-F', '4']
            else:
                cmd += ['-f', '4']
        if output_path:
            cmd += ['-o', output_path]
        if input_path:
            cmd += [input_path]

        return [cmd]

    def sam_to_fastq(input_path=None, out1=None, out2=None, threads=1, hcfilter=False):
        cmd = ['samtools', 'fastq', '--threads', f'{threads}', '-N']
        if out1 and out2:
            if hcfilter:
                cmd += ['-F', '12', '-f', '1']
            else:
                cmd += ['-f', '13']
            cmd += ['-1', out1, '-2', out2]
        if out1 and not out2:
            if hcfilter:
                cmd += ['-F', '4']
            else:
                cmd += ['-f', '4']
            cmd += ['-0', out1]
        if input_path:
            cmd += [input_path]
        else:
            cmd += ['-']

        return [cmd]
