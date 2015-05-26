'''
Created on Oct 22, 2014
Working November 11, 2014
@author: djlab
'''
import numpy as np
import cv2;
import cv;
import os.path
import time
#from collections import namedtuple
import matplotlib
#from numpy import float64, uint8
#from fileinput import filename
#from numpy import concatenate, uint8, dtype

matplotlib.use("Qt4Agg");
#what does this mean?
import matplotlib.pyplot as pp;
#def simple(videoFN, writer, ylevel=120, paths=["/Users/djlab/projects/seizureVideoAnalysis"]):
def simple(videoFN, writer, ylevel, paths):
    startTime=time.time()
    #get file info
    vidReader = cv2.VideoCapture(videoFN);
    directory = os.path.dirname(videoFN)
    wExt = os.path.basename(videoFN)
    fileName=os.path.splitext(wExt)[0]
    print(directory)
    print(fileName)
    #video properties        
    fCount=np.uint32(vidReader.get(cv.CV_CAP_PROP_FRAME_COUNT));
    fWidth=vidReader.get(cv.CV_CAP_PROP_FRAME_WIDTH);
    fHeight=vidReader.get(cv.CV_CAP_PROP_FRAME_HEIGHT);
    fRate=vidReader.get(cv.CV_CAP_PROP_FPS);
    vLength=fCount/fRate;

    #Separate frames into intervals    
    intervalSec=3;
    intervalFN=np.uint32(np.ceil(fRate*intervalSec));
    print intervalFN
    intervalBuffer=np.zeros((fHeight, fWidth, intervalFN), dtype='float64');
    #intervalBuffer=intervalFN*[None];
    tailSec=1
    tailFN=np.uint32(np.ceil(tailSec*fRate));
#    if(tailFNum>intervalFNum):
#         tailFNum=intervalFN;
    
    tailBuffer=(tailFN+intervalFN)*[None];
    tailBufInd=0;
 #would only go one loop because of size of array

    #frame manipulation    
    frameSub=np.zeros((fHeight, fWidth, intervalFN), dtype='float64');
    topSum=[];
    bottomSum=[];
    allTop=[];
    allBottom=[];
    topStdBuffer=[]

#for writing video
#     recordStartFN=0;
#     recordEndFN=0;
    prevIntHigh=False;
    #this can be added to the watchFolders2 script
    #fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
    #writer=cv2.VideoWriter(str(directory)+"/"+str(fileName)+"A.mov", fourcc, fRate, (320,240))
    #print fRate;
    #blackFrame=np.zeros((240,320), dtype='uint8');
    font = cv2.FONT_HERSHEY_SIMPLEX
    intervalsA=0
    
    for i in np.r_[0:fCount:intervalFN]:
        #THIS FIRST PART IS TO READ IN THE INTERVAL AND SAVE IT TO INTERVALBUFFER
        startFN=i;
        endFN=np.uint32(np.floor(i+intervalFN));
        curPos=endFN/fRate;
        #print "out of interval tailBufInd "+str(tailBufInd)
        if (endFN>fCount):
            print str(endFN)+" = endFN."+str(fCount)+" =fCount";
            endFN=fCount;
            #if was previously high, then write
            if prevIntHigh==True:
                #just write the interval
                intervalIndStart=((tailBufInd-intervalFN-1)%len(tailBuffer))
                intervalIndEnd=(intervalIndStart+intervalFN)%len(tailBuffer);
                #print str((intervalIndEnd-intervalIndStart)%len(tailBuffer))+"  these are the indices to be written for just the interval. it should be 90."
                for m in np.r_[0:intervalFN]:
                    cv2.putText(tailBuffer[intervalIndStart],"VidRootName: "+str(fileName),(10,10), font, 0.35, (255,255,255), 1);
                    cv2.putText(tailBuffer[intervalIndStart],"Start Time (min): "+str(round(((curPos-3)/60), 1)),(10,20), font, 0.35, (255,255,255), 1);
                    writer.write(tailBuffer[intervalIndStart])
                    intervalIndStart=(intervalIndStart+1)%len(tailBuffer)
                    print"writing to stream (first IF statement)" 
                    #if m==(intervalFN-1):
                        #print str(intervalIndStart)+" this is the last frame # written"
        if(not vidReader.isOpened()):
            print"problems with vidReader";
        for j in np.r_[startFN:endFN]:    
            success, frame=vidReader.read();
            #print "within interval tailBufInd "+str(tailBufInd)
            tailBuffer[tailBufInd]=frame;  #i think the problem is here
            #print "frame "+str(np.shape(frame));
            #print "tailBuf current frame "+str(np.shape(tailBuffer[tailBufInd]))
            tailBufInd=(tailBufInd+1)%len(tailBuffer);
            #print "tailBufInd "+str(tailBufInd)
            redFrame=frame[:,:,2]; #makes matrix into 2D
            intervalBuffer[:, :, j-startFN]=redFrame;
        #THIS PART DETECTS MOTION, AND SEPARATES THE TOP AND BOTTOM OF THE FRAME
        avgFrame=np.average(intervalBuffer, axis=2);
        
        for k in np.r_[startFN:endFN]:
            frameSub[:,:,k-startFN]=(abs(avgFrame-intervalBuffer[:,:,k-startFN]));
          
        topSum=np.sum(frameSub[0:ylevel, :, :]); #am i adding the frame in the 3rd dimension?
        allTop.append(topSum); #this is if you use python lists
        topStd=np.average(allTop[-100:])+2*(np.std(allTop[-100:]));
        topStdBuffer.append(topStd);
        #print str(np.shape(allTop))+"allTop";
        bottomSum=np.sum(frameSub[ylevel+1:240, :, :]);
        allBottom.append(bottomSum);
        #THIS WRITES THE INTERVALS ABOVE THRESHOLD
        if (topSum>=topStd):
            intervalsA+=1;
            if (not writer.isOpened()):
                print"problems with writer";
            if (prevIntHigh==False):
                prevIntHigh=True;
                #write black frames with text
#                 cv2.putText(blackFrame,"VidRootName: "+str(fileName),(10,10), font, 0.35, (255,255,255), 1)
#                 cv2.putText(blackFrame,"Time (min): "+str(curPos/60),(10,20), font, 0.35, (255,255,255), 1)
#                 for l in np.r_[0:200]:
#                     #print"writing black frame"
#                     writer.write(blackFrame);
                #write entire interval with tail
                bufIndStart=(tailBufInd)%len(tailBuffer)
                bufIndEnd=(tailBufInd-1)%len(tailBuffer)
                #print bufIndStart 
                #print bufIndEnd
                #print"this is the buffered interval. first number should be one more than second"
                for m in np.r_[0:(len(tailBuffer)-1)]:
                    cv2.putText(tailBuffer[bufIndStart],"VidRootName: "+str(fileName),(10,10), font, 0.35, (255,255,255), 1);
                    cv2.putText(tailBuffer[bufIndStart],"Start Time (min): "+str(round(((curPos-4)/60), 1))+"   Frames: "+str(startFN)+"-"+str(endFN),(10,20), font, 0.35, (255,255,255), 1);
                    writer.write(tailBuffer[bufIndStart])
                    bufIndStart=(bufIndStart+1)%len(tailBuffer)
                    #print"writing to buffered interval to stream"
#                     if m==(len(tailBuffer)-2):
#                         print str(bufIndStart)+" this is the last frame # written"  
            else:
                #just write the interval
                prevIntHigh=True;
                intervalIndStart=((tailBufInd-intervalFN-1)%len(tailBuffer))
                intervalIndEnd=(intervalIndStart+intervalFN)%len(tailBuffer);
                #print intervalIndStart
                #print str((intervalIndEnd-intervalIndStart)%len(tailBuffer))+"  these are the indices to be written for just the interval. it should be 90."
                for m in np.r_[0:intervalFN]:
                    cv2.putText(tailBuffer[intervalIndStart],"VidRootName: "+str(fileName),(10,10), font, 0.35, (255,255,255), 1);
                    cv2.putText(tailBuffer[intervalIndStart],"Start Time (min): "+str(round(((curPos-3)/60), 1)),(10,20), font, 0.35, (255,255,255), 1);
                    writer.write(tailBuffer[intervalIndStart])
                    intervalIndStart=(intervalIndStart+1)%len(tailBuffer)
                    #print "writing just the interval"
                    #if m==(intervalFN-1):
                        #print str(intervalIndStart)+" this is the last frame # written"
        else:
            prevIntHigh=False;
            #print prevIntHigh
         
        #print(str(curPos)+" seconds out of "+str(vLength));


    #intervalsA=len(sorted(i for i in allTop if i > topStdBuffer))
    print str(intervalsA*intervalSec)+"   seconds passed threshold"
    
    endTime=time.time();
    print "This program took "+str(endTime-startTime)+" seconds";

#     #PLOT MOTION
#     timeScale=np.arange(0, len(allTop), dtype="float64");
#     timeScale=timeScale * intervalSec/60.0;    
#     line1=pp.plot(timeScale, allTop, 'r');
#     pp.hold(True);
#     #line2=pp.plot(timeScale, allBottom,'b')
#     line3=pp.plot(timeScale, topStdBuffer, 'g')
#     pp.title(str(fileName))
#     pp.ylabel("Difference from Interval Avg");
#     pp.xlabel("Time (min)")
#     #pp.show();
#     pp.savefig(str(directory)+"/"+str(fileName)+"fig.png");
#     pp.hold(False);
    
#     vidSummary=namedtuple('vidSummary', 'field1 field2, field3 field4');
#     result=vidSummary(field1=timeScale, field2=allTop, field3=topStdBuffer, field4=videoFN);
    
    vidReader.release();
    #writer.release();
    #you will release the writer in the control stript
    
    return allTop, topStdBuffer, writer;