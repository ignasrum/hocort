from hocort.pipelines.kraken2 import Kraken2
import tempfile
import os

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/kraken2'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
out = temp_dir.name
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
no_path = ''

def test_pipeline_temp_dir():
    path = '.'
    returncode = Kraken2(path).run(idx, seq1, out, seq2=seq2)
    assert returncode == 0

def test_pipeline_mapq():
    returncode = Kraken2().run(idx, seq1, out, seq2=seq2)
    assert returncode == 0

def test_pipeline_idx_no_path():
    returncode = Kraken2().run(no_path, seq1, out)
    assert returncode == 1

def test_pipeline_seq1_no_path():
    returncode = Kraken2().run(idx, no_path, out)
    assert returncode == 0

def test_pipeline_out1_no_path():
    returncode = Kraken2().run(idx, seq1, no_path)
    assert returncode == 0

def test_pipeline_seq1_seq2_no_path():
    returncode = Kraken2().run(idx, no_path, out, seq2=no_path)
    assert returncode == 0

def test_pipeline_seq2_no_path():
    returncode = Kraken2().run(idx, seq1, out, seq2=no_path)
    assert returncode == 0

def test_pipeline_1():
    returncode = Kraken2().run(idx, seq1, out)
    assert returncode == 0

def test_pipeline_2():
    returncode = Kraken2().run(idx, seq1, out, seq2=seq2)
    assert returncode == 0

def test_pipeline_custom_options_1():
    options = []
    returncode = Kraken2().run(idx, seq1, out, options=options)
    assert returncode == 0

def test_pipeline_custom_options_2():
    options = []
    returncode = Kraken2().run(idx, seq1, out, seq2=seq2, options=options)
    assert returncode == 0
