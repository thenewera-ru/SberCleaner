from string import punctuation
import pymorphy2
from pathlib import Path
import re


class Parser:

    INC = set(['@', '*', '-', '_'])

    EXC = set(punctuation)

    def __init__(self, *args, **kwargs):
        self.morph = pymorphy2.MorphAnalyzer()
        self.stops = set()
        paths = kwargs.get('stopwords', [])
        for p in paths:
            with open(str(Path(p['path']))) as f:
                rubbish = set(f.read().split('\n'))
            self.stops = self.stops.union(rubbish)
        self.stops = self.stem(self.stops)

    def isRubbish(self, w):
        return self.normalForm(w) in self.stops

    def isMask(self, w):
        return self.mask(w) != w

    def preprocess(self, arg, **kwargs) -> []:
        '''
        :param arg: Sentence
        :return: -> list
        '''
        
        arg = arg.lower()
        arg = "".join([ch for ch in arg if ch not in Parser.EXC or ch in Parser.INC])
        arg = arg.split()
        arg = [word for word in arg if not self.isRubbish(self.normalForm(word.lower()))]
        arg = [self.mask(word) for word in arg]
        return arg

    def sentenceLength(self, arg, **kwargs) -> int:
        '''
        :param arg: ['hello', 'world', 'the', 'sky', 'is', 'blue']
        :param kwargs:
        :return:
        '''
        s = -1
        for w in arg:
            s += len(w)
        return s

    def normalForm(self, word):
        return self.morph.parse(word)[0].normal_form

    def maskWord(self, word, sym='*'):
        digits = ['0','1','2','3','4','5','6','7','8','9']
        for d in digits:
            word = word.replace(d, sym)
        return re.sub(r"(?<=.)[^@](?=[^@]*?@)|(?:(?<=@.)|(?!^)\\G(?=[^@]*$)).(?=.*\\.)", sym, word)


    def mask(self, arg):
        if isinstance(arg, str): return self.mask(arg.split())
        if isinstance(arg, list): return [self.maskWord(w) for w in arg]
        raise TypeError(arg)


    def stem(self, arg):
        if self.morph is None:
            raise ValueError('Stemmer is not defined')
        if isinstance(arg, str): return self.normalForm(arg)
        if isinstance(arg, list): return [self.normalForm(w) for w in arg]
        if isinstance(arg, set): return {self.normalForm(w) for w in arg}
        raise TypeError(arg)
