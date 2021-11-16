import hocort.execute as exe
from hocort.aligners.aligner import Aligner


class BBMap(Aligner):
    def build_index(path_out, fasta_in, threads=1, options=[]):
        cmd = ['bbmap.sh', f'threads={str(threads)}', f'ref={fasta_in}', f'path={path_out}']

        return exe.execute(cmd, decode_stderr=True)

    def align_sam(index, seq1, output, seq2=None, threads=1, options=[]):
        cmd = ['bbmap.sh', f'threads={str(threads)}', f'path={index}', f'out={output}.sam']
        if seq2:
            cmd += [f'in={seq1}', f'in2={seq2}']
        else: cmd += [f'in={seq1}']
        cmd += options

        return exe.execute(cmd, decode_stderr=True)

    def align_bam(index, seq1, output, seq2=None, threads=1, options=[]):
        cmd = ['bbmap.sh', f'threads={str(threads)}', f'path={index}', f'out={output}.bam']
        if seq2:
            cmd += [f'in={seq1}', f'in2={seq2}']
        else: cmd += [f'in={seq1}']
        cmd += options

        return exe.execute(cmd, decode_stderr=True)
