import cv;
import cv2;
import numpy as np;
from PySide.QtCore import QThread;

from .threadcommdata import ThreadCommData;

class VideoThread(QThread):
    def __init__(self, threadDataArr, parent=None):
        super(VideoThread, self).__init__(parent);
        
        self.__tDataArr=threadDataArr;
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
            self.__tDataArr.vidFrames[self.__tDataArr.acqFInd]=frame;
            self.__tDataArr.acqFInd=self.__tDataArr.acqFInd+1;
            
            if(self.__tDataArr.stopflag or (self.__tDataArr.acqFInd>=self.__tDataArr.totalFrames)):
                print("stopped");
                break;
            
        cam.release();
