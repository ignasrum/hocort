import tempfile
import os

import pytest

from hocort.pipelines.bowtie2_bowtie2 import Bowtie2Bowtie2

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/bowtie2/genome'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
out1 = f'{temp_dir.name}/out1.fastq'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
out2 = f'{temp_dir.name}/out2.fastq'
no_path = ''

def test_pipeline_temp_dir():
    path = '.'
    returncode = Bowtie2Bowtie2(path).run(idx, seq1, out1, seq2=seq2, out2=out2)
    assert returncode == 0

def test_pipeline_idx_no_path():
    with pytest.raises(ValueError):
        returncode = Bowtie2Bowtie2().run(no_path, seq1, out1)

def test_pipeline_seq1_no_path():
    with pytest.raises(ValueError):
        returncode = Bowtie2Bowtie2().run(idx, no_path, out1)

def test_pipeline_out1_no_path():
    returncode = Bowtie2Bowtie2().run(idx, seq1, no_path)
    assert returncode == 0

def test_pipeline_seq1_seq2_no_path():
    with pytest.raises(ValueError):
        returncode = Bowtie2Bowtie2().run(idx, no_path, out1, seq2=no_path)

def test_pipeline_seq2_no_path():
    with pytest.raises(ValueError):
        returncode = Bowtie2Bowtie2().run(idx, seq1, out1, seq2=no_path)

def test_pipeline_1():
    returncode = Bowtie2Bowtie2().run(idx, seq1, out1)
    assert returncode == 0

def test_pipeline_2():
    returncode = Bowtie2Bowtie2().run(idx, seq1, out1, seq2=seq2, out2=out2)
    assert returncode == 0

def test_pipeline_seq2_no_out2():
    with pytest.raises(ValueError):
        returncode = Bowtie2Bowtie2().run(idx, seq1, out1, seq2=seq2)

def test_pipeline_noseq2_out2():
    returncode = Bowtie2Bowtie2().run(idx, seq1, out1, out2=out2)
    assert returncode == 0
