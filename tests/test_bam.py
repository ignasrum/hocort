from hocort.parse.bam import BAM
import tempfile
import os

temp_dir = tempfile.TemporaryDirectory()
path = os.path.dirname(__file__)

seq1 = f'{path}/test_data/sequences/sequences1.fastq'
output = f'{temp_dir.name}/out.fastq'
ids = f'{path}/test_data/sequences/ids.list'
bam_output = f'{path}/test_data/sequences/output.bam'
no_path = ''

def test_valid():
    query_names = BAM.extract_ids(bam_output, add_slash=True)
    with open(ids, 'r') as id_file:
        for i, line in enumerate(id_file):
            assert line.strip('\n') == query_names[i]

def test_valid_no_slash():
    query_names = BAM.extract_ids(bam_output, add_slash=False)
    file_ids = []
    with open(ids, 'r') as id_file:
        for line in id_file:
            file_ids.append(line.split('/')[0])
    for query_name in query_names:
        assert query_name.split('/')[0] in file_ids

def test_no_path_bam():
    query_names = BAM.extract_ids(no_path)
    assert query_names == []
