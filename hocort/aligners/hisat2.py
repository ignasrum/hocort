import logging

import hocort.execute as exe
from hocort.aligners.aligner import Aligner

logger = logging.getLogger(__file__)


class HISAT2(Aligner):
    def build_index(path_out, fasta_in, threads=1, options=[], **kwargs):
        cmd = ['hisat2-build'] + options + ['-p', str(threads), fasta_in, path_out]

        returncode, stdout, stderr = exe.execute(cmd, decode_stdout=True, decode_stderr=True)
        logger.info('\n' + stdout[0])
        logger.info('\n' + stderr[0])
        return returncode[0]

    def align_sam(index, seq1, output, seq2=None, threads=1, options=[]):
        cmd = ['hisat2', '-p', str(threads), '-x', index, '-S', output] + options
        if seq2:
            cmd += ['-1', seq1, '-2', seq2]
        else: cmd += ['-U', seq1]

        return exe.execute(cmd, decode_stderr=True)

    def align_bam(index, seq1, output, seq2=None, threads=1, options=[]):
        cmd1 = ['hisat2', '-p', str(threads), '-x', index] + options
        if seq2:
            cmd1 += ['-1', seq1, '-2', seq2]
        else: cmd1 += ['-U', seq1]

        cmd2 = ['samtools', 'view', '-@', str(threads), '-b', '-o', output]

        return exe.execute_pipe(cmd1, cmd2, decode_stderr=True)
