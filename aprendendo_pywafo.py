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














    # mom, mom_txt = S.moment(nr=4, even=False, j=0)

    # sprc, spr, sprr = waveproc.spread_kuik1988(wavef['sn'], wavef['a1'], wavef['b1'])

    # fig = plt.figure()
    # ax1 = fig.add_subplot(211)
    # ax1.plot(wavef['f'], wavef['sn'][:,1])
    # ax1 = fig.add_subplot(212)
    # ax1.plot(wavef['f'], wavef['dire1'])
    # plt.show()

#     # cria matriz de tempo e heave
#     xs = np.array([t, n1]).T

#     # cria objeto com serie temporal
#     ts = wo.mat2timeseries(xs)

#     Sest = ts.tospecdata(L=None, tr=None, method='psd',
#                          detrend=None,
#                          window='parzen',
#                          noverlap=0,
#                          ftype='f',
#                          alpha=None)

#     plt.figure()
#     Sest.plot('--')
# # plt.axis([0, 3, 0, 5])


# Aprendendo WAFO

# import numpy as np
# import matplotlib.pyplot as plt
# import wafo.spectrum.models as wsm
# # import wafo.spectrum.models as sm
# plt.close('all')

# # vetor de frequencia
# f = np.linspace(start=0, stop=0.5, num=50)
# w = 2 * np.pi * f
# # w = np.linspace(0,4)

# # gera modelo espectral
# # S = wsm.Torsethaugen(Hm0=6, Tp=8);
# # S = wsm.Torsethaugen(Hm0=7, Tp=11, method='integration', wnc=6, gravity=9.81, chk_seastate=True)

# # S1 = S.tospecdata()

# Sj = wsm.Jonswap(Hm0=3, Tp=8)
# w = np.linspace(0,4,256)
# S1 = Sj.tospecdata(w)   #Make spectrum object from numerical values
# S = wsm.SpecData1D(Sj(w),w) # Alternatively do it manually


# plotflag = 1
# Nt = 101;   # number of angles
# th0 = np.pi / 2; # primary direction of waves
# Sp = 15;   # spreading parameter

# D1 = wsm.Spreading(type='cos', theta0=th0, method=None) # frequency independent
# D12 = wsm.Spreading(type='cos', theta0=0, method='mitsuyasu') # frequency dependent

# SD1 = D1.tospecdata2d(S1)
# SD12 = D12.tospecdata2d(S1)
# SD1.plot()
# SD12.plot()#linestyle='dashdot')

# plota espectro do modelo espectral com base
# no vetor de frequencia
# h=plt.plot(w,S(w),w,S.wind(w),w,S.swell(w))



# S = wsm.Torsethaugen(Hm0=6, Tp=8);
# S1 = S.tospecdata()


# h=S1.plot()

# Fs = 4;  
# xs = S1.sim(ns=int(20 * 60 * Fs), dt=1. / Fs) 
# ts = wo.mat2timeseries(xs) 
# Sest = ts.tospecdata(L=400)

# plt.figure()
# S1.plot()
# Sest.plot('--')
# plt.axis([0, 3, 0, 5]) # This may depend on the simulation  

# plotflag = 1
# Nt = 101;   # number of angles
# th0 = np.pi / 2; # primary direction of waves
# Sp = 15;   # spreading parameter

# D1 = wsm.Spreading(type='cos', theta0=th0, method=None) # frequency independent
# D12 = wsm.Spreading(type='cos', theta0=0, method='mitsuyasu') # frequency dependent

# plt.figure()

# SD1 = D1.tospecdata2d(S1)
# SD12 = D12.tospecdata2d(S1)
# SD1.plot()
# SD12.plot()#linestyle='dashdot')

# plt.show()

# D = wsm.Spreading('cos2s',s_a=10.0)

# # Make directionale spectrum
# S = wsm.Jonswap().tospecdata()
# SD = D.tospecdata2d(S)
# w = np.linspace(0,3,257)
# theta = np.linspace(-np.pi,np.pi,129)

# # Make frequency dependent direction spreading
# theta0 = lambda w: w*np.pi/6.0
# D2 = wsm.Spreading('cos2s',theta0=theta0)

# import matplotlib.pyplot as plt

# h = SD.plot()
# t = plt.contour(D(theta,w)[0].squeeze())

# t = plt.contour(D2(theta,w)[0])

# Plot all spreading functions
# alltypes = ('cos2s','box','mises','poisson','sech2','wrap_norm')
# for ix in range(len(alltypes)):
#     D3 = wsm.Spreading(alltypes[ix])
#     t = plt.figure(ix)
#     t = plt.contour(D3(theta,w)[0])
#     t = plt.title(alltypes[ix])

# plt.close('all')
# plt.show()


# Calcula parametros espectrais dos dados d CDIP com o WAFO

# import numpy as np
# import pandas as pd
# import xarray as xr
# import wafo.spectrum.models as wsm

# ds = xr.open_dataset('/home/hp/Documents/laura_cdip/214p1_historic.nc')

# # data em datetime
# datet = pd.to_datetime(ds.waveEnergyDensity.waveTime.values)

# # valores de frequencia e direcao
# f = ds.waveFrequency.values

# param = []
# for t in range(len(datet)):
#     print ('{} de {}'.format(t, len(datet)))

#     # espectro de energia
#     s = ds.waveEnergyDensity.values[t,:]

#     # calculo do espectro
#     S = wsm.SpecData1D(s, f, type='freq',
#                        freqtype='f', tr=None, h=np.inf)

#     # calculo do periodo de pico
#     Tp2 = 1/f[s == s.max()][0]

#     # largura de banda
#     bw = S.bandwidth(['alpha','eps2','eps4', 'Qp'])

#     # parametrosd e onda
#     [ch, R, txt] = S.characteristic(fact=np.arange(0, 15), T=2048, g=9.81)

#     # momentos espectrais
#     mom, mom_txt = S.moment(nr=4, even=False, j=0)

#     varr = [datet[t]] + list(np.concatenate((bw, ch, mom))) + [Tp2]

#     param.append(varr)

# cols = ['date', 'alpha','eps2','eps4', 'Qp1'] + txt + mom_txt + ['Tp2']

# param = pd.DataFrame(param, columns=cols)
# param.set_index('date', inplace=True)

# param.to_csv('/home/hp/Documents/laura_cdip/param_214p1_historic.csv', float_format='%.4f')





