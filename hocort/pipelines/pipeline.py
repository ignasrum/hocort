import logging
from abc import ABC, abstractmethod


class Pipeline(ABC):
    """
    Pipeline abstract base class. Meant to provide a consistent interface between different pipelines.

    """
    def __init__(self, logger_filename):
        """
        Constructor which setups the logger.

        Parameters
        ----------
        logger_filename : string
            Logger name.

        Returns
        -------
        None

        """
        self.logger = logging.getLogger(logger_filename)

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

    @abstractmethod
    def run(self, seq1, seq2=None, quiet=False):
        """
        Aligns FastQ sequences to reference genome and outputs FastQ files with/without matching sequences.

        Parameters
        ----------
        seq1 : string
            Path where the first input FastQ file is located.
        seq2 : string
            Path where the second input FastQ file is located.
        quiet : bool
            Toggles whether output is quiet or not.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        pass

    @abstractmethod
    def interface(self, args, quiet=False):
        """
        Main function for the user interface. Parses arguments and starts the pipeline.

        Parameters
        ----------
        args : list
            This list is parsed by ArgumentParser.
        quiet : bool
            Toggles whether output is quiet or not.

        Returns
        -------
        None

        """
        pass
