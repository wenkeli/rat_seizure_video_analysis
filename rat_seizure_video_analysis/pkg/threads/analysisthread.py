import time;
from PySide.QtCore import QThread;

from .threadcommdata import ThreadCommData;

class AnalysisThread(QThread):
    def __init__(self, threadData, parent=None):
        super(AnalysisThread, self).__init__(parent);
        
        self.__threadData=threadData;
        
    def run(self):
        while(True):
            time.sleep(1);
            print("2");
            if(self.__threadData.analysisInd<len(self.__threadData.vidFNames)):
                self.analyzeFile();
            if(self.__threadData.stopflag):
                print("stopped");
                break;
            
    def analyzeFile(self):
        print(self.__threadData.vidFNames[self.__threadData.analysisInd]);
        self.__threadData.analysisInd=self.__threadData.analysisInd+1;
    