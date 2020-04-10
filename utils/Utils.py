import os
import sys
import copy
from runtime import Params
from shutil import rmtree
from utils.strings import Strings
import time
import multiprocessing as mp
import re
import ntplib

import numpy as np

from itertools import islice, cycle


class Utils:

    encodings = {
        'Linux' : 'utf-8',
        'Windows': 'cp1251',
        'OS X': 'utf-8'
    }

    @staticmethod
    def removeAllFiles(path, extension):
        files = Utils.files(path, extension)
        for fileName in files:
            os.remove(path + os.sep + fileName)

    @staticmethod
    def removeAllFilesAndDirectories(path):
        content = Utils.getAllContent(path)
        for name in content:
            x = path + os.sep + name
            if os.path.isfile(x):
                os.remove(x)
            elif os.path.isdir(x):
                rmtree(x)
            else:
                raise ValueError("file {} is not a file or dir.".format(path))

    @staticmethod
    def getAllContent(path):
        return os.listdir(path)

    @staticmethod
    def update(obj, value):
        for key in obj.keys():
            if type(obj[key]) == dict:
                Utils.update(obj[key], value)
            elif type(obj[key]) == int:
                obj[key] = value

    @staticmethod
    def files(path, extension=''):
        '''
        :param path: Direction, where you want to list all files;
        :param extension: Extension to be considered, when counting files;
        :return: List all of files associated with given @extension located in @path directory
        '''
        list_dir = os.listdir(path)
        ans = []
        for file in list_dir:
            if not os.path.isfile(path + os.sep + file):
                continue
            if file.endswith(extension):
                ans.append(file)
        return ans

    @staticmethod
    def countFiles(path, extension):
        list_dir = os.listdir(path)
        count = 0
        for file in list_dir:
            if file.endswith(extension):
                count += 1
        return str(count)

    @staticmethod
    def getPlatform():
        platforms = {
            'linux1': 'Linux',
            'linux2': 'Linux',
            'darwin': 'OS X',
            'win32': 'Windows'
        }
        if sys.platform not in platforms:
            return sys.platform
        return platforms[sys.platform]

    @staticmethod
    def getEncoding():
        encodings = {
            'Linux': 'utf-8',
            'Windows': 'cp1251',
            'OS X': 'utf-8'
        }
        platform = Utils.getPlatform()
        if platform in encodings.keys():
            return encodings[platform]
        return 'None'

    @staticmethod
    def getPythonVersion():
        return sys.version

    @staticmethod
    def getNumberOfAvailableCores():
        return mp.cpu_count()

    @staticmethod
    def getGeneralInfo():
        readerInitJson = Params.getInstance().get('ReaderInitJson')
        ans = 'Operating system:->' + Utils.getPlatform() + '\n'
        ans += 'Python version:-> ' + str(Utils.getPythonVersion()) + '\n'
        ans += 'Encoding to read data:-> ' + str(readerInitJson.encodingInput) + '\n'
        ans += 'Кодировка to write data:-> ' + str(readerInitJson.encodingOutput) + '\n'
        return ans

    @staticmethod
    def copy(obj):
        return copy.deepcopy(obj)

    @staticmethod
    def getTimeSnapshot():
        return time.time()

    @staticmethod
    def getFormattedTime(seconds):
        '''
        :param seconds: Integer.
        :return: Pandas.Dictionary.
        '''
        res = {}
        res['hh'] = seconds // (60 * 60)
        res['mm'] = (seconds - res['hh'] * 60 * 60) // 60
        res['ss'] = seconds - res['hh'] * (60 * 60) - res['mm'] * 60
        return res

    @staticmethod
    def convertTime(mileseconds, language='en'):
        '''
        :param mileseconds: Int.
        :param language: Str, in ['en', 'ru'].
        :return: Prettified string.
        '''
        encode = {
            'en': {
                'hh': 'hour(s)',
                'mm': 'minute(s)',
                'ss': 'second(s)'
            },
            'ru': {
                'hh': 'часов',
                'mm': 'минут',
                'ss': 'секунд'
            }
        }
        time = Utils.getFormattedTime(mileseconds)
        if language not in encode.keys():
            language = 'en'
        hhS = encode[language]['hh']
        mmS = encode[language]['mm']
        ssS = encode[language]['ss']
        if language == 'ru':
            hhS = encode[language]['hh']
            mmS = encode[language]['mm']
            ssS = encode[language]['ss']
            # Hours
            # 22, 23, 24 часа, однако 12, 13, 14 часов
            if time['hh'] % 10 in [2, 3, 4] and time['hh'] // 10 != 1:
                hhS = 'часа'
            elif time['hh'] % 10 == 1 and time['hh'] // 10 != 1:
                hhS = 'час'
            # Minutes
            # 22, 23, 24 минуты, однако 12, 13, 14 минут
            if time['mm'] % 10 in [2, 3, 4] and time['mm'] // 10 != 1:
                mmS = 'минуты'
            elif time['mm'] % 10 == 1:
                mmS = 'минуту'
            # Seconds
            # 22, 23, 24 секунды, однако 12, 13, 14 секунд
            if time['ss'] % 10 in [2, 3, 4] and time['ss'] // 10 != 1:
                ssS = 'секунды'
            elif time['ss'] % 10 == 1:
                ssS = 'секунду'
        __keys = [hhS, mmS, ssS]
        __values = [time['hh'], time['mm'], time['ss']]
        ans = ''
        for i in range(3):
            if __values[i] == 0:
                continue
            ans += str(__values[i])
            ans += ' '
            ans += str(__keys[i])
            ans += ', '
        ans = Strings.removeEndingWithIfAny(ans, [',', ' '])
        return ans

    @staticmethod
    def remoteTime():
        c = ntplib.NTPClient()
        response = c.request('pool.ntp.org')
        ts = response.tx_time
        return time.ctime(ts)

    @staticmethod
    def waitKeypress():
        try:
            input("Press Enter co continue")
        except SyntaxError:
            pass

    @staticmethod
    def higher(container, lo, hi, key, valueFunction, **kwargs):
        '''
        :param container: Iterable container
        :param valueFunction: Function to be applied to the Iterable container
        :param lo: lower bound
        :param hi: higher bound
        :param key:
        :return: k = min{i : valueFunction(container[i]) >= key}
        '''
        while lo <= hi:
            m = int(lo + ((hi - lo) // 2))
            kwargs['arg'] = container[m]
            print('Comparing {:s} at position {:s} VS {:s}'.format(valueFunction(**kwargs), str(m), key))
            if int(valueFunction(**kwargs)) >= int(key):
                hi = m - 1
            else:
                lo = m + 1
        return lo

    @staticmethod
    def testFunction():
        pass
