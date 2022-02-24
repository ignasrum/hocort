import logging
import os
import sys

import hocort.execute as exe
from hocort.aligners.aligner import Aligner
from hocort.parser import ArgParser

logger = logging.getLogger(__file__)


class HISAT2(Aligner):
    """
    HISAT2 implementation of the Aligner abstract base class.

    """
    def build_index(self, path_out, fasta_in, threads=1, options=[], **kwargs):
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
        [cmd] : list
            List of commands to be executed.

        """
        if not path_out or not fasta_in: return None
        cmd = ['hisat2-build'] + options + ['-p', str(threads), fasta_in, path_out]

        return [cmd]

    def align(self, index, seq1, output=None, seq2=None, threads=1, options=[]):
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
        [cmd] : list
            List of commands to be executed.

        """
        if not index or not seq1: return None
        cmd = ['hisat2', '-p', str(threads), '-x', index]
        if output:
            cmd += ['-S', output]
        cmd += options
        if seq2:
            cmd += ['-1', seq1, '-2', seq2]
        else: cmd += ['-U', seq1]

        return [cmd]

    def index_interface(self, args):
        """
        Main function for the index generation interface. Parses arguments and generates the index.

        Parameters
        ----------
        args : list
            This list is parsed by ArgumentParser.

        Returns
        -------
        None

        """
        parser = ArgParser(
            description=f'{self.__class__.__name__} aligner',
            usage=f'hocort index {self.__class__.__name__} [-h] [--threads <int>] -i <fasta> -o <index>'
        )
        parser.add_argument(
            '-i',
            '--input',
            required=True,
            type=str,
            metavar=('<fasta>'),
            help='str: path to sequence files, max 2 (required)'
        )
        parser.add_argument(
            '-o',
            '--output',
            required=True,
            type=str,
            metavar=('<index>'),
            help='str: path to output files, max 2 (required)'
        )
        parser.add_argument(
            '-t',
            '--threads',
            required=False,
            type=int,
            metavar=('<int>'),
            default=os.cpu_count(),
            help='int: number of threads (default: max available on machine)'
        )
        parsed = parser.parse_args(args=args)

        ref = parsed.input
        out = parsed.output
        threads = parsed.threads

        s = os.path.split(out)
        out_dir = s[0]
        basename = s[1]
        if basename == '' or basename == out:
            logger.error(f'No basename was provided for output path (dir/basename): {basename}')
            sys.exit(1)
        if not os.path.isdir(out_dir):
            logger.error(f'Output path does not exist: {out}')
            sys.exit(1)

        cmd = self.build_index(out, ref, threads=threads)
        logger.warning(f'Generating index for: {self.__class__.__name__}')
        returncode = exe.execute(cmd, pipe=False, merge_stdout_stderr=True)
        return returncode[0]
