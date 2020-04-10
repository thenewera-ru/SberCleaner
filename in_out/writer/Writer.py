from pathlib import Path


class Writer:

    def __init__(self, directory=None, filename=None):
        self._directory = None
        self._filename = None
        self._filepath = None
        try:
            self._directory = Path(directory)
        except TypeError:
            pass
        try:
            self._filename = Path(filename)
        except TypeError:
            pass
        self.onUpdate()

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
        fpath = Path(arg)
        self.directory = fpath.parent
        self.filename = fpath.name
        self.onUpdate()

    def write(self, **kwargs):
        pass

    def onUpdate(self):
        try:
            self._filepath = self._directory / self._filename
        except TypeError:
            pass
