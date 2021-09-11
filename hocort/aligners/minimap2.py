import hocort.execute as exe
import multiprocessing


# minimap2 [options] <target.fa>|<target.idx> [query.fa] [...]

class Minimap2():
    def align(index, seq, output, options=[]):
        log = open(output, 'w')
        log.flush()

        threads = multiprocessing.cpu_count()
        executable = ['minimap2']
        parameters = ['-a', index, seq] + options

        result, returncode = exe.execute(executable, parameters, stdout=log, stderr=log)
        return result, returncode
