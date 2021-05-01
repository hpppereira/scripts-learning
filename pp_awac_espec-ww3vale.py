'''
Calculo do espectros dos dados
brutos do ADCP da Vale
'''

import numpy as np
import pylab as pl
import os
import espec
import proconda

pl.close('all')

#pt1 = np.loadtxt(os.environ['HOME'] + 'C:/Users/Cliente/Dropbox/ww3vale/Geral/TU/dados/brutos/PTU01_03134.wad')
pt1 = np.loadtxt('C:/Users/Cliente/Dropbox/ww3vale/Geral/TU/dados/brutos/PTU01_03134.wad')
#pt3 = np.loadtxt(os.environ['HOME'] + 'C:/Users/Cliente/Dropbox/ww3vale/Geral/TU/dados/brutos/PTU03_03154.wad')
pt3 = np.loadtxt('C:/Users/Cliente/Dropbox/ww3vale/Geral/TU/dados/brutos/PTU03_03154.wad')

aw1 = pt1[:,4]
aw3 = pt3[:,4]

nfft1 = 75
fs1 = 1
t1 = np.arange(aw1.shape[0])
nfft3 = 150 
fs3 = 2 
t3 = np.arange(0,aw1.shape[0],0.5)

aa1 = espec.espec1(aw1,nfft1,fs1)
aa3 = espec.espec1(aw3,nfft3,fs3)

df1 = aa1[2,0] - aa1[1,0]
df3 = aa3[2,0] - aa3[1,0]

hm01 = 4 * np.sqrt(sum(aa1[:,1] * df1))
hm03 = 4 * np.sqrt(sum(aa3[:36,1] * df3))

#processamento no dominio do tempo
Hs1,H101,Hmax1,Tmed1,THmax1 = proconda.ondat(t1,aw1,40)
Hs3,H103,Hmax3,Tmed3,THmax3 = proconda.ondat(t3,aw3,11)


# pl.figure()
pl.plot(aa1[:,0],aa1[:,2],label='ADCP-1')
pl.plot(aa3[:,0],aa3[:,2],label='ADCP-3')
pl.title('Espectro de energia - 14/02/2013 03:00')
pl.xlabel('Freq (Hz)')
pl.ylabel('m2/Hz')
pl.grid('on')
pl.legend()

pl.show()