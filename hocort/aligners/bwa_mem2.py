import hocort.execute as exe
import multiprocessing

from hocort.aligners.aligner import Aligner


class BWA_MEM2(Aligner):
    def generate_index(path, sequences):
        pass

    def align(index, seq, output, options=[]):
        threads = multiprocessing.cpu_count()
        # bwa-mem2 mem -t <num_threads> <prefix> <reads.fq/fa> > out.sam
        # bwa-mem2 mem -t 16 index_path reads.fastq > out.sam
        cmd = ['bwa-mem2', 'mem', '-t', str(threads), index, seq] + options

        returncode, result = exe.execute(cmd, out_file=output)
        return returncode, result
