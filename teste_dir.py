"""
teste de direcao com espectro cruzado
"""


import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import mlab

plt.close('all')

pathname = os.environ['HOME'] + '/GoogleDrive/AGES/data/boia_merenda/'

# data inicial e final para processar com base no nome do arquivo (YYMMDDHHMM.dat)
filename = 'Onda_06110110.dat'

raw = pd.read_table(pathname + 'brutos/' + filename, skiprows=13, sep='\s+',
                           names=['heave','roll','pitch','compass'])

# date in timestamp
date = pd.to_datetime(filename[-12:-4], format='%y%m%d%H')

# correcao
raw.roll = -raw.roll
raw.roll = np.cos(np.pi*raw.compass/180) * raw.roll + np.sin(np.pi*raw.compass/180) * raw.heave  
raw.pitch = -np.sin(np.pi*raw.compass/180) * raw.roll + np.cos(np.pi*raw.compass/180) * raw.heave 


# calculo da direcao pelo espectro cruzado

dt = 1
s1 = raw.heave
s2 = raw.roll

# First create power sectral densities for normalization

(ps1, f) = mlab.psd(s1, Fs=1./dt, scale_by_freq=False)
(ps2, f) = mlab.psd(s2, Fs=1./dt, scale_by_freq=False)

# plt.plot(f, ps1)
# plt.plot(f, ps2)




# Then calculate cross spectral density
(csd, f) = mlab.csd(s1, s2, NFFT=256, Fs=1./dt,sides='default', scale_by_freq=False)

angle = np.angle(csd, deg=True)
angle[angle<-90] += 360

# Normalize cross spectral absolute values by auto power spectral density

fig = plt.figure()

ax1 = fig.add_subplot(3, 1, 1)
ax1.plot(f, np.absolute(csd)**2 / (ps1 * ps2))

ax2 = fig.add_subplot(3, 1, 2)
ax2.plot(f, angle)

# # zoom in on frequency with maximum coherence
# ax1.set_xlim(9, 11)
# ax1.set_ylim(0, 1e-0)
# ax1.set_title("Cross spectral density: Coherence")
# ax2.set_xlim(9, 11)
# ax2.set_ylim(0, 90)
# ax2.set_title("Cross spectral density: Phase angle")

# plt.show()

# fig = plt.figure()
# ax = plt.subplot(111)

# ax.plot(f, np.real(csd), label='real')
# ax.plot(f, np.imag(csd), label='imag')

# ax.legend()
# plt.show()

plt.show()