
from model.data.DataSet import DataSet
from torch.utils.data import DataLoader as Loader

from structure import Vocabulary
from pathlib import Path
from utils.system import System


class DataLoader(Loader):

    def __init__(self, filepath, batchSize=1, numWorkers=System.cores() - 1):
        self.ds = DataSet(Path(filepath))
        self.batchSize = batchSize
        super(DataLoader, self).__init__(self.ds, batch_size=batchSize, num_workers=numWorkers, shuffle=False)
        # self.vcb = Vocabulary.build(corpus=self.sentences())

    def batchStartsWith(self, batchId):
        return self.ds.batchStartsWith(batchId)

    def batchEndsWith(self, batchId):
        return self.ds.batchEndsWith(batchId)

    def sentences(self) -> []:
        return self.ds.sentences

    def column(self, name, **kwargs) -> []:
        return self.ds.column(name, **kwargs)

    def __getitem__(self, index):
        return self.ds[index]
    
