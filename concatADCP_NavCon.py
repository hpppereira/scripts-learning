'''
Processamento dos dados do ADCP da BMOBR03
que foram disponibilizados pela NavCon

Henrique P P Pereira
2016/02/12
'''

import os
import numpy as np
import matplotlib.pylab as pl
import pandas as pd
import espec

pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/Sistemas-BMOP/Dados/BMOBR03/NavCon/ADCP/'

lista = np.sort(os.listdir(pathname))

dd = pd.read_table(pathname + lista[0],skiprows=6,
									   sep=',',
									   index_col=[1],
									   parse_dates=True,
									   header=None,
									   na_values='--')
									   #prefix='X')

#retira a ultima coluna que esta com nan
dd = dd.ix[:,:dd.shape[1]-1]

#foi retirada o header de hora que estava no dado
dd.columns = ['Horario','Contador','Heading','Pitch','Roll','Temperatura','SoS','BIT',
			  'Bin1','Dir1','Mag1','EW1','NS1','Vert1','Err1','Echo11','Echo21','Echo31','Echo41',
			  'Bin2','Dir2','Mag2','EW2','NS2','Vert2','Err2','Echo12','Echo22','Echo32','Echo42',
			  'Bin3','Dir3','Mag3','EW3','NS3','Vert3','Err3','Echo13','Echo23','Echo33','Echo43',
			  'Bin4','Dir4','Mag4','EW4','NS4','Vert4','Err4','Echo14','Echo24','Echo34','Echo44',
			  'Bin5','Dir5','Mag5','EW5','NS5','Vert5','Err5','Echo15','Echo25','Echo35','Echo45',
			  'Bin6','Dir6','Mag6','EW6','NS6','Vert6','Err6','Echo16','Echo26','Echo36','Echo46',
			  'Bin7','Dir7','Mag7','EW7','NS7','Vert7','Err7','Echo17','Echo27','Echo37','Echo47',
			  'Bin8','Dir8','Mag8','EW8','NS8','Vert8','Err8','Echo18','Echo28','Echo38','Echo48',
			  'Bin9','Dir9','Mag9','EW9','NS9','Vert9','Err9','Echo19','Echo29','Echo39','Echo49',
			  'Bin10','Dir10','Mag10','EW10','NS10','Vert10','Err10','Echo110','Echo210','Echo310','Echo410']

#remove coluna horario
#dd = dd.drop('Horario', axis=1)

#coloca nome no indice
dd.index.name = 'date'


#vetor de profundidades
prof = np.flipud(np.arange(-45,-45-32*10,-32))

#cria matriz de velocidade e direcao (para grafico de contorno)
mag = np.flipud(np.array(dd[['Mag1','Mag2','Mag3','Mag4','Mag5','Mag6','Mag7','Mag8','Mag9','Mag10']].T)) / 1000.0
dire = np.flipud(np.array(dd[['Dir1','Dir2','Dir3','Dir4','Dir5','Dir6','Dir7','Dir8','Dir9','Dir10']].T))
u = np.flipud(np.array(dd[['EW1','EW2','EW3','EW4','EW5','EW6','EW7','EW8','EW9','EW10']].T)) / 1000.0
v = np.flipud(np.array(dd[['NS1','NS2','NS3','NS4','NS5','NS6','NS7','NS8','NS9','NS10']].T)) / 1000.0


#calculo do espectro
aa = espec.espec1(dd.Mag4[20:],len(dd)/2,1./24)





fig = pl.figure(figsize=(14,9),facecolor='w')
ax = fig.add_subplot(111)
con = ax.contourf(mag,np.arange(0,1,0.001),color='k')
pl.colorbar(con,label=r'ms$^{-1}$')
qwind = ax.quiver(u, v, units='xy', scale=0.05, headwidth=0, pivot='tail', width=0.25, linewidths=(0.001,), edgecolors='k', color='k', alpha=1)
pl.xticks(range(0,len(dd),100),dd[0:-1:100].index,rotation=5)
pl.yticks(range(0,10),prof)
pl.ylabel('Depth (m)')
pl.axis('tight')
pl.ylim(-1,10)
pl.quiverkey(qwind,230,9.3,1,r'1 ms$^{-1}$',coordinates='data')


fig = pl.figure(figsize=(14,9),facecolor='w')
ax1 = fig.add_subplot(211)
con1 = ax1.contourf(dd.index,prof,mag,np.arange(0,1,0.001))
pl.colorbar(con1)
pl.xticks(rotation=10)
ax2 = fig.add_subplot(212)
con2 = ax2.contourf(dd.index,prof,dire,np.arange(0,360,1))
pl.xticks(rotation=10)
pl.colorbar(con2)


pl.show()