from abc import ABC, abstractmethod


class Classifier(ABC):
    @abstractmethod
    def generate_index(path, sequences):
        pass

    @abstractmethod
    def classify(index, seq1, classified_out, unclassified_out, seq2=None, options=[]):
        pass
