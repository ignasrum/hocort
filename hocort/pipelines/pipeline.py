import tempfile
from abc import ABC, abstractmethod

class Pipeline(ABC):
    def __init__(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    @abstractmethod
    def run(self, idx, seq, out):
        pass

    @abstractmethod
    def interface(self, args):
        pass
