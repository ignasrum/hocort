import logging

import hocort.execute as exe
from hocort.classifiers.classifier import Classifier

logger = logging.getLogger(__file__)


class Kraken2(Classifier):
    """
    Kraken2 implementation of the Classifier abstract base class.

    """
    def build_index(path_out, fasta_in, threads=1, options=[], **kwargs):
        """
        Builds an index.

        Parameters
        ----------
        path_out : string
            Path where the output index is written.
        fasta_in : string
            Path where the input FASTA file is located.
        threads : int
            Number of threads to use.
        options : list
            An options list where additional arguments may be specified.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        # 1. download taxonomy
            # kraken2-build --threads n --download-taxonomy --db database
        logger.info('Downloading taxonomy, this may take a while...')
        cmd1 = ['kraken2-build', '--threads', str(threads), '--download-taxonomy', '--db', path_out]
        returncode1, stdout1, stderr1 = exe.execute(cmd1, decode_stdout=True, decode_stderr=True)
        logger.info('\n' + stdout1[0])
        logger.info('\n' + stderr1[0])
        if(returncode1[0] != 0): return returncode1[0], stdout1[0], stderr1[0]

        # 2. add fasta to library
            # kraken2-build --threads n --add-to-library reference.fna --db database
        logger.info('Adding reference fasta to library...')
        cmd2 = ['kraken2-build', '--threads', str(threads), '--add-to-library', fasta_in, '--db', path_out]
        returncode2, stdout2, stderr2 = exe.execute(cmd2, decode_stdout=True, decode_stderr=True)
        logger.info('\n' + stdout2[0])
        logger.info('\n' + stderr2[0])
        if(returncode2[0] != 0): return returncode2[0], stdout2[0], stderr2[0]

        # 3. build db from library
            # kraken2-build --threads n --build --db database
        logger.info('Building database...')
        cmd3 = ['kraken2-build', '--threads', str(threads), '--build', '--db', path_out]
        returncode3, stdout3, stderr3 = exe.execute(cmd3, decode_stdout=True, decode_stderr=True)
        logger.info('\n' + stdout3[0])
        logger.info('\n' + stderr3[0])
        if(returncode3[0] != 0): return returncode3[0], stdout3[0], stderr3[0]

        # 4. clean up unnecessary files
            # kraken2-build --threads n --clean --db database 
        logger.info('Cleaning up...')
        cmd4 = ['kraken2-build', '--threads', str(threads), '--clean', '--db', path_out]
        returncode4, stdout4, stderr4 = exe.execute(cmd4, decode_stdout=True, decode_stderr=True)
        logger.info('\n' + stdout4[0])
        logger.info('\n' + stderr4[0])
        if(returncode4[0] != 0): return returncode4[0], stdout4[0], stderr4[0]

        stdout = stdout1[0] + stdout2[0] + stdout3[0] + stdout4[0]
        stderr = stderr1[0] + stderr2[0] + stderr3[0] + stderr4[0]

        return 0

    def classify(index, seq1, classified_out, unclassified_out, seq2=None, threads=1, options=[]):
        """
        Matches sequences to a reference database and classifies them.

        Parameters
        ----------
        index : string
            Path where the output index is written.
        seq1 : string
            Path where the first input FastQ file is located.
        classified_out : string
            Path where the output FastQ file with matching sequences is written.
        unclassified_out : string
            Path where the output FastQ file with non-matching sequences is written.
        seq2 : string
            Path where the second input FastQ file is located.
        threads : int
            Number of threads to use.
        options : list
            An options list where additional arguments may be specified.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        cmd = ['kraken2', '--threads', str(threads), '--db', index, '--classified-out', classified_out, '--unclassified-out', unclassified_out] + options
        if seq2:
            cmd += ['--paired', seq1, seq2]
        else: cmd += [seq1]

        return exe.execute(cmd, decode_stderr=True)
