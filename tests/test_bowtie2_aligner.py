from hocort.aligners.bowtie2 import Bowtie2 as bt2
import tempfile
import os

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/bowtie2/genome'
fasta = f'{path}/test_data/fasta/genome.fna'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
output = f'{temp_dir.name}/output'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
no_path = ''

def test_build_idx():
    returncode = bt2.build_index(output, fasta)
    assert returncode == 0

def test_build_idx_no_input():
    returncode = bt2.build_index(output, no_path)
    assert returncode == 1

def test_idx_no_path():
    returncode = bt2.align_sam(no_path, seq1, output)
    assert returncode == 1

def test_idx_path():
    returncode = bt2.align_sam(temp_dir.name, seq1, output)
    assert returncode == 255

def test_seq1_no_path():
    returncode = bt2.align_sam(idx, no_path, output)
    assert returncode == 1

def test_output_no_path():
    returncode = bt2.align_sam(idx, seq1, no_path)
    assert returncode == 1

def test_output_path():
    returncode = bt2.align_sam(idx, seq1, temp_dir.name)
    assert returncode == 1

def test_seq1_seq2_no_path():
    returncode = bt2.align_sam(idx, no_path, output, seq2=no_path)
    assert returncode == 1

def test_seq2_no_path():
    returncode = bt2.align_sam(idx, seq1, output, seq2=no_path)
    assert returncode == 0

def test_local_sam_1():
    options = ['--local']
    returncode = bt2.align_sam(idx, seq1, output, options=options)
    assert returncode == 0

def test_local_sam_2():
    options = ['--local']
    returncode = bt2.align_sam(idx, seq1, output, seq2=seq2, options=options)
    assert returncode == 0

def test_local_bam_1():
    options = ['--local']
    returncode = bt2.align_bam(idx, seq1, output, options=options)
    assert returncode[0] == 0
    assert returncode[1] == 0

def test_local_bam_2():
    options = ['--local']
    returncode = bt2.align_bam(idx, seq1, output, seq2=seq2, options=options)
    assert returncode[0] == 0
    assert returncode[1] == 0

def test_end_to_end_sam_1():
    options = ['--end-to-end']
    returncode = bt2.align_sam(idx, seq1, output, options=options)
    assert returncode == 0

def test_end_to_end_sam_2():
    options = ['--end-to-end']
    returncode = bt2.align_sam(idx, seq1, output, seq2=seq2, options=options)
    assert returncode == 0

def test_end_to_end_bam_1():
    options = ['--end-to-end']
    returncode = bt2.align_bam(idx, seq1, output, options=options)
    assert returncode[0] == 0
    assert returncode[1] == 0

def test_end_to_end_bam_2():
    options = ['--end-to-end']
    returncode = bt2.align_bam(idx, seq1, output, seq2=seq2, options=options)
    assert returncode[0] == 0
    assert returncode[1] == 0
