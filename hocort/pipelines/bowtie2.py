import time
import os

from hocort.pipelines.pipeline import Pipeline
from hocort.aligners.bowtie2 import Bowtie2 as bt2
from hocort.parse.sam import SAM
from hocort.parser import ArgParser
import hocort.execute as exe


class Bowtie2(Pipeline):
    """
    Bowtie2 pipeline which maps reads to a genome and includes/excludes matching reads from the output FastQ file/-s.

    """
    def __init__(self):
        """
        Sets the logger file source filename.

        Returns
        -------
        None

        """
        super().__init__(__file__)

    def run(self, idx, seq1, out1, seq2=None, out2=None, mfilter=True, mode='local', threads=1, options=[]):
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
        mode : string
            Bowtie2 execution mode. Can either be 'local' or 'end-to-end'.
        threads : int
            Number of threads to use.
        options : list
            An options list where additional arguments may be specified.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        Raises
        ------
            If input FastQ_2 file is given without output FastQ_2.

        """
        self.debug_log_args(self.run.__name__, locals())
        if seq2 and not out2:
            raise ValueError(f'Input FastQ_2 was given, but no output FastQ_2.')

        if len(options) > 0:
            options = options
        elif mode == 'local':
            options = ['--local', '--very-fast-local', '--score-min G,21,9']
        elif mode == 'end-to-end':
            options = ['--end-to-end', '--sensitive', '--score-min L,-0.4,-0.4']
        else:
            self.logger.error(f'Invalid mode: {mode}')
            return 1

        self.logger.warning(f'Running pipeline: {self.__class__.__name__}')
        start_time = time.time()

        bowtie2_cmd = bt2().align(idx, seq1, seq2=seq2, threads=threads, options=options)
        if bowtie2_cmd == None: return 1
        fastq_cmd = SAM.sam_to_fastq(out1=out1, out2=out2, threads=threads, mfilter=mfilter)

        returncodes = exe.execute(bowtie2_cmd + fastq_cmd, pipe=True)

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
            usage=f'hocort map {self.__class__.__name__} [-h] [--threads <int>] [--mode <mode>] [--filter <bool>] -x <idx> -i <fastq_1> [<fastq_2>] -o <fastq_1> [<fastq_2>]'
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
            '-m',
            '--mode',
            choices=['local', 'end-to-end'],
            default='local',
            help='str: operation mode (default: local)'
        )
        parser.add_argument(
            '-f',
            '--filter',
            choices=['True', 'False'],
            default='True',
            help='str: set to False to output mapped sequences, True to output unmapped sequences (default: True)'
        )
        parsed = parser.parse_args(args=args)

        idx = parsed.index
        seq = parsed.input
        out = parsed.output
        threads = parsed.threads if parsed.threads else 1
        mode = parsed.mode
        mfilter = True if parsed.filter == 'True' else False

        seq1 = seq[0]
        seq2 = None if len(seq) < 2 else seq[1]
        out1 = out[0]
        out2 = None if len(out) < 2 else out[1]

        return self.run(idx, seq1, out1, out2=out2, seq2=seq2, mfilter=mfilter, threads=threads, mode=mode)
