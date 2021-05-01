'''
Principal program to run DAAT/PLEDS
'''

import os
import matplotlib.pylab as pl
from matplotlib import reload
import numpy as np
import daatpleds
reload(daatpleds)

pathname = os.environ['HOME'] + '/Documents/database/historic/buoys/pnboia/triaxys/preproc/SAN/HNE/'

local = 'santos'

#caminho dos dados de vento

pathnamewind = os.environ['HOME'] + '/Documents/database/hindcast/CFSR/txt/'

time = np.loadtxt(pathnamewind + 'time_SAN_2013.txt')
u = np.loadtxt(pathnamewind + 'uCFSR_SAN_2013.txt')
v = np.loadtxt(pathnamewind + 'vCFSR_SAN_2013.txt')

#retira dias repetidos
[time1,ia] = np.unique(time, return_index=True);
time1 = time1[:-1]
u = u[ia[:-1]];
v = v[ia[:-1]];

ws1 = np.sqrt(u**2 + v**2);
wd1 = np.arctan2(v,u) * 180 / np.pi; #vento de onde vem
wd1 = 270 - wd1; #de onde vai para onde vem
wd1[pl.find(wd1<0)] = wd1[pl.find(wd1<0)] + 360;
wd1[pl.find(wd1>360)] = wd1[pl.find(wd1>360)] - 360;

# lista = np.array(lista_hne(pathname))

li = np.sort(os.listdir(pathname))

#li = li[np.where(li == '201301010000.HNE')[0][0]:np.where(li == '201301312300.HNE')[0][0]+1]

dmag = -17
h = 200 #profundidade 
nfft = 82 #numero de dados para a fft (p/ nlin=1312: 32gl;nfft=82, 16gl;nfft=164, 8gl;nfft=328)
fs = 1.28 #freq de amostragem

#varia os meses
for m in np.arange(1,13):
	lm = [] #lista mensal da onda
	time = [] #lista mensal do vento
	ws = [] #lista mensal do vento
	wd = [] #lista mensal do vento

	#separa arquivos de onda
	for l in li:
		if l.startswith('2013' + str(m).zfill(2)):
			lm.append(l)

	#separa arquivos de vento
	for cont in np.arange(len(time1)):
		if time1.astype(str)[cont].startswith('2013' + str(m).zfill(2)):
			time.append(time1.astype(str)[cont])
			ws.append(ws1[cont])
			wd.append(wd1[cont])

	#roda a daat
	espe, dire, energ = daatpleds.daathne(local, pathname, dmag, lm, h, nfft, fs)

	#roda a pleds
	daatpleds.pleds(espe[:,::3]*2, dire[:,::3], ws[::3], wd[::3], figname='SAN', date=lm[-1][:6])

	pl.close('all')