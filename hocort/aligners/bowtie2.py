import hocort.execute as exe
import multiprocessing

from hocort.aligners.aligner import Aligner


# bowtie2 [options]* -x <bt2-idx> {-1 <m1> -2 <m2> | -U <r> | --interleaved <i> | -b <bam>} [-S <sam>]

class Bowtie2(Aligner):
    def generate_index(path, sequences):
        pass

    def align_sam(index, seq1, output, seq2=None, options=[]):
        #if len(seq) <= 0 or len(seq) > 2: return -1
        threads = multiprocessing.cpu_count()
        cmd = ['bowtie2', '-p', str(threads), '-x', index, '-q', '-S', output] + options
        if seq2 is not None:
            cmd += ['-1', seq1, '-2', seq2]
        else: cmd += ['-U', seq1]

        return exe.execute(cmd, decode_stderr=True)

    def align_bam(index, seq1, output, seq2=None, options=[]):
        threads = multiprocessing.cpu_count()
        cmd1 = ['bowtie2', '-p', str(threads), '-x', index, '-q'] + options
        if seq2 is not None:
            cmd1 += ['-1', seq1, '-2', seq2]
        else: cmd1 += ['-U', seq1]

        cmd2 = ['samtools', 'view', '-b', '-o', output]

        return exe.execute_pipe(cmd1, cmd2, decode_stderr=True)
