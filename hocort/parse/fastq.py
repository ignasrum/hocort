import hocort.execute as exe
import logging

logger = logging.getLogger(__file__)


class FastQ:
    """
    FastQ parsing and processing class.

    """
    def filter_by_id(input_path, output_path, filter_path, include=False, options=[]):
        """
        Takes a FastQ file (input_path) and a file with sequence ids on each line (filter_path). Removes sequences specified in the second file (filter_path) and outputs a filtered FastQ (output_path).

        Parameters
        ----------
        input_path : string
            Input FastQ file path.
        output_path : string
            Output FastQ file path.
        filter_path : string
            Filter file path. Has sequence ids on each line.
        include : bool
            Whether to include or exclude the sequences specified in the filter file (filter_path).
        options : list
            An options list where additional arguments may be specified.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        # filterbyname.sh in=input.fastq out=filtered.fastq names=seq_ids_to_remove.fastq include=f ow=t
        include_arg = 't' if include else 'f'
        cmd = ['filterbyname.sh', f'in={input_path}', f'out={output_path}', f'names={filter_path}', f'include={include_arg}', 'ow=t'] + options

        returncode, stdout, stderr = exe.execute(cmd)
        logger.info('\n' + stdout)
        logger.info('\n' + stderr)
        return returncode

