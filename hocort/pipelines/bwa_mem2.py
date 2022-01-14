import os
import time

from hocort.pipelines.pipeline import Pipeline
from hocort.aligners.bwa_mem2 import BWA_MEM2 as bwa_mem2
from hocort.parse.sam import SAM
from hocort.parse.bam import BAM
from hocort.parse.fastq import FastQ
from hocort.parser import ArgParser


class BWA_MEM2(Pipeline):
    """
    BWA-MEM2 pipeline which maps reads to a genome and includes/excludes matching reads from the output FastQ file/-s.

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
        super().__init__(__file__, dir=dir)

    def run(self, idx, seq1, out1, seq2=None, out2=None, intermediary='SAM', hcfilter=False, threads=1, mapq=0, options=[]):
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
        intermediary : string
            The format of the intermediary mapping file. SAM or BAM.
        hcfilter : bool
            Whether to exclude or include the matching sequences from the output files.
        threads : int
            Number of threads to use.
        mapq : int
            Mapping quality lower bound.
        options : list
            An options list where additional arguments may be specified.

        Returns
        -------
        returncode : int
            Resulting returncode after the process is finished.

        """
        self.debug_log_args(self.run.__name__, locals())
        self.logger.warning(f'Starting pipeline: {self.__class__.__name__}')
        start_time = time.time()
        # MAP READS TO INDEX
        if len(options) > 0:
            options = options
        else:
            options = ['-O 20,20', '-E 6,6', '-L 2,2']

        bwa_mem2_output = f'{self.temp_dir.name}/output.sam'

        add_slash=False
        if seq2: add_slash = True
        query_names = []

        self.logger.info('Aligning reads with BWA-MEM2')
        if intermediary == 'BAM':
            returncode = bwa_mem2.align_bam(idx, seq1, bwa_mem2_output, seq2=seq2, threads=threads, options=options)
            if returncode[0] != 0 or returncode[1] != 0:
                self.logger.error('Pipeline was terminated')
                return 1
            self.logger.info('Extracting sequence ids')
            query_names = BAM.extract_ids(bwa_mem2_output, mapping_quality=mapq, threads=threads, add_slash=add_slash)
        else:
            returncode = bwa_mem2.align_sam(idx, seq1, bwa_mem2_output, seq2=seq2, threads=threads, options=options)
            if returncode != 0:
                self.logger.error('Pipeline was terminated')
                return 1
            self.logger.info('Extracting sequence ids')
            query_names = SAM.extract_ids(bwa_mem2_output, mapping_quality=mapq, add_slash=add_slash)

        # REMOVE FILTERED READS FROM ORIGINAL FASTQ FILES
        returncode = self.filter(query_names, seq1, out1, seq2=seq2, out2=out2, hcfilter=hcfilter)
        if returncode != 0:
            self.logger.error('Pipeline was terminated')
            return 1

        end_time = time.time()
        self.logger.warning(f'Pipeline run time: {end_time - start_time} seconds')
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
            usage=f'hocort {self.__class__.__name__} [-h] [--threads <int>] [--intermediary <format>] [--host-contam-filter <bool>] -x <idx> -i <fastq_1> [<fastq_2>] -o <fastq_1> [<fastq_2>]'
        )
        parser.add_argument(
            '-x',
            '--index',
            required=True,
            type=str,
            metavar=('<idx>'),
            help='str: path to BWA_MEM2 index (required)'
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
            '-r',
            '--intermediary',
            choices=['SAM', 'BAM'],
            default='SAM',
            help='str: intermediary step output format (default: SAM)'
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
        intermediary = parsed.intermediary
        hcfilter = True if parsed.host_contam_filter == 'True' else False

        seq1 = seq[0]
        seq2 = None if len(seq) < 2 else seq[1]
        out1 = out[0]
        out2 = None if len(out) < 2 else out[1]

        self.run(idx, seq1, out1, out2=out2, seq2=seq2, intermediary=intermediary, hcfilter=hcfilter, threads=threads)
