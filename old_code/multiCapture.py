'''
Created on Oct 15, 2014
camera 1 is on the left
camera 2 is on the right
@author: djlab
'''
import numpy as np
import cv2;
import cv;
import datetime;

def capFromCamera(cameraIDs, numVids, vidDurationSec, vidNameRoot, paths):
#move file name to arguments?
    #vidNameRoot="rat";
    print datetime.datetime.now();
    
    vidFPS=30;
    
    vidNumFrames=vidFPS*vidDurationSec;

    numCams=len(cameraIDs);

    capList=[];
    
    loopList=np.r_[0:numCams];
    
    for i in loopList:
        capList.append(cv2.VideoCapture(cameraIDs[i]));
    
        if(not capList[i].isOpened()):
            print("eh....");
            return;
        
        success = capList[i].set(cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        
        success = capList[i].set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
        success = capList[i].set(cv.CV_CAP_PROP_FPS, vidFPS);
        success = capList[i].set(cv.CV_CAP_PROP_BRIGHTNESS, 150)
        success = capList[i].set(cv.CV_CAP_PROP_EXPOSURE, 110)
    fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
    
    for i in np.r_[0:numVids]:
        outList=[];
        for j in loopList:
            outList.append(cv2.VideoWriter(paths[j]+"/"+vidNameRoot+str(j)+"_"+str(i)+".mov", fourcc, vidFPS, (320,240)))
        
            if(not outList[j].isOpened()):
                print("can't open video writer...");
                return;
        
        print("video #"+str(i));
        
        curFrameNum=0;
        frameList=[None]*numCams;
        while(curFrameNum<vidNumFrames):
            for j in loopList:
                success, frame = capList[j].read();
                frameList[j]=frame;
                
            for j in loopList:
                outList[j].write(frameList[j]);
            curFrameNum+=1;
            
        for j in loopList:
            outList[j].release();

 #   for i in loopList:
 #       capList[i].release();


    print datetime.datetime.now();

        