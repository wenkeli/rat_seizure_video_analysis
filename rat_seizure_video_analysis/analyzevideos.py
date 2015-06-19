import os;

from pkg.data.videoanalysis import VideoAnalysis;
from pkg.data.videoread import VideoRead;

def analyzeVideos(ratDir, fExt=".mov"):
    ratID=os.path.basename(ratDir);
    if(ratID==""):
        ratID=os.path.basename(os.path.dirname(ratDir));
    print("ratID "+ratID);
    
    vidRead=VideoRead(ratDir, "*"+fExt);
    vidProc=VideoAnalysis(ratID, ratDir, vidRead.getNumVids(), vidRead.getNumFramesPerVid());
    
    print("starting on "+ratDir);
    while(True):
        (frame, vidName)=vidRead.readFrame();
        if(frame is None):
            vidProc.terminate();
            break;
        vidProc.AnalyzeNextFrame(frame, vidName);
        
    print("finished");
    