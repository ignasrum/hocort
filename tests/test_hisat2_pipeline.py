from hocort.pipelines.hisat2 import HISAT2
import tempfile
import os

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/hisat2/genome'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
out1 = f'{temp_dir.name}/out1.fastq'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
out2 = f'{temp_dir.name}/out2.fastq'

def test_hisat2_pipeline_hcfilter_true_1():
    returncode, stdout, stderr = HISAT2().run(idx, seq1, out1, hcfilter='t')
    assert returncode[0] == 0

def test_hisat2_pipeline_hcfilter_false_1():
    returncode, stdout, stderr = HISAT2().run(idx, seq1, out1, hcfilter='f')
    assert returncode[0] == 0

def test_hisat2_pipeline_hcfilter_true_2():
    returncode, stdout, stderr = HISAT2().run(idx, seq1, out1, seq2=seq2, out2=out2, hcfilter='t')
    assert returncode[0] == 0

def test_hisat2_pipeline_hcfilter_false_2():
    returncode, stdout, stderr = HISAT2().run(idx, seq1, out1, seq2=seq2, out2=out2, hcfilter='f')
    assert returncode[0] == 0

def test_hisat2_pipeline_1():
    returncode, stdout, stderr = HISAT2().run(idx, seq1, out1)
    assert returncode[0] == 0

def test_hisat2_pipeline_2():
    returncode, stdout, stderr = HISAT2().run(idx, seq1, out1, seq2=seq2, out2=out2)
    assert returncode[0] == 0

def test_hisat2_pipeline_custom_options_1():
    options = []
    returncode, stdout, stderr = HISAT2().run(idx, seq1, out1, options=options)
    assert returncode[0] == 0

def test_hisat2_pipeline_custom_options_2():
    options = []
    returncode, stdout, stderr = HISAT2().run(idx, seq1, out1, seq2=seq2, out2=out2, options=options)
    assert returncode[0] == 0

def test_hisat2_pipeline_sam_1():
    intermediary = 'SAM'
    returncode, stdout, stderr = HISAT2().run(idx, seq1, out1, intermediary=intermediary)
    assert returncode[0] == 0

def test_hisat2_pipeline_sam_2():
    intermediary = 'SAM'
    returncode, stdout, stderr = HISAT2().run(idx, seq1, out1, seq2=seq2, out2=out2, intermediary=intermediary)
    assert returncode[0] == 0

def test_hisat2_pipeline_sam_1():
    intermediary = 'BAM'
    returncode, stdout, stderr = HISAT2().run(idx, seq1, out1, intermediary=intermediary)
    assert returncode[0] == 0

def test_hisat2_pipeline_sam_2():
    intermediary = 'BAM'
    returncode, stdout, stderr = HISAT2().run(idx, seq1, out1, seq2=seq2, out2=out2, intermediary=intermediary)
    assert returncode[0] == 0

def test_hisat2_pipeline_seq2_no_out2():
    returncode, stdout, stderr = HISAT2().run(idx, seq1, out1, seq2=seq2)
    assert returncode[0] == 0

def test_hisat2_pipeline_noseq2_out2():
    returncode, stdout, stderr = HISAT2().run(idx, seq1, out1, out2=out2)
    assert returncode[0] == 0
