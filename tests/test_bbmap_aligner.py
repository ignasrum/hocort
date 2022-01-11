from hocort.aligners.bbmap import BBMap as bb
import tempfile
import os

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/bbmap/'
fasta = f'{path}/test_data/fasta/genome.fna'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
output = f'{temp_dir.name}/output'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
no_path = ''

def test_build_idx():
    returncode = bb.build_index(output, fasta)
    assert returncode == 0

def test_build_idx_no_input():
    returncode = bb.build_index(output, no_path)
    assert returncode == 1

def test_idx_no_path():
    returncode = bb.align_sam(no_path, seq1, output)
    print(returncode)
    assert returncode == 1

def test_seq1_no_path():
    returncode = bb.align_sam(idx, no_path, output)
    assert returncode == 1

def test_seq1_path():
    returncode = bb.align_sam(idx, temp_dir.name, output)
    assert returncode == 1

def test_output_no_path():
    returncode = bb.align_sam(idx, seq1, no_path)
    assert returncode == 1

def test_output_path():
    returncode = bb.align_sam(idx, seq1, temp_dir.name)
    assert returncode == 0

def test_seq1_seq2_no_path():
    returncode = bb.align_sam(idx, no_path, output, seq2=no_path)
    assert returncode == 1

def test_seq1_seq2_path():
    returncode = bb.align_sam(idx, temp_dir.name, output, seq2=temp_dir)
    assert returncode == 2

def test_seq2_no_path():
    returncode = bb.align_sam(idx, seq1, output, seq2=no_path)
    assert returncode == 0

def test_sam_1():
    returncode = bb.align_sam(idx, seq1, output)
    assert returncode == 0

def test_sam_2():
    returncode = bb.align_sam(idx, seq1, output, seq2=seq2)
    assert returncode == 0

def test_bam_1():
    returncode = bb.align_bam(idx, seq1, output)
    assert returncode == 0

def test_bam_2():
    returncode = bb.align_bam(idx, seq1, output, seq2=seq2)
    assert returncode == 0
