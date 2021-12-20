from hocort.parse.fastq import FastQ
import tempfile
import os

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

seq1 = f'{path}/test_data/sequences/sequences1.fastq'
output = f'{temp_dir.name}/out.fastq'
ids = f'{path}/test_data/sequences/ids.list'
no_path = ''

def test_fastq_valid():
    returncode = FastQ.filter_by_id(seq1, output, ids)
    assert returncode == 0

def test_fastq_no_path_seq1():
    returncode = FastQ.filter_by_id(no_path, output, ids)
    assert returncode == 1

def test_fastq_no_path_output():
    returncode = FastQ.filter_by_id(seq1, no_path, ids)
    assert returncode == 0

def test_fastq_no_path_ids():
    returncode = FastQ.filter_by_id(seq1, output, no_path)
    assert returncode == 0
