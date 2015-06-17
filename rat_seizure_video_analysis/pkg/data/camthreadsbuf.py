from .videorecord import VideoRecord;
from .videoanalysis import VideoAnalysis;
from .videoacquire import VideoAcquire;

class CamThreadsBuf(object):
    def __init__(self, camID, ratID, dataDir, numVids, nFramesPerVid):
        self.__vidAcq=VideoAcquire(camID);
        self.__vidRecord=VideoRecord(ratID, dataDir, numVids, nFramesPerVid);
        self.__vidAnalysis=VideoAnalysis(ratID, dataDir, numVids, nFramesPerVid);
        
        self.__nTotalFs=numVids*nFramesPerVid;
        self.__buf=[None]*self.__nTotalFs;
        self.__acqInd=0;
        self.__procInd=0;
        self.__stopFlag=False;
        
        
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
        return True;
    
        
    def proccessFrame(self):
        if(self.__stopFlag):
            self.__stopProcessing();
            return False;
        
        if(self.__procInd<self.__acqInd):
            self.__process();        
        return True;

    def __process(self):
        self.__vidAnalysis.AnalyzeNextFrame(self.__buf[self.__procInd]);
        self.__vidRecord.writeNextFrame(self.__buf[self.__procInd]);
        self.__buf[self.__procInd]=None;
        self.__procInd=self.__procInd+1;

    def __stopAcquisition(self):
        self.__vidAcq.terminate();
        
    def __stopProcessing(self):
        while(self.__procInd<self.__acqInd):
            self.__proccess();
            
        self.__vidRecord.terminate();
        self.__vidAnalysis.temrinate();
