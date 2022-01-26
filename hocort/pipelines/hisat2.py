import time
import os

from hocort.pipelines.pipeline import Pipeline
from hocort.aligners.hisat2 import HISAT2 as hs2
from hocort.parse.sam import SAM
from hocort.parser import ArgParser
import hocort.execute as exe


class HISAT2(Pipeline):
    """
    HISAT2 pipeline which maps reads to a genome and includes/excludes matching reads from the output FastQ file/-s.

    """
    def __init__(self):
        """
        Sets the logger file source filename.

        Returns
        -------
        None

        """
        super().__init__(__file__)

    def run(self, idx, seq1, out1, seq2=None, out2=None, hcfilter=False, threads=1, quiet=False, options=[]):
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
        hcfilter : bool
            Whether to exclude or include the matching sequences from the output files.
        threads : int
            Number of threads to use.
        quiet : bool
            Toggles whether output is quiet or not.
        options : list
            An options list where additional arguments may be specified.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        self.debug_log_args(self.run.__name__, locals())
        if seq2 and not out2: return 1

        self.logger.warning(f'Starting pipeline: {self.__class__.__name__}')
        start_time = time.time()

        if len(options) > 0:
            options = options
        else:
            options = ['--sensitive', '--sp 3,2', '--mp 5,1']

        hs2_cmd = hs2().align(idx, seq1, seq2=seq2, threads=threads, options=options)
        if hs2_cmd == None: return 1
        fastq_cmd = SAM.sam_to_fastq(out1=out1, out2=out2, threads=threads, hcfilter=hcfilter)

        returncodes = exe.execute(hs2_cmd + fastq_cmd, pipe=True, quiet=quiet)

        self.logger.debug(returncodes)
        for returncode in returncodes:
            if returncode != 0: return 1

        end_time = time.time()
        self.logger.warning(f'Pipeline {self.__class__.__name__} run time: {end_time - start_time} seconds')
        return 0

    def interface(self, args, quiet=False):
        """
        Main function for the user interface. Parses arguments and starts the pipeline.

        Parameters
        ----------
        args : list
            This list is parsed by ArgumentParser.
        quiet : bool
            Toggles whether output is quiet or not.

        Returns
        -------
        None

        """
        parser = ArgParser(
            description=f'{self.__class__.__name__} pipeline',
            usage=f'hocort {self.__class__.__name__} [-h] [--threads <int>] [--host-contam-filter <bool>] -x <idx> -i <fastq_1> [<fastq_2>] -o <fastq_1> [<fastq_2>]'
        )
        parser.add_argument(
            '-x',
            '--index',
            required=True,
            type=str,
            metavar=('<idx>'),
            help='str: path to HISAT2 index (required)'
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
        out1 = out[0]
        out2 = None if len(out) < 2 else out[1]

        self.run(idx, seq1, out1, out2=out2, seq2=seq2, hcfilter=hcfilter, threads=threads, quiet=quiet)
