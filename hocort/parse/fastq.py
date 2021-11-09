import hocort.execute as exe

class FastQ:
    def filter_by_id(input_path, output_path, filter_path, include='f', options=[]):
        # filterbyname.sh in=input.fastq out=filtered.fastq names=seq_ids_to_remove.fastq include=f ow=t
        cmd = ['filterbyname.sh', f'in={input_path}', f'out={output_path}', f'names={filter_path}', f'include={include}', 'ow=t'] + options

        return exe.execute(cmd)
