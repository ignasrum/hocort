import time
import os
import logging

from hocort.pipelines.utils import debug_log_args
from hocort.aligners.bowtie2 import Bowtie2 as bt2
from hocort.parse.sam import SAM
from hocort.parse.parser import ArgParser
import hocort.execute as exe

logger = logging.getLogger(__file__)


class Bowtie2():
    """
    Bowtie2 pipeline which maps reads to a genome and includes/excludes matching reads from the output FastQ file/-s.

    """
    def run(self, idx, seq1, out1, seq2=None, out2=None, mfilter=True, preset='end-to-end', threads=1, options=''):
        """
        Run function which starts the pipeline.

        Parameters
        ----------
        idx : string
            Path where the index is located.
        seq1 : string
            Path where the first input FastQ file is located.
        out1 : string
            Path where the first output FastQ file will be written.
        seq2 : string
            Path where the second input FastQ file is located.
        out2 : string
            Path where the second output FastQ file will be written.
        mfilter : bool
            Whether to output mapped/unmapped sequences.
            True: output unmapped sequences
            False: output mapped sequences
        preset : string
            Bowtie2 execution mode. Can either be 'local' or 'end-to-end'.
        threads : int
            Number of threads to use.
        options : string
            An options string where arguments may be defined.
            Overrides "preset" argument.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        Raises
        ------
        ValueError
            If input FastQ_2 file is given without output FastQ_2.
            If disallowed characters are found in input.

        """
        debug_log_args(logger,
                       self.run.__name__,
                       locals())
        if seq2 and not out2:
            raise ValueError(f'Input FastQ_2 was given, but no output FastQ_2.')

        final_options = []
        if preset == 'local':
            final_options = ['--local']
        elif preset == 'end-to-end':
            final_options = ['--end-to-end']
        else:
            logger.warning(f'Invalid preset: {preset}')

        if len(options) > 0:
            final_options = [options]

        logger.info(f'Running pipeline: {self.__class__.__name__}')
        start_time = time.time()

        bowtie2_cmd = bt2().align(idx,
                                  seq1,
                                  seq2=seq2,
                                  threads=threads,
                                  options=final_options)
        if bowtie2_cmd == None: return 1
        fastq_cmd = SAM.sam_to_fastq(out1=out1,
                                     out2=out2,
                                     threads=threads,
                                     mfilter=mfilter)

        returncodes = exe.execute(bowtie2_cmd + fastq_cmd,
                                  pipe=True)

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
            usage=f'hocort map {self.__class__.__name__} [-h] [--threads <int>] [--filter <bool>] [--preset <str>] [-c=<str>] -x <idx> -i <fastq_1> [<fastq_2>] -o <fastq_1> [<fastq_2>]'
        )
        parser.add_argument(
            '-x',
            '--index',
            required=True,
            type=str,
            metavar=('<idx>'),
            help='str: path to Bowtie2 index (required)'
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
            nargs=('+'),
            metavar=('<fastq_1>', '<fastq_2>'),
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
        parser.add_argument(
            '-p',
            '--preset',
            required=False,
            choices=['local', 'end-to-end'],
            default='end-to-end',
            help='str: operation mode (default: end-to-end)'
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
        preset = parsed.preset
        mfilter = True if parsed.filter == 'true' else False
        config = parsed.config if parsed.config else ''

        seq1 = seq[0]
        seq2 = None if len(seq) < 2 else seq[1]
        out1 = out[0]
        out2 = None if len(out) < 2 else out[1]

        return self.run(idx,
                        seq1,
                        out1,
                        out2=out2,
                        seq2=seq2,
                        mfilter=mfilter,
                        threads=threads,
                        preset=preset,
                        options=config)
