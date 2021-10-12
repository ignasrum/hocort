import hocort.execute as exe
import pysam
import multiprocessing


class BAM:
    # bedtools bamtobed [OPTIONS] -i <BAM>
    def bam_to_bed(bam_path, output_path, options=[]):
        # bedtools bamtobed -i reads.bam > reads.bed
        cmd = ['bedtools', 'bamtobed', '-i', bam_path] + options

        return exe.execute(cmd, out_file=output_path)

    # input:  bam
    # output: bam
    def remove(input_path, output_path, quality_score, options=[]):
        cmd = ['samtools', 'view', '-bq', str(quality_score), input_path] + options

        return exe.execute(cmd, out_file=output_path)

    def extract_ids(path, mapping_quality=0, add_slash=False, mode='rb'):
        threads = multiprocessing.cpu_count()
        added = {}
        query_names = []
        with pysam.AlignmentFile(path, mode, threads=threads) as f:
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
        return query_names
