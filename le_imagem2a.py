import numpy as np
import cv2
from matplotlib import pyplot as plt
from pylab import *
 
#cap = cv2.VideoCapture('DSCN0171.MOV')

# load the image
img1 = cv2.imread('teste/flume2_0300.jpg',0)
img2 = cv2.imread('teste/flume2_0301.jpg',0)
img3 = cv2.imread('teste/flume2_0302.jpg',0)
img4 = cv2.imread('teste/flume2_0303.jpg',0)

# converting to gray scale
#gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

imgf = img3
imgi = img4

# remove noise
img_1 = cv2.GaussianBlur(imgi,(5,5),0)
img_2 = cv2.GaussianBlur(imgf,(5,5),0)

# convolute with proper kernels
lap1 = cv2.Laplacian(img_1,cv2.CV_64F)
lap2 = cv2.Laplacian(img_2,cv2.CV_64F)

sobelx1 = cv2.Sobel(img_1,cv2.CV_64F,1,0,ksize=5)  # x
sobely1 = cv2.Sobel(img_1,cv2.CV_64F,0,1,ksize=29)  # y

sobelx2 = cv2.Sobel(img_2,cv2.CV_64F,1,0,ksize=5)  # x
sobely2 = cv2.Sobel(img_2,cv2.CV_64F,0,1,ksize=29)  # y

img55 = sobely2 - sobely1 #lap2 - lap1 #


# Passando para valores entre 0 e 1:
img1 = (img55 + abs(img55.min()))
img11 = img1/img1.max()           

#print img11.min(), img11.max()

# Mudando de formato para uint8
imgdif = (img11* 255).round().astype(np.uint8)

#------------------
(L,C)=shape(imgdif)

img=imgdif
img22=imgdif

fator = 3

for m in range(0,C):
    std1=std(img[:,m])
    med=mean(img[:,m])
    istdU= find( img[:,m] > (med + fator *std1))
    istdD= find( img[:,m] < (med - fator *std1))
    
    img22[istdU,m]=0
    img22[istdD,m]=0
#plt.plot(img[:,10])

plt.imshow(imgdif)
plt.show()


plt.imshow(img55 ,cmap = 'gray')
plt.show()
