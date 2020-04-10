from utils.strings import Strings
import os
from pathlib import Path


class Reader:

    def __init__(self, directory=None, filename=None):
        self._directory, self._filename, self._filepath = None, None, None
        try:
            self._directory = Path(directory)
            self._filename = Path(filename)
            self._filepath = self._directory / self._filename
        except TypeError:
            pass

    @classmethod
    def fromFile(cls, filepath=None):
        instance = cls()
        instance.filepath = filepath
        return instance

    @property
    def directory(self):
        return str(self._directory)

    @directory.setter
    def directory(self, arg):
        self._directory = Path(arg)
        self.onUpdate()

    @property
    def filename(self):
        return str(self._filename)

    @filename.setter
    def filename(self, arg):
        self._filename = Path(arg)
        self.onUpdate()

    @property
    def filepath(self):
        return str(self._filepath)

    @filepath.setter
    def filepath(self, arg):
        argw = Path(arg)
        self.directory = argw.parent
        self.filename = argw.name
        self.onUpdate()

    def read(self, **kwargs):
        pass

    def onUpdate(self):
        try:
            self._filepath = self._directory / self._filename
        except TypeError:
            pass
