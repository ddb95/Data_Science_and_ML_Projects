import numpy as np
import cv2 as cv

'''
Often, we have to capture live stream with camera. 
OpenCV provides a very simple interface to this. 
Let's capture a video from the camera (I am using the in-built webcam of my laptop), convert it into grayscale video and display it. 
Just a simple task to get started.
'''

cap = cv.VideoCapture(0)
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Operations on the frame
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # display the frame
    cv.imshow('frame', gray)
    if cv.waitKey(0) & 0XFF == ord('q'):
        break;

cap.release()
cv.destroyAllWindows()
