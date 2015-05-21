'''
Created on Dec 17, 2014

@author: djlab
'''
#started December 5, 2014
import os;

import cv2;
import cv;
import time;
import simpleMotion 
import atexit
import datetime
import pickle
import matplotlib
import numpy as np;

matplotlib.use("Qt4Agg");
import matplotlib.pyplot as pp;

#on Dec 24, 2014
#this program analyzed the first video many many times.  Not incrimenting. 
#feb10
#intervalSec hard coded in plotting portion 
#frame rate hard coded 
#To Unpickle:  s=pickle.load(open("1227K2K11Results.txt", "rb"))
def watchFolders(path, vidRootName, numVid, extension=".mov", wait=180):
    masterDir=[];
    newDir=[]
    allTop=[]
    allStd=[]
    print datetime.datetime.now();
    #writers=[]
    fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v');
    writerWF=cv2.VideoWriter(str(path)+"/Analyzed.mov", fourcc, 30.0, (320,240));   
    
    if (not writerWF.isOpened()):
        print"problems with writer - not created";
     
    resultsFile = open(str(path)+"/"+str(vidRootName)+'Results.txt', 'w')
    resultsFileStd = open(str(path)+"/"+str(vidRootName)+'ResultsStd.txt', 'w')
    masterDirFile = open(str(path)+"/"+str(vidRootName)+'MasterDir.txt', 'w')
    
    
    while(1):
        time.sleep(wait)
        #get the files in the path and arrange them by creation time
        newDir=sorted(os.listdir(path), key=lambda x: os.path.getctime(os.path.join(path, x)))
        #keep only the ones that are the movies we are interested in
        newDir=[each for each in newDir if str(vidRootName) in each and each.endswith(extension)]
        print str(np.shape(newDir))+" shape of newDir"
        
        for i in np.r_[0:len(newDir)]:
            #masterFileObj=None;
            existInMaster=False;
            extendedI=str(path+"/"+str(newDir[i]))
            print extendedI+" = extendedI"
            #if nothing is in the masterDir, populate it
            if not masterDir:
                size=os.stat(extendedI).st_size;
                newFile=[extendedI, size, str(False)];
                masterDir.append(newFile);
                masterInd=0;
                existInMaster=True;
                print"i found a new file!"
            temp=[each for each in masterDir if extendedI in each]
            #see if it is in masterDir
            for record in np.r_[0:len(masterDir)]:
                if extendedI==str(masterDir[record][0]):
                    existInMaster=True;
                    #print "record exists in master"
                    break; 
                elif not temp:
                    size=os.stat(extendedI).st_size;
                    newFile=[extendedI, size, str(False)];
                    masterDir.append(newFile);
                    existInMaster=True;
                    print"i found a new file! v2"
                    break;
                    #masterFileObj=record;
            
                      
            if existInMaster:
                    time.sleep(wait)
                    print str(np.shape(masterDir))+" shape of masterDir"
                    masterInd=len(masterDir)-1;
                    for j in np.r_[0:len(masterDir)]:
                        if(extendedI == str(masterDir[j][0])):
                            size=os.stat(extendedI).st_size;
                            size1=os.stat(str(masterDir[j][0])).st_size;
                            if size>size1:
                                masterDir[j][1]==size;
                                continue;
                            elif size==size1:
                                print "going to simple"
                                curTop, curStd, writerWF=simpleMotion.simple(extendedI, writerWF, 120, [path]);
                                if (not writerWF.isOpened()):
                                    print"problems with writer";
                                allTop.extend(curTop);
                                allStd.extend(curStd);
                                masterDir[j][2]=str(True)
                                print str(masterDir[j][2])+" ....done with "+extendedI
        if masterInd==numVid-1:
            break;
    
    if masterDir[numVid-1][2]==str(True):
        print"almost done"
        t=pickle.dumps(allTop)
        s=pickle.dumps(allStd)
        resultsFile.write(t)
        resultsFileStd.write(s)
        print "pickled"
#         for item in allTop:
#             resultsFile.write(str(item)+"\n")
        for item in masterDir:
            masterDirFile.write(str(item)+"\n")
                                    #do you want to add a part to plot motion here?
        plotMovement(vidRootName, path, allTop, allStd);

        resultsFile.close();
        masterDirFile.close();
        writerWF.release();
        
        
    
        #atexit.register(watchFolders)  
 
 
def plotMovement(vidRootName, path, allTop, allStd):     
    timeScale=np.arange(0, len(allTop), dtype="float64");
    timeScale=timeScale * 3/60.0;    
    pp.plot(timeScale, allTop, 'b');
    pp.hold(True);
    pp.plot(timeScale, allStd, 'g', linewidth=2)
    pp.ylabel("Difference from Interval Avg");
    pp.xlabel("Time (min)")
    pp.annotate("green=2std threshold", xy=(30,6000000))
    pp.savefig(str(path)+"/"+str(vidRootName)+"fig.png");
    pp.hold(False);
    #pp.show();  
                
                
        #termination Condition
        #if all analyzed are true and sizes aren't changing for wait interval. break loop/stop waching'