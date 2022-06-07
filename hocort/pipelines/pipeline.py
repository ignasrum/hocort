from abc import ABC, abstractmethod

import hocort.parser


class Pipeline(ABC):
    """
    Pipeline abstract base class. Meant to provide a consistent interface between different pipelines.

    """
    def debug_log_args(self, logger, function_name, locals_vars):
        """
        Logs the arguments of a function.

        Parameters
        ----------
        logger : logging.Logger
            Logger instance which is used to log the arguments
        function_name : string
            Function name.
        locals_vars : dict
            Local symbol table of a function.

        Returns
        -------
        None

        """
        string = f'Logging args for: {function_name}()'
        for var in locals_vars:
            if var != 'self':
                string += f'\n{var}: {locals_vars[var]}'
        logger.debug(string + '\n')

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
