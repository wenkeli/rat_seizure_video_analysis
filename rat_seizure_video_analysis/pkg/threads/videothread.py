import time;
from PySide.QtCore import QThread;

from .threadcommdata import ThreadCommData;

class VideoThread(QThread):
    def __init__(self, threadData, parent=None):
        super(VideoThread, self).__init__(parent);
        
        self.__threadData=threadData;
        self.__curVidCount=0;
        
        
    def run(self):
        while(True):
            time.sleep(5);
            print("1");
            self.__threadData.vidFNames.append("test"+str(self.__curVidCount));
            self.__curVidCount=self.__curVidCount+1;
            
            if(self.__threadData.stopflag):
                print("stopped");
                break;

