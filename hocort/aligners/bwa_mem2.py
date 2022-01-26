import logging

import hocort.execute as exe
from hocort.aligners.aligner import Aligner

logger = logging.getLogger(__file__)


class BWA_MEM2(Aligner):
    """
    BWA_MEM2 implementation of the Aligner abstract base class.

    """
    def build_index(self, path_out, fasta_in, options=[], **kwargs):
        """
        Builds an index.

        Parameters
        ----------
        path_out : string
            Path where the output index is written.
        fasta_in : string
            Path where the input FASTA file is located.
        options : list
            An options list where additional arguments may be specified.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        if not path_out or not fasta_in: return 1
        cmd = [['bwa-mem2', 'index', '-p', path_out, fasta_in]]
        returncode = exe.execute(cmd, pipe=False)
        return returncode[0]

    def align(self, index, seq1, output=None, seq2=None, threads=1, options=[]):
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
        [cmd] : list
            List of commands to be executed.

        """
        if not index or not seq1: return None
        cmd = ['bwa-mem2', 'mem', '-t', str(threads)]
        if output:
            cmd += ['-o', output]
        cmd += [index, seq1]
        if seq2:
            cmd += [seq2]
        cmd += options

        return [cmd]
