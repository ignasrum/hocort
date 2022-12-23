import tempfile
import os

import pytest

from hocort.classifiers.biobloom import BioBloom

from helper import helper

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/biobloom/reference.bf'
fasta = f'{path}/test_data/fasta/genome.fna'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
output = f'{temp_dir.name}/output'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
no_path = ''

def test_build_idx_no_input():
    with pytest.raises(ValueError):
        cmd = BioBloom().build_index(output, no_path)

def test_idx_no_path():
    with pytest.raises(ValueError):
        cmd = BioBloom().classify(no_path, seq1, output)

def test_idx_path():
    cmd = BioBloom().classify(temp_dir.name, seq1, output)
    helper(cmd, -6)

def test_seq1_no_path():
    with pytest.raises(ValueError):
        cmd = BioBloom().classify(idx, no_path, output)

def test_seq1_path():
    cmd = BioBloom().classify(idx, temp_dir.name, output)
    helper(cmd, 0)

def test_seq1_seq2_no_path():
    with pytest.raises(ValueError):
        cmd = BioBloom().classify(idx, no_path, output, seq2=no_path)

def test_seq1_seq2_path():
    cmd = BioBloom().classify(idx, temp_dir.name, output, seq2=temp_dir.name)
    helper(cmd, 0)

def test_seq2_no_path():
    cmd = BioBloom().classify(idx, seq1, output, seq2=no_path)
    helper(cmd, 0)

def test_1():
    cmd = BioBloom().classify(idx, seq1, output)
    helper(cmd, 0)

def test_2():
    cmd = BioBloom().classify(idx, seq1, output, seq2=seq2)
    helper(cmd, 0)
