import numpy as np;
import cv2;
import time;
from datetime import datetime;
import os;
import cPickle as pickle;

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
        
        ylevel=120;
        
        topSumArray=np.zeros(self.__tData.totalFrames, dtype="float32");
        buttomSumArray=np.zeros(self.__tData.totalFrames, dtype="float32");
        
        avgFrame=np.zeros((240, 320), dtype="float32");
        
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
                                    
                if(curFrame is None):
                    print("empty frame!");
                    continue;
                
                vidOut.write(curFrame);
                
                avgFrame=avgFrame+(curFrame[:,:, 2]/90.0);
                avgSubInd=self.__tData.analysisInd-90;
                if(self.__tData.analysisInd>=90):
                    avgFrame=avgFrame-(self.__tData.vidFrames[avgSubInd][:,:,2]/90.0);
                    wAvgF=avgFrame;
                else:
                    wAvgF=avgFrame*90/(self.__tData.analysisInd+1);
                
                self.__tData.vidFrames[avgSubInd]=None;
                
                subFrame=abs(wAvgF-curFrame[:,:,2]);
                
                topSum=np.sum(subFrame[0:ylevel, :]);
                buttomSum=np.sum(subFrame[ylevel+1:, :]);
                topSumArray[self.__tData.analysisInd]=topSum;
                buttomSumArray[self.__tData.analysisInd]=buttomSum;
                
                
                self.__tData.analysisInd=self.__tData.analysisInd+1;
                
            
            if(self.__tData.stopflag and (self.__tData.analysisInd>=self.__tData.acqFInd)):
                if(vidOut is not None):
                    vidOut.release();
                print("stopped");
                break;
            
        fname=os.path.join(self.__tData.ratDirs[0], "results.np");
        fh=open(fname, "wb");
        pickle.dump(topSumArray, fh, protocol=2);
        pickle.dump(buttomSumArray, fh, protocol=2);
        fh.close();
    