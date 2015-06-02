import numpy as np;
import cv;
import cv2;
import time;
from datetime import date;
from datetime import datetime;
import os;

from PySide.QtCore import QThread;

from .threadcommdata import ThreadCommData;

class AnalysisThread(QThread):
    def __init__(self, threadData, parent=None):
        super(AnalysisThread, self).__init__(parent);
        
        self.__tData=threadData;
        
    def run(self):
        fourcc=cv2.cv.CV_FOURCC("m", "p", "4", "v");
        vidOut=None;
        numVids=0;
        
        while(True):
            if(self.__tData.analysisInd<self.__tData.acqFInd):
                if(self.__tData.analysisInd%self.__tData.framesPerVid==0):
                    if(vidOut is not None):
                        vidOut.release();
                    
                    timestamp=time.time();
                    dt=datetime.fromtimestamp(timestamp);
                    
                    fName=(str(dt.year)+"_"+str(dt.month)+"_"+str(dt.day)+"_"+
                           self.__tData.ratIDs[0]+"_"+str(dt.hour)+"_"+str(dt.minute)+".mov");
                    fName=os.path.join(self.__tData.ratDirs[0],
                                       fName);
                    vidOut=cv2.VideoWriter(fName, fourcc, 30, (320,240));
                    if(not vidOut.isOpened()):
                        print("can't open video writer! >:(");
                        break;
                    print("video #"+str(numVids));
                    numVids=numVids+1;
                
                curFrame=self.__tData.vidFrames[self.__tData.analysisInd];
                self.__tData.vidFrames[self.__tData.analysisInd]=None;
                self.__tData.analysisInd=self.__tData.analysisInd+1;
                
                if(curFrame is None):
                    print("empty frame!");
                    continue;
                
                vidOut.write(curFrame);
                del(curFrame);
            
            if(self.__tData.stopflag and (self.__tData.analysisInd>=self.__tData.acqFInd)):
                if(vidOut is not None):
                    vidOut.release();
                print("stopped");
                break;
    