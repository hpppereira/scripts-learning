# Processamento dos dados brutos de ac. Z, ac. V, pitch, roll..
#
# a) Calcular o espectro de heave pela divisao do espectro
#    de aceleracao vertical por w4
#
# b) Calcular a direcao utilizando o espectro cruzado de heave,
#    pitch e roll (dividindo o espectro de ac.V1 por w4).
#
# c) Passar um filtro passa alta (com 20 seg) nas series de acV1
#    para ver se diminui o ruido e calcular novamente a direcao.
#
# d) Obter a serie temporal de heave a partir da IFFT do espectro
#    bruto de acV1, e calcular a direcao e os parametros de onda
#    no dominio do tempo e frequencia.
#
# Dados: pitch, roll, yaw, ac.X, ac.Y, ac.Z, ac.EW, ac.NS, ac.V

import numpy as np
import os
from matplotlib import mlab
from matplotlib import pylab as pl
from scipy import signal
import espec
import proconda

pl.close('all')

# =============================================================================== #

pathname = os.environ['HOME'] + '/Dropbox/ambid/TEBIG-microstr_20140417/'
# pathname = 'C:/Users/henrique/Dropbox/ambid/TEBIG-microstr_20140417/'


p = np.loadtxt(pathname + 'TOA5_55915.microstrain_pitch.dat',
	delimiter=',',skiprows=4,dtype=str)
r = np.loadtxt(pathname + 'TOA5_55915.microstrain_roll.dat',
	delimiter=',',skiprows=4,dtype=str)
y = np.loadtxt(pathname + 'TOA5_55915.microstrain_yaw.dat',
	delimiter=',',skiprows=4,dtype=str)
ax = np.loadtxt(pathname + 'TOA5_55915.microstrain_stbacelX.dat',
	delimiter=',',skiprows=4,dtype=str)
ay = np.loadtxt(pathname + 'TOA5_55915.microstrain_stbacelY.dat',
	delimiter=',',skiprows=4,dtype=str)
#o acz esta delimitado com espaco
az = np.loadtxt(pathname + 'TOA5_55915.microstrain_stbacelZ.dat',
	delimiter=' ',skiprows=4,dtype=str)
aew = np.loadtxt(pathname + 'TOA5_55915.microstrain_stbaclEW.dat',
	delimiter=',',skiprows=4,dtype=str)
ans = np.loadtxt(pathname + 'TOA5_55915.microstrain_stbaclNS.dat',
	delimiter=',',skiprows=4,dtype=str)
#o acv esta delimitado com espaco
av = np.loadtxt(pathname + 'TOA5_55915.microstrain_stbaclV.dat',
	delimiter=' ',skiprows=4,dtype=str)

#profundidade
h = 22

#vetor de data (str)
data = p[:,0]

#intervalo de amostragem de onda
t = np.arange(1,1025)

#variaveis (matriz 1024x20 de float)
p = p[:,2:].astype(np.float).T
r = r[:,2:].astype(np.float).T
y = y[:,2:].astype(np.float).T
ax = ax[:,2:].astype(np.float).T #* -9.81 #m/s2
ay = ay[:,2:].astype(np.float).T #* -9.81 #m/s2
az = az[:,3:].astype(np.float).T #* -9.81 #m/s2
aew = aew[:,2:].astype(np.float).T #* -9.81 #m/s2
ans = ans[:,2:].astype(np.float).T #* -9.81 #m/s2
# av = av[:,3:].astype(np.float).T # * -9.81 #m/s2

#calculo para transformar acZ (referencia boia) em acV (referencia terra)
# av1 = (ax * np.sin(p*np.pi/180)) - (ay * (np.cos(p*np.pi/180) * np.sin(r*np.pi/180))) - (az * (np.cos(p*np.pi/180) * np.cos(r*np.pi/180)))
# av1 = av1 * -1 #fica igual a ac.V

#retira a media dos valores de aceleracoes verticais (bom para comparar 
#series temp)

# az = np.array([az[:,i] - np.mean(az[:,i]) for i in range(az.shape[1])]).T
# av = np.array([av[:,i] - np.mean(av[:,i]) for i in range(av.shape[1])]).T
# av1 = np.array([av1[:,i] - np.mean(av1[:,i]) for i in range(av1.shape[1])]).T

narq = 0 #numero do arquivo processado


# =============================================================================== #
# Espectro simples

# nfft = 64 #numero do bloco para realizar a fft
# fs = 1 #frequencia de amostragem
# gl = len(p) / nfft * 2 #graus de liberdade para o calculo do espectro

# #espectros simples
# aap = espec.espec1(p[:,narq],nfft,fs)
# aar = espec.espec1(r[:,narq],nfft,fs)
# aax = espec.espec1(ax[:,narq],nfft,fs)
# aay = espec.espec1(ay[:,narq],nfft,fs)
# aaz = espec.espec1(az[:,narq],nfft,fs)
# aaew = espec.espec1(aew[:,narq],nfft,fs)
# aans = espec.espec1(ans[:,narq],nfft,fs)
# aav = espec.espec1(av[:,narq],nfft,fs)
# aav1 = espec.espec1(av1[:,narq],nfft,fs)

# f = aap[:,0] #vetor de frequencia
# w4 = (2 * np.pi * f ) ** 4 #omega a quarta

# # a) espectro do deslocamento verical (eta) (divide por w4)
# aan_z = aaz[:,1] / w4
# aan_v = aav[:,1] / w4
# aan_v1 = aav1[:,1] / w4

# =============================================================================== #
# Figuras

#series temporais 

#aceleracao
pl.figure()
pl.title('Series temporais das aceleracoes X, Y e Z')
pl.plot(ax[:,narq],label='acX')
pl.plot(ay[:,narq],label='acY')
pl.plot(az[:,narq],'r',label='acZ')
pl.xlabel('Tempo (s)')
pl.ylabel('g')
pl.legend()

#aceleracao (primeiros valores) - retirando a media
pl.figure()
pl.title('Series das aceleracoes X, Y e Z')
pl.plot(ax[0:25,narq] - np.mean(ax[0:25,narq]),'b',label='acX')
pl.plot(ay[0:25,narq] - np.mean(ay[0:25,narq]),'g',label='acY')
pl.plot(az[0:25,narq] - np.mean(az[0:25,narq]),'r',label='acZ')
pl.legend()
pl.xlabel('Tempo (s)')
pl.ylabel('g')

# #aceleracao (primeiros valores) - retirando a media
# fig1 = pl.figure()
# pl.title('Series das aceleracoes X, Y e Z')
# ax1 = fig1.add_subplot(111)
# ax1.plot(ax[0:25,0],'b',label='acX')
# ax1.plot(ay[0:25,0],'g',label='acY')
# ax1.set_ylabel('m/s^2')
# ax1.set_xlabel('Tempo (s)')
# ax2 = ax1.twinx()
# ax2.plot(az[0:25,0],'r',label='acZ')
# ax2.set_ylabel('m/s^2')
# h1, l1 = ax1.get_legend_handles_labels()
# h2, l2 = ax2.get_legend_handles_labels()
# ax1.legend(h1+h2, l1+l2, loc=1)

#pitch e roll e yaw
pl.figure()
pl.subplot(211)
pl.title('Series de Pitch, Roll e Yaw')
pl.plot(p[:,narq],'b',label='pitch')
pl.plot(r[:,narq],'g',label='roll')
pl.legend()
pl.ylabel('Graus')
pl.subplot(212)
pl.plot(y[:,narq],'r',label='yaw')
pl.xlabel('Tempo (s)')
pl.ylabel('Graus')
pl.legend()

#pitch e roll (primeiros valores)
pl.figure()
pl.title('Series de Pitch e Roll')
pl.plot(p[0:25,narq],label='pitch')
pl.plot(r[0:25,narq],label='roll')
pl.xlabel('Tempo (s)')
pl.ylabel('Graus')
pl.legend()

# #acZ, pitch e roll (primeiros valores)
# fig1 = pl.figure()
# pl.title('Series de Pitch, Roll e acZ')
# ax1 = fig1.add_subplot(111)
# ax1.plot(p[0:25,0],'b',label='pitch')
# ax1.plot(r[0:25,0],'g',label='roll')
# ax1.set_ylabel('Graus')
# ax1.set_xlabel('Tempo (s)')
# ax2 = ax1.twinx()
# ax2.plot(az[0:25,0],'r',label='acZ')
# ax2.set_ylabel('m/s^2')
# h1, l1 = ax1.get_legend_handles_labels()
# h2, l2 = ax2.get_legend_handles_labels()
# ax1.legend(h1+h2, l1+l2, loc=1)

# #aceleracoes EW e NS comparando com X e Y (retirando a media)
# pl.figure()
# pl.title('Series das aceleracoes EW-NS e X-Y')
# pl.subplot(211)
# pl.plot(ax[:,0]-np.mean(ax),label='acX')
# pl.plot(aew[:,0]-np.mean(aew),label='acEW')
# pl.legend()
# pl.subplot(212)
# pl.plot(ay[:,0]-np.mean(ay),label='acY')
# pl.plot(ans[:,0]-np.mean(ans),label='acNS')
# pl.legend()

#series temporais de acZ e acV1 (sem tirar a media)
# pl.figure()
# pl.title('Series das aceleracoes Z e V1')
# pl.plot(az[:,0],label='acZ')
# pl.plot(av1[:,0],label='acV1')
# pl.legend()

#series de ???
# pl.figure()
# pl.subplot(121)
# pl.plot(aaz[:,0],aaz[:,1],label='acZ') #acZ
# pl.plot(aav1[:,0],aav1[:,1],label='acV1') #acV1
# pl.axis([0,0.5,0,0.015])
# pl.legend()
# pl.xlabel('Frequencia (Hz)')
# pl.title('Espectros das aceleracoes Z e V1')
# pl.subplot(122)
# pl.plot(f,aan_z,label='acZ/w4') #acZ / w4
# pl.plot(f,aan_v1,label='acV1/w4') #acV1 / w4
# pl.axis([0,0.5,0,0.002])
# pl.title('Espectro de Heave')
# pl.legend()
# pl.xlabel('Frequencia (Hz)')

pl.show()