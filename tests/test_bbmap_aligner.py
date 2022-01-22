import tempfile
import os

from hocort.aligners.bbmap import BBMap as bb

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
    cmd = bb.build_index(idx_out, fasta)
    helper(cmd, 0)

def test_build_idx_no_input():
    cmd = bb.build_index(idx_out, no_path)
    assert cmd == None

def test_idx_no_path():
    cmd = bb.align(no_path, seq1, output)
    assert cmd == None

def test_seq1_no_path():
    cmd = bb.align(idx, no_path, output)
    assert cmd == None

def test_seq1_path():
    cmd = bb.align(idx, temp_dir.name, output)
    helper(cmd, 1)

def test_output_no_path():
    cmd = bb.align(idx, seq1, no_path)
    helper(cmd, 0)

def test_output_path():
    cmd = bb.align(idx, seq1, temp_dir.name)
    helper(cmd, 1)

def test_seq1_seq2_no_path():
    cmd = bb.align(idx, no_path, output, seq2=no_path)
    assert cmd == None

def test_seq1_seq2_path():
    cmd = bb.align(idx, seq1, output, seq2=seq2)
    helper(cmd, 0)

def test_seq2_no_path():
    cmd = bb.align(idx, seq1, output, seq2=no_path)
    helper(cmd, 0)

def test_sam_1():
    cmd = bb.align(idx, seq1, output)
    helper(cmd, 0)
