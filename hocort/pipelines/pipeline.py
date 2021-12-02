import tempfile
import logging
from abc import ABC, abstractmethod

from hocort.parse.fastq import FastQ


class Pipeline(ABC):
    """
    Pipeline abstract base class. Meant to provide a consistent interface between different pipelines.

    """
    def __init__(self, logger_filename, dir=None):
        """
        Constructor which setups the logger and temporary directory.

        Parameters
        ----------
        logger_filename : string
            Logger name.
        dir : string
            Path where the temporary files are written.

        Returns
        -------
        None

        """
        self.temp_dir = tempfile.TemporaryDirectory(dir=dir)
        self.logger = logging.getLogger(logger_filename)
        self.logger.debug(str(self.temp_dir))

    def debug_log_args(self, function_name, locals_vars):
        """
        Logs the arguments of a function.

        Parameters
        ----------
        function_name : string
            Function name.
        locals_vars : dict
            Local symbol table from the function.

        Returns
        -------
        None

        """
        string = f'Logging args for: {function_name}()'
        for var in locals_vars:
            if var != 'self':
                string += f'\n{var}: {locals_vars[var]}'
        self.logger.debug(string + '\n')

    def filter(self, query_names, seq1, out1, seq2=None, out2=None, hcfilter='f'):
        """
        Fiters FastQ files.

        Parameters
        ----------
        query_names : list
            List of sequence ids.
        seq1 : string
            Path where the first input FastQ file is located.
        out1 : string
            Path where the first output FastQ file will be written.
        seq2 : string
            Path where the second input FastQ file is located.
        out2 : string
            Path where the second output FastQ file will be written.
        hcfilter : bool
            Whether to exclude or include the matching sequences from the output files.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
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
        returncode1 = FastQ.filter_by_id(seq1, out1, seq_ids_output, include=hcfilter)
        if returncode1 != 0:
            return 1

        if seq2:
            self.logger.info('Removing reads from input fastq file 2')
            returncode2 = FastQ.filter_by_id(seq2, out2, seq_ids_output, include=hcfilter)
            if returncode2 != 0:
                return 1
        return 0

    @abstractmethod
    def run(self, seq1, seq2=None):
        """
        Aligns FastQ sequences to reference genome and outputs FastQ files with/without matching sequences.

        Parameters
        ----------
        seq1 : string
            Path where the first input FastQ file is located.
        seq2 : string
            Path where the second input FastQ file is located.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        pass

    @abstractmethod
    def interface(self, args):
        """
        Main function for the user interface. Parses arguments and starts the pipeline.

        Parameters
        ----------
        args : list
            This list is parsed by ArgumentParser.

        Returns
        -------
        None

        """
        pass
