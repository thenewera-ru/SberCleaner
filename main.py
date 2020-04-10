from init import Runner as Init
from runtime import Params
from model.data import DataLoader
from utils.system import System
import os
import pandas as pd
from in_out import WriterCsv
from pathlib import Path

if __name__ == '__main__':
    Init.run()
    initParams = Params.getInstance().data['InitParams']
    filenames = System.files(initParams.chatsLocation, 'csv')
    print('Started processing files located in {:s}'.format(str(Path(os.getcwd()) / initParams.chatsLocation)))
    begin = System.timeSnapshot()
    for filename in filenames:
        chatLoader = DataLoader(filepath=os.path.join(initParams.chatsLocation, filename))
        columns = initParams.columns
        writer = WriterCsv(directory=initParams.chatsOutputLocation, filename=filename)
        out = pd.DataFrame(columns=columns)
        for i, chat in enumerate(chatLoader):
            dialogue = pd.DataFrame(columns=columns)
            for name in columns:
                dialogue[name] = pd.Series(dtype=object, data=chatLoader.column(name, batchIndex=i))
            out = out.append(dialogue)
        writer.write(data=out)
        print('File {:s} is processed.'.format(filename))
    end = System.timeSnapshot()

