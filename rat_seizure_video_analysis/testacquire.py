import numpy as np;

from pkg.data.videoacquire import VideoAcquire;
from pkg.data.videorecord import VideoRecord;


rec=VideoRecord("test", "/Users/consciousness/Desktop/testvids/test", 1, 1800);
acq=VideoAcquire(0);

for i in np.r_[0:1800]:
    frame=acq.acquireFrame();
    rec.writeNextFrame(frame);
    if((i%100)==0):
        print(str(i));

