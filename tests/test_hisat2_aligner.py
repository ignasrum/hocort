from hocort.aligners.hisat2 import HISAT2 as hs2
import tempfile
import os

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/hisat2/genome'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
output = f'{temp_dir.name}/output'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'

def test_sam_1():
    options = []
    returncode, stdout, stderr = hs2.align_sam(idx, seq1, output, options=options)
    assert returncode == 0

def test_sam_2():
    options = []
    returncode, stdout, stderr = hs2.align_sam(idx, seq1, output, seq2=seq2, options=options)
    assert returncode == 0

def test_bam_1():
    options = []
    returncode, stdout, stderr = hs2.align_bam(idx, seq1, output, options=options)
    assert returncode[0] == 0
    assert returncode[1] == 0

def test_bam_2():
    options = []
    returncode, stdout, stderr = hs2.align_bam(idx, seq1, output, seq2=seq2, options=options)
    assert returncode[0] == 0
    assert returncode[1] == 0
