import tempfile
import os

import pytest

from hocort.aligners.bwa_mem2 import BWA_MEM2

from helper import helper

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/bwa_mem2/genome'
fasta = f'{path}/test_data/fasta/genome.fna'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
output = f'{temp_dir.name}/output'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
no_path = ''

def test_build_idx():
    cmd = BWA_MEM2().build_index(output, fasta)
    helper(cmd, 0)

def test_build_idx_no_input():
    with pytest.raises(ValueError):
        cmd = BWA_MEM2().build_index(output, no_path)

def test_idx_no_path():
    with pytest.raises(ValueError):
        cmd = BWA_MEM2().align(no_path, seq1, output)

def test_seq1_no_path():
    with pytest.raises(ValueError):
        cmd = BWA_MEM2().align(idx, no_path, output)

def test_seq1_path():
    cmd = BWA_MEM2().align(idx, temp_dir.name, output)
    helper(cmd, 1)

def test_output_no_path():
    cmd = BWA_MEM2().align(idx, seq1, no_path)
    helper(cmd, 0)

def test_seq1_seq2_no_path():
    with pytest.raises(ValueError):
        cmd = BWA_MEM2().align(idx, no_path, output, seq2=no_path)

def test_seq1_seq2_path():
    cmd = BWA_MEM2().align(idx, temp_dir.name, output, seq2=temp_dir.name)
    helper(cmd, 1)

def test_seq2_no_path():
    cmd = BWA_MEM2().align(idx, seq1, output, seq2=no_path)
    helper(cmd, 0)

def test_1():
    cmd = BWA_MEM2().align(idx, seq1, output)
    helper(cmd, 0)

def test_2():
    cmd = BWA_MEM2().align(idx, seq1, output, seq2=seq2)
    helper(cmd, 0)
