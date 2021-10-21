import hocort.execute as exe
import multiprocessing

from hocort.aligners.aligner import Aligner


class HISAT2(Aligner):
    def generate_index(path, sequences):
        pass

    def align_sam(index, seq1, output, seq2=None, threads=multiprocessing.cpu_count(), options=[]):
        # hisat2 -x genome -U reads.fq -S output.sam
        # hisat2 -x grch38_snp/genome_snp -U SRR3733117.1.fastq -S output.sam -p 16
        cmd = ['hisat2', '-p', str(threads), '-x', index, '-S', output] + options
        if seq2 is not None:
            cmd += ['-1', seq1, '-2', seq2]
        else: cmd += ['-U', seq1]

        return exe.execute(cmd, decode_stderr=True)

    def align_bam(index, seq1, output, seq2=None, threads=multiprocessing.cpu_count(), options=[]):
        cmd1 = ['hisat2', '-p', str(threads), '-x', index] + options
        if seq2 is not None:
            cmd1 += ['-1', seq1, '-2', seq2]
        else: cmd1 += ['-U', seq1]

        cmd2 = ['samtools', 'view', '-@', str(threads), '-b', '-o', output]

        return exe.execute_pipe(cmd1, cmd2, decode_stderr=True)
