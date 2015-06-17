import cv;
import cv2;

class VideoAcquire(object):
    def __init__(self, camID):
        self.__camID=camID;
        self.__cam=None;
        
        self.__frameW=320;
        self.__frameH=240;
        self.__FPS=30;
        self.__brightness=150;
        self.__exposure=110;
        
    def initCamera(self):
        self.__cam=cv2.VideoCapture(self.__camID);
        if(not self.__cam.isOpened()):
            return False;
        
        success=True;
        success = success and self.__cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, self.__frameW);
        success = success and self.__cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, self.__frameH);
        success = success and self.__cam.set(cv.CV_CAP_PROP_FPS, self.__FPS);
        success = success and self.__cam.set(cv.CV_CAP_PROP_BRIGHTNESS, self.__brightness);
        success = success and self.__cam.set(cv.CV_CAP_PROP_EXPOSURE, self.__exposure);
        
        return success;
    
    def acquireFrame(self):
        (success, frame)=self.__cam.read();
        return frame;
    
    
    def terminate(self):
        if(self.__cam is None):
            return;
        
        self.__cam.release();
        self.__cam=None;
        