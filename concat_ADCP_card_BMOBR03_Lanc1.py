'''
Concatenate ADCP's memory card data from
BMOBR03_CF1, Launch 1

ADCP 75 kHz
'''

import pandas as pd
import numpy as np
import pylab as pl
import os
import datetime as datetime

pl.close('all')

#choose the data
#pathname = os.environ['HOME'] + '/Dropbox/projetos/BMOP/Sistemas-BMOP/Processamento/dados/BMOBR04_CF2/Lanc1/ADCP/cartao/txt/ADCP_20150510.txt'
#dd = dd['2015-03-04 17':] #periodo de dados bons

pathname = os.environ['HOME'] + '/Dropbox/projetos/BMOP/Sistemas-BMOP/Processamento/dados/BMOBR03_CF1/Lanc1/ADCP/txt/'
#dd = dd['2015-03-04 17':] #periodo de dados bons

lista = np.sort(os.listdir(pathname))

filename = 'DPL3_009.txt'
#figname1 = 'fig/BMOBR03_CF2_Lanc1_ADCP_Status.png'
#figname2 = 'fig/BMOBR03_CF2_Lanc1_ADCP_MagDir.png'

dateparse = lambda x: pd.datetime.strptime(x, '%y %m %d %H %M %S')

columns = ['Ens','YR','MO','DA','HH','MM','SS','NAN','NAN','Pit','Rol','Hea','Tem','Dep','Ori','BIT','Bat',
		   'Eas1','Eas2','Eas3','Eas4','Eas5','Eas6','Eas7','Eas8','Eas9','Eas10',
		   'Nor1','Nor2','Nor3','Nor4','Nor5','Nor6','Nor7','Nor8','Nor9','Nor10',
		   'Ver1','Ver2','Ver3','Ver4','Ver5','Ver6','Ver7','Ver8','Ver9','Ver10',
		   'Err1','Err2','Err3','Err4','Err5','Err6','Err7','Err8','Err9','Err10',
		   'Mag1','Mag2','Mag3','Mag4','Mag5','Mag6','Mag7','Mag8','Mag9','Mag10',
		   'Dir1','Dir2','Dir3','Dir4','Dir5','Dir6','Dir7','Dir8','Dir9','Dir10']

dd = pd.DataFrame()

for filename in lista:

	aux_dd = pd.read_table(pathname + filename, skiprows=15, parse_dates=[['YR','MO','DA','HH','MM','SS']],
		date_parser=dateparse, index_col='YR_MO_DA_HH_MM_SS',
		names=columns)

	dd = pd.concat((dd, aux_dd))


#magnitude matrix (m/s)
mag  = np.flipud(dd[['Mag1','Mag2','Mag3','Mag4','Mag5','Mag6','Mag7','Mag8','Mag9','Mag10']].values.T) / 1000
dire = np.flipud(dd[['Dir1','Dir2','Dir3','Dir4','Dir5','Dir6','Dir7','Dir8','Dir9','Dir10']].values.T) / 1000
u    = np.flipud(dd[['Eas1','Eas2','Eas3','Eas4','Eas5','Eas6','Eas7','Eas8','Eas9','Eas10']].values.T) / 1000
v    = np.flipud(dd[['Nor1','Nor2','Nor3','Nor4','Nor5','Nor6','Nor7','Nor8','Nor9','Nor10']].values.T) / 1000

fig = pl.figure(figsize=(15,10), facecolor='w')
ax1 = fig.add_subplot(311)
ax1.plot(dd.index, dd.Bat, 'b-o')
ax1.set_ylabel('Bat (cnt)')
ax1.grid()
ax2 = fig.add_subplot(312)
ax2.plot(dd.index, dd.Pit, 'b')
ax2.plot(dd.index, dd.Rol, 'r')
ax2.set_ylim(-10, 10)
ax2.grid()
ax22 = ax2.twinx()
ax22.plot(dd.index, dd.Hea, 'g')
ax22.set_yticks(np.arange(0, 360+45, 45))
ax22.set_ylim(0,360)
ax2.set_ylabel('Pitch, Roll e Head')
ax2.legend(['Pit','Rol'], ncol=2, loc=2)
ax22.legend(['Hea'], ncol=1, loc=1)
ax3 = fig.add_subplot(313)
ax3.plot(dd.index, dd.Tem, 'b')
ax3.set_ylabel('Temp. (graus)')
ax3.grid()
#pl.savefig(figname1, bbox_inches='tight')

fig = pl.figure(figsize=(12,7),facecolor='w')
ax = fig.add_subplot(111)
con = ax.contourf(mag,np.arange(0,1,0.001),color='k')
pl.colorbar(con,label=r'ms$^{-1}$')
qwind = ax.quiver(u, v, units='xy', scale=0.025, headwidth=0, pivot='tail', width=0.25, linewidths=(0.001,), edgecolors='k', color='k', alpha=1)
pl.xticks(np.linspace(0,len(dd),10),dd.index[np.linspace(0,len(dd)-1,10).astype(int)].strftime('%d/%m/%Y'), rotation=10)
pl.yticks([0,1,2,3,4,5,6,7,8,9],np.flipud(np.arange(40,40+32*10,32))*-1)
pl.ylabel('Intensidade e Direcao das Correntes (m/s e graus)')
pl.axis('tight')
pl.ylim(-0.2,9.2)
#pl.quiverkey(qwind,100,2.15,1,''.ljust(5) + r'1 ms$^{-1}$',coordinates='data')
#pl.savefig(figname2, bbox_inches='tight')





pl.show()