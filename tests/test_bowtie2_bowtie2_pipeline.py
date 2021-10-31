from hocort.pipelines.bowtie2_bowtie2 import Bowtie2Bowtie2
import tempfile
import os

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/bowtie2/genome'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
out1 = f'{temp_dir.name}/out1.fastq'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
out2 = f'{temp_dir.name}/out2.fastq'
no_path = ''

def test_bowtie2_bowtie2_pipeline_idx_no_path():
    returncode, stdout, stderr = Bowtie2Bowtie2().run(no_path, seq1, out1)
    assert returncode[0] == 255
    assert returncode[1] == 255

def test_bowtie2_bowtie2_pipeline_seq1_no_path():
    returncode, stdout, stderr = Bowtie2Bowtie2().run(idx, no_path, out1)
    assert returncode[0] == 1
    assert returncode[1] == 1

def test_bowtie2_bowtie2_pipeline_out1_no_path():
    returncode, stdout, stderr = Bowtie2Bowtie2().run(idx, seq1, no_path)
    assert returncode[0] == 0
    assert returncode[1] == 0

def test_bowtie2_bowtie2_pipeline_seq1_seq2_no_path():
    returncode, stdout, stderr = Bowtie2Bowtie2().run(idx, no_path, out1, seq2=no_path)
    assert returncode[0] == 0
    assert returncode[1] == 1

def test_bowtie2_bowtie2_pipeline_seq2_no_path():
    returncode, stdout, stderr = Bowtie2Bowtie2().run(idx, seq1, out1, seq2=no_path)
    assert returncode[0] == 1
    assert returncode[1] == 1

def test_bowtie2_bowtie2_pipeline_1():
    returncode, stdout, stderr = Bowtie2Bowtie2().run(idx, seq1, out1)
    assert returncode[0] == 0
    assert returncode[1] == 0

def test_bowtie2_bowtie2_pipeline_2():
    returncode, stdout, stderr = Bowtie2Bowtie2().run(idx, seq1, out1, seq2=seq2, out2=out2)
    assert returncode[0] == 0
    assert returncode[1] == 0

def test_bowtie2_bowtie2_pipeline_seq2_no_out2():
    returncode, stdout, stderr = Bowtie2Bowtie2().run(idx, seq1, out1, seq2=seq2)
    assert returncode[0] == 0
    assert returncode[1] == 0

def test_bowtie2_bowtie2_pipeline_noseq2_out2():
    returncode, stdout, stderr = Bowtie2Bowtie2().run(idx, seq1, out1, out2=out2)
    assert returncode[0] == 0
    assert returncode[1] == 0

"""
def test_bowtie2_hisat2_pipeline_custom_options_1():
    options = ['--local']
    returncode, stdout, stderr = Bowtie2HISAT2().run(idx, seq1, out1, options=options)
    assert returncode == 0

def test_bowtie2_hisat2_pipeline_custom_options_2():
    options = ['--local']
    returncode, stdout, stderr = Bowtie2HISAT2().run(idx, seq1, out1, seq2=seq2, out2=out2, options=options)
    assert returncode == 0
"""