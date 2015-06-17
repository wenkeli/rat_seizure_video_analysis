import numpy as np;
from PySide.QtCore import QThread;

from ..data.camthreadsbuf import CamThreadsBuf;

class ProcessThread(QThread):
    def __init__(self, threadData, parent=None):
        super(ProcessThread, self).__init__(parent);
        
        self.__tData=threadData;
        self.__numData=len(self.__tData);
        self.__dataInds=np.r_[0:self.__numData];
        
        
    def run(self):
        while(True):
            notDone=False;
            for i in self.__dataInds:
                notDone=notDone or self.__tData[i].processFrame();
            
            if(not notDone):
                print("processing done");
                break;

