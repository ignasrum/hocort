import hocort.execute as exe


class BED:
    def extract_sequence_ids(bed_path, output_path, options=[]):
        log = open(output_path, 'w')
        log.flush()

        # awk '{ print $4 }' in.bed
        executable = ['awk']
        parameters = ['{ print $4 }', bed_path] + options

        result, returncode = exe.execute(executable, parameters, stdout=log, stderr=log)
        return result, returncode
