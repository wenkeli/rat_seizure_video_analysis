'''
Created on Oct 22, 2014
this grabs the first frame from a video to check the threshold, and static levels
works today
@author: djlab
'''
import numpy as np
import cv2;
import os.path
import cv;

def makeScreenShot(path):
    cap=cv2.VideoCapture(path);
    
    wExt = os.path.basename(path)
    filename=os.path.splitext(wExt)[0]
    print(filename)
    if cap.isOpened():
        for i in np.r_[0:2]:
            success, frame =cap.read();
            topFrame=frame[0:120, :, :];
            bottomFrame=frame[121:240, :, :];
            noMotion=frame[20:60, 20:60, :];
            if success == True:
                cv2.imwrite(filename+str(i)+".png", frame);
                cv2.imwrite(filename+"bottom"+path+str(i)+".png", bottomFrame);
                cv2.imwrite(filename+"top"+str(i)+".png", topFrame);
                cv2.imwrite(filename+"noMotion"+str(i)+".png", noMotion);
                print"images written";
            else:
                print"problems writing";
        
        
    cap.release();