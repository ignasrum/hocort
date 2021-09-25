from abc import ABC, abstractmethod

class Aligner(ABC):
    @abstractmethod
    def generate_index(path, sequences):
        pass

    @abstractmethod
    def align(index, seq, output, options=[]):
        pass
