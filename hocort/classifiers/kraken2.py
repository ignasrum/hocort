import logging

import hocort.execute as exe
from hocort.classifiers.classifier import Classifier

logger = logging.getLogger(__file__)


class Kraken2(Classifier):
    """
    Kraken2 implementation of the Classifier abstract base class.

    """
    def build_index(self, path_out, fasta_in, threads=1, options=[], **kwargs):
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
        if not path_out or not fasta_in: return 1
        # 1. download taxonomy
            # kraken2-build --threads n --download-taxonomy --db database
        logger.info('Downloading taxonomy, this may take a while...')
        cmd1 = [['kraken2-build', '--threads', str(threads), '--download-taxonomy', '--db', path_out]]
        returncode1 = exe.execute(cmd1)[0]
        if(returncode1 != 0): return returncode1

        # 2. add fasta to library
            # kraken2-build --threads n --add-to-library reference.fna --db database
        logger.info('Adding reference fasta to library...')
        cmd2 = [['kraken2-build', '--threads', str(threads), '--add-to-library', fasta_in, '--db', path_out]]
        returncode2 = exe.execute(cmd2)[0]
        if(returncode2 != 0): return returncode2

        # 3. build db from library
            # kraken2-build --threads n --build --db database
        logger.info('Building database...')
        cmd3 = [['kraken2-build', '--threads', str(threads), '--build', '--db', path_out]]
        returncode3 = exe.execute(cmd3)[0]
        if(returncode3 != 0): return returncode3

        # 4. clean up unnecessary files
            # kraken2-build --threads n --clean --db database 
        logger.info('Cleaning up...')
        cmd4 = [['kraken2-build', '--threads', str(threads), '--clean', '--db', path_out]]
        returncode4 = exe.execute(cmd4)[0]
        if(returncode4 != 0): return returncode4

        return 0

    def classify(self, index, seq1, classified_out=None, unclassified_out=None, seq2=None, threads=1, options=[]):
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
        [cmd] : list
            List of commands to be executed.

        """
        if not index or not seq1: return None
        cmd = ['kraken2', '--threads', str(threads), '--db', index]
        if classified_out:
            cmd += ['--classified-out', classified_out]
        if unclassified_out:
            cmd += ['--unclassified-out', unclassified_out]
        if seq2:
            cmd += ['--paired', seq1, seq2]
        else: cmd += [seq1]
        cmd += options

        return [cmd]
