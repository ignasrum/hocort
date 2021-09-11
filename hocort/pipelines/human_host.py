from hocort.aligners.bowtie2 import Bowtie2
from hocort.pipelines.pipeline import Pipeline

class HumanHost(Pipeline):
    def __init__(self):
        super().__init__()

    def run(self):
        print("Human Host Contamination Removal")
