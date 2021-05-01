#! /usr/bin/python
# -*- coding: utf-8 -*-


import os
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle



def pledscur(espe1,dire1,ws1,wd1):

	ad = np.array(['Jan','Fev','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
	
	
	fig = plt.figure(figsize=(8,10),facecolor='w')
	ax = fig.add_subplot(111)
	ax.set_position([0,0,1,1]) # set a new position
	
	ax.plot( 0, 'w')
	
	xaxis = [-0.1,20.2]
	yaxis = [0, 300]
	
	ax.set_xlim(xaxis)
	ax.set_ylim(yaxis)
	
	#ax.axis([-0.1,20.2,0,300])
	
	v6 = np.hanning(15)
	v61 = np.hanning(11)
	
	ad1 = np.array([31,29,31,30,31,30,31,31,30,31,30,31]) #???
	
	plt.axis('off')
	
	# arq2 = np.array(([ [1,0.00,0],
	# 				   [1,0.00,0],
	# 				   [1,0.55,0],
	# 				   [1,0.55,0],
	# 				   [1,1.00,0],
	# 				   [1,1.00,0],
	# 				   [0,1.00,0],
	# 				   [0,1.00,0] ]))
	
	#col = np.array([0.7,0.7,0.7])
	
	
	# #codigo de cores para faixas de periodos
	# x = np.array([0.5,3,3,0.5]) + 0.5
	# y = np.array([1,1,12,12]) - 3.5
	
	
	ax.add_patch(Rectangle((0,0), 3.3, 8,alpha=0.8,facecolor='#2c7fb8'))
	ax.text(0.5,1.5, "Prof: 5 m")
	
	ax.add_patch(Rectangle((3.3, 0), 3.3, 8,alpha=0.8,facecolor='#41b6c4'))
	ax.text(3.8,1.5, "Prof: 16 m")
	
	ax.add_patch(Rectangle((6.6, 0), 3.3, 8,alpha=0.8,facecolor='#a1dab4'))
	ax.text(7.1,1.5, "Prof 36 m")
	
	ax.add_patch(Rectangle((9.9, 0), 3.3, 8,alpha=0.8,facecolor='#ffffcc'))
	ax.text(10.4,1.5, "Prof: 46 m")
	
	ax.add_patch(Rectangle((13.2, 0), 3.3, 8,alpha=0.8,facecolor='w'))
	ax.text(13.5,1.5, "5 div=10 m/s")
	
	ax.add_patch(Rectangle((16.5, 0), 3.3, 8,alpha=0.8,facecolor='w'))
	ax.text(16.8,1.5, "5 div=0.1 m2")
	
	pl.draw()
	
	#linhas verticais
	y = np.array([20,283])
	for i in range(1,20):
		x = [i,i]
		ax.plot(x,y,'k',alpha=0.2)
	
	#linhas horizontais (dias)
	x = np.array([0.9,19.1])
	dia = 0
	for i in range(20,260+8,8):
		dia += 1
		y = [i,i]
		ax.plot(x,y,'k',alpha=0.3)
		ax.text(0.3,y[0],str(dia))
		ax.text(19.3,y[0],str(dia))
	
	#linhas horizontais (3 horas)
	x = np.array([1,19])
	for i in range(20,284,2):
		y = [i,i]
		ax.plot(x,y,'k',alpha=0.2)
	
	# ax.text(1.13,286,'DIAGRAMA DE PARENTE - CORRENTES')
	
	
	#plotagem do espectro direcional a cada dia por faixa de periodos
	#plota de cima para baixo (de 31 para 1)
	
	#eixo horizontal de direcao
	# a = np.arange(310,720,20)
	# a[pl.find(a>360)] = a[pl.find(a>360)] - 360
	
	a = np.arange(350,760,20)
	a[pl.find(a>360)] = a[pl.find(a>360)] - 360
	
	for i in range(1,19):
		ax.text( i+0.15,15, str(a[i-1]), color='red', fontsize=11)
		if i == 18:
			ax.text( i+0.92,15, '[graus]', color='red', fontsize=8)
			ax.text( i+0.9,10, u'[direção]', color='black', fontsize=8)
	
	
	ld = np.array(['N ','NE','E ','SE','S ','SW','W ','NW', 'W ', 'NW'])
	
	k = 1.55;
	d = np.arange(1.75,13,2.25)
	
	for i in range(8):
		ax.text( k,10, ld[i], weight='bold')
		k = k+2.25
	
	
	ax.text( 1.15, 80, u'[dd/%s/%s]'%(ad[0],2015), fontsize=14, weight='bold', rotation=90)
	# Xaxis = np.linspace(xaxis[0],xaxis[1],espe1.shape[1])
	# ax.axvspan(0,10 , ymin=4*5, ymax=9*5, color='w') 
	
	
	for t in range(dire1.shape[1]-1,-1,-1):
		#define os vetores de direcao e espectro (energia)
		s1 = dire1[:,t]
		s2 = espe1[:,t]
	
		#varia as 4 faixas
		cor = -1
		for i in [0,2,6,8]:
	
			## Cores das janelas hanning para cada profundidade
			cor += 1
			arq5 = ['#2c7fb8','#41b6c4','#a1dab4','#ffffcc']
	
	
	
			s11 = s1[i] #valor da direcao no tempo i
			s12 = s2[i] #valor do espectro no tempo i
	
			b1 = s11 / 20 # corrigindo direcao ao eixo
			b2 = s12 / 2  # espectro
	
			if b1 > 0:
				b1 = b1 + 1 # ajuste da direcao
	
				if b1 > 18:
					b1 = b1 - 18
	
				b1 = b1 + 1     # o zero comecaem 111 (ou 11??)
				n1 = t + 9 + 10 # shift na escala vertical
	
				#monta um triangulo (x)
				v7 = np.linspace( b1-0.3, b1+0.3, len(v61))
				x = np.array( list(v7) + list( np.flipud(v7) ) )
	
				#cria un hanning
				y = np.array( list(n1+v61*b2) + list( n1*np.ones(len(v61)) ) )
	
				# ??
				z1 = 1
				z2 = 1
	
				if b2 * b1 > 0:
					ax.fill(x,y,arq5[cor])
	
	
	
	#####################################################
	#vento (u e v)
	
	for t in np.arange( len(ws1)-1, -1, -1):
	
		s1 = ws1[t]
		s2 = wd1[t]
	
		if s1 > 0:
	
			s2 = s2/20
			st = t+9+10
			s2 = s2 + 1
	
			if s2 > 18:
	
				s2 = s2 - 18
	
			s2 = s2 + 1
	
	       	#s1 eh a velocidade do vento, colocada na escala certa
	       	#1 divisao=2m/s
	       	#s2 eha direcao em caixas de 18 graus
	       	#st eh a posicao de plotagem ao logo da vertical
	
	       	x = [s2-0.05,s2+0.05,s2+0.05,s2-0.05]
	       	y = [st,st,st+s1,st+s1]
	
	       	if s2 < 2:
	
	       		x = np.nan
	       		y = np.nan
	
	       	if s2 > 18:
	
	       		x = np.nan
	       		y = np.nan
	
	
	       	if s1 > 0:
	       		ax.fill(x,y,'k', lw=0.4, edgecolor='magenta')
	       	elif s1 > 10:
	       		ax.fill(x,y,'y')
	       	elif s1 >20:
	       		ax.fill(x,y,'r')
	
	
	
	ROOTdir = '/Users/Phellipe/Studies/Masters/Project/Thesis/'
	FIGdir  = os.path.join( ROOTdir, 'Text/Chapters/Chapter_3/fig_results/' )
	fig.savefig( FIGdir + 'pleds_jan2015.pdf', dpi=200 )
	
	plt.show()
	