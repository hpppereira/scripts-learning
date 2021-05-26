'''
Wave processing for Triaxys buoy from PNBOIA

use class WaveProc
'''

import os
import numpy as np
import pandas as pd
import matplotlib.pylab as pl
import matplotlib.pyplot as plt

import waveproc
reload(waveproc)
from waveproc import WaveProc

pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/bruto/triaxys/pre_proc/santos/hne/'
pathnamefig = os.environ['HOME'] + '/Dropbox/partspec/rot/fig/RIG/'
dmag = -17
ini = '201204210100.HNE'

w = WaveProc(pathname)

w.listdir()

w.en1 = []
w.en2 = []
w.en3 = []

ini1 = pl.find(w.filelist == ini)[0]

d = []
for file in w.filelist[ini1:]:

    w.read_HNE(filename = file,
     		   fs       = 1.28,
     		   nfft     = 82,
     		   h        = 200)

    if len(w.n1) > 1000 and np.sort(w.n1)[-100:].mean() > 0.5:

    	print w.date

        #w.wavenumber()
    
        w.timedomain()
    
        w.freqdomain()

        d.append({'date'   : w.date,
        		  'hs'     : w.hs,
        		  'h10'    : w.h10,
        		  'hmax'   : w.hmax,
        		  'tmed'   : w.tmed,
        		  'thmax'  : w.thmax,
        		  'hm0'    : w.hm0,
        		  'tp'     : w.tp,
        		  'dp'     : w.dp + dmag,
                  'tzamax' : w.tzamax
        		})

        w.en1.append(w.sn1[:,1])
        w.en2.append(w.sn2[:,1])
        w.en3.append(w.sn3[:,1])


        # pl.figure()
        # pl.title(str(w.date) + '\n Hm0 = %.1f m ; Tp = %.1f s ; Dp = %i deg' %(w.hm0, w.tp, w.dp))
        # pl.plot(w.f, w.sn1[:,1], w.f, w.sn2[:,1], w.f, w.sn3[:,1])
        # pl.legend(['Heave', 'Dsp.NS', 'Dsp.EW'])
        # pl.savefig(pathnamefig + 'espec_' + file[:-4] + '.png')
        # pl.close('all')

    else:

    	print '%s -- Reprovado' %w.date

df = pd.DataFrame(d)
df = df.set_index('date')

#array com espectros 1d de heave, dspEW e dspNS
w.en1 = np.array(w.en1).T
w.en2 = np.array(w.en2).T
w.en3 = np.array(w.en3).T


##################################


fig = plt.figure(figsize=(17,15))
ax1 = fig.add_subplot(311)
cax1 = ax1.plot(df.index,df.hm0)
ax1.set_ylabel('Hm0 (m)')
ax1.grid()

ax2 = fig.add_subplot(312)
cax2 = ax2.plot(df.index,df.tp,'.')
ax2.set_ylabel('Tp (s)')
ax2.grid()

ax3 = fig.add_subplot(313)
cax3 = ax3.plot(df.index,df.dp,'.')
ax3.set_ylabel('Dp (deg)')
ax3.grid()

plt.savefig('fig/param.png')




##################################

nli = np.arange(0,np.array([w.en1, w.en2, w.en3]).max()+0.25,0.25)

fig = plt.figure(figsize=(17,15))
ax1 = fig.add_subplot(311)
cax1 = ax1.contourf(df.index,w.f,w.en1,nli)
#cbar1 = plt.colorbar(cax1, cax = None)
ax1.set_ylim(0.016,0.3)
ax1.set_ylabel('Heave')
ax1.grid()

ax2 = fig.add_subplot(312)
cax2 = ax2.contourf(df.index,w.f,w.en2,nli)
#cbar2 = plt.colorbar(cax2, cax = None)
ax2.set_ylim(0.016,0.3)
ax2.set_ylabel('Dsp.NS')
ax2.grid()

ax3 = fig.add_subplot(313)
cax3 = ax3.contourf(df.index,w.f,w.en3,nli,extend='both')
# fig.subplots_adjust(left=None, bottom=0.001, right=None, top=None,
#                   wspace=None, hspace=None)
cbar_ax = fig.add_axes([0.2,0.03,0.6,0.03])
cbar3 = plt.colorbar(cax3, cax = cbar_ax, orientation='horizontal')
cbar3.set_ticks(np.arange(0,nli.max()+1,2))
cbar3.set_label(u'm2/Hz')
ax3.set_ylim(0.016,0.3)
ax3.set_ylabel('Dsp.EW')
ax3.grid()

plt.savefig('fig/evolspec.png')

##############################################
#evolucao espetral das diferencas

#maximo valor da diferenca
aux = int(abs(np.array([np.array([w.en1-w.en2,w.en1-w.en3,w.en2-w.en3]).min(), 
               np.array([w.en1-w.en2,w.en1-w.en3,w.en2-w.en3]).max()])).max())

nli = np.arange(-aux, aux+0.25, 0.25)


fig = plt.figure(figsize=(17,15))
ax1 = fig.add_subplot(311)
cax1 = ax1.contourf(df.index,w.f,w.en1-w.en2,nli)
#cbar1 = plt.colorbar(cax1, cax = None)
ax1.set_ylim(0.016,0.3)
ax1.set_ylabel('Heave - Dsp.NS')
ax1.grid()

ax2 = fig.add_subplot(312)
cax2 = ax2.contourf(df.index,w.f,w.en1-w.en3,nli)
#cbar2 = plt.colorbar(cax2, cax = None)
ax2.set_ylim(0.016,0.3)
ax2.set_ylabel('Dsp.NS - Dsp.EW')
ax2.grid()

ax3 = fig.add_subplot(313)
cax3 = ax3.contourf(df.index,w.f,w.en2-w.en3,nli,extend='both')
# fig.subplots_adjust(left=None, bottom=0.001, right=None, top=None,
#                   wspace=None, hspace=None)
cbar_ax = fig.add_axes([0.2,0.03,0.6,0.03])
cbar3 = plt.colorbar(cax3, cax=cbar_ax, orientation='horizontal')
cbar3.set_ticks(np.arange(nli.min(),nli.max()+1,2))
cbar3.set_label(u'm2/Hz')
ax3.set_ylim(0.016,0.3)
ax3.set_ylabel('Dsp.NS - Dsp.EW')
ax3.grid()

plt.savefig('fig/evolspec_diff.png')


pl.show()
#df.to_csv()


