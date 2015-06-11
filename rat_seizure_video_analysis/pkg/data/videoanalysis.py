import os;
import numpy as np;

class VideoAnalysis(object):
    def __init__(self, ratID, dataDir, nFramesPerVid):
        self.__ratID=ratID;
        self.__dataDir=dataDir;
        self.__nFramesPerVid=nFramesPerVid;
        self.__FPS=30;
        self.__curFrameN=0;
        self.__curVidN=0;
        self.__intervalBuffer=[None]*90;
        self.__intervalBufferInd=0;
        
        
    