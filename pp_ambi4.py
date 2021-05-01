#Processamento dos dados de aceleracao vertical de 20 horas
#no TEBIG
#
# a) Calcular a direcao com a ac.Z,pitch e roll
# b) Calcular a direcao com ac.V1, pitch e roll
# c) Calcular a direcao com a ac.Z, ac.X e ax.Y
# d) Calcular a direcao com ac.V1, ac.X e ax.Y
#
#Observacoes:
# - Realiza o processamento em batelada das 20 series

from matplotlib import pylab as pl
import numpy as np
import os
from scipy import io, integrate
import espec
import proconda
import numeronda

reload(proconda)
reload(espec)
reload(numeronda)

pl.close('all')

# =============================================================================== #

pathname = os.environ['HOME'] + '/Dropbox/ambid/TEBIG-microstr_20140417/'

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

h = 22 #profundidade
nfft = 128
fs = 1

#vetor de data (str)
data = p[:,0]

#intervalo de amostragem de onda
t = np.arange(1,1025)

#variaveis (matriz 1024x20 de float)
p = p[:,2:].astype(np.float).T
r = r[:,2:].astype(np.float).T
y = y[:,2:].astype(np.float).T
ax = ax[:,2:].astype(np.float).T * -9.81 #m/s2
ay = ay[:,2:].astype(np.float).T * -9.81 #m/s2
az = az[:,3:].astype(np.float).T * -9.81 #m/s2
aew = aew[:,2:].astype(np.float).T * -9.81 #m/s2
ans = ans[:,2:].astype(np.float).T * -9.81 #m/s2
av = av[:,3:].astype(np.float).T * -9.81 #m/s2

#calculo para transformar acZ (referencia boia) em acV (referencia terra)
# av1 = (aew * np.sin(p)) - (ans * np.cos(p) * np.sin(r)) - (az * np.cos(p) * np.cos(r))
av1 = (ax * np.sin(p*np.pi/180)) - (ay * (np.cos(p*np.pi/180) * np.sin(r*np.pi/180))) - (az * (np.cos(p*np.pi/180) * np.cos(r*np.pi/180)))
av1 = -av1 #fica igual a ac.V

#retira a media dos valores de aceleracoes verticais (bom para comparar series temp)
# az = np.array([az[:,i] - np.mean(az[:,i]) for i in range(az.shape[1])]).T
# av1 = np.array([av1[:,i] - np.mean(av1[:,i]) for i in range(av1.shape[1])]).T


# =============================================================================== #
# Processamento em batelada

## para o calculo dos param de onda com filtro passa banda

#frequencia de corte (limita a banda entre 4 - 15s)
aux = range(6,15)

# pondaf = [] #parametros de onda no dominio da freq. (proc. em batelada)
# dp = [] #direcao do periodo de pico filtrado
tp_z = [] #periodo de pico filtrado
tp_v1 = []
dp_zpr = []
dp_zxy = []
dp_v1pr = []
dp_v1xy = []

# pl.figure()

#variar as 20 horas
for i in range(av.shape[1]):

	#calcula a direcao com filtro passa banda

	#espectro simples
	snz = espec.espec1(az[:,i],nfft,fs) #aceleracao z
	snv1 = espec.espec1(av1[:,i],nfft,fs) #ac. vertical corrigida
	snp = espec.espec1(p[:,i],nfft,fs)  #pitch
	snr = espec.espec1(r[:,i],nfft,fs) #roll
	snx = espec.espec1(ax[:,i],nfft,fs) #acel. x
	sny = espec.espec1(ay[:,i],nfft,fs) #acel. y

	#deltaf (para 32 gl)
	f = snz[:,0]
	df = f[1] - f[0]

	#calculo de omega a 4
	w4 = (2 * np.pi * f) ** 4

	#espectro de heave (optido pela divisao do espec de acV1 por w4)
	snn = snv1[:,1] / w4

	pl.figure()
	pl.subplot(211), pl.title('serie de acV1')
	pl.plot(av1[:,i]), pl.axis('tight')
	pl.ylabel('m/s^2')
	pl.legend(['acZ','acV1'])
	pl.subplot(223)
	pl.plot(f,snv1[:,1]), pl.title('espec. acV1')
	pl.xlabel('Frequencia (Hz)')
	pl.subplot(224)
	pl.plot(f,snn), pl.title('espec. acV1/w4'), pl.axis([0,0.5,0,0.1])
	pl.xlabel('Frequencia (Hz)')

	#calculo do numero de onda
	k = numeronda.k(h,f,len(f))
	k = np.array(k)

	#calculo dos espectros cruzados (pitch e roll)
	sn2zp = espec.espec2(az[:,i],p[:,i],nfft,fs) #espectro cruzado de acZ e pitch
	sn2zr = espec.espec2(az[:,i],r[:,i],nfft,fs) #espectro cruzado de acZ e roll
	sn2pr = espec.espec2(p[:,i],r[:,i],nfft,fs) #espectro cruzado de pitch e roll
	sn2v1p = espec.espec2(av1[:,i],p[:,i],nfft,fs) #espectro cruzado de ac.V1 e pitch
	sn2v1r = espec.espec2(av1[:,i],r[:,i],nfft,fs) #espectro cruzado de ac.V1 e roll

	#calculo dos espectros cruzados (ac.X e acY)
	sn2zx = espec.espec2(az[:,i],aew[:,i],nfft,fs) #espectro cruzado de ac.Z e ac.X
	sn2zy = espec.espec2(az[:,i],ans[:,i],nfft,fs) #espectro cruzado de ac.Z e ac.Y
	sn2xy = espec.espec2(aew[:,i],ans[:,i],nfft,fs) #espectro cruzado de ac.X e ac.Y
	sn2v1x = espec.espec2(av1[:,i],aew[:,i],nfft,fs) #espectro cruzado de ac.V1 e ac.X
	sn2v1y = espec.espec2(av1[:,i],ans[:,i],nfft,fs) #espectro cruzado de ac.V1 e ac.Y
	

	#calculo dos coeficientes de fourier

	#ac.Z, pitch e roll
	a1zpr = sn2zp[:,3] / (k * np.pi * snz[:,1])
	b1zpr = sn2zr[:,3] / (k * np.pi * snz[:,1])

	#ac.Z, acX e acY
	a1zxy = sn2zx[:,3] / (k * np.pi * snz[:,1])
	b1zxy = sn2zy[:,3] / (k * np.pi * snz[:,1])

	#ac.V1, pitch e roll
	a1v1pr = sn2v1p[:,3] / (k * np.pi * snv1[:,1])
	b1v1pr = sn2v1r[:,3] / (k * np.pi * snv1[:,1])

	#ac.v1, acX e acY
	a1v1xy = sn2v1x[:,3] / (k * np.pi * snv1[:,1])
	b1v1xy = sn2v1y[:,3] / (k * np.pi * snv1[:,1])

	#calcular utilizando o heave e o pitch 

	#calcula direcao de onda

	#ac.Z, pitch e roll
	dire_zpr = np.array([np.angle(np.complex(a1zpr[i],b1zpr[i]),deg=True) for i in range(len(f))])
	#ac.Z, acX e acY
	dire_zxy = np.array([np.angle(np.complex(a1zxy[i],b1zxy[i]),deg=True) for i in range(len(f))])
	#ac.V1, pitch e roll
	dire_v1pr = np.array([np.angle(np.complex(a1v1pr[i],b1v1pr[i]),deg=True) for i in range(len(f))])
	#ac.V1, acX e acY
	dire_v1xy = np.array([np.angle(np.complex(a1v1xy[i],b1v1xy[i]),deg=True) for i in range(len(f))])

	#condicao para valores maiores que 360 e menores que 0
	dire_zpr[np.where(dire_zpr < 0)] = dire_zpr[np.where(dire_zpr < 0)] + 360
	dire_zpr[np.where(dire_zpr > 360)] = dire_zpr[np.where(dire_zpr > 360)] - 360

	dire_zxy[np.where(dire_zxy < 0)] = dire_zxy[np.where(dire_zxy < 0)] + 360
	dire_zxy[np.where(dire_zxy > 360)] = dire_zxy[np.where(dire_zxy > 360)] - 360
	
	dire_v1pr[np.where(dire_v1pr < 0)] = dire_v1pr[np.where(dire_v1pr < 0)] + 360
	dire_v1pr[np.where(dire_v1pr > 360)] = dire_v1pr[np.where(dire_v1pr > 360)] - 360
	
	dire_v1xy[np.where(dire_v1xy < 0)] = dire_v1xy[np.where(dire_v1xy < 0)] + 360
	dire_v1xy[np.where(dire_v1xy > 360)] = dire_v1xy[np.where(dire_v1xy > 360)] - 360

	#indice da frequencia de pico
	
	#ac.Z
	aux1z = pl.find(snz[aux,1] == max(snz[aux,1]))
	ind_z = pl.find(f == f[aux[aux1z]]) 

	#ac.V1
	aux1v1 = pl.find(snv1[aux,1] == max(snv1[aux,1]))
	ind_v1 = pl.find(f == f[aux[aux1v1]]) 

	#periodo de pico
	tp_z.append((1. / f[ind_z])[0])
	tp_v1.append((1. / f[ind_v1])[0])

	#direcao do periodo de pico
	
	#ac.Z, pitch e roll
	dp_zpr.append(dire_zpr[ind_z][0])
	#ac.Z, acX e acY
	dp_zxy.append(dire_zxy[ind_z][0])
	#ac.V1, pitch e roll
	dp_v1pr.append(dire_v1pr[ind_v1][0])
	#ac.V1, acX e acY
	dp_v1xy.append(dire_v1xy[ind_v1][0])

#Figuras

# pl.figure()
# pl.subplot(211)
# pl.plot(tp_z)
# pl.legend(['Tp_acZ'])
# pl.title('Periodo de pico - acZ')
# pl.ylabel('Segundos')
# pl.axis('tight')
# pl.subplot(212)
# pl.plot(dp_zpr)
# pl.plot(dp_zxy)
# pl.ylabel('Graus')
# pl.legend(['zpr','zxy'])
# pl.title('Direcao do Periodo de pico')
# pl.axis('tight')

# pl.figure()
# pl.subplot(211)
# pl.plot(tp_v1)
# pl.legend(['Tp_acV1'])
# pl.ylabel('Segundos')
# pl.title('Periodo de pico - acV1')
# pl.axis('tight')
# pl.subplot(212)
# pl.plot(dp_v1pr)
# pl.plot(dp_v1xy)
# pl.ylabel('Graus')
# pl.legend(['v1pr','v1xy'])
# pl.title('Direcao do Periodo de pico')
# pl.xlabel('Horas')
# pl.axis('tight')

# pl.figure()
# pl.plot(tp_z)
# pl.plot(tp_v1)
# pl.legend(['Tp_acZ','Tp_acV1'])

pl.show()

