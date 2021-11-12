import hocort.execute as exe
from hocort.aligners.aligner import Aligner


class BWA_MEM2(Aligner):
    def build_index(path_out, fasta_in, options=[]):
        cmd = ['bwa-mem2', 'index', '-p', path_out, fasta_in]

        return exe.execute(cmd, decode_stderr=True)

    def align_sam(index, seq1, output, seq2=None, threads=1, options=[]):
        cmd = ['bwa-mem2', 'mem', '-t', str(threads), '-o', output, index, seq1]
        if seq2:
            cmd += [seq2]
        cmd += options

        return exe.execute(cmd, decode_stderr=True)

    def align_bam(index, seq1, output, seq2=None, threads=1, options=[]):
        cmd1 = ['bwa-mem2', 'mem', '-t', str(threads), index, seq1]
        if seq2:
            cmd1 += [seq2]
        cmd1 += options

        cmd2 = ['samtools', 'view', '-@', str(threads), '-b', '-o', output]

        return exe.execute_pipe(cmd1, cmd2, decode_stderr=True)
