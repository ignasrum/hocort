import hocort.execute as exe
import multiprocessing

from hocort.aligners.aligner import Aligner


class BWA_MEM2(Aligner):
    def generate_index(path, sequences):
        pass

    def align(index, seq1, output, seq2=None, threads=multiprocessing.cpu_count(), options=[]):
        # bwa-mem2 mem -t <num_threads> <prefix> <reads.fq/fa> > out.sam
        # bwa-mem2 mem -t 16 index_path reads.fastq > out.sam
        cmd = ['bwa-mem2', 'mem', '-t', str(threads), '-o', output, index, seq1]
        if seq2:
            cmd += [seq2]
        cmd += options

        return exe.execute(cmd, decode_stderr=True)
