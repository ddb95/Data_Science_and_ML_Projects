import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


# Read a image
img = cv.imread('/home/debadatta/Pictures/passport.jpg', 1)

# Read a image in grayScale
imgGrayScale = cv.imread('/home/debadatta/Pictures/passport.jpg', 0)

# Print the image
cv.imshow('colored', img)
cv.imshow('gray', imgGrayScale)
'''
cv.waitKey() is a keyboard binding function. 
Its argument is the time in milliseconds. 
The function waits for specified milliseconds for any keyboard event. 
If you press any key in that time, the program continues. 
If 0 is passed, it waits indefinitely for a key stroke. 
It can also be set to detect specific key strokes like, if key a is pressed etc.
'''

cv.imwrite('passportGray.jpg', imgGrayScale)
cv.waitKey(0)
cv.destroyAllWindows()
