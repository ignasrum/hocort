import pysam
import hocort.execute as exe
import multiprocessing

class SAM:
    def count_reads(path, mapping_quality, mode='r'):
        threads = multiprocessing.cpu_count()
        samfile = pysam.AlignmentFile(path, mode, threads=threads)
        query_names = []
        for read in samfile.fetch():
            if read.mapping_quality >= mapping_quality:
                query_names.append(read.query_name)
        samfile.close()
        return query_names

    # input:  sam
    # output: bam
    def remove(input_path, output_path, quality_score, options=[]):
        cmd = ['samtools', 'view', '-bSq', str(quality_score), input_path] + options

        returncode, result = exe.execute(cmd, out_file=output_path)
        return returncode, result
