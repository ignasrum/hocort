import logging

import hocort.execute as exe
from hocort.aligners.aligner import Aligner

logger = logging.getLogger(__file__)


class Minimap2(Aligner):
    """
    Minimap2 implementation of the Aligner abstract base class.

    """
    def build_index(path_out, fasta_in, threads=1, options=[], **kwargs):
        """
        Builds an index.

        Parameters
        ----------
        path_out : string
            Path where the output index is written.
        fasta_in : string
            Path where the input FASTA file is located.
        threads : int
            Number of threads to use.
        options : list
            An options list where additional arguments may be specified.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        cmd = ['minimap2', '-t', str(threads), '-d', path_out] + options + [fasta_in]

        returncode, stdout, stderr = exe.execute(cmd, decode_stdout=True, decode_stderr=True)
        logger.info('\n' + stdout[0])
        logger.info('\n' + stderr[0])
        return returncode[0]

    def align_sam(index, seq1, output, seq2=None, threads=1, options=[]):
        """
        Aligns FastQ sequences to reference genome and outputs a SAM file.

        Parameters
        ----------
        index : string
            Path where the aligner index is located.
        seq1 : string
            Path where the first input FastQ file is located.
        output : string
            Path where the output SAM file is written.
        seq2 : string
            Path where the second input FastQ file is located.
        threads : int
            Number of threads to use.
        options : list
            An options list where additional arguments may be specified.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        cmd = ['minimap2', '-t', str(threads), '-a', '-o', output] + options
        cmd += [index, seq1]
        if seq2:
            cmd += [seq2]

        returncode, stdout, stderr = exe.execute(cmd, decode_stdout=True, decode_stderr=True)
        logger.info('\n' + stdout[0])
        logger.info('\n' + stderr[0])
        return returncode[0]

    def align_bam(index, seq1, output, seq2=None, threads=1, options=[]):
        """
        Aligns FastQ sequences to reference genome and outputs a BAM file.

        Parameters
        ----------
        index : string
            Path where the aligner index is located.
        seq1 : string
            Path where the first input FastQ file is located.
        output : string
            Path where the output BAM file is written.
        seq2 : string
            Path where the second input FastQ file is located.
        threads : int
            Number of threads to use.
        options : list
            An options list where additional arguments may be specified.

        Returns
        -------
        [minimap2_returncode, samtools_returncode] : list of ints
            Resulting returncodes after the processes are finished.

        """
        cmd1 = ['minimap2', '-t', str(threads), '-a'] + options
        cmd1 += [index, seq1]
        if seq2:
            cmd1 += [seq2]

        cmd2 = ['samtools', 'view', '-@', str(threads), '-b', '-o', output]

        returncode, stdout, stderr = exe.execute_pipe(cmd1, cmd2, decode_stdout=True, decode_stderr=True)
        logger.info('\n' + stderr[0])
        logger.info('\n' + stdout[0])
        logger.info('\n' + stderr[1])
        return returncode
