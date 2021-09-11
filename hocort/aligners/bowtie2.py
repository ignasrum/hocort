import hocort.execute as exe
import multiprocessing


# bowtie2 [options]* -x <bt2-idx> {-1 <m1> -2 <m2> | -U <r> | --interleaved <i> | -b <bam>} [-S <sam>]

class Bowtie2():
    def align(index, seq, output, options=[]):
        threads = multiprocessing.cpu_count()
        executable = ['bowtie2']
        parameters = [f'-p {str(threads)} -x {index} -q {seq} -S {output}'] + options
        parameters = ['-p', str(threads), '-x', index, '-q', seq, '-S', output] + options

        result, returncode = exe.execute(executable, parameters)
        return result, returncode
