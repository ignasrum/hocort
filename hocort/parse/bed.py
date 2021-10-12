import hocort.execute as exe


class BED:
    def extract_sequence_ids(bed_path, output_path, options=[]):
        # awk '{ print $4 }' in.bed
        cmd = ['awk', '{ print $4 }', bed_path] + options

        return exe.execute(cmd, out_file=output_path)
