import cv2;
import time;
from datetime import datetime;
import os;

class VideoRecord(object):
    def __init__(self, ratID, dataDir, numVids, nFramesPerVid):
        self.__fcc=cv2.cv.CV_FOURCC("m", "p", "4", "v");
        self.__vidWriter=None;
        self.__ratID=ratID;
        self.__dataDir=dataDir;
        self.__numVids=numVids;
        self.__nFramesPerVid=nFramesPerVid;
        self.__totalFrames=numVids*nFramesPerVid;
        self.__FPS=30;
        self.__frameDim=(320, 240);    
        
        self.__framesWritten=0;
        self.__currentVidN=0;
        
        
    def writeNextFrame(self, frame):
        if(self.__framesWritten>=self.__totalFrames):
            return False;
        if(self.__framesWritten%self.__nFramesPerVid==0):
            if(self.__vidWriter is not None):
                self.__vidWriter.release();
            timestamp=time.time();
            dt=datetime.fromtimestamp(timestamp);
            fName=(str(self.__currentVidN)+"_"+str(dt.year)+"_"+str(dt.month)+"_"+
                   str(dt.day)+"_"+self.__ratID+str(dt.hour)+str(dt.minute)+".mov");
            fName=os.path.join(self.__dataDir, fName);
            self.__vidWriter=cv2.VideoWriter(fName, self.__fcc, self.__FPS, self.__frameDim);
            if(not self.__vidWriter.isOpened()):
                print("critical error: can't open vid writer");
                return None;
            print(self.__ratID+" video #"+str(self.__currentVidN));
            self.__currentVidN=self.__currentVidN+1;
            
        self.__framesWritten=self.__framesWritten+1;
        if(frame is None):
            print("empty frame");
            return False;
        
        self.__vidWriter.write(frame);
        return True;
    
    def terminateWrite(self):
        if(self.__vidWriter is not None):
            self.__vidWriter.release();
            