import os;
import glob;

from pkg.data.videoanalysis import VideoAnalysis;

def analyzeVideos(ratDir, secondsPerVid):
    ratDir=os.path.expanduser(ratDir);
    ratDir=os.path.abspath(ratDir);
    
    files=glob.glob1(ratDir, "*.mov");
    files.sort(key=lambda x: os.stat(os.path.join(ratDir, x)).st_ctime);
    
    