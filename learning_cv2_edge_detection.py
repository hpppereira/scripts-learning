
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

plt.close('all')

pathname = 'fig/frames/'

listfiles = np.sort(os.listdir(pathname))

filename = listfiles[100]

img = cv2.imread(pathname + filename)

edges = cv2.Canny(img,203,204)

#coloca nan nos edges (para plotar junto com a figura real)
# edges[np.where(edges==0)] = np.nan

plt.figure()
plt.subplot(121),
plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),
plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.figure()
plt.imshow(img,cmap = 'gray')
plt.imshow(edges,cmap = 'gray')


plt.show()
