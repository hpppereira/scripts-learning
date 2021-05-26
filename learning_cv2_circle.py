import os
import numpy as np
import cv2

cv2.destroyAllWindows()

# ---------------------------------------------- #

#BGR cor da bolinha
b, g, r = 255, 189, 64

# nframei = 100
# nframef = 1000

pathname = 'fig/frames/'

listfiles = np.sort(os.listdir(pathname))

for filename in listfiles[50::10]:

	print (filename)
	
	# imagem original
	imgo = cv2.imread(pathname + filename)

	# imagem sem o fundo
	img = np.copy(imgo)

	# ---------------------------------------------- #
	# limite para achar a bola
	lim = 40

	# RGB das bolas
	r, g, b = 255, 189, 64

	# RGB para  pintar as bolas
	r1, g1,  b1 = 255,255,255

	# ---------------------------------------------- #
	#remove background

	l, c, p = img.shape

	for cc in range(c):

		for ll in range(l):

			if (img[ll, cc] > (b-lim, g-lim, r-lim)).all() and (img[ll, cc] < (b+lim, g+lim, r+lim)).all():

				img[ll, cc] = np.array([b1, g1, r1])

			else:

				img[ll, cc] = np.array([0, 0, 0]) #preto

	# img = img[:,:,0]
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,5,param1=10,param2=5,minRadius=8,maxRadius=10)
	# circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2, 5)

	# circles = np.uint16(np.around(circles))

	#posicoes de cada bola

	for i in circles[0,:]:

		# draw the outer circle
		cv2.circle(imgo,(i[0],i[1]),i[2],(0,255,0),2)

		# draw the center of the circle
		cv2.circle(imgo,(i[0],i[1]),2,(0,0,255),3)


	# ---------------------------------------------- #

	# cv2.imshow('detected circles',img1)
	cv2.imwrite('fig/' + filename + '_detected circles',imgo)

	# cv2.imshow('img',img)
	# img = img.