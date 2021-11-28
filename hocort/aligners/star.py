import logging

import hocort.execute as exe
from hocort.aligners.aligner import Aligner

logger = logging.getLogger(__file__)


class STAR(Aligner):
    def build_index(path_out, fasta_in, threads=1, options=[], **kwargs):
        cmd = ['STAR', '--runThreadN', str(threads)] + options + ['--runMode', 'genomeGenerate', '--genomeDir', path_out, '--genomeFastaFiles', fasta_in]

        returncode, stdout, stderr = exe.execute(cmd, decode_stdout=True, decode_stderr=True)
        logger.info('\n' + stdout[0])
        logger.info('\n' + stderr[0])
        return returncode[0]

    def align_sam(index, seq1, output_path, seq2=None, threads=1, options=[]):
        cmd = ['STAR', '--runThreadN', str(threads), '--genomeDir', index, '--outFileNamePrefix', output_path] + options
        cmd += ['--readFilesIn', seq1]
        if seq2:
            cmd += [seq2]

        return exe.execute(cmd, decode_stderr=True)

    def align_bam(index, seq1, output_path, seq2=None, threads=1, options=[]):
        cmd = ['STAR', '--runThreadN', str(threads), '--genomeDir', index, '--outFileNamePrefix', output_path, '--outSAMtype BAM Unsorted'] + options
        cmd += ['--readFilesIn', seq1]
        if seq2:
            cmd += [seq2]

        return exe.execute(cmd, decode_stderr=True)
