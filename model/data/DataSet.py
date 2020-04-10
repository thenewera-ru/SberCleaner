import pandas as pd
from utils.nlp import Parser

from runtime import Params
from torch.utils.data import Dataset


class DataSet(Dataset):

    def __init__(self, filepath):
        self.initParams = Params.getInstance().data['InitParams']
        data = pd.read_csv(filepath, sep=self.initParams.separator)
        self._data = {}
        self._indices = {}

        self.onInit(data=data, id=self.initParams.id)

        # self.group = data.groupby(self.initParams.id)
        # self.keyId = [key for key in self.group.indices.keys()]

        # self.x = lines[self.initParams.clientMessage].tolist()
        # self.author = lines[self.initParams.authorMessage].tolist()

        self.maxSequences = int(self.initParams.maxSequences)
        self.minSequenceWords = int(self.initParams.minSequenceWords)
        self.maxSequenceLength = int(self.initParams.maxSequenceLength)

        self.parser = Parser(stopwords=self.initParams.stopwords)

        self._indexesCached = {}
        self._sensCached = {}
        self._cached = set()
        # Holds ids of sentences that will be sent to the final pipeline

    def onInit(self, data, id):
        group = data.groupby(id)
        self._indices = {i: group.indices[k] for i, k in enumerate(group.indices)}
        for key in data.columns.tolist():
            self._data[key] = data[key].tolist()

    def column(self, name, **kwargs):
        if name not in self.columns:
            raise KeyError('No column named {:s} in your dataset'.format(name))
        if name == self.initParams.clientMessage:
            return self._data[name] if 'batchIndex' not in kwargs.keys() \
                else [" ".join(self.parser.mask(self._data[name][j])) for j in self.queries(kwargs['batchIndex'])]
        return self._data[name] if 'batchIndex' not in kwargs.keys() \
            else [self._data[name][j] for j in self.queries(kwargs['batchIndex'])]

    @property
    def sentences(self):
        return self._data[self.initParams.clientMessage]

    @property
    def author(self):
        return self._data[self.initParams.authorMessage]

    @property
    def indices(self):
        return self._indices

    def batchStartsWith(self, batchId):
        return self.indices[batchId][0]

    def batchEndsWith(self, batchId):
        return self.indices[batchId][-1]

    def __len__(self):
        return len(self.indices)

    @property
    def columns(self):
        return self._data.keys()

    @property
    def data(self):
        return self._data

    def query(self, batchIndex):
        if batchIndex not in self._cached:
            lo = self.batchStartsWith(batchIndex)
            hi = self.batchEndsWith(batchIndex)
            sens = self.sentences[lo:hi]
            author = [lo + i for i, sen in enumerate(sens) if self.author[lo + i] == 'Client']
            sens = [[self.sentences[j], j] for j in author]
            sensParsed = [[self.parser.preprocess(sen[0]), sen[1]] for sen in sens]
            sensParsed = [[sen[0], sen[1]] for sen in sensParsed if len(sen[0]) >= self.minSequenceWords]
            ids = [sen[1] for sen in sensParsed]
            ids = ids[:self.maxSequences]
            sens = [sen[0] for sen in sens if sen[1] in ids]
            self._indexesCached[batchIndex] = ids
            self._sensCached[batchIndex] = sens
        self._cached.add(batchIndex)

    def queries(self, batchIndex):
        self.query(batchIndex)
        return self._indexesCached[batchIndex]

    def __getitem__(self, index):
        self.query(batchIndex=index)
        return self._sensCached[index]
