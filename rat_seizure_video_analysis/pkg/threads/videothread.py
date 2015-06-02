import cv;
import cv2;
import numpy as np;
from PySide.QtCore import QThread;

from .threadcommdata import ThreadCommData;

class VideoThread(QThread):
    def __init__(self, threadData, parent=None):
        super(VideoThread, self).__init__(parent);
        
        self.__tData=threadData;
        self.__curVidCount=0;
        
        
    def run(self):
        cam=cv2.VideoCapture(0);
        if(not cam.isOpened()):
            print("nope");
            return;
        
        success = cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        
        success = cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
        success = cam.set(cv.CV_CAP_PROP_FPS, 30);
        success = cam.set(cv.CV_CAP_PROP_BRIGHTNESS, 150)
        success = cam.set(cv.CV_CAP_PROP_EXPOSURE, 110)
        
        while(True):
            (success, frame)=cam.read();
            self.__tData.vidFrames[self.__tData.acqFInd]=frame;
            self.__tData.acqFInd=self.__tData.acqFInd+1;
            
            if(self.__tData.stopflag or (self.__tData.acqFInd>=self.__tData.totalFrames)):
                print("stopped");
                break;
