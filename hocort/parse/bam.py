import hocort.execute as exe


class BAM:
    # bedtools bamtobed [OPTIONS] -i <BAM>
    def bam_to_bed(bam_path, output_path, options=[]):
        log = open(output_path, 'w')
        log.flush()

        # bedtools bamtobed -i reads.bam > reads.bed
        executable = ['bedtools']
        parameters = ['bamtobed', '-i', bam_path] + options

        result, returncode = exe.execute(executable, parameters, stdout=log, stderr=log)
        return result, returncode
