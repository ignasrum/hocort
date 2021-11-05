from hocort.classifiers.kraken2 import Kraken2 as kr2
import tempfile
import os

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/kraken2'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
class_out = f'{temp_dir.name}/class#.fq'
unclass_out = f'{temp_dir.name}/unclass#.fq'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
no_path = ''

def test_idx_no_path():
    returncode, stdout, stderr = kr2.classify(no_path, seq1, class_out, unclass_out)
    print(stderr[0])
    assert returncode[0] == 2

def test_seq1_no_path():
    returncode, stdout, stderr = kr2.classify(idx, no_path, class_out, unclass_out)
    print(stderr[0])
    assert returncode[0] == 0

def test_output_no_path():
    returncode, stdout, stderr = kr2.classify(idx, seq1, class_out, unclass_out)
    print(stderr[0])
    assert returncode[0] == 0

def test_seq1_seq2_no_path():
    returncode, stdout, stderr = kr2.classify(idx, no_path, class_out, unclass_out, seq2=no_path)
    print(stderr[0])
    assert returncode[0] == 0

def test_seq2_no_path():
    returncode, stdout, stderr = kr2.classify(idx, seq1, class_out, unclass_out, seq2=no_path)
    print(stderr[0])
    assert returncode[0] == 0

def test_1():
    returncode, stdout, stderr = kr2.classify(idx, seq1, class_out, unclass_out)
    print(stderr[0])
    assert returncode[0] == 0

def test_2():
    returncode, stdout, stderr = kr2.classify(idx, seq1, class_out, unclass_out, seq2=seq2)
    print(stderr[0])
    assert returncode[0] == 0
