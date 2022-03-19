import tempfile
import os

import pytest

from hocort.aligners.bbmap import BBMap

from helper import helper

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/bbmap/'
fasta = f'{path}/test_data/fasta/genome.fna'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
output = f'{temp_dir.name}/output.sam'
idx_out = f'{temp_dir.name}/test_idx/test_idx'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
no_path = ''

def test_build_idx():
    cmd = BBMap().build_index(idx_out, fasta)
    helper(cmd, 0)

def test_build_idx_no_input():
    with pytest.raises(ValueError):
        cmd = BBMap().build_index(idx_out, no_path)

def test_idx_no_path():
    with pytest.raises(ValueError):
        cmd = BBMap().align(no_path, seq1, output)

def test_seq1_no_path():
    with pytest.raises(ValueError):
        cmd = BBMap().align(idx, no_path, output)

def test_seq1_path():
    cmd = BBMap().align(idx, temp_dir.name, output)
    helper(cmd, 1)

def test_output_no_path():
    cmd = BBMap().align(idx, seq1, no_path)
    helper(cmd, 0)

def test_output_path():
    cmd = BBMap().align(idx, seq1, temp_dir.name)
    helper(cmd, 1)

def test_seq1_seq2_no_path():
    with pytest.raises(ValueError):
        cmd = BBMap().align(idx, no_path, output, seq2=no_path)

def test_seq1_seq2_path():
    cmd = BBMap().align(idx, seq1, output, seq2=seq2)
    helper(cmd, 0)

def test_seq2_no_path():
    cmd = BBMap().align(idx, seq1, output, seq2=no_path)
    helper(cmd, 0)

def test_sam_1():
    cmd = BBMap().align(idx, seq1, output)
    helper(cmd, 0)
