import tempfile
import os

import pytest

from hocort.pipelines.kraken2_hisat2 import Kraken2HISAT2

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

hs2_idx = f'{path}/test_data/hisat2/genome'
kr2_idx = f'{path}/test_data/kraken2'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
out1 = f'{temp_dir.name}/out1.fastq'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
out2 = f'{temp_dir.name}/out2.fastq'
no_path = ''

def test_pipeline_temp_dir():
    path = '.'
    returncode = Kraken2HISAT2(path).run(hs2_idx, kr2_idx, seq1, out1, seq2=seq2, out2=out2)
    assert returncode == 0

def test_pipeline_hs2_idx_no_path():
    with pytest.raises(ValueError):
        returncode = Kraken2HISAT2().run(no_path, kr2_idx, seq1, out1)

def test_pipeline_kr2_idx_no_path():
    with pytest.raises(ValueError):
        returncode = Kraken2HISAT2().run(hs2_idx, no_path, seq1, out1)

def test_pipeline_seq1_no_path():
    with pytest.raises(ValueError):
        returncode = Kraken2HISAT2().run(hs2_idx, kr2_idx, no_path, out1)

def test_pipeline_out1_no_path():
    returncode = Kraken2HISAT2().run(hs2_idx, kr2_idx, seq1, no_path)
    assert returncode == 0

def test_pipeline_seq1_seq2_no_path():
    with pytest.raises(ValueError):
        returncode = Kraken2HISAT2().run(hs2_idx, kr2_idx, no_path, out1, seq2=no_path)

def test_pipeline_seq2_no_path():
    with pytest.raises(ValueError):
        returncode = Kraken2HISAT2().run(hs2_idx, kr2_idx, seq1, out1, seq2=no_path)

def test_pipeline_1():
    returncode = Kraken2HISAT2().run(hs2_idx, kr2_idx, seq1, out1)
    assert returncode == 0

def test_pipeline_2():
    returncode = Kraken2HISAT2().run(hs2_idx, kr2_idx, seq1, out1, seq2=seq2, out2=out2)
    assert returncode == 0

def test_pipeline_seq2_no_out2():
    with pytest.raises(ValueError):
        returncode = Kraken2HISAT2().run(hs2_idx, kr2_idx, seq1, out1, seq2=seq2)

def test_pipeline_noseq2_out2():
    returncode = Kraken2HISAT2().run(hs2_idx, kr2_idx, seq1, out1, out2=out2)
    assert returncode == 0

def test_pipeline_mfilter_true_1():
    returncode = Kraken2HISAT2().run(hs2_idx, kr2_idx, seq1, out1, mfilter=True)
    assert returncode == 0

def test_pipeline_mfilter_false_1():
    returncode = Kraken2HISAT2().run(hs2_idx, kr2_idx, seq1, out1, mfilter=False)
    assert returncode == 0

def test_pipeline_mfilter_true_2():
    returncode = Kraken2HISAT2().run(hs2_idx, kr2_idx, seq1, out1, seq2=seq2, out2=out2, mfilter=True)
    assert returncode == 0

def test_pipeline_mfilter_false_2():
    returncode = Kraken2HISAT2().run(hs2_idx, kr2_idx, seq1, out1, seq2=seq2, out2=out2, mfilter=False)
    assert returncode == 0
