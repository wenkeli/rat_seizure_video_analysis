import numpy as np;

from PySide.QtCore import QThread;
from ..data.camthreadsbuf import CamThreadsBuf;

class CamThread(QThread):
    def __init__(self, threadData, parent=None):
        super(CamThread, self).__init__(parent);
        
        self.__tData=threadData;
        
    def run(self):
        
        success=self.__tData.startCam();
        print self.__tData.getRatID();
        print self.__tData;
        if(not success):
            print("camera error, abort");
            return;
        
        while(True):
            notDone=False;
            self.__tData.grabFrame();        
            notDone=self.__tData.acquireFrame();
            
            if(not notDone):
                print("camera stopped");
                break;
            
