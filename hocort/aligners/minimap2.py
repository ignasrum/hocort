import logging

import hocort.execute as exe
from hocort.aligners.aligner import Aligner

logger = logging.getLogger(__file__)


class Minimap2(Aligner):
    """
    Minimap2 implementation of the Aligner abstract base class.

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
        if not path_out or not fasta_in: return None
        cmd = ['minimap2', '-t', str(threads), '-d', path_out] + options + [fasta_in]

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
        cmd = ['minimap2', '-t', str(threads), '-a']
        if output:
            cmd += ['-o', output]
        cmd += options
        cmd += [index, seq1]
        if seq2:
            cmd += [seq2]

        return [cmd]
