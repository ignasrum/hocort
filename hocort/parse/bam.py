import pysam

class BAM:
    """
    BAM parsing and processing class.

    """
    def extract_ids(path, threads=1, mapping_quality=0, add_slash=False):
        """
        Extracts sequence ids from a BAM file.

        Parameters
        ----------
        path : string
            Input BAM file path.
        threads : int
            Number of threads to use.
        mapping_quality : int
            Lower bound of mapping quality for extracted sequences.
        add_slash : bool
            If true, for each sequence, add two names, one ending with '/1', the other ending with '/2'.

        Returns
        -------
        query_names : list
            List of sequence ids.

        """
        added = {}
        query_names = []
        try:
            with pysam.AlignmentFile(path, 'rb', threads=threads) as f:
                for read in f:
                    read_added = False
                    try: read_added = added[read.query_name]
                    except: pass
                    if read.mapping_quality > mapping_quality and not read_added:
                        added[read.query_name] = True
                        if add_slash:
                            query_names.append(read.query_name + '/1')
                            query_names.append(read.query_name + '/2')
                        else:
                            query_names.append(read.query_name)
        except Exception as e:
            print(e)
            return query_names
        return query_names
