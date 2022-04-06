import time
import os
import tempfile
import logging

from hocort.pipelines.pipeline import Pipeline
from hocort.pipelines.bowtie2 import Bowtie2
from hocort.pipelines.hisat2 import HISAT2
from hocort.parser import ArgParser

logger = logging.getLogger(__file__)


class Bowtie2HISAT2(Pipeline):
    """
    Bowtie2HISAT2 pipeline which first runs Bowtie2 in 'end-to-end' mode, then runs HISAT2. It maps reads to a genome and includes/excludes matching reads from the output FastQ file/-s.

    """
    def __init__(self, dir=None):
        """
        Constructor which sets temporary file directory if specified.

        Parameters
        ----------
        dir : string
            Path where the temporary files are written.

        Returns
        -------
        None

        """
        self.temp_dir = tempfile.TemporaryDirectory(dir=dir)
        logger.debug(self.temp_dir.name)

    def run(self, bt2_idx, hs2_idx, seq1, out1, seq2=None, out2=None, mfilter=True, threads=1, bt2_options=[], hs2_options=[]):
        """
        Run function which starts the pipeline.

        Parameters
        ----------
        bt2_idx : string
            Path where the Bowtie2 index is located.
        hs2_idx : string
            Path where the HISAT2 index is located.
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
        threads : int
            Number of threads to use.
        bt2_options : list
            An options list, for Bowtie2, where arguments passed to the tool may be configured.
        hs2_options : list
            An options list, for HISAT2, where arguments passed to the tool may be configured.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        Raises
        ------
        ValueError
            If input FastQ_2 file is given without output FastQ_2.

        """
        self.debug_log_args(logger,
                            self.run.__name__,
                            locals())
        if seq2 and not out2:
            raise ValueError(f'Input FastQ_2 was given, but no output FastQ_2.')

        logger.warning(f'Running pipeline: {self.__class__.__name__}')
        start_time = time.time()
        temp1 = f'{self.temp_dir.name}/temp1.fastq.gz'
        temp2 = None if seq2 == None else f'{self.temp_dir.name}/temp2.fastq.gz'
        returncode = Bowtie2().run(bt2_idx,
                                   seq1,
                                   temp1,
                                   seq2=seq2,
                                   out2=temp2,
                                   preset='end-to-end',
                                   threads=threads,
                                   mfilter=mfilter,
                                   options=bt2_options)
        if returncode != 0:
            logger.error('Pipeline was terminated')
            return 1
        returncode = HISAT2().run(hs2_idx,
                                  temp1,
                                  out1,
                                  seq2=temp2,
                                  out2=out2,
                                  threads=threads,
                                  mfilter=mfilter,
                                  options=hs2_options)
        if returncode != 0:
            logger.error('Pipeline was terminated')
            return 1
        end_time = time.time()
        logger.warning(f'Pipeline {self.__class__.__name__} run time: {end_time - start_time} seconds')
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
            usage=f'hocort map {self.__class__.__name__} [-h] [--threads <int>] [--filter <bool>] --bowtie2_index <idx> --hisat2_index <idx> -i <fastq_1> [<fastq_2>] -o <fastq_1> [<fastq_2>]'
        )
        parser.add_argument(
            '-b',
            '--bowtie2_index',
            required=True,
            type=str,
            metavar=('<idx>'),
            help='str: path to Bowtie2 index (required)'
        )
        parser.add_argument(
            '-s',
            '--hisat2_index',
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
            help='str: path to sequence files, max 2 (.gz compression supported) (required)'
        )
        parser.add_argument(
            '-o',
            '--output',
            required=True,
            type=str,
            nargs=('+'),
            metavar=('<fastq_1>', '<fastq_2>'),
            help='str: path to output files, max 2 (.gz compression supported) (required)'
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
        parsed = parser.parse_args(args=args)

        bt2_idx = parsed.bowtie2_index
        hs2_idx = parsed.hisat2_index
        seq = parsed.input
        out = parsed.output
        threads = parsed.threads if parsed.threads else 1
        mfilter = True if parsed.filter == 'true' else False

        seq1 = seq[0]
        seq2 = None if len(seq) < 2 else seq[1]
        out1 = out[0]
        out2 = None if len(out) < 2 else out[1]

        return self.run(bt2_idx,
                        hs2_idx,
                        seq1,
                        out1,
                        seq2=seq2,
                        out2=out2,
                        threads=threads,
                        mfilter=mfilter)
