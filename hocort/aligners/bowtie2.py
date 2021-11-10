import hocort.execute as exe
from hocort.aligners.aligner import Aligner


class Bowtie2(Aligner):
    def generate_index(path, sequences):
        pass

    def align_sam(index, seq1, output, seq2=None, threads=1, options=[]):
        cmd = ['bowtie2', '-p', str(threads), '-x', index, '-q', '-S', output] + options
        if seq2:
            cmd += ['-1', seq1, '-2', seq2]
        else: cmd += ['-U', seq1]

        return exe.execute(cmd, decode_stderr=True)

    def align_bam(index, seq1, output, seq2=None, threads=1, options=[]):
        cmd1 = ['bowtie2', '-p', str(threads), '-x', index, '-q'] + options
        if seq2:
            cmd1 += ['-1', seq1, '-2', seq2]
        else: cmd1 += ['-U', seq1]

        cmd2 = ['samtools', 'view', '-@', str(threads), '-b', '-o', output]

        return exe.execute_pipe(cmd1, cmd2, decode_stderr=True)
