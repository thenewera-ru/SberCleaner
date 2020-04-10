import threading

from utils import Utils


class Params:
    '''
    The purpose of this object is to share Heavy-lifted objects. E.g. Pandas.DataFrame that holds huge table.
    '''
    # Single-tone design
    _data = {}
    _instance = None
    _lock = threading.RLock

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Params._instance is None:
            Params()

        return Params._instance

    def __init__(self):
        if Params._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Params._instance = self
            Params._lock = threading.Lock()

    @property
    def keys(self):
        return self._data.keys()

    @property
    def data(self):
        return self._data

    def set(self, key, value):
        self.lock()
        self._data[key] = value
        self.unlock()

    def snapshot(self, key):
        self.lock()
        snapshot = Utils.copy(self._data[key])
        self.unlock()
        return snapshot

    def update(self, objectKey, newValue):
        self.lock()
        self._data[objectKey] = newValue
        self.unlock()

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()


