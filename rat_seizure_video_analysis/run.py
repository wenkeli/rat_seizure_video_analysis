import sys;

from PySide.QtGui import QApplication;

from pkg.gui.mainw import MainW;

if __name__=="__main__":
    app=QApplication(sys.argv);
    frame=MainW(app);
    frame.show();
    app.exec_();