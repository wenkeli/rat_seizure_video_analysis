import numpy as np;
from PySide.QtCore import QThread;

from ..data.camthreadsbuf import CamThreadsBuf;

class ProcessThread(QThread):
    def __init__(self, threadDataArr, parent=None):
        super(ProcessThread, self).__init__(parent);
        
        self.__tDataArr=threadDataArr;
        
        
    def run(self):
        while(True):
            notDone=False;
            for data in self.__tDataArr:
                notDone=notDone or data.processFrame();
            
            if(not notDone):
                print("processing done");
                break;

