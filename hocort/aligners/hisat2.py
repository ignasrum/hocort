import hocort.execute as exe
import multiprocessing

from hocort.aligners.aligner import Aligner


class HISAT2(Aligner):
    def generate_index(path, sequences):
        pass

    def align(index, seq, output, options=[]):
        threads = multiprocessing.cpu_count()
        # hisat2 -x genome -U reads.fq -S output.sam
        # hisat2 -x grch38_snp/genome_snp -U SRR3733117.1.fastq -S output.sam -p 16
        cmd = ['hisat2', '-p', str(threads), '-x', index, '-U', seq, '-S', output] + options

        returncode, result = exe.execute(cmd)
        return returncode, result
