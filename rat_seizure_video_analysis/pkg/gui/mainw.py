import os;
from datetime import date;
import time;

from PySide.QtGui import QMainWindow, QApplication;
from PySide.QtGui import QFileDialog;

from PySide import QtCore;
from PySide.QtCore import Qt, QThread;

# from ..threads.threadcommdata import ThreadCommData;
# from ..threads.videothread import VideoThread;
# from ..threads.analysisthread import AnalysisThread;

from ..data.camthreadsbuf import CamThreadsBuf;
from ..threads.camthread import CamThread;
from ..threads.processthread import ProcessThread;

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
        
        self.__rat1CamID=-1;
        self.__rat2CamID=-1;
        
        self.__nFsPerVid=-1;
        self.__numVids=-1;
        
        self.__tData=[];
        self.__camThread=None;
        self.__procThread=None;
                
        self.setWindowFlags(Qt.CustomizeWindowHint
                            | Qt.WindowMinimizeButtonHint);
        self.__setInputUIEnabled(False);
            
        
    def quit(self):
        self.__app.closeAllWindows();
        
    
    def selectMasterFolder(self):
        self.__dataDir=QFileDialog.getExistingDirectory(self, "select master data directory", 
                                                        os.path.expanduser("~/"));
        self.__dataDirValid=True;
        print(self.__dataDir);
        self.masterPathLabel.setText(self.__dataDir);
        self.__setInputUIEnabled(True);
        self.stopButton.setEnabled(False);
        
        
    def __setInputUIEnabled(self, enable):
        self.rat1IDInput.setEnabled(enable);
        self.rat2IDInput.setEnabled(enable);
        self.rat1CamIDBox.setEnabled(enable);
        self.rat2CamIDBox.setEnabled(enable);
        self.videoDurationBox.setEnabled(enable);
        self.numVideosBox.setEnabled(enable);
        self.startButton.setEnabled(enable);
        self.stopButton.setEnabled(enable);
        
        
    def __validateInputs(self):
        if(not self.__dataDirValid):
            return False;
        self.__rat1ID=self.rat1IDInput.text();
        self.__rat2ID=self.rat2IDInput.text();
        self.__rat1CamID=self.rat1CamIDBox.value();
        self.__rat2CamID=self.rat2CamIDBox.value();
        rat1Valid=(self.__rat1ID!="") and (self.__rat1CamID>=0);
        rat2Valid=(self.__rat2ID!="") and (self.__rat2CamID>=0);
        if((not rat1Valid) and (not rat2Valid)):
            return False;
        return True;
    
    
    def startRun(self):
        if(not self.__setupData()):
            return;
        self.__setInputUIEnabled(False);
        self.selectMasterButton.setEnabled(False);
        self.quitButton.setEnabled(False);
        
        self.stopButton.setEnabled(True);
        
        self.__nFsPerVid=self.videoDurationBox.value()*60*30;
        self.__numVids=self.numVideosBox.value();


    def __setupData(self):
        if(not self.__validateInputs()):
            return False;
        timestamp=time.time();
        dateobj=date.fromtimestamp(timestamp);
        dateStr=str(dateobj.year)+"_"+str(dateobj.month)+"_"+str(dateobj.day);
        
        if((self.__rat1ID!="") and (self.__rat1CamID>=0)):
            self.__initSingleRatData(self.__rat1CamID, self.__rat1ID, dateStr);
        if((self.__rat2ID!="") and (self.__rat2CamID>=0)):
            self.__initSingleRatData(self.__rat2CamID, self.__rat2ID, dateStr);
            
        self.__initThreads();
        return True;
        
        
    def __initSingleRatData(self, camID, ratID, dateStr):
        folderStr=dateStr+"_"+ratID;
        folderStr=os.path.join(self.__dataDir, folderStr);
        os.mkdir(folderStr);
        
        tData=CamThreadsBuf(camID, ratID, folderStr, self.__numVids, self.__nFsPerVid);
        self.__tData.append(tData);
        
    
    def __initThreads(self):
        self.__camThread=CamThread(self.__tData);
        self.__procThread=ProcessThread(self.__tData);
        QtCore.QObject.connect(self.__camThread, QtCore.SIGNAL("finished()"), self.stopRun);
        QtCore.QObject.connect(self.__procThread, QtCore.SIGNAL("finished()"), self.__enableQuit);
        
        self.__camThread.start(QThread.TimeCriticalPriority);
        self.__procThread.start(QThread.LowestPriority);
        
        
    def stopRun(self):
        for data in self.__tData:
            data.terminate();
        self.stopButton.setEnabled(False);
        
        
    def __enableQuit(self):
        self.stopButton.setEnabled(False);
        self.quitButton.setEnabled(True);

