import numpy as np;

class FrameBuffer(object):
    def __init__(self, numTotalFrames):
        self.__frames=[None]*numTotalFrames;
        self.__numTotalFrames=numTotalFrames;
        self.__acqInd=0;
        self.__analysisInd=0;
        
    def addNextFrame(self, frame):
        if(self.__acqInd>=self.__numTotalFrames):
            return False;
        self.__frames[self.__acqInd]=frame;
        self.__acqInd=self.__acqInd+1;
        return True;
        
    def getNextFrame(self):
        if(self.__analysisInd>=self.__acqInd):
            return None;
        frame=self.__frames[self.__analysisInd];
        self.__analysisInd=self.__analysisInd+1;
        return frame;
    
    def removeFrame(self, relativeInd):
        rmInd=self.__analysisInd+relativeInd;
        if((rmInd<0) or (rmInd>=self.__acqInd)):
            return False;
        self.__frames[rmInd]=None;
        return True;
    
    def getFrame(self, relativeInd):
        ind=self.__analysisInd+relativeInd;
        if((ind<0) or (ind>=self.__acqInd)):
            return None;
        return self.__frames[ind];
        
