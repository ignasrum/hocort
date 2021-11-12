from abc import ABC, abstractmethod


class Aligner(ABC):
    @abstractmethod
    def build_index(path_out, fasta_in):
        pass

    @abstractmethod
    def align_sam(index, seq1, output, seq2=None, options=[]):
        pass

    @abstractmethod
    def align_bam(index, seq1, output, seq2=None, options=[]):
        pass
