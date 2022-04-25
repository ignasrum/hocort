import tempfile
import os

import pytest

from hocort.pipelines.bowtie2 import Bowtie2

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/bowtie2/genome'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
out1 = f'{temp_dir.name}/out1.fastq'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
out2 = f'{temp_dir.name}/out2.fastq'
no_path = ''


def test_pipeline_idx_no_path():
    with pytest.raises(ValueError):
        returncode = Bowtie2().run(no_path, seq1, out1)

def test_pipeline_seq1_no_path():
    with pytest.raises(ValueError):
        returncode = Bowtie2().run(idx, no_path, out1)

def test_pipeline_out1_no_path():
    returncode = Bowtie2().run(idx, seq1, no_path)
    assert returncode == 0

def test_pipeline_seq1_seq2_no_path():
    with pytest.raises(ValueError):
        returncode = Bowtie2().run(idx, no_path, out1, seq2=no_path)

def test_pipeline_seq2_no_path():
    returncode = Bowtie2().run(idx, seq1, out1, seq2=no_path)
    assert returncode == 0

def test_pipeline_mfilter_true_1():
    returncode = Bowtie2().run(idx, seq1, out1, mfilter=True)
    assert returncode == 0

def test_pipeline_mfilter_false_1():
    returncode = Bowtie2().run(idx, seq1, out1, mfilter=False)
    assert returncode == 0

def test_pipeline_mfilter_true_2():
    returncode = Bowtie2().run(idx, seq1, out1, seq2=seq2, out2=out2, mfilter=True)
    assert returncode == 0

def test_pipeline_mfilter_false_2():
    returncode = Bowtie2().run(idx, seq1, out1, seq2=seq2, out2=out2, mfilter=False)
    assert returncode == 0

def test_pipeline_end_to_end_1():
    preset = 'end-to-end'
    returncode = Bowtie2().run(idx, seq1, out1, preset=preset)
    assert returncode == 0

def test_pipeline_end_to_end_2():
    preset = 'end-to-end'
    returncode = Bowtie2().run(idx, seq1, out1, seq2=seq2, out2=out2, preset=preset)
    assert returncode == 0

def test_pipeline_local_1():
    preset = 'local'
    returncode = Bowtie2().run(idx, seq1, out1, preset=preset)
    assert returncode == 0

def test_pipeline_local_2():
    preset = 'local'
    returncode = Bowtie2().run(idx, seq1, out1, seq2=seq2, out2=out2, preset=preset)
    assert returncode == 0

def test_pipeline_custom_options_1():
    options = '--local'
    returncode = Bowtie2().run(idx, seq1, out1, options=options)
    assert returncode == 0

def test_pipeline_custom_options_2():
    options = '--local'
    returncode = Bowtie2().run(idx, seq1, out1, seq2=seq2, out2=out2, options=options)
    assert returncode == 0

def test_pipeline_1():
    returncode = Bowtie2().run(idx, seq1, out1)
    assert returncode == 0

def test_pipeline_2():
    returncode = Bowtie2().run(idx, seq1, out1, seq2=seq2, out2=out2)
    assert returncode == 0

def test_pipeline_seq2_no_out2():
    with pytest.raises(ValueError):
        returncode = Bowtie2().run(idx, seq1, out1, seq2=seq2)

def test_pipeline_noseq2_out2():
    returncode = Bowtie2().run(idx, seq1, out1, out2=out2)
    assert returncode == 0
