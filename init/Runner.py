from runtime import Params
from in_out import ReaderJson
import os, sys
from utils import Utils


class Runner:
    """
    All the initial settings, such as:
    DEBUG,
    STOP_WORDS,
    RUBBISH_RESPONSES,
    etc...
    are set up here.
    All the single-ton objects are also initialized here. And some heavy-lifed objects are initalized here as well.
    """
    # Single-tone design
    _data = {}
    _instance = None

    @staticmethod
    def run():
        """ Static access method. """
        if Runner._instance is None:
            Runner()

        return Runner._instance

    def __init__(self):
        """ Virtually private constructor. """
        if Runner._instance is not None:

            raise Exception("This class is a singleton!")

        else:
            Runner._instance = self
        params = Params.getInstance()
        # DEBUG(ON) => RELEASE(OFF), DEBUG(OFF) => RELEASE(ON)
        params.set('DEBUG', 'OFF')
        initParams = ReaderJson(directory=os.getcwd() + os.sep, filename='init.json')
        initParams.read()
        params.set('InitParams', initParams)

    def set(self, key, value):
        self._data[key] = value

    @property
    def data(self):
        return self._data
