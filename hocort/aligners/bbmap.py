import logging

import hocort.execute as exe
from hocort.aligners.aligner import Aligner

logger = logging.getLogger(__file__)


class BBMap(Aligner):
    """
    BBMap implementation of the Aligner abstract base class.

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
        cmd = ['bbmap.sh', f'threads={str(threads)}', f'ref={fasta_in}', f'path={path_out}']

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
        cmd = ['bbmap.sh', f'threads={str(threads)}', f'path={index}', f'out={output}.sam']
        if seq2:
            cmd += [f'in={seq1}', f'in2={seq2}']
        else: cmd += [f'in={seq1}']
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
        returncode : int
            Resulting returncode after the process is finished.

        """
        cmd = ['bbmap.sh', f'threads={str(threads)}', f'path={index}', f'out={output}.bam']
        if seq2:
            cmd += [f'in={seq1}', f'in2={seq2}']
        else: cmd += [f'in={seq1}']
        cmd += options

        returncode, stdout, stderr = exe.execute(cmd)
        logger.info('\n' + stdout)
        logger.info('\n' + stderr)

        return returncode
