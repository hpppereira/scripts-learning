


import numpy as np
import os
import proconda
import pylab as pl
reload(proconda)
pl.close('all')
pathname = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/partespec/dados/'

arqname = '200908090600.HNE'
arqname = '200906090600.HNE'
# arqname = '200909090600.HNE' #unimodal

dados = np.loadtxt(pathname + arqname,skiprows=11)

time, eta, etay, etax = dados.T

h = 200 #profundidade 
nfft = 82 #numero de dados para a fft (para nlin=1312 -- p/ 32gl, nfft=82 ; p/8 gl, nfft=328)
fs = 1.28 #freq de amostragem
nlin = 1312 #comprimento da serie temporal a ser processada
gl = (nlin/nfft) * 2


#processamento no dominio da frequencia
hm0, tp, dp, sigma1p, sigma2p, freq, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
    eta,etax,etay,h,nfft,fs)


sf = sn[:,1]
f = freq
lim = pl.find(f<=0.5)
f1,sf1 = f[lim], sf[lim]
df = f1[3] - f1[2]

esb = []
for i in range (len(f1)):
	esb.append( (8*np.pi* np.sum(f1**2*sf1[i]*df))/((9.81*np.sum(sf1[i]*df))**0.5) )

esb= np.array(esb)

picomax = pl.find(esb==max(esb))

fm = f1[picomax]
fs = 4.112*(fm**1.746)
y = [0, max(sf1)]
x = [fs,fs]
pl.figure()
pl.plot(f1,sf1)
pl.plot(x,y,'r--')
pl.show()