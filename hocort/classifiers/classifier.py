from abc import ABC, abstractmethod


class Classifier(ABC):
    """
    Classifier abstract base class. Meant to provide a consistent interface between different classifiers.

    """
    @abstractmethod
    def build_index(path_out, fasta_in, options=[], **kwargs):
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
        pass

    @abstractmethod
    def classify(index, seq1, classified_out, unclassified_out, seq2=None, options=[]):
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
        options : list
            An options list where additional arguments may be specified.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        pass
