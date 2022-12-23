import tempfile
import os

import pytest

from hocort.pipelines.biobloom import BioBloom

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/biobloom/reference.bf'
fasta = f'{path}/test_data/fasta/genome.fna'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
out = f'{temp_dir.name}/output'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
no_path = ''

def test_pipeline_idx_no_path():
    with pytest.raises(ValueError):
        returncode = BioBloom().run(no_path, seq1, out)

def test_pipeline_seq1_no_path():
    with pytest.raises(ValueError):
        returncode = BioBloom().run(idx, no_path, out)

def test_pipeline_seq1_seq2_no_path():
    with pytest.raises(ValueError):
        returncode = BioBloom().run(idx, no_path, out, seq2=no_path)

def test_pipeline_seq2_no_path():
    returncode = BioBloom().run(idx, seq1, out, seq2=no_path)
    assert returncode == 0

def test_pipeline_1():
    returncode = BioBloom().run(idx, seq1, out)
    assert returncode == 0

def test_pipeline_2():
    returncode = BioBloom().run(idx, seq1, out, seq2=seq2)
    assert returncode == 0

def test_pipeline_custom_options_1():
    options = ''
    returncode = BioBloom().run(idx, seq1, out, options=options)
    assert returncode == 0

def test_pipeline_custom_options_2():
    options = ''
    returncode = BioBloom().run(idx, seq1, out, seq2=seq2, options=options)
    assert returncode == 0
