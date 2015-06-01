from PySide.QtCore import QThread;

from .threadcommdata import ThreadCommData;

class AnalysisThread(QThread):
    def __init__(self, threadData, parent=None):
        super(AnalysisThread, self).__init__(parent);
        
        self.__threadData=threadData;
        
    def run(self):
        while(True):
#             self.msleep(150);
            if(self.__threadData.analysisInd<self.__threadData.acqFrameInd):
                curFrame=self.__threadData.vidFrames[self.__threadData.analysisInd];
                print(str(self.__threadData.analysisInd));
                self.__threadData.vidFrames[self.__threadData.analysisInd]=None;
                self.__threadData.analysisInd=self.__threadData.analysisInd+1;
                del(curFrame);
            
            if(self.__threadData.stopflag and (self.__threadData.analysisInd>=self.__threadData.acqFrameInd)):
                print("stopped");
                break;
    