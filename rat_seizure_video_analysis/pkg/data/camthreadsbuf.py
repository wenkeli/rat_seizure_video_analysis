# import numpy as np;
# import gc;

from .videorecord import VideoRecord;
from .videoanalysis import VideoAnalysis;
from .videoacquire import VideoAcquire;

class CamThreadsBuf(object):
    def __init__(self, camID, ratID, dataDir, numVids, nFramesPerVid):
        self.__vidAcq=VideoAcquire(camID);
        self.__vidRecord=VideoRecord(ratID, dataDir, numVids, nFramesPerVid);
        self.__vidAnalysis=VideoAnalysis(ratID, dataDir, numVids, nFramesPerVid);
        self.__ratID=ratID;
        self.__camID=camID;
        self.__nTotalFs=numVids*nFramesPerVid;
        print(str(self.__nTotalFs)+" total number of frames")
        self.__buf=[None]*self.__nTotalFs;
        self.__acqInd=0;
        self.__procInd=0;
        self.__stopFlag=False;
        
    def getRatID(self):
        return self.__ratID;   
        
    def terminate(self):
        self.__stopFlag=True;
        
    def startCam(self):
        camSuccess=self.__vidAcq.initCamera();
        if(not camSuccess):
            self.__stopFlag=True;
        return camSuccess;
    
    def acquireFrame(self):
        if(self.__acqInd>=self.__nTotalFs):
            self.__stopFlag=True;
            
        if(self.__stopFlag):
            self.__stopAcquisition();
            return False;
        self.__buf[self.__acqInd]=self.__vidAcq.acquireFrame();
        self.__acqInd=self.__acqInd+1;
        if((self.__acqInd%1800)==0):
            print(str(self.__acqInd));
        return True;
    
        
    def processFrame(self):
        if(self.__stopFlag):
            self.__stopProcessing();
            return False;
        
        if(self.__procInd<self.__acqInd):
            self.__process();
#         else:
#             gc.collect();        
        return True;

    def __process(self):
        frame=self.__buf[self.__procInd];
        self.__vidRecord.writeNextFrame(frame);
        self.__vidAnalysis.AnalyzeNextFrame(frame, self.__vidRecord.getCurVidName());
        self.__buf[self.__procInd]=None;
        self.__procInd=self.__procInd+1;

    def __stopAcquisition(self):
        self.__vidAcq.terminate();
        
    def __stopProcessing(self):
#         print("terminating proc for "+str(self.__ratID));
        while(self.__procInd<self.__acqInd):
            self.__process();
        self.__vidRecord.terminate();
        self.__vidAnalysis.terminate();
