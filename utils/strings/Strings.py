import re
import os


class Strings:
    '''
    The purpose of this object is to share Heavy-lifted objects. E.g. Pandas.DataFrame that holds huge table.
    '''
    # Single-tone design.
    # Sometimes it is useful to add multiple regex expressions...
    __data = {}
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Strings.__instance is None:
            Strings()

        return Strings.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Strings.__instance is not None:

            raise Exception("This class is a singleton!")

        else:

            Strings.__instance = self

    @staticmethod
    def split(arg, delimiters):
        '''
        :param arg: String object
        :param delimiters: Python.list = [token_i] i=0^(n-1). E.g. delimiters = [',',';','\n']
        :return: Python.list of tokens
        '''
        __delimiters = str(r'')
        n = len(delimiters)
        specialChars = [os.sep, '.', '?', '*', '-']
        for i in range(n):
            # TODO: Don't forget to get all the special tokens...
            if delimiters[i] in specialChars:
                __delimiters += '\\'
            __delimiters += delimiters[i]
            if i < n - 1:
                __delimiters += "|"
        ans = re.split(__delimiters, arg)
        # re.split(';|,|\*|\n|\.', arg) -> because ['*', 'n', '.'] are special symbols
        return list(filter(None, ans))

    @staticmethod
    def splitAndGet(arg, delimiters, index):
        return Strings.split(arg, delimiters)[index]

    @staticmethod
    def startsWith(arg, prefix):
        '''
        :param arg: String object
        :param prefix: String object to check against
        :return: True -||- False
        '''
        return arg.startswith(prefix)

    @staticmethod
    def endsWith(arg, suffix):
        '''
        :param arg: String object
        :param suffix: String object to check against
        :return: True -||- False
        '''
        # i = len(arg) - 1
        # j = len(suffix) - 1
        # while j >= 0 and i >= 0 and suffix[j] == arg[i]:
        #     j -= 1
        #     i -= 1
        # return j < 0

        return arg.endswith(suffix)

    @staticmethod
    def removeEndingWithIfAny(arg, charSet):
        '''
        :param arg: String object
        :param charSet: Python.list of characters to be removed from @arg string from the end if any present
        :return: String object
        '''
        if len(arg) <= 0:
            return arg
        i = len(arg) - 1
        while i >= 0 and arg[i] in charSet:
            i -= 1

        return arg[0:(i + 1)]

    @staticmethod
    def removeDuplicates(arg):
        '''
        :param arg: Python.list of strings = ['CHAT', 'CHAT', 'CHAT', 'SBBOL 1 Line', 'SBBOL 1 Line', 'SBBOL 1 Line']
        :return: Python.list = ['CHAT', 'SBBOL 1 Line']
        '''
        # TODO:
        ans = []
        j = 0
        for i in range(len(arg)):
            if i < j:
                continue
            ans.append(arg[i])
            while j < len(arg) and arg[j] == arg[i]:
                j += 1

        return ans

    @staticmethod
    def equals(u, v):
        '''
        :param u:
        :param v:
        :return:
        '''
        return Strings.contains(u, v) and Strings.contains(v, u)

    @staticmethod
    def contains(s, t):
        '''
        :param s: ['hello', 'world', 'or', 'hell', 'of', 'WTF']
        :param t: ['world', 'or', 'hell']
        :return: False / True
        True iff
        exists k: s[k] == t[0], s[k + 1] == t[1], ... , s[k + len(t) - 1] == t[len(t) - 1]
        '''
        if len(t) > len(s):
            return False
        for i in range(len(s) - len(t) + 1):
            ans = True
            for j in range(len(t)):
                if s[i + j] != t[j]:
                    ans = False
            if ans:
                return True
        return False

    @staticmethod
    def getDirectoryAndFileName(path):
        '''
        :param path: '../aaa/bbb/ccc/myFile.json
        :return: {
                    "directory": '../aaa/bbb/ccc/
                    "fileName": 'myFile.json'
                }
        '''
        ans = {}
        res = Strings.split(path, [str(os.sep)])
        directory = ''
        for i in range(len(res) - 1):
            directory += res[i]
            directory += os.sep
        fileName = res[-1]
        # TODO:
        ans['directory'] = directory
        ans['fileName'] = fileName
        
        return ans
