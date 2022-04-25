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

    def validate(self, locals_vars):
        """
        Validates a list of arguments/variables.
        Implements positive security model by checking for
        valid characters instead of invalid ones.

        Parameters
        ----------
        locals_vars : dict
            Local symbol table of a function.

        Returns
        -------
        (bool, var, []) : tuple with a boolean, a string, and a list
            A tuple containing a boolean, a string, and a list is returned.
            The boolean is True if an argument is valid, False if
            it is invalid.
            The string contains the variable in question.
            The list contains the invalid characters, if any.
        """
        for var in locals_vars:
            var = locals_vars[var]
            if type(var) == str:
                valid, chars = hocort.parser.validate(var)
                if not valid:
                    return valid, var, chars
        return True, '', []

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
