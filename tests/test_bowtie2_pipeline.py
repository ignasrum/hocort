from hocort.pipelines.bowtie2 import Bowtie2
import tempfile
import os

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/bowtie2/genome'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
out1 = f'{temp_dir.name}/out1.fastq'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
out2 = f'{temp_dir.name}/out2.fastq'

def test_bowtie2_pipeline_end_to_end_1():
    options = ['--end-to-end']
    returncode, stdout, stderr = Bowtie2().run(idx, seq1, out1, options=options)
    assert returncode == 0

def test_bowtie2_pipeline_end_to_end_2():
    options = ['--end-to-end']
    returncode, stdout, stderr = Bowtie2().run(idx, seq1, out1, seq2=seq2, out2=out2, options=options)
    assert returncode == 0

def test_bowtie2_pipeline_local_1():
    options = ['--local']
    returncode, stdout, stderr = Bowtie2().run(idx, seq1, out1, options=options)
    assert returncode == 0

def test_bowtie2_pipeline_local_2():
    options = ['--local']
    returncode, stdout, stderr = Bowtie2().run(idx, seq1, out1, seq2=seq2, out2=out2, options=options)
    assert returncode == 0
