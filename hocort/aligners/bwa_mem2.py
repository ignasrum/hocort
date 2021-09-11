import hocort.execute as exe
import multiprocessing



class BWA_MEM2():
    def align(index, seq, output_path, options=[]):
        log = open(output_path, 'w')
        log.flush()

        threads = multiprocessing.cpu_count()
        # bwa-mem2 mem -t <num_threads> <prefix> <reads.fq/fa> > out.sam
        executable = ['bwa-mem2']
        parameters = ['mem', '-t', str(threads), index, seq]

        result, returncode = exe.execute(executable, parameters)
        return result, returncode
