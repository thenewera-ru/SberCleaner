from in_out.reader.Reader import Reader as Parent
import os
from runtime import Params
import pandas as pd
from utils import Utils


class ReaderCsv(Parent):

    def __init__(self, directory, filename):
        super(ReaderCsv, self).__init__(directory=directory, filename=filename)
        self.initParams = Params.getInstance().data['InitParams']

    @classmethod
    def fromFile(cls, filepath=None):
        return Parent.fromFile(filepath)

    def read(self, separator=','):
        '''
        :param separator: separator that is used in .csv file
        :return: Pandas.DataFrame
        '''
        return pd.read_csv(self.filepath, sep=separator, encoding='utf-8')

    def columns(self, separator=','):
        return pd.read_csv(self.filepath, sep=separator, encoding='utf-8', nrows=1)
