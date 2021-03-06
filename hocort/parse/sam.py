class SAM:
    """
    SAM parsing and processing class.

    """
    def select(input_path=None, output_path=None, paired=True, threads=1, mfilter=True):
        """
        Takes SAM input, selects mapped/unmapped reads, and outputs SAM.

        Parameters
        ----------
        input_path : string
            Input SAM file path.
        output_path : string
            Output SAM file path.
        paired : bool
            Process reads as paired or unpaired.
        threads : int
            Number of threads to use.
        mfilter : bool
            Whether to output mapped/unmapped sequences.
            True: output unmapped sequences
            False: output mapped sequences

        Returns
        -------
        [cmd] : list
            List of commands to be executed.

        """
        cmd = ['samtools', 'view', '--threads', f'{threads}', '-h']
        if paired:
            if mfilter:
                cmd += ['-f', '13']
            else:
                cmd += ['-F', '12', '-f', '1']
        else:
            if mfilter:
                cmd += ['-f', '4']
            else:
                cmd += ['-F', '4']
        if output_path:
            cmd += ['-o', output_path]
        if input_path:
            cmd += [input_path]
        else:
            cmd += ['-']

        return [cmd]

    def sam_to_fastq(input_path=None, out1=None, out2=None, threads=1, mfilter=False):
        """
        Takes SAM input, selects mapped/unmapped reads, and outputs FastQ.

        Parameters
        ----------
        input_path : string
            Input SAM file path.
        out1 : string
            FastQ READ1 (if paired), READ_OTHER (if unpaired) output path.
        out2 : string
            FastQ READ2 output path.
        threads : int
            Number of threads to use.
        mfilter : bool
            Whether to output mapped/unmapped sequences.
            True: output unmapped sequences
            False: output mapped sequences

        Returns
        -------
        [cmd] : list
            List of commands to be executed.

        """
        cmd = ['samtools', 'fastq', '--threads', f'{threads}', '-N']
        if out1 and out2:
            if mfilter:
                cmd += ['-f', '13']
            else:
                cmd += ['-F', '12', '-f', '1']
            cmd += ['-1', out1, '-2', out2]
        if out1 and not out2:
            if mfilter:
                cmd += ['-f', '4']
            else:
                cmd += ['-F', '4']
            cmd += ['-0', out1]
        if input_path:
            cmd += [input_path]
        else:
            cmd += ['-']

        return [cmd]
