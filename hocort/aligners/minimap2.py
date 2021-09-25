import hocort.execute as exe
import multiprocessing

from hocort.aligners.aligner import Aligner

# minimap2 [options] <target.fa>|<target.idx> [query.fa] [...]

class Minimap2(Aligner):
    def generate_index(path, sequences):
        pass

    def align(index, seq, output, options=[]):
        log = open(output, 'w')
        log.flush()

        threads = multiprocessing.cpu_count()
        cmd = ['minimap2', '-a', index, seq] + options

        returncode, result = exe.execute(cmd, out_file=log)
        return returncode, result
