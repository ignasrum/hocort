import time
import os
import logging

from hocort.pipelines.utils import debug_log_args
from hocort.aligners.kraken2 import Kraken2 as kr2
from hocort.parse.sam import SAM
from hocort.parse.parser import ArgParser
import hocort.execute as exe

logger = logging.getLogger(__file__)


class Kraken2():
    """
    Kraken2 pipeline which maps reads to a genome and includes/excludes matching reads from the output FastQ file/-s.

    """
    def run(self, idx, seq1, out, seq2=None, mfilter=True, threads=1, options=''):
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
        mfilter : bool
            Whether to output mapped/unmapped sequences.
            True: output unmapped sequences
            False: output mapped sequences
        threads : int
            Number of threads to use.
        options : string
            An options string where additional arguments may be specified.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        Raises
        ------
        ValueError
            If disallowed characters are found in input.

        """
        debug_log_args(logger,
                       self.run.__name__,
                       locals())

        final_options = []
        if len(options) > 0:
            final_options = [options]
        final_options += ['--output', '-']

        logger.info(f'Running pipeline: {self.__class__.__name__}')
        start_time = time.time()

        class_out = None
        unclass_out = None
        if mfilter:
            unclass_out = out
        else:
            class_out = out

        kr2_cmd = kr2().classify(idx,
                                 seq1,
                                 classified_out=class_out,
                                 unclassified_out=unclass_out,
                                 seq2=seq2,
                                 threads=threads,
                                 options=final_options)
        if kr2_cmd == None: return 1
        returncodes = exe.execute(kr2_cmd,
                                  pipe=False)

        logger.debug(returncodes)
        for returncode in returncodes:
            if returncode != 0: return 1

        end_time = time.time()
        logger.info(f'Pipeline {self.__class__.__name__} run time: {end_time - start_time} seconds')
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
            usage=f'hocort map {self.__class__.__name__} [-h] [--threads <int>] [--filter <bool>] [-c=<str>] -x <idx> -i <fastq_1> [<fastq_2>] -o <out#.fastq>'
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
            help='str: path to sequence files, max 2 (.gz compression supported) (required)'
        )
        parser.add_argument(
            '-o',
            '--output',
            required=True,
            type=str,
            metavar=('<out#.fastq>'),
            help='str: output path kraken2 format (with # if paired input) (.gz compression NOT supported) (required)'
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
            '--filter',
            required=False,
            choices=['true', 'false'],
            default='true',
            help='str: set to false to output mapped sequences, true to output unmapped sequences (default: true)'
        )
        parser.add_argument(
            '-c',
            '--config',
            required=False,
            type=str,
            metavar=('<str>'),
            help='str: used to pass along arguments to the aligner, use with caution, usage: -c="list arguments here"'
        )
        parsed = parser.parse_args(args=args)

        idx = parsed.index
        seq = parsed.input
        out = parsed.output
        threads = parsed.threads if parsed.threads else 1
        mfilter = True if parsed.filter == 'true' else False
        config = parsed.config if parsed.config else ''

        seq1 = seq[0]
        seq2 = None if len(seq) < 2 else seq[1]

        return self.run(idx,
                        seq1,
                        out,
                        seq2=seq2,
                        mfilter=mfilter,
                        threads=threads,
                        options=config)
