from hocort.aligners.star import STAR
import tempfile
import os

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/star'
fasta = f'{path}/test_data/fasta/genome.fna'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
output = f'{temp_dir.name}/output'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
no_path = ''

def test_build_idx():
    returncode, stdout, stderr = STAR.build_index(output, fasta)
    assert returncode[0] == 0

def test_build_idx_no_input():
    returncode, stdout, stderr = STAR.build_index(output, no_path)
    assert returncode[0] == 102

def test_idx_no_path():
    returncode, stdout, stderr = STAR.align_sam(no_path, seq1, output)
    print(stderr[0])
    assert returncode[0] == 102

def test_seq1_no_path():
    returncode, stdout, stderr = STAR.align_sam(idx, no_path, output)
    print(stderr[0])
    assert returncode[0] == 102

def test_output_no_path():
    returncode, stdout, stderr = STAR.align_sam(idx, seq1, no_path)
    print(stderr[0])
    assert returncode[0] == 102

def test_seq1_seq2_no_path():
    returncode, stdout, stderr = STAR.align_sam(idx, no_path, output, seq2=no_path)
    print(stderr[0])
    assert returncode[0] == 102

def test_seq2_no_path():
    returncode, stdout, stderr = STAR.align_sam(idx, seq1, output, seq2=no_path)
    print(stderr[0])
    assert returncode[0] == 0

def test_sam_1():
    returncode, stdout, stderr = STAR.align_sam(idx, seq1, output)
    print(stderr[0])
    assert returncode[0] == 0

def test_sam_2():
    returncode, stdout, stderr = STAR.align_sam(idx, seq1, output, seq2=seq2)
    print(stderr[0])
    assert returncode[0] == 0

def test_bam_1():
    returncode, stdout, stderr = STAR.align_bam(idx, seq1, output)
    print(stderr[0])
    assert returncode[0] == 0

def test_bam_2():
    returncode, stdout, stderr = STAR.align_bam(idx, seq1, output, seq2=seq2)
    print(stderr[0])
    assert returncode[0] == 0
