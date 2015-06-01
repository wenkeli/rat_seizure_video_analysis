import os;
from datetime import date;
import time;

from PySide.QtGui import QMainWindow, QApplication;
from PySide.QtGui import QFileDialog;

from PySide import QtCore;
from PySide.QtCore import Qt, QThread;

from ..threads.threadcommdata import ThreadCommData;
from ..threads.videothread import VideoThread;
from ..threads.analysisthread import AnalysisThread;

from mainw_ui import Ui_MainW;

class MainW(QMainWindow, Ui_MainW):
    def __init__(self, app, parent=None):
        super(MainW, self).__init__(parent);
        self.setupUi(self);
        
        self.__app=app;
        self.__dataDir=None;
        self.__dataDirValid=False;
        
        self.__rat1ID="";
        self.__rat2ID="";
        
        self.__threadData=ThreadCommData();
        self.__vidThread=VideoThread(self.__threadData);
        self.__analysisThread=AnalysisThread(self.__threadData);
        QtCore.QObject.connect(self.__vidThread, QtCore.SIGNAL("finished()"), self.stopRun);
        QtCore.QObject.connect(self.__analysisThread, QtCore.SIGNAL("finished()"), self.enableQuit);
        
        self.__analysisThread.isFinished()
                
        self.setWindowFlags(Qt.CustomizeWindowHint
                            | Qt.WindowMinimizeButtonHint);
                            
        self.setInputUIEnabled(False);
        
        
    def quit(self):
        self.__app.closeAllWindows();
        
    
    def selectMasterFolder(self):
        self.__dataDir=QFileDialog.getExistingDirectory(self, "select master data directory", 
                                                        os.path.expanduser("~/"));
        self.__dataDirValid=True;
        print(self.__dataDir);
        self.masterPathLabel.setText(self.__dataDir);
        self.setInputUIEnabled(True);
        
        
    def setInputUIEnabled(self, enable):
        self.rat1IDInput.setEnabled(enable);
        self.rat2IDInput.setEnabled(enable);
        self.videoDurationBox.setEnabled(enable);
        self.numVideosBox.setEnabled(enable);
        
        
    def validateRatIDs(self):
        self.__rat1ID=self.rat1IDInput.text();
        self.__rat2ID=self.rat2IDInput.text();
        if(self.__rat1ID=="" or self.__rat2ID==""):
            return False;
        return True;
        
    def validateInputs(self):
        if(not self.__dataDirValid):
            return False;
        if(not self.validateRatIDs()):
            return False;
        return True;
    
    def startRun(self):
        self.setupFolders();
        self.setInputUIEnabled(False);
        self.startButton.setEnabled(False);
        self.selectMasterButton.setEnabled(False);
        self.quitButton.setEnabled(False);
        numFrames=self.numVideosBox.value()*self.videoDurationBox.value()*60*30;
        self.__threadData.vidFrames=[None]*numFrames;
        self.__threadData.totalFrames=numFrames;
        
        self.__vidThread.start(QThread.TimeCriticalPriority);
        self.__analysisThread.start(QThread.LowestPriority);
    
    def setupFolders(self):
        if(not self.validateInputs()):
            return;
        timestamp=time.time();
        dateobj=date.fromtimestamp(timestamp);
        
        dateStr=str(dateobj.year)+"_"+str(dateobj.month)+"_"+str(dateobj.day);
        
        folder1Str=dateStr+"_"+self.__rat1ID;
        folder2Str=dateStr+"_"+self.__rat2ID;
        
        self.__rat1Dir=os.path.join(self.__dataDir, folder1Str);
        self.__rat2Dir=os.path.join(self.__dataDir, folder2Str);
        
        os.mkdir(self.__rat1Dir);
        os.mkdir(self.__rat2Dir);
        
    def stopRun(self):
        self.__threadData.stopflag=True;
        self.stopButton.setEnabled(False);
        
    def enableQuit(self):
        self.stopButton.setEnabled(False);
        self.quitButton.setEnabled(True);
    