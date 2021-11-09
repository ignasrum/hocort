import hocort.execute as exe
import multiprocessing
from hocort.aligners.aligner import Aligner


class STAR(Aligner):
    def generate_index(path, sequences):
        pass

    def align_sam(index, seq1, output_path, seq2=None, threads=multiprocessing.cpu_count(), options=[]):
        cmd = ['STAR', '--runThreadN', str(threads), '--genomeDir', index, '--outFileNamePrefix', output_path] + options
        cmd += ['--readFilesIn', seq1]
        if seq2:
            cmd += [seq2]

        return exe.execute(cmd, decode_stderr=True)

    def align_bam(index, seq1, output_path, seq2=None, threads=multiprocessing.cpu_count(), options=[]):
        cmd = ['STAR', '--runThreadN', str(threads), '--genomeDir', index, '--outFileNamePrefix', output_path, '--outSAMtype BAM Unsorted'] + options
        cmd += ['--readFilesIn', seq1]
        if seq2:
            cmd += [seq2]

        return exe.execute(cmd, decode_stderr=True)
