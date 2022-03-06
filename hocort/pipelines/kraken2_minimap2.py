import time
import os
import tempfile

from hocort.pipelines.pipeline import Pipeline
from hocort.pipelines.minimap2 import Minimap2
from hocort.pipelines.kraken2 import Kraken2
from hocort.parser import ArgParser


class Kraken2Minimap2(Pipeline):
    """
    Kraken2Minimap2 pipeline which first runs Kraken2, then runs Minimap2. It maps reads to a genome and includes/excludes matching reads from the output FastQ file/-s.

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
        super().__init__(__file__)
        self.temp_dir = tempfile.TemporaryDirectory(dir=dir)
        self.logger.debug(self.temp_dir.name)

    def run(self, mn2_idx, kr2_idx, seq1, out1, seq2=None, out2=None, hcfilter=False, preset='illumina', threads=1):
        """
        Run function which starts the pipeline.

        Parameters
        ----------
        mn2_idx : string
            Path where the Minimap2 index is located.
        kr2_idx : string
            Path where the Kraken2 index is located.
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
        preset : str
            Type of reads to align to reference.
            Types: 'illumina', 'nanopore' or 'pacbio'
        threads : int
            Number of threads to use.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        self.debug_log_args(self.run.__name__, locals())
        if seq2 and not out2: return 1
        self.logger.warning(f'Running pipeline: {self.__class__.__name__}')
        start_time = time.time()

        kr2_out = self.temp_dir.name + '/out#.fastq' if seq2 and out2 else self.temp_dir.name + '/out_1.fastq'
        returncode = Kraken2().run(kr2_idx, seq1, kr2_out, seq2=seq2, hcfilter=hcfilter, threads=threads)
        if returncode != 0:
            self.logger.error('Pipeline was terminated')
            return 1

        temp1 = f'{self.temp_dir.name}/out_1.fastq'
        temp2 = None if seq2 == None else f'{self.temp_dir.name}/out_2.fastq'

        returncode = Minimap2().run(mn2_idx, temp1, out1, seq2=temp2, out2=out2, threads=threads, hcfilter=hcfilter, preset=preset)
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
            usage=f'hocort map {self.__class__.__name__} [-h] [--threads <int>] [--host-contam-filter <bool>] --minimap2_index <idx> --kraken2_index <idx> -i <fastq_1> [<fastq_2>] -o <fastq_1> [<fastq_2>]'
        )
        parser.add_argument(
            '-m',
            '--minimap2_index',
            required=True,
            type=str,
            metavar=('<idx>'),
            help='str: path to Minimap2 index (required)'
        )
        parser.add_argument(
            '-k',
            '--kraken2_index',
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
            '--host-contam-filter',
            required=False,
            choices=['True', 'False'],
            default='False',
            help='str: set to True to keep host sequences, False to keep everything besides host sequences (default: False)'
        )
        parser.add_argument(
            '-p',
            '--preset',
            required=False,
            choices=['illumina', 'nanopore', 'pacbio'],
            default='illumina',
            help='str: type of reads (default: illumina)'
        )
        parsed = parser.parse_args(args=args)

        mn2_idx = parsed.minimap2_index
        kr2_idx = parsed.kraken2_index
        seq = parsed.input
        out = parsed.output
        threads = parsed.threads if parsed.threads else 1
        hcfilter = True if parsed.host_contam_filter == 'True' else False
        preset = parsed.preset

        seq1 = seq[0]
        seq2 = None if len(seq) < 2 else seq[1]
        out1 = out[0]
        out2 = None if len(out) < 2 else out[1]

        return self.run(mn2_idx, kr2_idx, seq1, out1, seq2=seq2, out2=out2, threads=threads, hcfilter=hcfilter, preset=preset)
