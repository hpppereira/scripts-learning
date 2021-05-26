
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

plt.close('all')

pathname = 'fig/frames/'

listfiles = np.sort(os.listdir(pathname))

filename = listfiles[100]

img = cv2.imread(pathname + filename)

imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(img,203,204)

# ret,thresh = cv2.threshold(imgray,127,255,0)
ret,thresh = cv2.threshold(edges,127,255,0)

# there are three arguments in cv2.findContours() function, first one is source image, second is contour retrieval
# mode, third is contour approximation method. And it outputs the image, contours and hierarchy. contours is a
# Python list of all the contours in the image. Each individual contour is a Numpy array of (x,y) coordinates of boundary
# points of the object.

image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# To draw the contours, cv2.drawContours function is used. It can also be used to draw any shape provided you
# have its boundary points. Its first argument is source image, second argument is the contours which should be passed
# as a Python list, third argument is index of contours (useful when drawing individual contour. To draw all contours,
# pass -1) and remaining arguments are color, thickness etc.

# img = cv2.drawContours(image, contours, -1, (0,255,0), 3)

# To draw an individual contour, say 4th contour

cnt = contours[4]
img = cv2.drawContours(image, [cnt], 0, (0,255,0), 3)

plt.figure(figsize=(12,7))

plt.subplot(131)
plt.imshow(img)

plt.subplot(132)
plt.imshow(image)

plt.subplot(133)
plt.imshow(img)


# Moments
# Image moments help you to calculate some features like center of mass of the object, area of the object etc. Check out
# the wikipedia page on Image Moments
# The function cv2.moments() gives a dictionary of all moment values calculated. See below:




plt.show()