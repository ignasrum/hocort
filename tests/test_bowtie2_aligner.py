import tempfile
import os

from hocort.aligners.bowtie2 import Bowtie2

from helper import helper

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/bowtie2/genome'
fasta = f'{path}/test_data/fasta/genome.fna'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
output = f'{temp_dir.name}/output'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
no_path = ''

def test_build_idx():
    returncode = Bowtie2().build_index(output, fasta)
    assert returncode == 0

def test_build_idx_no_input():
    returncode = Bowtie2().build_index(output, no_path)
    assert returncode == 1

def test_idx_no_path():
    cmd = Bowtie2().align(no_path, seq1, output)
    assert cmd == None

def test_idx_path():
    cmd = Bowtie2().align(temp_dir.name, seq1, output)
    helper(cmd, 1)

def test_seq1_no_path():
    cmd = Bowtie2().align(idx, no_path, output)
    assert cmd == None

def test_output_no_path():
    cmd = Bowtie2().align(idx, seq1, no_path)
    helper(cmd, 0)

def test_output_path():
    cmd = Bowtie2().align(idx, seq1, temp_dir.name)
    helper(cmd, 1)

def test_seq1_seq2_no_path():
    cmd = Bowtie2().align(idx, no_path, output, seq2=no_path)
    assert cmd == None

def test_seq2_no_path():
    cmd = Bowtie2().align(idx, seq1, output, seq2=no_path)
    helper(cmd, 0)

def test_local_1():
    options = ['--local']
    cmd = Bowtie2().align(idx, seq1, output, options=options)
    helper(cmd, 0)

def test_local_2():
    options = ['--local']
    cmd = Bowtie2().align(idx, seq1, output, seq2=seq2, options=options)
    helper(cmd, 0)

def test_end_to_end_1():
    options = ['--end-to-end']
    cmd = Bowtie2().align(idx, seq1, output, options=options)
    helper(cmd, 0)

def test_end_to_end_sam_2():
    options = ['--end-to-end']
    cmd = Bowtie2().align(idx, seq1, output, seq2=seq2, options=options)
    helper(cmd, 0)
