import numpy as np;

from PySide.QtCore import QThread;
from ..data.camthreadsbuf import CamThreadsBuf;

class CamThread(QThread):
    def __init__(self, threadData, parent=None):
        super(CamThread, self).__init__(parent);
        
        self.__tData=threadData;
        self.__numData=len(self.__tData);
        self.__dataInds=np.r_[0:self.__numData];
        
    def run(self):
        success=True;
        
        for i in self.__dataInds:
            success= success and self.__tData[i].startCam;
        
        if(not success):
            print("camera error, abort");
            return;
        
        while(True):
            notDone=False;
            for i in self.__dataInds:
                notDone=notDone or self.__tData[i].acquireFrame();
            
            if(not notDone):
                print("camera stopped");
                break;
            
