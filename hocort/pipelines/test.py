from hocort.pipelines.pipeline import Pipeline

class Test(Pipeline):
    def __init__(self):
        super().__init__()

    def run(self):
        print('test pipeline')
