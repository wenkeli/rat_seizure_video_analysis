

class ThreadCommData(object):
    def __init__(self):
        self.stopflag=False;
        self.vidFNames=[];
        self.analysisInd=0;
        self.vidFrames=[];
        self.acqFInd=0;
        self.totalFrames=0;
        self.framesPerVid=0;
        self.numVids=0;
        
        self.ratIDs=[];
        self.ratDirs=[];
