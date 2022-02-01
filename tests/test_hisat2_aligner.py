import tempfile
import os

from hocort.aligners.hisat2 import HISAT2

from helper import helper

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/hisat2/genome'
fasta = f'{path}/test_data/fasta/genome.fna'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
output = f'{temp_dir.name}/output'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
no_path = ''

def test_build_idx():
    cmd = HISAT2().build_index(output, fasta)
    helper(cmd, 0)

def test_build_idx_no_input():
    cmd = HISAT2().build_index(output, no_path)
    assert cmd == None

def test_idx_no_path():
    cmd = HISAT2().align(no_path, seq1, output)
    assert cmd == None

def test_idx_path():
    cmd = HISAT2().align(temp_dir.name, seq1, output)
    helper(cmd, 255)

def test_seq1_no_path():
    cmd = HISAT2().align(idx, no_path, output)
    assert cmd == None

def test_output_no_path():
    cmd = HISAT2().align(idx, seq1, no_path)
    helper(cmd, 0)

def test_seq1_seq2_no_path():
    cmd = HISAT2().align(idx, no_path, output, seq2=no_path)
    assert cmd == None

def test_seq2_no_path():
    cmd = HISAT2().align(idx, seq1, output, seq2=no_path)
    helper(cmd, 0)

def test_1():
    cmd = HISAT2().align(idx, seq1, output)
    helper(cmd, 0)

def test_2():
    cmd = HISAT2().align(idx, seq1, output, seq2=seq2)
    helper(cmd, 0)
