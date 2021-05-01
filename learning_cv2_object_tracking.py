

import cv2
import numpy as np
import os

# cap = cv2.VideoCapture(0)
# pathname of frames
pathname = os.environ['HOME'] + '/Dropbox/Random_Drift/data/DERIVA_RANDOMICA/VIDEO/CAM1/T100/'

# image to be used
filename = 'T100_010100_CAM1.avi'

# ------------------------------------------------------------------------------------------------------- #
# playing video from a file

cap = cv2.VideoCapture(pathname + filename)

while(1):
	# Take each frame
	_, frame = cap.read()

	# Convert BGR to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# define range of blue color in HSV
	lower_blue = np.array([0,0,0])
	upper_blue = np.array([30,255,255])

	# lower_blue = np.array([110,50,50])
	# upper_blue = np.array([130,255,255])

	# Threshold the HSV image to get only blue colors
	mask = cv2.inRange(hsv, lower_blue, upper_blue)

	# Bitwise-AND mask and original image
	res = cv2.bitwise_and(frame,frame, mask= mask)
	cv2.imshow('frame',frame)
	cv2.imshow('mask',mask)
	cv2.imshow('res',res)

	# ESC para fechar figura
	k = cv2.waitKey(5) & 0xFF

	if k == 27:
		break

cv2.destroyAllWindows()