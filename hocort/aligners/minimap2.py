import logging

import hocort.execute as exe
from hocort.aligners.aligner import Aligner

logger = logging.getLogger(__file__)


class Minimap2(Aligner):
    def build_index(path_out, fasta_in, threads=1, options=[], **kwargs):
        cmd = ['minimap2', '-t', str(threads), '-d', path_out] + options + [fasta_in]

        returncode, stdout, stderr = exe.execute(cmd, decode_stdout=True, decode_stderr=True)
        logger.info('\n' + stdout[0])
        logger.info('\n' + stderr[0])
        return returncode[0]

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
