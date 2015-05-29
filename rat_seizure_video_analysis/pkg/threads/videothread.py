import time;
from PySide.QtCore import QThread;

from .threadcommdata import ThreadCommData;

class VideoThread(QThread):
    def __init__(self, threadData, parent=None):
        super(VideoThread, self).__init__(parent);
        
        self.__threadData=threadData;
        
        
    def run(self):
        while(True):
            time.sleep(1);
            print("1");
            if(self.__threadData.stopflag):
                print("stopped");
                break;

