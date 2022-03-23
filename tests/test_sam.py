import tempfile
import os

from hocort.parse.sam import SAM

from helper import helper

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

seq1 = f'{path}/test_data/sequences/sequences1.fastq'
out_1_fastq = f'{temp_dir.name}/out_1.fastq'
out_2_fastq = f'{temp_dir.name}/out_2.fastq'
out_sam = f'{temp_dir.name}/out.sam'
ids = f'{path}/test_data/sequences/ids.list'
sam_paired = f'{path}/test_data/sequences/paired.sam'
sam_unpaired = f'{path}/test_data/sequences/unpaired.sam'
no_path = ''

def test_select_paired_mfilter_true():
    cmd = SAM.select(input_path=sam_paired, paired=True, output_path=out_sam, mfilter=True)
    helper(cmd, 0)

def test_select_paired_mfilter_false():
    cmd = SAM.select(input_path=sam_paired, paired=True, output_path=out_sam, mfilter=False)
    helper(cmd, 0)

def test_select_unpaired_mfilter_true():
    cmd = SAM.select(input_path=sam_unpaired, paired=False, output_path=out_sam, mfilter=True)
    helper(cmd, 0)

def test_select_unpaired_mfilter_false():
    cmd = SAM.select(input_path=sam_unpaired, paired=False, output_path=out_sam, mfilter=False)
    helper(cmd, 0)

def test_sam_to_fastq_paired_mfilter_true():
    cmd = SAM.sam_to_fastq(input_path=sam_paired, out1=out_1_fastq, out2=out_2_fastq, mfilter=True)
    helper(cmd, 0)

def test_sam_to_fastq_paired_mfilter_false():
    cmd = SAM.sam_to_fastq(input_path=sam_paired, out1=out_1_fastq, out2=out_2_fastq, mfilter=False)
    helper(cmd, 0)

def test_sam_to_fastq_unpaired_mfilter_true():
    cmd = SAM.sam_to_fastq(input_path=sam_unpaired, out1=out_1_fastq, mfilter=True)
    helper(cmd, 0)

def test_sam_to_fastq_unpaired_mfilter_false():
    cmd = SAM.sam_to_fastq(input_path=sam_unpaired, out1=out_1_fastq, mfilter=False)
    helper(cmd, 0)
