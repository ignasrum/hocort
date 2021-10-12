import pysam
import hocort.execute as exe
import multiprocessing

class SAM:
    def extract_ids(path, mapping_quality=0, add_slash=False, mode='r'):
        threads = multiprocessing.cpu_count()
        added = {}
        query_names = []
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

        return query_names

    # input:  sam
    # output: bam
    def remove(input_path, output_path, quality_score, options=[]):
        cmd = ['samtools', 'view', '-bSq', str(quality_score), '-o', output_path, input_path] + options

        return exe.execute(cmd)
