'''
Aprendendo WAFO
'''


import os
import pandas as pd
import wafo as wf
from  waveproc import WaveProc
import numpy as np
import pylab as pl

pl.close('all')


pathname = os.environ['HOME'] + '/Dropbox/reserva/dados/ADCP_Reef_Reserva/'

wad = pd.read_table(pathname + '20150916/ADCP_REEF_16_09_2015016.wad', sep='\s*', header=None, index_col=False,
		            names=['bur','coun','pres','spare','analog','vxe','vyn','vzu','amp1','amp2','amp3','ampna'])


w = WaveProc(pathname)

w.n1 = np.array(wad.pres) - wad.pres.mean()
w.n2 = wad.vxe
w.n3 = wad.vyn
w.h = wad.pres.mean() + 0.9
w.t = np.array(wad.coun)
w.dt = w.t[3] - w.t[2]
w.fs = 1/w.dt
w.nfft = 256

w.timedomain()
w.freqdomain()


#==================================================#
#						WAFO
#==================================================#


#==================================================#
#Simulation from spectrum, estimation of spectrum

#Simulation of the sea surface from spectrum. The following code generates
#200 seconds of data sampled with 10Hz from the Torsethaugen spectrum.

import wafo.spectrum.models as wsm
from matplotlib.pyplot import *
S = wsm.Torsethaugen(Hm0=w.hm0, Tp=w.tp);
S1 = S.tospecdata()
S1.plot()

import wafo.objects as wo
xs = S1.sim(ns=2000, dt=0.1)
ts = wo.mat2timeseries(xs)
ts.plot_wave('-', nsub=1)

#==================================================#
#Estimation of spectrum

#==================================================#
#A common situation is that one wants to estimate the spectrum
#for wave measurements. The following code simulate 20 minutes
#signal sampled at 4Hz and compare the spectral estimate with 
#the original Torsethaugen spectum.
#
# S1.args - vetor de frequencia


pl.figure()
clf()
Fs = 4;  
#xs = S1.sim(ns=fix(20 * 60 * Fs), dt=1. / Fs) 
xs = np.array([w.t, w.n1]).T
ts = wo.mat2timeseries(xs) 
Sest = ts.tospecdata(L=None)
S1.plot()
Sest.plot('--')
axis([0, 3, 0, 5]) # This may depend on the simulation
show()

#==================================================#
#Probability distributions of wave characteristics.

#Probability distribution of wave trough period: WAFO gives the possibility
#of computing the exact probability distributions for a number of 
#characteristics given a spectral density. In the following example we study 
#the trough period extracted from the time series and compared with the theoretical
#density computed with exact spectrum, S1, and the estimated spectrum, Sest.

pl.figure()

import wafo.misc as wm
#dtyex = S1.to_t_pdf(pdef='Tt', paramt=(0, 10, 51), nit=3)
#dtyest = Sest.to_t_pdf(pdef='Tt', paramt=(0, 10, 51), nit=3)
T, index = ts.wave_periods(vh=0, pdef='d2u')
bins = wm.good_bins(T, num_bins=25, odd=True)
wm.plot_histgrm(T, bins=bins, normed=True)

#dtyex.plot()
#dtyest.plot('-.')
axis([0, 10, 0, 0.35])
show()

#==================================================#
#Directional spectra

#Here are a few lines of code, which produce directional
#spectra with frequency independent and frequency dependent spreading.


plotflag = 1
Nt = 101;   # number of angles
th0 = np.pi / 2; # primary direction of waves
Sp = 15;   # spreading parameter

D1 = wsm.Spreading(type='cos', theta0=th0, method=None) # frequency independent
D12 = wsm.Spreading(type='cos', theta0=0, method='mitsuyasu') # frequency dependent

SD1 = D1.tospecdata2d(S1)
SD12 = D12.tospecdata2d(S1)

pl.figure()
SD1.plot()

pl.figure()
SD12.plot()#linestyle='dashdot')
show()


#==================================================#














