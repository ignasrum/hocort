import time
import os

from hocort.pipelines.pipeline import Pipeline
from hocort.classifiers.kraken2 import Kraken2 as kr2
from hocort.parse.sam import SAM
from hocort.parser import ArgParser
import hocort.execute as exe


class Kraken2(Pipeline):
    """
    Kraken2 pipeline which maps reads to a genome and includes/excludes matching reads from the output FastQ file/-s.

    """
    def __init__(self):
        """
        Sets the logger file source filename.

        Returns
        -------
        None

        """
        super().__init__(__file__)

    def run(self, idx, seq1, out, seq2=None, hcfilter=False, threads=1, options=[]):
        """
        Run function which starts the pipeline.

        Parameters
        ----------
        idx : string
            Path where the index is located.
        seq1 : string
            Path where the first input FastQ file is located.
        out : string
            Path (directory) where the output FastQ files will be written.
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
        self.debug_log_args(self.run.__name__, locals())

        if len(options) > 0:
            options = options
        else:
            options = []
        options += ['--output', '-']

        self.logger.warning(f'Starting pipeline: {self.__class__.__name__}')
        start_time = time.time()

        class_out = None
        unclass_out = None
        if hcfilter:
            class_out = out
        else:
            unclass_out = out

        kr2_cmd = kr2().classify(idx, seq1, classified_out=class_out, unclassified_out=unclass_out, seq2=seq2, threads=threads, options=options)
        if kr2_cmd == None: return 1
        returncodes = exe.execute(kr2_cmd, pipe=False)

        self.logger.debug(returncodes)
        for returncode in returncodes:
            if returncode != 0: return 1

        end_time = time.time()
        self.logger.warning(f'Pipeline {self.__class__.__name__} run time: {end_time - start_time} seconds')
        return 0

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
        parser = ArgParser(
            description=f'{self.__class__.__name__} pipeline',
            usage=f'hocort {self.__class__.__name__} [-h] [--threads <int>] [--host-contam-filter <bool>] -x <idx> -i <fastq_1> [<fastq_2>] -o <out#.fastq>'
        )
        parser.add_argument(
            '-x',
            '--index',
            required=True,
            type=str,
            metavar=('<idx>'),
            help='str: path to Kraken2 index (required)'
        )
        parser.add_argument(
            '-i',
            '--input',
            required=True,
            type=str,
            nargs=('+'),
            metavar=('<fastq_1>', '<fastq_2>'),
            help='str: path to sequence files, max 2 (required)'
        )
        parser.add_argument(
            '-o',
            '--output',
            required=True,
            type=str,
            metavar=('<out#.fastq>'),
            help='str: output path kraken2 format (with # if paired input) (required)'
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
        parser.add_argument(
            '-f',
            '--host-contam-filter',
            choices=['True', 'False'],
            default='False',
            help='str: set to True to keep host sequences, False to keep everything besides host sequences (default: False)'
        )
        parsed = parser.parse_args(args=args)

        idx = parsed.index
        seq = parsed.input
        out = parsed.output
        threads = parsed.threads if parsed.threads else 1
        hcfilter = True if parsed.host_contam_filter == 'True' else False

        seq1 = seq[0]
        seq2 = None if len(seq) < 2 else seq[1]

        self.run(idx, seq1, out, seq2=seq2, hcfilter=hcfilter, threads=threads)
