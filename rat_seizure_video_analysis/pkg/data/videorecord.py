import cv2;
import os;
from datetime import datetime;
import time;

class VideoRecord(object):
    def __init__(self, ratID, dataDir, numVids, nFramesPerVid):
        self.__fcc=cv2.VideoWriter_fourcc("m", "p", "4", "v");
        self.__vidWriter=None;
        self.__ratID=ratID;
        self.__curVidName="";
        self.__dataDir=dataDir;
        self.__numVids=numVids;
        self.__nFsPerVid=nFramesPerVid;
        self.__totalNFs=numVids*nFramesPerVid;
        self.__FPS=30;
        self.__fX=320;
        self.__fY=240; 
        
        self.__fWritten=0;
        self.__curVidN=0;
        
        self.__prevTimestamp=-1.0;
        self.__curTimestamp=-1.0;
        self.__dateObj=None;
        self.__dateStr=None;
        self.__font=cv2.FONT_HERSHEY_SIMPLEX;
        
    def getCurVidName(self):
        return self.__curVidName;
        
    def writeNextFrame(self, frame, timestamp):
        if(self.__fWritten>=self.__totalNFs):
            return False;
        if(self.__fWritten%self.__nFsPerVid==0):
            if(self.__vidWriter is not None):
                self.__vidWriter.release();
            self.__curVidName=(str(self.__ratID)+"_"+str(self.__curVidN)+".mov");
            fName=os.path.join(self.__dataDir, self.__curVidName);
            self.__vidWriter=cv2.VideoWriter(fName, self.__fcc, self.__FPS, 
                                             (self.__fX, self.__fY));
            if(not self.__vidWriter.isOpened()):
                print("critical error: can't open vid writer");
                return None;
            print(self.__ratID+" video #"+str(self.__curVidN));
            self.__curVidN=self.__curVidN+1;
            
        self.__fWritten=self.__fWritten+1;
        if(frame is None):
            print("empty frame");            
            return True;
#         print(frame.shape);

        self.__curTimestamp=timestamp;
        if(self.__curTimestamp!=self.__prevTimestamp):
            self.__dateObj=datetime.fromtimestamp(self.__curTimestamp);
            self.__dateStr="{:0>2d}".format(self.__dateObj.month)+"/"+"{:0>2d}".format(self.__dateObj.day)+"/"+str(self.__dateObj.year)+" "+"{:0>2d}".format(self.__dateObj.hour)+":"+"{:0>2d}".format(self.__dateObj.minute)+":"+"{:0>2d}".format(self.__dateObj.second);
        self.__prevTimestamp=self.__curTimestamp;
        cv2.putText(frame, self.__dateStr, (2, 237), self.__font, 0.35, (255, 255, 255), 1);
        
        self.__vidWriter.write(frame);
        return True;
    
    def terminate(self):
#         print("vid record terminating");
        if(self.__vidWriter is None):
#             print("no vid writer");
            return;
        self.__vidWriter.release();
        print("released vid writer");
        self.__vidWriter=None;
            