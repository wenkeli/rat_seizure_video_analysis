import numpy as np;
import cv2;
# import gc;
# from pympler import tracker;

# import time;
from pkg.data.videoacquire import VideoAcquire;
from pkg.data.videorecord import VideoRecord;


rec=VideoRecord("test", "/mnt/FastData/testvids/test10", 1, 1800*30);
acq=VideoAcquire(0);
acq.initCamera();

# memTracker=tracker.SummaryTracker();

# cam=cv2.VideoCapture(0);
# print(cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320));
# print(cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240));
# print(cam.set(cv2.cv.CV_CAP_PROP_FPS, 30));
# print(cam.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, 150));
# print(cam.set(cv2.cv.CV_CAP_PROP_EXPOSURE, 110));

# cam=cv.CaptureFromCAM(0);

# memTracker.print_diff();

# for i in np.r_[0:100]:
#     time.sleep(300);
#     print(i);

i=0;
 
# frame=np.zeros((240, 320, 3), dtype="uint8");
 
while(True):
# for i in np.r_[0:7200]:
    frame=acq.acquireFrame();
    rec.writeNextFrame(frame);
    if(i>=1800*30):
        acq.terminate();
        rec.terminate();
        break;
#     (success, frame)=cam.read();
#     del(frame);
#     if(not cam.grab()):
#     if(not cv.GrabFrame(cam)):
#         continue;
#     cam.retrieve(frame);
#     cam.retrieve();
#     cv.RetrieveFrame(cam);
#     del(frame1);
#     del(success);
    i=i+1;
 
    if((i%300)==0):
        print(str(i));
#         memTracker.print_diff();
         
#         print(frame.shape);


