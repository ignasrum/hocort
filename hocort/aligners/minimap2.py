import hocort.execute as exe
from hocort.aligners.aligner import Aligner


class Minimap2(Aligner):
    def build_index(path_out, fasta_in, threads=1, options=[]):
        cmd = ['minimap2', '-t', str(threads), '-d', path_out] + options + [fasta_in]

        return exe.execute(cmd, decode_stderr=True)

    def align_sam(index, seq1, output, seq2=None, threads=1, options=[]):
        cmd = ['minimap2', '-t', str(threads), '-a', '-o', output] + options
        cmd += [index, seq1]
        if seq2:
            cmd += [seq2]

        return exe.execute(cmd, decode_stderr=True)

    def align_bam(index, seq1, output, seq2=None, threads=1, options=[]):
        cmd1 = ['minimap2', '-t', str(threads), '-a'] + options
        cmd1 += [index, seq1]
        if seq2:
            cmd1 += [seq2]

        cmd2 = ['samtools', 'view', '-@', str(threads), '-b', '-o', output]

        return exe.execute_pipe(cmd1, cmd2, decode_stderr=True)
