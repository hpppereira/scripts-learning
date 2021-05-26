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

plt.close('all')
cv2.destroyAllWindows()

# ------------------------------------------------------------------------------------------------------- #
# pathname and filenames

# pathname of frames
pathname = os.environ['HOME'] + '/Dropbox/Random_Drift/data/DERIVA_RANDOMICA/VIDEO/CAM1/T100/'

# image to be used
filename = 'T100_010100_CAM1.avi'

# ------------------------------------------------------------------------------------------------------- #
# playing video from a file

cap = cv2.VideoCapture(pathname + filename)

while(cap.isOpened()):
    
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()