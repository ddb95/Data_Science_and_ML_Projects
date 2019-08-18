

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

image = cv.imread('/home/debadatta/Pictures/passport.jpg')
# convert to grayscale

grayImage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)


'''
Shi-Tomasi Corner Detector & Good Features to Track
'''

'''
Params to pass:
1. image
2. maxcorners
3. minDistance
4. qualityLevel
'''
corners = cv.goodFeaturesToTrack(grayImage, 25, 0.01, 10)
corners = np.int0(corners)

for i in corners:
    x, y = i.ravel()
    cv.circle(image, (x, y), 3, 255, -1)

plt.imshow(image)
plt.show()


# cv.imshow('image', image)
# cv.waitKey(0)
# cv.destroyAllWindows()
