import os
from in_out.reader.Reader import Reader as Parent
import pandas as pd

import json


class ReaderJson(Parent):

    def __init__(self, directory, filename):
        """
        :param directory: Path to current working directory
        :param filename: File to open
        """
        super(ReaderJson, self).__init__(directory=directory, filename=filename)

        self.data = None
        self.chatsLocation = None
        self.chatsOutputLocation = None
        self.clientMessage = None
        self.authorMessage = None

        self.maxSequences = None
        self.minSequenceWords = None
        self.maxSequenceLength = None

        self.stopwordsPath = None

        self.columns = None

        self.id = None
        self.encodingInput = None
        self.encodingOutput = None

        self.separator = None

    def read(self):
        # TODO: По хорошему нужно вставить кодировку из @Utils.getEncoding().
        if not self._filepath.exists():
            raise FileNotFoundError(str(self._filepath))
        with open(self._filepath) as f:
            self.data = json.load(f)

        self.chatsLocation = self.data['data']['input']['path']
        self.chatsOutputLocation = self.data['data']['output']['path']
        self.clientMessage = self.data['data']['params']['clientMessage']
        self.authorMessage = self.data['data']['params']['authorMessage']

        self.maxSequences = int(self.data['data']['params']['maxSequences'])
        self.minSequenceWords = int(self.data['data']['params']['minSequenceWords'])
        self.maxSequenceLength = int(self.data['data']['params']['maxSequenceLength'])

        self.stopwords = self.data['data']['params']['stopwords']
        self.separator = ','
        self.columns = self.data['data']['output']['params']['columns']
        self.id = self.data['data']['params']['id']
        for f in self.data['data']['formats']:
            if f['type'] == 'csv':
                config = f['config']
                self.separator = config['separator']