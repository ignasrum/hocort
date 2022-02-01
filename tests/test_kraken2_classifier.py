import tempfile
import os

from hocort.classifiers.kraken2 import Kraken2

from helper import helper

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/kraken2'
fasta = f'{path}/test_data/fasta/genome.fna'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
class_out = f'{temp_dir.name}/class#.fq'
unclass_out = f'{temp_dir.name}/unclass#.fq'
output = f'{temp_dir.name}/output'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
no_path = ''

def test_build_idx_no_input():
    cmd = Kraken2().build_index(output, no_path)
    assert cmd == None

def test_idx_no_path():
    cmd = Kraken2().classify(no_path, seq1, class_out, unclass_out)
    assert cmd == None

def test_idx_path():
    cmd = Kraken2().classify(temp_dir.name, seq1, class_out, unclass_out)
    helper(cmd, 2)

def test_seq1_no_path():
    cmd = Kraken2().classify(idx, no_path, class_out, unclass_out)
    assert cmd == None

def test_seq1_path():
    cmd = Kraken2().classify(idx, temp_dir.name, class_out, unclass_out)
    helper(cmd, 0)

def test_class_out_no_path():
    cmd = Kraken2().classify(idx, seq1, no_path, unclass_out)
    helper(cmd, 0)

def test_class_out_path():
    cmd = Kraken2().classify(idx, seq1, temp_dir.name, unclass_out)
    helper(cmd, 0)

def test_unclass_out_no_path():
    cmd = Kraken2().classify(idx, seq1, class_out, no_path)
    helper(cmd, 0)

def test_unclass_out_path():
    cmd = Kraken2().classify(idx, seq1, class_out, temp_dir.name)
    helper(cmd, 0)

def test_output_no_path():
    cmd = Kraken2().classify(idx, seq1, class_out, unclass_out)
    helper(cmd, 0)

def test_seq1_seq2_no_path():
    cmd = Kraken2().classify(idx, no_path, class_out, unclass_out, seq2=no_path)
    assert cmd == None

def test_seq1_seq2_path():
    cmd = Kraken2().classify(idx, temp_dir.name, class_out, unclass_out, seq2=temp_dir.name)
    helper(cmd, 0)

def test_seq2_no_path():
    cmd = Kraken2().classify(idx, seq1, class_out, unclass_out, seq2=no_path)
    helper(cmd, 0)

def test_1():
    cmd = Kraken2().classify(idx, seq1, class_out, unclass_out)
    helper(cmd, 0)

def test_2():
    cmd = Kraken2().classify(idx, seq1, class_out, unclass_out, seq2=seq2)
    helper(cmd, 0)
