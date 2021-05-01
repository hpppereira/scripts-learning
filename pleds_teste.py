'''
PLEDS (Parente's Diagram)

Programa para plotagem da evolucao do espectro direcional
Plotting the Evolution of Directional Spectrum

Carlos Eduardo Parente
Henrique P P Pereira
Izabel C M Nogueira
Ricardo M Campos

Ultima modificacao: 18/07/2015
'''

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle

plt.close('all')

#carrega os arquivos da saida da DAAT (10x248)
pathname = os.environ['HOME'] + '/Dropbox/daatpleds/pydaat/dados/'

energ1 = np.loadtxt(pathname + 'energ1.txt')
espe1 = np.loadtxt(pathname + 'espe1.txt')
dire1 = np.loadtxt(pathname + 'dire1.txt')


ad = np.array(['Jan','Fev','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])


fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)

a = 0
plt.plot(a,'w')
plt.axis([-0.1,20.2,0,300])

v6 = np.hanning(15)
v61 = np.hanning(11)

ad1 = np.array([31,29,31,30,31,30,31,31,30,31,30,31]) #???

plt.axis('off')

col = np.array([0.7,0.7,0.7])

ax.set_position([0,0,1,1]) # set a new position

# #codigo de cores para faixas de periodos
# x = np.array([0.5,3,3,0.5]) + 0.5
# y = np.array([1,1,12,12]) - 3.5


ax.add_patch(Rectangle((0,3), 3.3, 8,alpha=0.8,facecolor='r'))
ax.text(0.5,4.5, "21.3-16.2 s")

ax.add_patch(Rectangle((3.3, 3), 3.3, 8,alpha=0.8,facecolor='b'))
ax.text(3.8,4.5, "15.0-12.8 s")

ax.add_patch(Rectangle((6.6, 3), 3.3, 8,alpha=0.8,facecolor='y'))
ax.text(7.1,4.5, "12.0-08.0 s")

ax.add_patch(Rectangle((9.9, 3), 3.3, 8,alpha=0.8,facecolor='g'))
ax.text(10.4,4.5, "07.0-03.0 s")

ax.add_patch(Rectangle((13.2, 3), 3.3, 8,alpha=0.8,facecolor='w'))
ax.text(13.5,4.5, "5 div=10 m/s")

ax.add_patch(Rectangle((16.5, 3), 3.3, 8,alpha=0.8,facecolor='w'))
ax.text(16.8,4.5, "5 div=0.1 m2")

plt.draw()

#linhas verticais
y = np.array([20,283])
for i in range(1,20):
	x = [i,i]
	pl.plot(x,y,'k',alpha=0.2)

#linhas horizontais (dias)
x = np.array([0.9,19.1])
dia = 0
for i in range(20,260+8,8):
	dia += 1
	y = [i,i]
	pl.plot(x,y,'k',alpha=0.3)
	pl.text(0.3,y[0],str(dia))
	pl.text(19.3,y[0],str(dia))

#linhas horizontais (3 horas)
x = np.array([1,19])
for i in range(20,284,2):
	y = [i,i]
	pl.plot(x,y,'k',alpha=0.2)

pl.text(1.13,286,'DIRECTIONAL WAVE SPECTRUM - Rio Grande/RS 2013/05 - ADCP - Vale')


#plotagem do espectro direcional a cada dia por faixa de periodos
#plota de cima para baixo (de 31 para 1)

#eixo horizontal de direcao
a = np.arange(310,720,20)
a[pl.find(a>360)] = a[pl.find(a>360)] - 360

for i in range(1,19):
	pl.text(i+0.15,15,str(a[i-1]),color='red',fontsize=11)


ld = np.array(['NW','N ','NE','E ','SE','S ','SW','W ','SW','W '])

k = 1.55;
d = np.arange(1.75,13,2.25)

for i in range(8):
	pl.text(k,20.8,ld[i],weight='bold')
	k=k+2.25;
 
pl.text(1.15,80,'days in a month',rotation=90)

#w=[[1;6] [2;7] [3;8] [4;9]];
#bb = np.array([0.3]*10) #utilizado para montar o triangulo??

for t in range(dire1.shape[1]-1,-1,-1):

	#define os vetores de direcao e espectro (energia)
	s1 = dire1[:,t]
	s2 = espe1[:,t]

	#varia as 4 faixas
	cor = -1
	for i in [0,2,4,6]:

		# arq5 = arq2[i,:] #cor - fazer com 'r', 'b', ... ??

		cor += 1
		arq5 = ['r','b','y','g']

		s11 = s1[i] #valor da direcao no tempo i
		s12 = s2[i] #valor do espectro no tempo i

		b1 = s11 / 20 #direcao (correcao para o eixo??)
		b2 = s12 / 2  #espectro

		if b1 > 0:
			b1 = b1 + 3 #ajuste da direcao

			if b1 > 18:
				b1 = b1 - 18

			b1 = b1 + 1 #o zero comecaem 111 (ou 11??)
			n1 = t + 9 + 10 #shift na escala vertical

			#monta um triangulo (x)
			v7 = np.linspace(b1-0.3,b1+0.3,len(v61))
			x = np.array(list(v7) + list(np.flipud(v7)))

			#cria un hanning
			y = np.array( list(n1+v61*b2) + list(n1*np.ones(len(v61))))

			# ??
			z1 = 1
			z2 = 1

			if b2 * b1 > 0:

				pl.fill(x,y,arq5[cor])

	# return x, y

pl.savefig('fig/pledspy_teste.png')

plt.show()