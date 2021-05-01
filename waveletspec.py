'''
Calculates wavelet spectrum from 
a heave time series of measured from a metocean
buoy

Show wavelet spectrum in contour plot
'''

import pywt
from piwavelet import piwavelet
import os
import pandas as pd
import matplotlib.pylab as plt
from matplotlib.cm import * 
from scipy import signal
import numpy as np

plt.close('all')

pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/bruto/triaxys/rio_grande/HNE/'
filename = '201201211900.HNE'
filename = '200907241900.HNE' #freakwave - hmax=11,5 metros

df = pd.read_table(pathname + filename, delimiter='\s*', names=['time','hv','dn','de'], skiprows=11)

#cria wavelet
M = 100 #numero de pontos

mo = signal.wavelets.morlet(100, w=5.0, s=1.0, complete=True)


#################
'''
Transformada wavelet continua
'''

t = np.arange(len(df.hv))
sig = df.hv

#t = np.linspace(-1, 1, 200, endpoint=False)
#sig  = np.cos(2 * np.pi * 7 * t) + signal.gausspulse(t - 0.4, fc=2)

plt.figure()
plt.subplot(211)
plt.plot(t,sig)
plt.axis('tight')
plt.subplot(212)
widths = np.arange(1,100)
cwtmatr = signal.cwt(sig, signal.ricker, widths)
plt.imshow(cwtmatr, extent=None, cmap='jet', aspect='auto',
            vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())


plt.show()



'''
Spectrogram

Compute and plot a spectrogram of data in *x*.  Data are split into
*NFFT* length segments and the spectrum of each section is
computed.  The windowing function *window* is applied to each
segment, and the amount of overlap of each segment is
specified with *noverlap*. The spectrogram is plotted as a colormap
(using imshow).

interpolation = linear, nearest, 
'''

#plt.figure()
#plt.specgram(df.hv, NFFT=256, Fs=2, noverlap=32, detrend=mlab.detrend_none, 
#	window=mlab.window_hanning, noverlap=128, cmap=None, xextend=None, pad_to=None,
#	sides='default', scale_by_freq=None, mode='default', scale='default', )

#plt.show()


##################
'''
One dimensional discrete wavlet transform
'''

#(cA, cD) = pywt.dwt(df.hv, 'db4', mode='sym')


################
#Wavelet Coherence Analysis:
'''
#Rsq	Coherence Wavelet
#period	a vector of "Fourier" periods associated with Wxy
#scale	a vector of wavelet scales associated with Wxy
#coi	the cone of influence
#sig95	Significance
'''

#mycoherence = piwavelet.wcoherence(df.hv,df.de)
#Rsq,period,scale,coi,sig95=mycoherence()

#Plot wavelet coherence of the signals x,y.
'''
Parameters :

Key	Mean
title (string)	Title of the Plot
t	array with time
units: (string)	Units of the period and time (e.g. 'days')

Optional parameters

Key	Default	Mean
gray	(boolean) True for gray map	False
levels	List with significance level that will be showed in the plot	[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
labels	List with the Label of significance level that will be apper into the color bar. If not defined, the levels list is used instead	None
pArrow (boolean)	True for draw vector of phase angle (it has problem not recomended for large sample of data)	False
pSigma (boolean)	True for draw the significance contour lines	True
nameSave (string)	path plus name to save the figure, if it is define, the plot is saved but not showed	None
scale	(boolean) True for not log2 scale of the Plot	False
'''

#mycoherence.plot(t = time, title='My Title',units='year')


#####################
#Wavelet Cross Power Spectrum Analysis:

'''
Given tow signal, with zero mean, to start the cross wavelet analysis, it is necessary
to call the wcross (Wavelet Cross Spectrum) class:

xwt	cross Wavelet
period	a vector of "Fourier" periods associated with Wxy
scale	a vector of wavelet scales associated with Wxy
coi	the cone of influence
sig95	Significance

'''

#myXSpec = piwavelet.wcross(df.hv,df.de)
#xwt,period, scale, coi, sig95=myXSpec()

##plot
'''
Key	Mean
title (string)	Title of the Plot
t	array with time
units: (string)	Units of the period and time (e.g. 'days')

Optional parameters

Key	Default	Mean
gray	(boolean) True for gray map	False
levels	List with significance level that will be showed in the plot	[0.125, 0.25, 0.5, 1, 2, 4, 8]
labels	List with the Label of significance level that will be apper into the color bar. If not defined, the levels list is used instead	['1/8', '1/4', '1/2', '1', '2', '4', '8']
pArrow (boolean)	True for draw vector of phase angle (it has problem not recomended for large sample of data)	False
pSigma (boolean)	True for draw the significance contour lines	True

'''

#myXSpec.plot(t = time, title='My Title',units='year')



###################
#Extra functions

'''
plot wavelet spectrum
'''


# y1 = df.hv
# x = range(len(df.hv))

# #y1 = np.random.rand(50) #Generation of the Random Signal
# #x = np.arange(0,50,1) # Time step

# plt.plot(x,y1,label='y')
# plt.legend(loc=4)
# plt.show()
# plt.clf()
# y1 = (y1-y1.mean())/y1.std() #Normalization of the Signal 1
# plt.plot(x,y1,label='y1')
# plt.legend(loc=4)
# plt.show()
# wave, scales, freqs, coi, fft, fftfreqs=piwavelet.cwt(y1) # If you want to know the individual properties.'
# piwavelet.plotWavelet(y1,title=filename,label='Heave (m)',units='sec')




