import tempfile
import os

import pytest

from hocort.pipelines.kraken2 import Kraken2

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/kraken2'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
out = f'{temp_dir.name}/out#.fastq'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
no_path = ''

def test_pipeline_idx_no_path():
    with pytest.raises(ValueError):
        returncode = Kraken2().run(no_path, seq1, out)

def test_pipeline_seq1_no_path():
    with pytest.raises(ValueError):
        returncode = Kraken2().run(idx, no_path, out)

def test_pipeline_out1_no_path():
    returncode = Kraken2().run(idx, seq1, no_path)
    assert returncode == 0

def test_pipeline_seq1_seq2_no_path():
    with pytest.raises(ValueError):
        returncode = Kraken2().run(idx, no_path, out, seq2=no_path)

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

def test_pipeline_mfilter_true_1():
    returncode = Kraken2().run(idx, seq1, out, mfilter='t')
    assert returncode == 0

def test_pipeline_mfilter_false_1():
    returncode = Kraken2().run(idx, seq1, out, mfilter='f')
    assert returncode == 0

def test_pipeline_mfilter_true_2():
    returncode = Kraken2().run(idx, seq1, out, seq2=seq2, mfilter='t')
    assert returncode == 0

def test_pipeline_mfilter_false_2():
    returncode = Kraken2().run(idx, seq1, out, seq2=seq2, mfilter='f')
    assert returncode == 0
