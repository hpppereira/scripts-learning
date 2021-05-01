"""
Rastreia as bolas do laboceano

- retira o fundo com threshold
- deixa bolas preta e fundo branco
- acha contornos (bolas)
- pinta bolas com valores de 10 pixels de diferenca (isso vai ser o identificador das bolas)
- subtraio pixels posteior (ja em preto e branco) e subtrai do pixel anteior com as bolas colorias
- faz a mesma coisa para todos os pixels 

# Referencias
https://docs.opencv.org/3.1.0/d3/db4/tutorial_py_watershed.html
http://cmm.ensmp.fr/~beucher/wtshed.html
https://docs.opencv.org/trunk/db/d8e/tutorial_threshold.html
"""


import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

plt.close('all')
cv2.destroyAllWindows()

# ---------------------------------------------------------------------- #

pathname = os.environ['HOME'] + \
           '/GoogleDrive/wavescatter/data/DERIVA_RANDOMICA/VIDEO/CAM1/T100/'

filename = 'T100_010100_CAM1.avi'

# ---------------------------------------------------------------------- #

# le o video
cap = cv2.VideoCapture(pathname+filename)

# ---------------------------------------------------------------------- #

# escolhe o frame inicial
cap.set(cv2.CAP_PROP_POS_FRAMES, 1000)

# divide por 2 a resolucao da camera
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# take first frame of the video
ret,frame1 = cap.read()  
ret,frame2 = cap.read()  

# leitura de 2 frames consecutivos
img1 = np.copy(frame1)
img2 = np.copy(frame2)


# ---------------------------------------------------------------------- #
# Image Segmentation with Watershed Algorithm

# retira o relogio
# img = img2 - img1

img = img1[:-130,:]

# escala de cinza
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# threshold com otsu
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)

# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

# Finding unknown region
# sure_fg = np.uint8(sure_fg)
# unknown = cv2.subtract(sure_bg,sure_fg)
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

 # Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)
# ret, markers = cv2.connectedComponents(sure_bg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers+10

# Now, mark the region of unknown with zero
markers[unknown==255] = 0

markers = cv2.watershed(img,markers)

img[markers == -1] = [255,0,0]




# ---------------------------------------------------------------------- #
# plotagem

plt.figure()
plt.imshow(markers)
plt.title('markers')

plt.figure()
plt.imshow(img)
plt.title('img')

# plt.figure()
# plt.imshow(thresh)
# plt.title('thresh')

# plt.figure()
# plt.imshow(opening)
# plt.title('opening')

# plt.figure()
# plt.imshow(sure_bg)
# plt.title('sure_bg')

# plt.figure()
# plt.imshow(dist_transform)
# plt.title('dist_transform')

# plt.figure()
# plt.imshow(sure_fg)
# plt.title('sure_fg')

# plt.figure()
# plt.imshow(markers)
# plt.title('thresh')

# plt.show()


# cv2.namedWindow('image',cv2.WINDOW_NORMAL)
# cv2.resizeWindow('image', width/2, height/2)
# cv2.imshow('image',markers)

# cv2.namedWindow('image1',cv2.WINDOW_NORMAL)
# cv2.resizeWindow('image1', width/2, height/2)
# cv2.imshow('image1',img)


plt.show()











# # informacoes do video
# length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps    = cap.get(cv2.CAP_PROP_FPS)


# stop

# # setup initial location of window
# r,h,c,w = 250,90,400,125 # simply hardcoded the values
# track_window = (c,r,w,h)

# # set up the ROI for tracking
# roi = frame[r:r+h, c:c+w]
# hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
# roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
# cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
# term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

# while(1):
#     ret ,frame = cap.read()
#     if ret == True:
#         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#         dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
#         # apply meanshift to get the new location
#         ret, track_window = cv2.meanShift(dst, track_window, term_crit)
#         # Draw it on image
#         x,y,w,h = track_window
#         img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
#         cv2.imshow('img2',img2)
#         k = cv2.waitKey(60) & 0xff
#         if k == 27:
#             break
#         else:
#             cv2.imwrite(chr(k)+".jpg",img2)
#     else:
#         break
# cv2.destroyAllWindows()
# cap.release()