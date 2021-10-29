from hocort.pipelines.bowtie2_hisat2 import Bowtie2HISAT2
import tempfile
import os

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

bt2_idx = f'{path}/test_data/bowtie2/genome'
hs2_idx = f'{path}/test_data/hisat2/genome'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
out1 = f'{temp_dir.name}/out1.fastq'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
out2 = f'{temp_dir.name}/out2.fastq'

def test_bowtie2_hisat2_pipeline_1():
    returncode, stdout, stderr = Bowtie2HISAT2().run(bt2_idx, hs2_idx, seq1, out1)
    assert returncode[0] == 0

def test_bowtie2_hisat2_pipeline_2():
    returncode, stdout, stderr = Bowtie2HISAT2().run(bt2_idx, hs2_idx, seq1, out1, seq2=seq2, out2=out2)
    assert returncode[0] == 0

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
