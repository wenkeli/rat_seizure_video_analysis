import os;
import numpy as np;
import cv2;
import cPickle as pickle;

class VideoAnalysis(object):
    def __init__(self, ratID, dataDir, numVids, nFramesPerVid):
        self.__ratID=ratID;
        self.__dataDir=dataDir;
        self.__nFsPerVid=nFramesPerVid;
        self.__numVids=numVids;
        self.__totalNFs=self.__nFsPerVid*self.__numVids;
        self.__FPS=30;
        
        self.__curFN=0;
        
        self.__stableThreshStart=60*self.__FPS;
        self.__threshLen=300*self.__FPS;
        
        self.__actIntevral=2*self.__FPS;
        self.__actHighLevel=self.__actIntevral/2;
        self.__postEventLen=5*self.__FPS;
        self.__actFBuf=[None]*self.__actIntevral;
        self.__actVidNBuf=[None]*self.__actIntevral;
        self.__actFBufInd=0;
        
        self.__intBufLen=3*self.__FPS;
        self.__intervalBuf=[None]*self.__intBufLen;
        self.__intBufInd=0;
        self.__chN=2;
        
        self.__yLevel=120;
        self.__fX=320;
        self.__fY=240;
        
        self.__topDifData=np.zeros(self.__totalNFs, dtype="float32");
        self.__bottomDifData=np.zeros(self.__totalNFs, dtype="float32");
        
        self.__topDifThAvg=np.zeros(self.__totalNFs, dtype="float32");
        self.__topDifThStd=np.zeros(self.__totalNFs, dtype="float32");
        self.__topDifThresh=np.zeros(self.__totalNFs, dtype="float32");
        self.__passThresh=np.zeros(self.__totalNFs, dtype="bool");
        
        self.__passRecord=np.zeros(self.__totalNFs, dtype="bool");
        
        self.__avgFrame=np.zeros((self.__fY, self.__fX), dtype="float32");
        
        self.__fcc=cv2.cv.CV_FOURCC("m", "p", "4", "v");
        fName=ratID+"_filtered.mov";
        fName=os.path.join(dataDir, fName);
        self.__sumVid=cv2.VideoWriter(fName, self.__fcc, self.__FPS,
                                      (self.__fX, self.__fY));
        
        self.__vidIntervalEnd=0;
        self.__font = cv2.FONT_HERSHEY_SIMPLEX;
        
        
    
    def AnalyzeNextFrame(self, frame, vidName):
        if(self.__curFN>=self.__totalNFs):
            return False;
        
        frameForBuf=frame[:,:, self.__chN]/float(self.__intBufLen);
        
        self.__avgFrame=self.__avgFrame+frameForBuf;
        
        bufFrame=self.__intervalBuf[self.__intBufInd];
        self.__intervalBuf[self.__intBufInd]=frameForBuf;
        
        if(bufFrame is not None):
            self.__avgFrame=self.__avgFrame-bufFrame;
            
        subFrame=np.abs(self.__avgFrame-frame[:, :, self.__chN]);
        topSum=np.sum(subFrame[0:self.__yLevel, :]);
        bottomSum=np.sum(subFrame[self.__yLevel+1:, :]);
        self.__topDifData[self.__curFN]=topSum;
        self.__bottomDifData[self.__curFN]=bottomSum;
        
        actFrame=self.__actFBuf[self.__actFBufInd];
        actVidName=self.__actVidNBuf[self.__actFBufInd];
        self.__actFBuf[self.__actFBufInd]=frame;
        self.__actVidNBuf[self.__actFBufInd]=vidName;
        self.__actFBufInd=(self.__actFBufInd+1)%self.__actIntevral;
        
        self.__calcThresh();
        
        self.__writeSumFrame(actFrame, actVidName);
        self.__intBufInd=(self.__intBufInd+1)%self.__intBufLen;
        self.__curFN=self.__curFN+1;
        
        return True;
    
    def __calcThresh(self):
        if(self.__curFN<self.__stableThreshStart):
            return;
        if(self.__curFN>self.__threshLen+self.__intBufLen):
            thStartInd=self.__curFN-self.__threshLen;
        else:
            thStartInd=self.__intBufLen;
            
        avg=np.average(self.__topDifData[thStartInd:self.__curFN]);
        std=np.std(self.__topDifData[thStartInd:self.__curFN]);
        self.__topDifThAvg[self.__curFN]=avg;
        self.__topDifThStd[self.__curFN]=std;
        
        thresh=avg+2*std;
        self.__topDifThresh[self.__curFN]=thresh;
        
        self.__passThresh[self.__curFN]=self.__topDifData[self.__curFN]>thresh;
        
        record=np.sum(self.__passThresh[self.__curFN-self.__actIntevral:self.__curFN])>self.__actHighLevel;
        self.__passRecord[self.__curFN-self.__actIntevral]=record;
        
        if(record):
            self.__vidIntervalEnd=self.__curFN+self.__postEventLen;
    
    
    def terminate(self):
        if(self.__sumVid is None):
            return;
        
        self.__sumVid.release();
        self.__sumVid=None;
        
        fName=self.__ratID+"_analysisData.np";
        fName=os.path.join(self.__dataDir, fName);
        fh=open(fName, "wb");
        pickle.dump(self.__topDifData, fh, protocol=2);
        pickle.dump(self.__bottomDifData, fh, protocol=2);
        pickle.dump(self.__topDifThresh, fh, protocol=2);
        pickle.dump(self.__passThresh, fh, protocol=2);
        pickle.dump(self.__passRecord, fh, protocol=2);
        
        fh.close();

        
        
    def __writeSumFrame(self, frame, vidName):
        frameN=self.__curFN-self.__actIntevral;
        if(frameN>=self.__vidIntervalEnd):
            return;
        
        cv2.putText(frame, vidName, (10, 10), self.__font,
                    0.35, (255, 255, 255), 1);
                    
        fNInVid=frameN%self.__nFsPerVid;
        secInVid=np.floor(fNInVid/self.__FPS);
        minInVid=np.floor(secInVid/60);
        secInVid=secInVid%60;
        timeStr=str(minInVid)+"m "+str(secInVid)+"s";
        cv2.putText(frame, timeStr, (10, 20), self.__font, 0.35, (255, 255, 255), 1);
            
        self.__sumVid.write(frame);
        