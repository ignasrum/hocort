import tempfile
import logging
from abc import ABC, abstractmethod

class Pipeline(ABC):
    def __init__(self, logger_filename):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.logger = logging.getLogger(logger_filename)

    @abstractmethod
    def run(self, idx, seq, out):
        pass

    @abstractmethod
    def interface(self, args):
        pass
