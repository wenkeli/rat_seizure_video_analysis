import os;
from datetime import date;
import time;

from PySide.QtGui import QMainWindow, QApplication;
from PySide.QtGui import QFileDialog;

from PySide.QtCore import Qt;

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
                
        self.setWindowFlags(Qt.CustomizeWindowHint
                            | Qt.WindowMinimizeButtonHint);
        
        
    def quit(self):
        self.__app.closeAllWindows();
        
    
    def selectMasterFolder(self):
        self.__dataDir=QFileDialog.getExistingDirectory(self, "select master data directory", 
                                                        os.path.expanduser("~/"));
        self.__dataDirValid=True;
        print(self.__dataDir);
        self.masterPathLabel.setText(self.__dataDir);
        
        
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
        