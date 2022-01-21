import time
import os
import tempfile

from hocort.pipelines.pipeline import Pipeline
from hocort.pipelines.bowtie2 import Bowtie2
from hocort.parser import ArgParser


class Bowtie2Bowtie2(Pipeline):
    """
    Bowtie2Bowtie2 pipeline which first runs Bowtie2 in 'end-to-end' mode, then in 'local' mode. It maps reads to a genome and includes/excludes matching reads from the output FastQ file/-s.

    """
    def __init__(self):
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
        super().__init__(__file__)
        self.temp_dir = tempfile.TemporaryDirectory()
        self.logger.debug(self.temp_dir.name)

    def run(self, idx, seq1, out1, seq2=None, out2=None, hcfilter=False, threads=1):
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

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        self.debug_log_args(self.run.__name__, locals())
        self.logger.warning(f'Starting pipeline: {self.__class__.__name__}')
        start_time = time.time()
        temp1 = f'{self.temp_dir.name}/temp1.fastq'
        temp2 = None if seq2 == None else f'{self.temp_dir.name}/temp2.fastq'
        returncode = Bowtie2().run(idx, seq1, temp1, seq2=seq2, out2=temp2, mode='end-to-end', hcfilter=hcfilter)
        if returncode != 0:
            self.logger.error('Pipeline was terminated')
            return 1
        returncode = Bowtie2().run(idx, temp1, out1, seq2=temp2, out2=out2, mode='local', hcfilter=hcfilter)
        if returncode != 0:
            self.logger.error('Pipeline was terminated')
            return 1
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
            usage=f'hocort {self.__class__.__name__} [-h] [--threads <int>] [--host-contam-filter <bool>] -x <idx> -i <fastq_1> [<fastq_2>] -o <fastq_1> [<fastq_2>]'
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

        self.run(idx, seq1, out1, seq2=seq2, out2=out2, threads=threads, hcfilter=hcfilter)
