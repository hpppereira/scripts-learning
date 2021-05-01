'''
Learning CV2 with images
Henrique Pereira
2018/01/19
'''

# ------------------------------------------------------------------------------------------------------- #
# import libraries

import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

# ------------------------------------------------------------------------------------------------------- #
# close open figures

# plt.close('all')
# cv2.destroyAllWindows()

# ------------------------------------------------------------------------------------------------------- #
# pathname and filenames

# pathname of frames
pathname = pathname = os.environ['HOME'] + '/Dropbox/Random_Drift/code/fig/frames/'

# list of frames
framelist = np.sort(os.listdir(pathname))

# image to be used
filename = framelist[50]

# ------------------------------------------------------------------------------------------------------- #
# loading image

# cv2.IMREAD_COLOR : Loads a color image. Any transparency of image will be neglected. It is the default
# flag.
# cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode
# cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel
# Note: Instead of these three flags, you can simply pass integers 1, 0 or -1 respectively.

# img = cv2.imread(pathname+filename, 1)

# ------------------------------------------------------------------------------------------------------- #
# show image

# cv2.waitKey() is a keyboard binding function. Its argument is the time in milliseconds. The function waits for
# specified milliseconds for any keyboard event. If you press any key in that time, the program continues. If 0 is passed,
# it waits indefinitely for a key stroke. It can also be set to detect specific key strokes like, if key a is pressed etc which
# we will discuss below.

# cv2.destroyAllWindows() simply destroys all the windows we created. If you want to destroy any specific window,
# use the function cv2.destroyWindow() where you pass the exact window name as the argument

# Note: There is a special case where you can already create a window and load image to it later. In that case, you can
# specify whether window is resizable or not. It is done with the function cv2.namedWindow(). By default, the flag is
# cv2.WINDOW_AUTOSIZE. But if you specify flag to be cv2.WINDOW_NORMAL, you can resize window. It will be
# helpful when image is too large in dimension and adding track bar to windows.

# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# ------------------------------------------------------------------------------------------------------- #
# write an image

# cv2.imwrite('teste_opencv1.png',img)

# ------------------------------------------------------------------------------------------------------- #
# plot with matplotlib

# plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
# plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis
# plt.show()

# ------------------------------------------------------------------------------------------------------- #
# close all figures

# cv2.destroyAllWindows()
# plt.close('all')

# ------------------------------------------------------------------------------------------------------- #
# converting to gray scale

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ------------------------------------------------------------------------------------------------------- #
# remove noise, make filters

# remove noise
# img = cv2.GaussianBlur(gray,(3,3),0)

# # convolute with proper kernels
# laplacian = cv2.Laplacian(img,cv2.CV_64F)
# sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)  # x
# sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)  # y

# plt.figure()

# plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
# plt.title('Original'), plt.xticks([]), plt.yticks([])
# plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
# plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
# plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
# plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
# plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
# plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

# plt.show()

# plt.close('all')

####################################################
# plot edges

# img = cv2.imread(pathname+filename,0)
# edges = cv2.Canny(img,100,200)

# plt.figure()

# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

# plt.show()


# ------------------------------------------------------------------------------------------------------- #
# Basic operations on images

# Access pixel values and modify them
# Access image properties
# Setting Region of Image (ROI)
# Splitting and Merging images

img = cv2.imread('messigray2.png')

# Accessing and Modifying pixel values

px = img[100,100]

print ('valor do pixel (b, r, g): %s' %px)

# acessing only the blue pixel
blue = img[100,100,0]

print ('valor do pixel azul: %s' %blue)

# You can modify the pixel values the same way

img[100,100] = [255,255,255]

print ('valor do pixel modificado: %s' %img[100,100])

# Numpy array methods, array.item() and array.itemset() is considered to
# be better. But it always returns a scalar. So if you want to access all B,G,R values, you need to call array.item()
# separately for all.

# acessing the RED value
print ('valor do pixel RED com funcao item: %s' %img.item(10, 10, 2))

# modifying the RED value

img.itemset((10,10,2),100)
print ('valor do pixel modificado: %s' %img.item(10,10,2))

# acessing image properties

print ('image shape: %s' %str(img.shape))

# total number of pixels

print ('total number of pixels: %s' %img.size)

# image datatype

print ('image datatype: %s' %img.dtype)

# Note: img.dtype is very important while debugging because a large number of errors in OpenCV-Python code is
# caused by invalid datatype.

# ------------------------------------------------------------------------------------------------------- #
# Image ROI

# Sometimes, you will have to play with certain region of images. For eye detection in images, first perform face
# detection over the image until the face is found, then search within the face region for eyes. This approach improves
# accuracy (because eyes are always on faces :D ) and performance (because we search for a small area).
# ROI is again obtained using Numpy indexing. Here I am selecting the ball and copying it to another region in the
# image:

ball = img[280:340, 330:390]
img[273:333, 100:160] = ball


# ------------------------------------------------------------------------------------------------------- #
# Splitting and Merging Image Channels

# The B,G,R channels of an image can be split into their individual planes when needed. Then, the individual channels
# can be merged back together to form a BGR image again. This can be performed by:

b,g,r = cv2.split(img)
img = cv2.merge((b,g,r))


# ------------------------------------------------------------------------------------------------------- #
# Arithmetic Operations on Images

# There is a difference between OpenCV addition and Numpy addition. OpenCV addition is a saturated operation
# while Numpy addition is a modulo operation.


x = np.uint8([250])
y = np.uint8([10])

print cv2.add(x,y) # 250+10 = 260 => 255

# changing color-space

flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
# print flags



