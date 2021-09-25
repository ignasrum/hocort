import hocort.execute as exe
import multiprocessing

from hocort.aligners.aligner import Aligner


# bowtie2 [options]* -x <bt2-idx> {-1 <m1> -2 <m2> | -U <r> | --interleaved <i> | -b <bam>} [-S <sam>]

class Bowtie2(Aligner):
    def generate_index(path, sequences):
        pass

    def align(index, seq, output, options=[]):
        threads = multiprocessing.cpu_count()
        cmd = ['bowtie2', '-p', str(threads), '-x', index, '-q', seq, '-S', output] + options

        returncode, result = exe.execute(cmd)
        return returncode, result
