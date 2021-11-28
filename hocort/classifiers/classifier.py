from abc import ABC, abstractmethod


class Classifier(ABC):
    @abstractmethod
    def build_index(path_out, fasta_in, options=[], **kwargs):
        pass

    @abstractmethod
    def classify(index, seq1, classified_out, unclassified_out, seq2=None, options=[]):
        pass
