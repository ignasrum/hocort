import tempfile
import logging
from abc import ABC, abstractmethod
from hocort.parse.fastq import FastQ

class Pipeline(ABC):
    def __init__(self, logger_filename, dir=None):
        self.temp_dir = tempfile.TemporaryDirectory(dir=dir)
        self.logger = logging.getLogger(logger_filename)
        self.logger.debug(str(self.temp_dir))

    def filter(self, query_names, seq1, out1, seq2=None, out2=None, hcfilter='f'):
        seq_ids_output = f'{self.temp_dir.name}/removed.list'
        try:
            with open(seq_ids_output, 'w') as f:
                for query in query_names:
                    f.write(f'{query}\n')
        except Exception as e:
            self.logger.error(e)
            return 1

        # REMOVE FILTERED READS FROM ORIGINAL FASTQ FILES
        self.logger.info('Removing reads from input fastq file 1')
        returncode1, stdout1, stderr1 = FastQ.filter_by_id(seq1, out1, seq_ids_output, include=hcfilter)
        if returncode1[0] != 0:
            self.logger.error(stdout1[0])
            self.logger.error(stderr1[0])
            return 1

        if seq2:
            self.logger.info('Removing reads from input fastq file 2')
            returncode2, stdout2, stderr2 = FastQ.filter_by_id(seq2, out2, seq_ids_output, include=hcfilter)
            if returncode2[0] != 0:
                self.logger.error(stdout2[0])
                self.logger.error(stderr2[0])
                return 1
        return 0

    @abstractmethod
    def run(self, seq1, seq2=None):
        pass

    @abstractmethod
    def interface(self, args):
        pass
