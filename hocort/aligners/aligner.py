from abc import ABC, abstractmethod


class Aligner(ABC):
    """
    Aligner abstract base class. Meant to provide a consistent interface between different aligners.

    """
    @abstractmethod
    def build_index(self, path_out, fasta_in, quiet=False, options=[], **kwargs):
        """
        Builds an index.

        Parameters
        ----------
        path_out : string
            Path where the output index is written.
        fasta_in : string
            Path where the input FASTA file is located.
        quiet : bool
            Toggles whether output is quiet or not.
        options : list
            An options list where additional arguments may be specified.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        pass

    @abstractmethod
    def align(self, index, seq1, output, seq2=None, options=[]):
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
        options : list
            An options list where additional arguments may be specified.

        Returns
        -------
        [cmd] : list
            List of commands to be executed.

        """
        pass
