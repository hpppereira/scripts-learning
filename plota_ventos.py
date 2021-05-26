''' plota ventos Fev/2013

'''


import os
import numpy as np
import matplotlib.pylab as pl
from datetime import *

import windrose
reload(windrose)
from windrose import WindroseAxes

pl.close('all')

binsvel=np.arange(0,12,1)
# diretorios com os dados extraidos do CFSR
pathname = os.environ['HOME'] + '/Dropbox/ww3vale/hidrodinamico/vento/'
uTU = np.loadtxt(pathname + 'uTU.txt')
vTU = np.loadtxt(pathname + 'vTU.txt')
time = np.loadtxt(pathname + 'time.txt')

data = time.astype(str) #ano mes dia hora
datam = np.array([datetime(int(data[i][0:4]),int(data[i][4:6]),int(data[i][6:8]),int(data[i][8:10])) for i in range(len(data))])

uTU=uTU[0:-1]
#vTU=vTU[0:-1]
vel=np.sqrt(uTU**2 + vTU**2)

dire=np.arctan(vTU/uTU)*(180/np.pi)
#dire=np.ones(len(vel))*270
dire=np.mod(dire,180)


pl.figure()
pl.plot(datam,uTU,'og')
pl.plot(datam,vTU,'bo')

pl.figure()
pl.subplot(211)
pl.plot(datam,vel,'b-o')
pl.ylim([0,12])
pl.ylabel('Intensidade (m/s)')
pl.grid()
pl.subplot(212)
pl.plot(datam,dire,'bo')
pl.ylabel('Direcao (graus)')
pl.grid()



# windrose
def new_axes():
    fig = pl.figure(figsize=(10, 8), dpi=80, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(loc="center right",borderaxespad=-10.8)
    # l.get_frame().set_fill(False) #transparent legend
    pl.setp(l.get_texts(), fontsize=10,weight='bold')
    
  

#windrose like a stacked histogram with normed (displayed in percent) results
ax = new_axes()
ax.bar(dire, vel, normed=True, bins=binsvel, opening=.8, edgecolor='white',nsector=32)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
pl.savefig('windrose', dpi=None, edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=True, bbox_inches=None, pad_inches=0.01) 

# juntando para escrever um unico arquivo
datas = np.array([[int(datam[i].strftime('%Y%m%d%H')) for i in range(len(datam))]]).T
#vento1=np.concatenate((datas[:,0],vel,dire),axis=1) # pegando somente fev   

out=file('out/vento201302.txt','w')
#out.write('#Data,int,dire')
#out.write('\n')
#np.savetxt(out,vento1,fmt=['%i']+2*['%.2f'],delimiter=',')
for i in range(len(datam)):
	np.savetxt(out,np.c_[datas[i,0],vel[i],dire[i]],fmt='%5.2f',delimiter=',')


#out.close