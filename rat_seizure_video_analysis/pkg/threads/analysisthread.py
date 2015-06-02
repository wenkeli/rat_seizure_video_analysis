import numpy as np;
import cv;
import cv2;


from PySide.QtCore import QThread;

from .threadcommdata import ThreadCommData;

class AnalysisThread(QThread):
    def __init__(self, threadData, parent=None):
        super(AnalysisThread, self).__init__(parent);
        
        self.__tData=threadData;
        
    def run(self):
        while(True):
            if(self.__tData.analysisInd<self.__tData.acqFInd):
                curFrame=self.__tData.vidFrames[self.__tData.analysisInd];
                self.__tData.vidFrames[self.__tData.analysisInd]=None;
                self.__tData.analysisInd=self.__tData.analysisInd+1;
                del(curFrame);
            
            if(self.__tData.stopflag and (self.__tData.analysisInd>=self.__tData.acqFInd)):
                print("stopped");
                break;
    