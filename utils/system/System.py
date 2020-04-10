import os, time
import multiprocessing as mp

class System:

    @staticmethod
    def files(directory, extension=''):
        '''
        :param directory: Direction, where you want to list all files;
        :param extension: Extension to be considered, when counting files;
        :return: List all of files associated with given @extension located in @path directory
        '''
        list_dir = os.listdir(directory)
        ans = []
        for filename in list_dir:
            if not os.path.isfile(os.path.join(directory, filename)):
                continue
            if filename.endswith(extension):
                ans.append(filename)
        return ans

    @staticmethod
    def timeSnapshot():
        return time.time

    @staticmethod
    def cores(*args):
        return mp.cpu_count()
