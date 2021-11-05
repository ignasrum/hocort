import hocort.execute as exe
import multiprocessing

from hocort.classifiers.classifier import Classifier


class Kraken2(Classifier):
    def generate_index(path, sequences):
        pass

    def classify(index, seq1, classified_out, unclassified_out, seq2=None, threads=multiprocessing.cpu_count(), options=[]):
        cmd = ['kraken2', '--threads', str(threads), '--db', index, '--classified-out', classified_out, '--unclassified-out', unclassified_out] + options
        if seq2:
            cmd += ['--paired', seq1, seq2]
        else: cmd += [seq1]

        return exe.execute(cmd, decode_stderr=True)
