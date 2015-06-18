import numpy as np;

from PySide.QtCore import QThread;
from ..data.camthreadsbuf import CamThreadsBuf;

class CamThread(QThread):
    def __init__(self, threadDataArr, parent=None):
        super(CamThread, self).__init__(parent);
        
        self.__tDataArr=threadDataArr;
        
    def run(self):
        success=True;
        
        for data in self.__tDataArr:
            success= success and data.startCam();
        
        if(not success):
            print("camera error, abort");
            return;
        
        while(True):
            notDone=False;
            for data in self.__tDataArr:
                notDone=notDone or data.acquireFrame();
            
            if(not notDone):
                print("camera stopped");
                break;
            
