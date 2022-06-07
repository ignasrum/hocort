import logging
import os
import sys

import hocort.execute as exe
from hocort.classifiers.classifier import Classifier
from hocort.parse.parser import ArgParser
from hocort.parse.parser import validate_args

logger = logging.getLogger(__file__)


class Kraken2(Classifier):
    """
    Kraken2 implementation of the Classifier abstract base class.

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
        [cmd1, cmd2, cmd3, cmd4] : list
            List of commands to be executed.

        Raises
        ------
        ValueError
            Raised if no input FASTA file is given, or no output path is given.
            If disallowed characters are found in input.

        """
        # validate input
        valid, arg, chars = validate_args([path_out, fasta_in] + options)
        if not valid:
            raise ValueError(f'Input with disallowed characters detected: "{arg}" - {chars}')

        if not fasta_in:
            raise ValueError(f'No input FASTA file was given.')
        if not path_out:
            raise ValueError(f'No output path was given.')
        # 1. download taxonomy
            # kraken2-build --threads n --download-taxonomy --db database
        cmd1 = ['kraken2-build', '--threads', str(threads), '--download-taxonomy', '--db', path_out]

        # 2. add fasta to library
            # kraken2-build --threads n --add-to-library reference.fna --db database
        cmd2 = ['kraken2-build', '--threads', str(threads), '--add-to-library', fasta_in, '--db', path_out]

        # 3. build db from library
            # kraken2-build --threads n --build --db database
        cmd3 = ['kraken2-build', '--threads', str(threads), '--build', '--db', path_out]

        # 4. clean up unnecessary files
            # kraken2-build --threads n --clean --db database 
        cmd4 = ['kraken2-build', '--threads', str(threads), '--clean', '--db', path_out]

        return [cmd1, cmd2, cmd3, cmd4]

    def classify(self, index, seq1, classified_out=None, unclassified_out=None, seq2=None, threads=1, options=[]):
        """
        Matches sequences to a reference database and classifies them.

        Parameters
        ----------
        index : string
            Path where the output index is written.
        seq1 : string
            Path where the first input FastQ file is located.
        classified_out : string
            Path where the output FastQ file with matching sequences is written.
        unclassified_out : string
            Path where the output FastQ file with non-matching sequences is written.
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

        Raises
        ------
        ValueError
            Raised if no input index path is given, or no input FastQ file is given.
            If disallowed characters are found in input.

        """
        # validate input
        valid, arg, chars = validate_args([index, seq1, classified_out, unclassified_out, seq2] + options)
        if not valid:
            raise ValueError(f'Input with disallowed characters detected: "{arg}" - {chars}')

        if not index:
            raise ValueError(f'No index path was given.')
        if not seq1:
            raise ValueError(f'No input FastQ was given.')
        cmd = ['kraken2', '--threads', str(threads), '--db', index]
        if classified_out:
            cmd += ['--classified-out', classified_out]
        if unclassified_out:
            cmd += ['--unclassified-out', unclassified_out]
        if seq2:
            cmd += ['--paired', seq1, seq2]
        else: cmd += [seq1]
        cmd += options

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
            help='str: path to sequence files (required)'
        )
        parser.add_argument(
            '-o',
            '--output',
            required=True,
            type=str,
            metavar=('<index>'),
            help='str: path to output index (dir/basename) (required)'
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

        cmds = self.build_index(out, ref, threads=threads)
        logger.warning(f'Generating index for: {self.__class__.__name__}')
        logger.info('Downloading taxonomy, this may take a while...')
        returncode = exe.execute([cmds[0]], pipe=False, merge_stdout_stderr=True)
        logger.info('Adding reference fasta to library...')
        returncode = exe.execute([cmds[1]], pipe=False, merge_stdout_stderr=True)
        logger.info('Building database...')
        returncode = exe.execute([cmds[2]], pipe=False, merge_stdout_stderr=True)
        logger.info('Cleaning up...')
        returncode = exe.execute([cmds[3]], pipe=False, merge_stdout_stderr=True)
        return returncode[0]
