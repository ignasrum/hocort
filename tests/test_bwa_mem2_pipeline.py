from hocort.pipelines.bwa_mem2 import BWA_MEM2
import tempfile
import os

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

idx = f'{path}/test_data/bwa_mem2/genome'
seq1 = f'{path}/test_data/sequences/sequences1.fastq'
out1 = f'{temp_dir.name}/out1.fastq'
seq2 = f'{path}/test_data/sequences/sequences2.fastq'
out2 = f'{temp_dir.name}/out2.fastq'
no_path = ''

def test_pipeline_temp_dir():
    path = '.'
    returncode = BWA_MEM2(path).run(idx, seq1, out1, seq2=seq2, out2=out2)
    assert returncode == 0

def test_pipeline_mapq():
    returncode = BWA_MEM2().run(idx, seq1, out1, seq2=seq2, out2=out2, mapq=2)
    assert returncode == 0

def test_pipeline_idx_no_path():
    returncode = BWA_MEM2().run(no_path, seq1, out1)
    assert returncode == 1

def test_pipeline_seq1_no_path():
    returncode = BWA_MEM2().run(idx, no_path, out1)
    assert returncode == 1

def test_pipeline_out1_no_path():
    returncode = BWA_MEM2().run(idx, seq1, no_path)
    assert returncode == 0

def test_pipeline_seq1_seq2_no_path():
    returncode = BWA_MEM2().run(idx, no_path, out1, seq2=no_path)
    assert returncode == 1

def test_pipeline_seq2_no_path():
    returncode = BWA_MEM2().run(idx, seq1, out1, seq2=no_path)
    assert returncode == 1

def test_pipeline_hcfilter_true_1():
    returncode = BWA_MEM2().run(idx, seq1, out1, hcfilter='t')
    assert returncode == 0

def test_pipeline_hcfilter_false_1():
    returncode = BWA_MEM2().run(idx, seq1, out1, hcfilter='f')
    assert returncode == 0

def test_pipeline_hcfilter_true_2():
    returncode = BWA_MEM2().run(idx, seq1, out1, seq2=seq2, out2=out2, hcfilter='t')
    assert returncode == 0

def test_pipeline_hcfilter_false_2():
    returncode = BWA_MEM2().run(idx, seq1, out1, seq2=seq2, out2=out2, hcfilter='f')
    assert returncode == 0

def test_pipeline_1():
    returncode = BWA_MEM2().run(idx, seq1, out1)
    assert returncode == 0

def test_pipeline_2():
    returncode = BWA_MEM2().run(idx, seq1, out1, seq2=seq2, out2=out2)
    assert returncode == 0

def test_pipeline_custom_options_1():
    options = []
    returncode = BWA_MEM2().run(idx, seq1, out1, options=options)
    assert returncode == 0

def test_pipeline_custom_options_2():
    options = []
    returncode = BWA_MEM2().run(idx, seq1, out1, seq2=seq2, out2=out2, options=options)
    assert returncode == 0

def test_pipeline_sam_1():
    intermediary = 'SAM'
    returncode = BWA_MEM2().run(idx, seq1, out1, intermediary=intermediary)
    assert returncode == 0

def test_pipeline_sam_2():
    intermediary = 'SAM'
    returncode = BWA_MEM2().run(idx, seq1, out1, seq2=seq2, out2=out2, intermediary=intermediary)
    assert returncode == 0

def test_pipeline_sam_1():
    intermediary = 'BAM'
    returncode = BWA_MEM2().run(idx, seq1, out1, intermediary=intermediary)
    assert returncode == 0

def test_pipeline_sam_2():
    intermediary = 'BAM'
    returncode = BWA_MEM2().run(idx, seq1, out1, seq2=seq2, out2=out2, intermediary=intermediary)
    assert returncode == 0

def test_pipeline_seq2_no_out2():
    returncode = BWA_MEM2().run(idx, seq1, out1, seq2=seq2)
    assert returncode == 0

def test_pipeline_noseq2_out2():
    returncode = BWA_MEM2().run(idx, seq1, out1, out2=out2)
    assert returncode == 0
