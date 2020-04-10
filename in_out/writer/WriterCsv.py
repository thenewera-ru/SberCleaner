from in_out.writer.Writer import Writer as Parent

from utils import Utils
from runtime import Params
from utils.strings import Strings
import os


class WriterCsv(Parent):

    def __init__(self, directory=None, filename=None):
        super(WriterCsv, self).__init__(directory, filename)
        self.initParams = Params.getInstance().data['InitParams']

    @classmethod
    def fromFile(cls, filepath=None):
        return Parent.fromFile(filepath)

    def write(self, data):
        '''
        :param data: Pandas.DataFrame
        :return:
        '''
        data.to_csv(self.filepath, encoding='utf-8-sig', sep=self.initParams.separator, index=False)
