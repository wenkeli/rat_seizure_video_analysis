import numpy as np;
import cv;
import cv2;
from pkg.data.videoacquire import VideoAcquire;
from pkg.data.videorecord import VideoRecord;


rec=VideoRecord("test", "/Users/consciousness/Desktop/testvids/test", 1, 1800);
acq=VideoAcquire(0);
acq.initCamera();

# cam=cv2.VideoCapture(0);
# print(cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, 320));
# print(cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240));
# print(cam.set(cv.CV_CAP_PROP_FPS, 30));
# print(cam.set(cv.CV_CAP_PROP_BRIGHTNESS, 150));
# print(cam.set(cv.CV_CAP_PROP_EXPOSURE, 110));


for i in np.r_[0:1800]:
    frame=acq.acquireFrame();
    rec.writeNextFrame(frame);
    
#     (success, frame)=cam.read();

    if((i%100)==0):
        print(str(i));
#         print(frame.shape);

