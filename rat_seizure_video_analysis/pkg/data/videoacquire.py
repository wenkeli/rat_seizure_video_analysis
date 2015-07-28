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
        
        self.__cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.__frameW);
        self.__cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__frameH);
        self.__cam.set(cv2.CAP_PROP_FPS, self.__FPS);
        self.__cam.set(cv2.CAP_PROP_BRIGHTNESS, self.__brightness);
        self.__cam.set(cv2.CAP_PROP_EXPOSURE, self.__exposure);
        
        return True;
    
    
    def acquireFrame(self):
        if(not self.__cam.grab()):
            return None;
        (success, frame)=self.__cam.retrieve();
        return frame;
    
    
    def terminate(self):
        if(self.__cam is None):
            return;
        
        self.__cam.release();
        self.__cam=None;
        