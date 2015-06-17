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
        self.__curVidN=0;
        self.__intBufLen=90;
        self.__intervalBuf=[None]*self.__intBufLen;
        self.__intBufInd=0;
        self.__chN=2;
        
        self.__yLevel=120;
        self.__fDim=(320, 240);
        
        self.__topDifData=np.zeros(self.__totalNFs, dtype="float32");
        self.__bottomDifData=np.zeros(self.__totalNFs, dtype="float32");
        
        self.__avgFrame=np.zeros(self.__fDim, dtype="float32");
        
        self.__fcc=cv2.cv.CV_FOURCC("m", "p", "4", "v");
        fName=ratID+"_filtered.mov";
        fName=os.path.join(dataDir, fName);
        self.__sumVid=cv2.VideoWriter(fName, self.__fcc, self.__FPS, self.__fDim);
        
        self.__curVidName=ratID+"_"+str(self.__curVidN);
        self.__vidIntervalEnd=0;
        self.__font = cv2.FONT_HERSHEY_SIMPLEX;
        
        
    
    def AnalyzeNextFrame(self, frame):
        if(self.__curFN>=self.__totalNFs):
            return False;
        
        if(self.__curFN%self.__nFsPerVid==0):
            self.__curVidN=self.__curVidN+1;
            self.__curVidName=self.__ratID+"_"+str(self.__curVidN);
        
        frameForBuf=frame[:,:, self.__chN]/self.__intBufLen;
        
        self.__avgFrame=self.__avgFrame+frameForBuf;
        
        bufFrame=self.__intervalBuf[self.__intBufInd];
        self.__intervalBuf[self.__intBufInd]=frameForBuf;
        
        if(bufFrame is None):
            self.__vidIntervalEnd=self.__intBufLen;
        else:
            self.__avgFrame=self.__avgFrame-bufFrame;
            
        subFrame=np.abs(self.__avgFrame-frame[:, :, self.__chN]);
        topSum=np.sum(subFrame[0:self.__yLevel, :]);
        bottomSum=np.sum(subFrame[self.__yLevel+1:, :]);
        self.__topDifData[self.__curFN]=topSum;
        self.__bottomDifData[self.__curFN]=bottomSum;
        
        #insert code for checking threshold etc
        
        self.__writeSumFrame(frame);
        self.__intBufInd=(self.__intBufInd+1)%self.__intBufLen;
        self.__curFN=self.__curFN+1;
        
        return True;
    
    def temrinate(self):
        if(self.__sumVid is None):
            return;
        
        self.__sumVid.release();
        self.__sumVid=None;
        
        fName=self.__ratID+"_analysisData.np";
        fName=os.path.join(self.__dataDir, fName);
        fh=open(fName, "wb");
        pickle.dump(self.__topDifData, fh, protocol=2);
        pickle.dump(self.__bottomDifData, fh, protocol=2);
        fh.close();
        
        
    def __writeSumFrame(self, frame):
        if(self.__curFN>=self.__vidIntervalEnd):
            return;
        
        cv2.putText(frame, "file: "+self.__curVidName, (10, 10), self.__font,
                    0.35, (255, 255, 255), 1);
                    
        fNInVid=self.__curFN%self.__nFsPerVid;
        secInVid=np.floor(fNInVid/self.__FPS);
        minInVid=np.floor(secInVid/60);
        secInVid=secInVid%60;
        timeStr="time: "+str(minInVid)+" "+str(secInVid);
        cv2.putText(frame, timeStr, (10, 20), self.__font, 0.35, (255, 255, 255), 1);
            
        self.__sumVid.write(frame);
        