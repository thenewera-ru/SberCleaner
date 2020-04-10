from utils.nlp import Parser
from runtime import Params


class Vocabulary:

    PAD_token = 0
    SOS_token = 1
    EOS_token = 2

    @classmethod
    def pad_token(cls): return cls.PAD_token

    @classmethod
    def sos_token(cls): return cls.SOS_token

    @classmethod
    def eos_token(cls): return cls.EOS_token

    def __init__(self):
        self.w2i = {}
        self.w2cnt = {}
        self.i2w = {
            self.pad_token(): "PAD",
            self.sos_token(): "SOS",
            self.eos_token(): "EOF"
        }
        self.size = 3  # Holds the size of vocabulary
        self.parser = Parser(stopwords=Params.getInstance().data['InitParams'].stopwords)
        self.trimmed = False

    @classmethod
    def build(cls, corpus):
        instance = cls()
        for line in corpus:
            sen = instance.parser.preprocess(line)
            for word in sen:
                instance.addWord(word)
        return instance

    def addSentence(self, sen):
        for word in self.parser.preprocess(sen):
            self.addWord(word)
        return self

    def addWord(self, word):
        if word in self.w2i:
            self.w2cnt[word] += 1
        else:
            self.w2i[word] = self.size
            self.w2cnt[word] = 1
            self.i2w[self.size] = word
            self.size += 1
        return self

    def trim(self, minCount):
        if not self.trimmed:
            self.trimmed = True
            keepWords = []
            for k, v in self.w2i.items():
                if v >= minCount:
                    keepWords.append(k)

            # Reinitialize dictionaries

            self.w2i = {}
            self.w2cnt = {}
            self.i2w = {self.pad_token(): "PAD", self.sos_token: "SOS", self.eos_token: "EOS"}
            self.size = 3  # Count default tokens

            for word in keepWords:
                self.addWord(word)
        return self

    def indexes(self, sentence) -> []:
        return [self.w2i[w] for w in sentence]

    @staticmethod
    def pad(sequence, seqLen):
        '''
        :param sequence: preprocessed sequence
        :param seqLen:
        :return:
        '''
        if len(sequence) >= seqLen:
            ans = sequence[:seqLen]
        else:
            ans = sequence + [Vocabulary.pad_token()] * (seqLen - len(sequence))
        return ans
