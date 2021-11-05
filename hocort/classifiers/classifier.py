from abc import ABC, abstractmethod

class Classifier(ABC):
    @abstractmethod
    def generate_index(path, sequences):
        pass

    @abstractmethod
    def classify(index, seq, classified_out, unclassified_out, options=[]):
        pass
