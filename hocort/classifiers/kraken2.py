import hocort.execute as exe
from hocort.classifiers.classifier import Classifier


class Kraken2(Classifier):
    def build_index(path_out, fasta_in, threads=1):
        # 1. download taxonomy
            # kraken2-build --threads n --download-taxonomy --db database
        cmd1 = ['kraken2-build', '--threads', str(threads), '--download-taxonomy', '--db', path_out]
        returncode1, stdout1, stderr1 = exe.execute(cmd1, decode_stderr=True)

        # 2. add fasta to library
            # kraken2-build --threads n --add-to-library reference.fna --db database
        cmd2 = ['kraken2-build', '--threads', str(threads), '--add_to_library', fasta_in, '--db', path_out]
        returncode2, stdout2, stderr2 = exe.execute(cmd2, decode_stderr=True)

        # 3. build db from library
            # kraken2-build --threads n --build --db database
        cmd3 = ['kraken2-build', '--threads', str(threads), '--build', '--db', path_out]
        returncode3, stdout3, stderr3 = exe.execute(cmd3, decode_stderr=True)

        # 4. clean up unnecessary files
            # kraken2-build --threads n --clean --db database 
        cmd4 = ['kraken2-build', '--threads', str(threads), '--clean', '--db', path_out]
        returncode4, stdout4, stderr4 = exe.execute(cmd4, decode_stderr=True)

        returncodes = returncode1 + returncode2 + returncode3 + returncode4
        stdout = stdout1 + stdout2 + stdout3 + stdout4
        stderr = stderr1 + stderr2 + stderr3 + stderr4

        return returncodes, stdout, stderr

    def classify(index, seq1, classified_out, unclassified_out, seq2=None, threads=1, options=[]):
        cmd = ['kraken2', '--threads', str(threads), '--db', index, '--classified-out', classified_out, '--unclassified-out', unclassified_out] + options
        if seq2:
            cmd += ['--paired', seq1, seq2]
        else: cmd += [seq1]

        return exe.execute(cmd, decode_stderr=True)
