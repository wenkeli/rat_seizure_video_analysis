import numpy as np;
from PySide.QtCore import QThread;

from .threadcommdata import ThreadCommData;

class VideoThread(QThread):
    def __init__(self, threadData, parent=None):
        super(VideoThread, self).__init__(parent);
        
        self.__threadData=threadData;
        self.__curVidCount=0;
        
        
    def run(self):
        while(True):
#             self.msleep(100);
            self.__threadData.vidFrames[self.__threadData.acqFrameInd]=np.random.random((500, 500));
            self.__threadData.acqFrameInd=self.__threadData.acqFrameInd+1;
            
            if(self.__threadData.stopflag or (self.__threadData.acqFrameInd>=self.__threadData.totalFrames)):
                print("stopped");
                break;

