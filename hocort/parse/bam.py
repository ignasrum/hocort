import hocort.execute as exe


class BAM:
    # bedtools bamtobed [OPTIONS] -i <BAM>
    def bam_to_bed(bam_path, output_path, options=[]):
        # bedtools bamtobed -i reads.bam > reads.bed
        cmd = ['bedtools', 'bamtobed', '-i', bam_path] + options

        returncode, result = exe.execute(cmd, out_file=output_path)
        return returncode, result
