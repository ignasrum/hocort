from abc import ABC, abstractmethod


class Aligner(ABC):
    @abstractmethod
    def generate_index(path, sequences):
        pass

    @abstractmethod
    def align_sam(index, seq1, output, seq2=None, options=[]):
        pass

    @abstractmethod
    def align_bam(index, seq1, output, seq2=None, options=[]):
        pass
