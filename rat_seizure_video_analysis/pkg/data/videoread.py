import cv2;
import cv;
import numpy as np;
import os;
import glob;

class VideoRead(object):
    def __init__(self, dataDir, fileExt):
        self.__vidReader=None;
        
        self.__dataDir=None;
        self.__fileList=None;
        self.__nFsPerVid=-1;
        self.__curNFsInVid=-1;
        self.__numVids=-1;
        self.__curVidN=0;
        self.__curFN=0;
        
        self.__dataDir=os.path.expanduser(dataDir);
        self.__dataDir=os.path.abspath(self.__dataDir);
        
        files=glob.glob1(self.__dataDir, fileExt);
        files.sort(key=lambda x: os.stat(os.path.join(self.__dataDir, x)).st_ctime);
        self.__fileList=files;
        
        self.__numVids=len(files);
        
        vidName=os.path.join(self.__dataDir, self.__fileList[self.__curVidN]);
        self.__vidReader=cv2.VideoCapture(vidName);
        self.__nFsPerVid=np.uint32(self.__vidReader.get(cv.CV_CAP_PROP_FRAME_COUNT));
        self.__curNFsInVid=self.__nFsPerVid;
        self.__curVidN=self.__curVidN+1;
        
        
    def readFrame(self):
        if(self.__curFN>=self.__curNFsInVid):
            if(self.__curVidN>=self.__numVids):
                self.__vidReader.release();
                return (None, None);
            self.__vidReader.release();
            
            vidName=os.path.join(self.__dataDir, self.__fileList[self.__curVidN]);
            self.__vidReader=cv2.VideoCapture(vidName);
            if(not self.__vidReader.IsOpened()):
                print("problem with reading video");
                return (None, None);
            self.__curNFsInVid=np.uint32(self.__vidReader.get(cv.CV_CAP_PROP_FRAME_COUNT));
            self.__curVidN=self.__curVidN+1;
            self.__curFN=0;
            
            
        (success, frame)=self.__vidReader.read();            
        self.__curFN=self.__curFN+1;
        return (frame, self.__fileList[self.__curVidN]);
        
        
    def getNumFramesPerVid(self):
        return self.__nFsPerVid;
    
    def getNumVids(self):
        return self.__numVids;