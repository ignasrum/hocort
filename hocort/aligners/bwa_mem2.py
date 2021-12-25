import logging

import hocort.execute as exe
from hocort.aligners.aligner import Aligner

logger = logging.getLogger(__file__)


class BWA_MEM2(Aligner):
    """
    BWA_MEM2 implementation of the Aligner abstract base class.

    """
    def build_index(path_out, fasta_in, options=[], **kwargs):
        """
        Builds an index.

        Parameters
        ----------
        path_out : string
            Path where the output index is written.
        fasta_in : string
            Path where the input FASTA file is located.
        options : list
            An options list where additional arguments may be specified.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        cmd = ['bwa-mem2', 'index', '-p', path_out, fasta_in]

        returncode, stdout, stderr = exe.execute(cmd)
        logger.info('\n' + stdout)
        logger.info('\n' + stderr)

        return returncode

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
        cmd = ['bwa-mem2', 'mem', '-t', str(threads), '-o', output, index, seq1]
        if seq2:
            cmd += [seq2]
        cmd += options

        returncode, stdout, stderr = exe.execute(cmd)
        logger.info('\n' + stdout)
        logger.info('\n' + stderr)

        return returncode

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
        (bwa_mem2_returncode, samtools_returncode) : tuple of ints
            Resulting returncodes after the processes are finished.

        """
        cmd1 = ['bwa-mem2', 'mem', '-t', str(threads), index, seq1]
        if seq2:
            cmd1 += [seq2]
        cmd1 += options

        cmd2 = ['samtools', 'view', '-@', str(threads), '-b', '-o', output]

        returncode, stdout, stderr = exe.execute_pipe(cmd1, cmd2)
        logger.info('\n' + stderr[0])
        logger.info('\n' + stdout)
        logger.info('\n' + stderr[1])

        return returncode
