import pysam

class SAM:
    def extract_ids(path, threads=1, mapping_quality=0, add_slash=False, mode='r'):
        added = {}
        query_names = []
        try:
            with pysam.AlignmentFile(path, mode, threads=threads) as f:
                for read in f.fetch():
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
