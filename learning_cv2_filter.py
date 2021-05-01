"""
Detecting Circles in Images using OpenCV and Hough Circles
s
Take a look at the function signature below:

cv2.HoughCircles(image, method, dp, minDist)

image: 8-bit, single channel image. If working with a color image, convert to grayscale first.

method: Defines the method to detect circles in images. Currently, the only implemented method
		 is cv2.HOUGH_GRADIENT, which corresponds to the Yuen et al. paper.

dp: This parameter is the inverse ratio of the accumulator resolution to the image
 resolution (see Yuen et al. for more details). Essentially, the larger the dp gets, 
 the smaller the accumulator array gets.

minDist: Minimum distance between the center (x, y) coordinates of detected circles. 
If the minDist is too small, multiple circles in the same neighborhood as the original
 may be (falsely) detected. If the minDist is too large, then some circles may not be detected at all.

param1: Gradient value used to handle edge detection in the Yuen et al. method.

param2: Accumulator threshold value for the cv2.HOUGH_GRADIENT method. The smaller 
the threshold is, the more circles will be detected (including false circles). 
The larger the threshold is, the more circles will potentially be returned.

minRadius: Minimum size of the radius (in pixels).

maxRadius: Maximum size of the radius (in pixels).
"""


import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

plt.close('all')
cv2.destroyAllWindows()

# ---------------------------------------------- #

nframe = 100
pathname = 'fig/frames/'

listfiles = np.sort(os.listdir(pathname))

filename1 = listfiles[nframe]
filename2 = listfiles[nframe+1]

# img = cv2.imread(pathname + filename)
img1 = cv2.imread(pathname + filename1)
img2 = cv2.imread(pathname + filename2)

# img = img2 - img1
img = img1

# ---------------------------------------------- #

blurred = cv2.GaussianBlur(img, (5, 5), 0) # Remove noise


def edgedetect (channel):
    sobelX = cv2.Sobel(channel, cv2.CV_16S, 1, 0)
    sobelY = cv2.Sobel(channel, cv2.CV_16S, 0, 1)
    sobel = np.hypot(sobelX, sobelY)

    sobel[sobel > 255] = 255; # Some values seem to go above 255. However RGB channels has to be within 0-255

    return sobel

sobel0 = edgedetect(blurred[:,:, 0])
sobel1 = edgedetect(blurred[:,:, 1])
sobel2 = edgedetect(blurred[:,:, 2])

edgeImg = np.max( np.array([sobel0, sobel1,  sobel2 ]), axis=0 )

# stop
mean = np.mean(edgeImg);
# Zero any value that is less than mean. This reduces a lot of noise.
edgeImg[edgeImg <= mean] = 0;



def findSignificantContours (img, edgeImg):

    image, contours, heirarchy = cv2.findContours(edgeImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find level 1 contours
    level1 = []
    for i, tupl in enumerate(heirarchy[0]):
        # Each array is in format (Next, Prev, First child, Parent)
        # Filter the ones without parent
        if tupl[3] == -1:
            tupl = np.insert(tupl, 0, [i])
            level1.append(tupl)

    # From among them, find the contours with large surface area.
    significant = []
    tooSmall = edgeImg.size * 5 / 100 # If contour isn't covering 5% of total area of image then it probably is too small
    for tupl in level1:
        contour = contours[tupl[0]];
        area = cv2.contourArea(contour)
        if area > tooSmall:
            significant.append([contour, area])

            # Draw the contour on the original image
            cv2.drawContours(img, [contour], 0, (0,255,0),2, cv2.LINE_AA, maxLevel=1)

    significant.sort(key=lambda x: x[1])
    #print ([x[1] for x in significant]);
    return [x[0] for x in significant],  contour;

edgeImg_8u = np.asarray(edgeImg, np.uint8)

# Find contours
significant, contour = findSignificantContours(img, edgeImg_8u)


# Mask
mask = edgeImg.copy()
mask[mask > 0] = 0
cv2.fillPoly(mask, significant, 255)
# Invert mask
mask = np.logical_not(mask)

#Finally remove the background
img[mask] = 0;


epsilon = 0.10*cv2.arcLength(contour,True)
approx = cv2.approxPolyDP(contour, 3,True)
contour = approx                


# from scipy.signal import savgol_filter
# # ...
# # Use Savitzky-Golay filter to smoothen contour.
# window_size = int(round(min(img.shape[0], img.shape[1]) * 0.05)) # Consider each window to be 5% of image dimensions
# x = savgol_filter(contour[:,0,0], window_size * 2 + 1, 3)
# y = savgol_filter(contour[:,0,1], window_size * 2 + 1, 3)

# approx = np.empty((x.size, 1, 2))
# approx[:,0,0] = x
# approx[:,0,1] = y
# approx = approx.astype(int)
# contour = approx





# plt.imshow(edgeImg)

# ---------------------------------------------- #



# stop

# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

# fgbg = cv2.createBackgroundSubtractorGMG()
# fgbg = cv2.createBackgroundSubtractorMOG2()#varThreshold=50, detectShadows=False)
# fgbg = cv2.createBackgroundSubtractorKNN()

# fgmask = fgbg.apply(img)
# fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

# img = cv2.GaussianBlur(img,(1,1),0)
# sobelX = cv2.Sobel(img, cv2.CV_16S)#, 1, 0)
# sobelY = cv2.Sobel(img, cv2.CV_16S)#, 0, 1)
# sobel = np.hypot(sobelX, sobelY)

# plt.imshow(img)
# plt.imshow(fgmask)
# plt.show()

# cv2.imshow('img',fgmask)
# ---------------------------------------------- #

# img = cv2.Canny(img1,203,204)

# ---------------------------------------------- #

# img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# img = cv2.GaussianBlur(img,(3,3),0)
# bgr = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = cv2.medianBlur(img,5)

# img = cv2.GaussianBlur(img,(3,3),0)


# stop
# img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

# stop

# define range of blue color in HSV
# lower_blue = np.array([0,0,0])
# upper_blue = np.array([30,255,255])

# lower_blue = np.array([110,50,50])
# upper_blue = np.array([130,255,255])

# Threshold the HSV image to get only blue colors
# mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Bitwise-AND mask and original image
# res = cv2.bitwise_and(,frame, mask= mask)
# cv2.imshow('hsv',hsv)
# cv2.imshow('mask',mask)
# cv2.imshow('res',res)

# ---------------------------------------------- #
# stop


# circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,5,param1=10,param2=10,minRadius=8,maxRadius=10)
# circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2, 5)

# circles = np.uint16(np.around(circles))

# for i in circles[0,:]:

# 	# draw the outer circle
# 	cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)

# 	# draw the center of the circle
# 	cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)


# ---------------------------------------------- #

# cv2.imshow('detected circles',img)
# plt.imshow(img)

# cv2.waitKey(0)

# cv2.destroyAllWindows()

# plt.show()