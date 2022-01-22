import logging

import hocort.execute as exe
from hocort.aligners.aligner import Aligner

logger = logging.getLogger(__file__)


class Bowtie2(Aligner):
    """
    Bowtie2 implementation of the Aligner abstract base class.

    """
    def build_index(path_out, fasta_in, options=[], **kwargs):
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
        if not path_out or not fasta_in: return None
        cmd = ['bowtie2-build'] + options + [fasta_in, path_out]

        return [cmd]

    def align(index, seq1, output=None, seq2=None, threads=1, options=[]):
        """
        Aligns FastQ sequences to reference genome and outputs a SAM file.

        Parameters
        ----------
        index : string
            Path where the aligner index is located.
        seq1 : string
            Path where the first input FastQ file is located.
        output : string
            Path where the output SAM file is written.
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
        if not index or not seq1: return None
        cmd = ['bowtie2', '-p', str(threads), '-x', index, '-q']
        if output:
            cmd += ['-S', output]
        cmd += options
        if seq2:
            cmd += ['-1', seq1, '-2', seq2]
        else: cmd += ['-U', seq1]

        return [cmd]
