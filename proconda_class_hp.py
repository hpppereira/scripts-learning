### CALCULA PARAMETROS DE ONDA NO DOMINIO DO TEMPO E FREQUENCIA ###
# Desenvolvido por: Henrique P. P. Pereira - pereira.henriquep@gmail.com
# Data da ultima modificacao: 20/05/2014
# ================================================================================== #
# Funcao 'ondat': Processamento de dados de onda no dominio do tempo
# Funcao 'ondaf': Processamento de dados de onda no dominio da frequencia
# ================================================================================== #

import numpy as np
from matplotlib import mlab

#import para o relatorio
from numpy import *
from pylab import *


import numpy as np
import pylab as pl
import os
from datetime import datetime

import numpy as np
import pylab as pl
import copy as cp

from scipy.stats import nanmean, nanstd

import time
from numpy import *
from pylab import *
import numpy as np
import matplotlib.pylab as pl
from scipy.signal import lfilter, filtfilt, butter
# import loadhne
import espec



#Espectro simples
def espec1(x,nfft,fs):

	"""
	#======================================================================#
	#
	# Calcula o espectro simples de uma serie real
	#
	# Dados de entrada: x = serie real
	#                   nfft - Numero de pontos utilizado para o calculo da FFT
	#                   fs - frequencia de amostragem
	#
	# Dados de saida: [aa] - col 0: vetor de frequencia
	#                        col 1: autoespectro
	#                        col 2: intervalo de confianca inferior
	#                        col 3: intervalo de confianca superior
	#
	# Infos:	detrend - mean
	#			window - hanning
	#			noverlap (welch) - 50%
	#
	#======================================================================#
	"""

	#calculo do espectro
	sp = mlab.psd(x,NFFT=nfft,Fs=fs,detrend=mlab.detrend_mean,window=mlab.window_hanning,noverlap=nfft/2)
	f, sp = sp[1][1:],sp[0][1:]

	#graus de liberdade
	gl = len(x) / nfft * 2

	#intervalo de confianca 95%
	ici = sp * gl / 26.12
	ics = sp * gl / 5.63

	aa = np.array([f,sp,ici,ics]).T

	return aa

#Espectro cruzado
def espec2(x,y,nfft,fs):

	"""
	# ================================================================================== #
	#
	# Calcula o espectro cruzado entre duas series reais
	#
	# Dados de entrada: x = serie real 1 (potencia de 2)
	#                   y = serie real 2 (potencia de 2)
	#                   nfft - Numero de pontos utilizado para o calculo da FFT
	#                   fs - frequencia de amostragem
	#
	# Dados de saida: [aa2] - col 0: vetor de frequencia
	#                         col 1: amplitude do espectro cruzado
	#                         col 2: co-espectro
	#                         col 3: quad-espectro
	#                         col 4: espectro de fase
	#                         col 5: espectro de coerencia
	#                         col 6: intervalo de confianca inferior do espectro cruzado
	#                         col 7: intervalo de confianca superior do espectro cruzado
	#                         col 8: intervalo de confianca da coerencia
	#
	# Infos:	detrend - mean
	#			window - hanning
	#			noverlap - 50%
	#
	# ================================================================================== #
	"""

	#cross-spectral density - welch method (complex valued)
	sp = mlab.csd(x,y,NFFT=nfft,Fs=fs,detrend=mlab.detrend_mean,window=mlab.window_hanning,noverlap=nfft/2)
	f = sp[1][1:]
	sp2 = sp[0][1:]

	#co e quad espectro (real e imag) - verificar com parente
	co = np.real(sp2)
	qd = np.imag(sp2)

	#phase (angle function)
	ph = np.angle(sp2,deg=True)

	#ecoherence between x and y (0-1)
	coer = mlab.cohere(x,y,NFFT=nfft,Fs=fs,detrend=mlab.detrend_mean,window=mlab.window_hanning,noverlap=nfft/2)
	coer = coer[0][1:]

	#intervalo de confianca para a amplitude do espectro cruzado - 95%
	ici = sp2 * 14 /26.12
	ics = sp2 * 14 /5.63

	#intervalo de confianca para coerencia
	icc = np.zeros(len(sp2))
	icc[:] = 1 - (0.05 ** (1 / (14 / 2.0 - 1)))

	aa2 = np.array([f,sp2,co,qd,ph,coer,ici,ics,icc]).T

	return aa2



def numeronda(h,deltaf,reg):

	'''
	# ================================================================================== #
	#
	# Calcula o numero de onda (k)
	#
	# Dados de entrada: h - profundidade
	#	  			    deltaf - vetor de frequencia
	#				    reg - comprimento do vetor de frequencia
	#
	# Dados de saida: k - vetor numero de onda
	#
	# ================================================================================== #
	'''

	#gravidade
	g = 9.8

	#vetor numero de onda a ser criado
	k = []

	#k anterior
	kant = 0.001

	#k posterior
	kpos = 0.0011

	for j in range(reg):
		sigma = (2*np.pi*deltaf[j])**2
		while abs(kpos - kant) > 0.001:
			kant = kpos
			dfk = g*kant*h*(1/np.cosh(kant*h))**2+g+np.tanh(kant*h)
			fk = g*kant*np.tanh(kant*h) - sigma
			kpos = kant - fk/dfk
		kant = kpos - 0.002
		k.append(kpos)
	return k


#Processamento no dominio do tempo
def ondat(t,eta,h):

	'''
	#======================================================================#
	#
	# Calcula parametros de onda no dominio do tempo
	#
	# Dados de entrada: t - vetor de tempo  
	#                   eta - vetor de elevacao
	#                   h - profundidade
	#
	# Dados de saida: pondat = [Hs,H10,Hmax,THmax,Tmed,]
	#				  Hs - altura significativa
	#                 H10 - altura de 1/10 das maiores
	#                 Hmax - altura maxima
	#                 THmax - periodo associado a altura maxima
	#                 Tmed - periodo medio
	#
	#======================================================================#
	'''

	#retira a media
	eta = eta - np.mean(eta)

	#criando os vetores H(altura),Cr(crista),Ca(cavado),T (periodo)
	Cr = []
	Ca = []
	H = []
	T = []

	#acha os indices que cruzam o zero
	z = np.where(np.diff(np.sign(eta)))[0]

	#zeros ascendentes e descendentes
	zas=z[0::2]
	zde=z[1::2]

	#calcula ondas individuas
	for i in range(0,len(zas)-1):
	    onda = eta[zas[i]:(zas[i+1])+1]
	    cr = np.max(onda)
	    Cr.append(cr)
	    ca = np.min(onda)
	    Ca.append(ca)
	    H.append(cr + np.abs(ca))
	    T.append(((zas[i+1])+1) - zas[i])

	#coloca as alturas em ordem crescente
	Hss = np.sort(H)
	Hss = np.flipud(Hss)

	#calcula a altura significativa (H 1/3)
	div = len(Hss) / 3
	Hs = np.mean(Hss[0:div+1])
	
	#calcula a altura das 1/10 maiores (H 1/10)
	div1 = len(Hss) / 10
	H10 = np.mean(Hss[0:div1+1]) #altura da media das um decimo maiores
	
	#altura maxima
	Hmax = np.max(H)
	
	#periodo medio
	Tmed = np.mean(T)
	
	#calcula periodo associado a altura maxima
	ind = np.where(H == Hmax)[0][0]
	THmax = T[ind]

	#parametros de onda no tempo
	pondat = np.array([Hs,H10,Hmax,Tmed,THmax])

	return Hs,H10,Hmax,Tmed,THmax

#Processamento no dominio da frequencia
def ondaf(eta,etax,etay,h,nfft,fs):

	"""
	#======================================================================#
	#
	# Calcula parametros de onda no dominio da frequencia
	#
	# Dados de entrada: eta - vetor de elevacao
	#                   etax - vetor de deslocamento em x
	#                   etay - vetor de deslocamento em y
	#					h - profundidade
	#					nfft - Numero de pontos utilizado para o calculo da FFT
	#                   fs - frequencia de amostragem
	#
	# Dados de saida: pondaf = [hm0 tp dp]	
	#
	#======================================================================#
	"""

	#espectro simples
	sn = espec1(eta,nfft,fs)
	snx = espec1(etax,nfft,fs)
	sny = espec1(etay,nfft,fs)

	#espectros cruzados
	snn = espec2(eta,eta,nfft,fs)
	snnx = espec2(eta,etax,nfft,fs)
	snny = espec2(eta,etay,nfft,fs)
	snxny = espec2(etax,etay,nfft,fs)
	snxnx = espec2(etax,etax,nfft,fs)
	snyny = espec2(etay,etay,nfft,fs)

	#vetor de frequencia
	f = sn[:,0]

	#deltaf
	df = f[1] - f[0]

	#calculo do numero de onda
	k = numeronda(h,f,len(f))
	k = np.array(k)

	#calculo dos coeficientes de fourier - NDBC 96_01 e Steele (1992)
	c = snx[:,1] + sny[:,1]
	cc = np.sqrt(sn[:,1] * (c))

	a1 = snnx[:,3] / cc
	b1 = snny[:,3] / cc

	a2 = (snx[:,1] - sny[:,1]) / c
	b2 = 2 * snxny[:,2] / c

	#calcula direcao de onda
	#mean direction
	dire1 = np.array([np.angle(np.complex(b1[i],a1[i]),deg=True) for i in range(len(a1))])

	#principal direction
	dire2 = 0.5 * np.array([np.angle(np.complex(b2[i],a2[i]),deg=True) for i in range(len(a2))])

	#condicao para valores maiores que 360 e menores que 0
	dire1[np.where(dire1 < 0)] = dire1[np.where(dire1 < 0)] + 360
	dire1[np.where(dire1 > 360)] = dire1[np.where(dire1 > 360)] - 360

	dire2[np.where(dire2 < 0)] = dire2[np.where(dire2 < 0)] + 360
	dire2[np.where(dire2 > 360)] = dire2[np.where(dire2 > 360)] - 360

	#acha o indice da frequencia de pico
	ind = np.where(sn[:,1] == np.max(sn[:,1]))[0]

	#periodo de pico
	tp = (1. / f[ind])[0]

	#momento espectral de ordem zero total - m0
	m0 = np.sum(sn[:,1]) * df

	#calculo da altura significativa
	hm0 = 4.01 * np.sqrt(m0)

	#direcao do periodo de pico
	dp = dire1[ind][0]

	#Espalhamento direcional
	#Formula do sigma1 do livro Tucker&Pitt(2001) "Waves in Ocean Engineering" pags 196-198
	c1 = np.sqrt(a1 ** 2 + b1 **2)
	c2 = np.sqrt(a2 ** 2 + b2 ** 2)
	
	s1 = c1 / (1-c1)
	s2 = (1 + 3 * c2 + np.sqrt(1 + 14 * c2 + c2 ** 2)) / (2 * (1 - c2))
	
	sigma1 = np.sqrt(2 - 2 * c1) * 180 / np.pi
	sigma2 = np.sqrt((1 - c2) / 2) * 180 / np.pi

	sigma1p = np.real(sigma1[ind])[0]
	sigma2p = np.real(sigma2[ind])[0]

	# pondaf = np.array([hm0, tp, dp, sigma1p, sigma2p])

	return hm0, tp, dp, sigma1p, sigma2p, f, df, k, sn, snx, sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2

def ondap(hm0,tp,dp,sn,dire1,df):

	'''
	# Programa para calcular parametros
	# de onda nas particoes de sea e swell
	#
	# desenvolvido para 32 gl
	#
	# divide o espectro em 2 partes: 
	# parte 1 - 8.33 a 50 seg
	# parte 2 - 1.56 a 7.14 seg
	#
	# calcula o periodo de pico de cada particao, e despreza o
	# pico 2 (menos energetico) se a energia for inferior a 15% da
	# energia do pico 1 (mais energetico)
	'''
	#vetor de frequencia e energia
	f,s = sn[:,[0,1]].T

	# seleciona os picos espectrais - considera somente 2 picos
	g1=np.diff(s)
	g1=np.sign(g1)
	g1=np.diff(g1)
	g1=np.concatenate(([0],g1))
	g2=np.where(g1==-2)[0]
	picos=1 # a principio e unimodal
	l=np.size(g2)

	# inicializar considerando ser unimodal
	hm02 = np.nan #9999
	tp2 = np.nan #9999
	dp2 = np.nan #9999
	hm01 = hm0
	tp1 = tp 
	dp1 = dp 

	if l > 1: #verificando espacamento entre picos (espacamento maior que 4 df)
		fr=np.argsort(s[g2])[::-1] #frequencia decrescente
		er=np.sort(s[g2])[::-1] # energia decrescente

		if (f[g2[fr[1]]]-f[g2[fr[0]]]) > 4*(f[1]-f[0]) and (er[1]/er[0] >= 0.15): #adota criterio de 4*deltaf
			picos=2
	    
	    # calcular o Hs dos picos pegando a cava e dividindo em pico 1 e pico 2
		if picos == 2:
			n1=g2[0] #pico mais energetico
			n2=g2[1] #pico menos energetico
			nc=np.where(g1[n1:n2]==2) #indice da cava

			#particao do swell e sea
			swell = range(n1+nc+1)
			sea = range(n1+nc+1,len(s))

			#maxima energia do swell
			esw = max(s[swell])

			#maxima energia do sea
			ese = max(s[sea])

			#indice do pico do swell
			isw = np.where(s==esw)[0][0]

			#indice do pico do sea
			ise = np.where(s==ese)[0][0]

			#altura sig. do swell
			hm0sw = 4.01 * np.sqrt(sum(s[swell]) * df)

			#altura sig. do sea
			hm0se = 4.01 * np.sqrt(sum(s[sea]) * df)

			#periodo de pico do swell
			tpsw = 1./f[isw]

			#periodo de pico do sea
			tpse = 1./f[ise]

			#direcao do swell
			dpsw = dire1[isw]

			#direcao do sea
			dpse = dire1[ise]

			#seleciona pico 1 como mais energetico
			# e pico 2 com o menos energetico
			if esw > ese:
				en1 = esw ; en2 = ese
				hm01 = hm0sw ; hm02 = hm0se
				tp1 = tpsw ; tp2 = tpse
				dp1 = dpsw ; dp2 = dpse
			else:
				en1 = ese ; en2 = esw
				hm01 = hm0se ; hm02 = hm0sw
				tp1 = tpse ; tp2 = tpsw
				dp1 = dpse ; dp2 = dpsw
        

      
	# pondaf1 = np.array([hm01, tp1, dp1, hm02, tp2, dp2])

	return hm01, tp1, dp1, hm02, tp2, dp2 #pondaf1



## Cria relatorio para ser impresso no terminal



def report(f,lista,listap,listac,listai,flagb,flagp,h,local,latlon,idargos,idwmo):


    # ================================================================================== #
    # Quantifica dados reprovados por teste
    # cria matriz de flags por variavel
    # ================================================================================== #


    # ================================================================================== #
    # flags dos dados brutos

    #heave
    feta = [] ; [feta.append(list(flagb[i,1])) for i in range(len(flagb))]
    feta = np.array(feta)
    #dsp.EO
    fetax = [] ; [fetax.append(list(flagb[i,2])) for i in range(len(flagb))]
    fetax = np.array(fetax)

    #dsp.NS
    fetay = [] ; [fetay.append(list(flagb[i,3])) for i in range(len(flagb))]
    fetay = np.array(fetay)

    # ================================================================================== #
    # quantifica flags dos dados brutos

    #eta
    etaa = np.zeros(feta.shape[1])
    etar = np.zeros(feta.shape[1])
    etas = np.zeros(feta.shape[1])

    #etax
    etaxa = np.zeros(fetax.shape[1])
    etaxr = np.zeros(fetax.shape[1])
    etaxs = np.zeros(fetax.shape[1])

    #etay
    etaya = np.zeros(fetay.shape[1])
    etayr = np.zeros(fetay.shape[1])
    etays = np.zeros(fetay.shape[1])

    #varia quantidade de testes
    for i in range(feta.shape[1]):

        #aprovados
        etaa[i] = len(np.where(feta[:,i] == '1')[0])
        etaxa[i] = len(np.where(fetax[:,i] == '1')[0])
        etaya[i] = len(np.where(fetay[:,i] == '1')[0])
        
        #suspeitos
        etas[i] = len(np.where(feta[:,i] == '3')[0])
        etaxs[i] = len(np.where(fetax[:,i] == '3')[0])
        etays[i] = len(np.where(fetay[:,i] == '3')[0])
        
        #reprovados
        etar[i] = len(np.where(feta[:,i] == '4')[0])
        etaxr[i] = len(np.where(fetax[:,i] == '4')[0])
        etayr[i] = len(np.where(fetay[:,i] == '4')[0])


    # ================================================================================== #
    # flags dados processados

    #hs
    fhs = [] ; [fhs.append(list(flagp[i,1])) for i in range(len(flagp))]
    fhs = np.array(fhs)

    #h10
    fh10 = [] ; [fh10.append(list(flagp[i,2])) for i in range(len(flagp))]
    fh10 = np.array(fh10)

    #hmax
    fhmax = [] ; [fhmax.append(list(flagp[i,3])) for i in range(len(flagp))]
    fhmax = np.array(fhmax)

    #tmed
    ftmed = [] ; [ftmed.append(list(flagp[i,4])) for i in range(len(flagp))]
    ftmed = np.array(ftmed)

    #thmax
    fthmax = [] ; [fthmax.append(list(flagp[i,5])) for i in range(len(flagp))]
    fthmax = np.array(fthmax)

    #hm0
    fhm0 = [] ; [fhm0.append(list(flagp[i,6])) for i in range(len(flagp))]
    fhm0 = np.array(fhm0)

    #tp
    ftp = [] ; [ftp.append(list(flagp[i,7])) for i in range(len(flagp))]
    ftp = np.array(ftp)

    #dp
    fdp = [] ; [fdp.append(list(flagp[i,8])) for i in range(len(flagp))]
    fdp = np.array(fdp)

    #sigma1p
    fsigma1p = [] ; [fsigma1p.append(list(flagp[i,9])) for i in range(len(flagp))]
    fsigma1p = np.array(fsigma1p)

    #sigma2p
    fsigma2p = [] ; [fsigma2p.append(list(flagp[i,10])) for i in range(len(flagp))]
    fsigma2p = np.array(fsigma2p)

    #hm01
    fhm01 = [] ; [fhm01.append(list(flagp[i,11])) for i in range(len(flagp))]
    fhm01 = np.array(fhm01)

    #tp1
    ftp1 = [] ; [ftp1.append(list(flagp[i,12])) for i in range(len(flagp))]
    ftp1 = np.array(ftp1)

    #tp1
    fdp1 = [] ; [fdp1.append(list(flagp[i,13])) for i in range(len(flagp))]
    fdp1 = np.array(fdp1)

    #hm02
    fhm02 = [] ; [fhm02.append(list(flagp[i,14])) for i in range(len(flagp))]
    fhm02 = np.array(fhm02)
    
    #tp1
    ftp2 = [] ; [ftp2.append(list(flagp[i,15])) for i in range(len(flagp))]
    ftp2 = np.array(ftp2)

    #dp1
    fdp2 = [] ; [fdp2.append(list(flagp[i,16])) for i in range(len(flagp))]
    fdp2 = np.array(fdp2)


    # ================================================================================== #
    # quantifica flags dos dados processados

    # aprovados
    hsa = np.zeros(fhs.shape[1])
    h10a = np.zeros(fh10.shape[1])
    hmaxa = np.zeros(fhmax.shape[1])
    tmeda = np.zeros(ftmed.shape[1])
    thmaxa = np.zeros(fthmax.shape[1])
    hm0a = np.zeros(fhm0.shape[1])
    tpa = np.zeros(ftp.shape[1])
    dpa = np.zeros(fdp.shape[1])
    sigma1pa = np.zeros(fsigma1p.shape[1])
    sigma2pa = np.zeros(fsigma2p.shape[1])
    hm01a = np.zeros(fhm01.shape[1])
    tp1a = np.zeros(ftp1.shape[1])
    dp1a = np.zeros(fdp1.shape[1])
    hm02a = np.zeros(fhm02.shape[1])
    tp2a = np.zeros(ftp2.shape[1])
    dp2a = np.zeros(fdp2.shape[1])

    #nao avaliado
    hsn = np.zeros(fhs.shape[1])
    h10n = np.zeros(fh10.shape[1])
    hmaxn = np.zeros(fhmax.shape[1])
    tmedn = np.zeros(ftmed.shape[1])
    thmaxn = np.zeros(fthmax.shape[1])
    hm0n = np.zeros(fhm0.shape[1])
    tpn = np.zeros(ftp.shape[1])
    dpn = np.zeros(fdp.shape[1])
    sigma1pn = np.zeros(fsigma1p.shape[1])
    sigma2pn = np.zeros(fsigma2p.shape[1])
    hm01n = np.zeros(fhm01.shape[1])
    tp1n = np.zeros(ftp1.shape[1])
    dp1n = np.zeros(fdp1.shape[1])
    hm02n = np.zeros(fhm02.shape[1])
    tp2n = np.zeros(ftp2.shape[1])
    dp2n = np.zeros(fdp2.shape[1])

    #suspeito
    hss = np.zeros(fhs.shape[1])
    h10s = np.zeros(fh10.shape[1])
    hmaxs = np.zeros(fhmax.shape[1])
    tmeds = np.zeros(ftmed.shape[1])
    thmaxs = np.zeros(fthmax.shape[1])
    hm0s = np.zeros(fhm0.shape[1])
    tps = np.zeros(ftp.shape[1])
    dps = np.zeros(fdp.shape[1])
    sigma1ps = np.zeros(fsigma1p.shape[1])
    sigma2ps = np.zeros(fsigma2p.shape[1])
    hm01s = np.zeros(fhm01.shape[1])
    tp1s = np.zeros(ftp1.shape[1])
    dp1s = np.zeros(fdp1.shape[1])
    hm02s = np.zeros(fhm02.shape[1])
    tp2s = np.zeros(ftp2.shape[1])
    dp2s = np.zeros(fdp2.shape[1])

    #reprovados
    hsr = np.zeros(fhs.shape[1])
    h10r = np.zeros(fh10.shape[1])
    hmaxr = np.zeros(fhmax.shape[1])
    tmedr = np.zeros(ftmed.shape[1])
    thmaxr = np.zeros(fthmax.shape[1])
    hm0r = np.zeros(fhm0.shape[1])
    tpr = np.zeros(ftp.shape[1])
    dpr = np.zeros(fdp.shape[1])
    sigma1pr = np.zeros(fsigma1p.shape[1])
    sigma2pr = np.zeros(fsigma2p.shape[1])
    hm01r = np.zeros(fhm01.shape[1])
    tp1r = np.zeros(ftp1.shape[1])
    dp1r = np.zeros(fdp1.shape[1])
    hm02r = np.zeros(fhm02.shape[1])
    tp2r = np.zeros(ftp2.shape[1])
    dp2r = np.zeros(fdp2.shape[1])

    #valor faltando
    hsf = np.zeros(fhs.shape[1])
    h10f = np.zeros(fh10.shape[1])
    hmaxf = np.zeros(fhmax.shape[1])
    tmedf = np.zeros(ftmed.shape[1])
    thmaxf = np.zeros(fthmax.shape[1])
    hm0f = np.zeros(fhm0.shape[1])
    tpf = np.zeros(ftp.shape[1])
    dpf = np.zeros(fdp.shape[1])
    sigma1pf = np.zeros(fsigma1p.shape[1])
    sigma2pf = np.zeros(fsigma2p.shape[1])
    hm01f = np.zeros(fhm01.shape[1])
    tp1f = np.zeros(ftp1.shape[1])
    dp1f = np.zeros(fdp1.shape[1])
    hm02f = np.zeros(fhm02.shape[1])
    tp2f = np.zeros(ftp2.shape[1])
    dp2f = np.zeros(fdp2.shape[1])

    #varia a quantidade de testes
    for i in range(fhs.shape[1]):

        #aprovados
        hsa[i] = len(np.where(fhs[:,i] == '1')[0])
        h10a[i] = len(np.where(fh10[:,i] == '1')[0])
        hmaxa[i] = len(np.where(fhmax[:,i] == '1')[0])
        tmeda[i] = len(np.where(ftmed[:,i] == '1')[0])
        thmaxa[i] = len(np.where(fthmax[:,i] == '1')[0])
        hm0a[i] = len(np.where(fhm0[:,i] == '1')[0])
        tpa[i] = len(np.where(ftp[:,i] == '1')[0])
        dpa[i] = len(np.where(fdp[:,i] == '1')[0])
        sigma1pa[i] = len(np.where(fsigma1p[:,i] == '1')[0])
        sigma2pa[i] = len(np.where(fsigma2p[:,i] == '1')[0])
        hm01a[i] = len(np.where(fhm01[:,i] == '1')[0])
        tp1a[i] = len(np.where(ftp1[:,i] == '1')[0])
        dp1a[i] = len(np.where(fdp1[:,i] == '1')[0])
        hm02a[i] = len(np.where(fhm02[:,i] == '1')[0])
        tp2a[i] = len(np.where(ftp2[:,i] == '1')[0])
        dp2a[i] = len(np.where(fdp2[:,i] == '1')[0])

        #nao avaliado
        hsn[i] = len(np.where(fhs[:,i] == '2')[0])
        h10n[i] = len(np.where(fh10[:,i] == '2')[0])
        hmaxn[i] = len(np.where(fhmax[:,i] == '2')[0])
        tmedn[i] = len(np.where(ftmed[:,i] == '2')[0])
        thmaxn[i] = len(np.where(fthmax[:,i] == '2')[0])
        hm0n[i] = len(np.where(fhm0[:,i] == '2')[0])
        tpn[i] = len(np.where(ftp[:,i] == '2')[0])
        dpn[i] = len(np.where(fdp[:,i] == '2')[0])
        sigma1pn[i] = len(np.where(fsigma1p[:,i] == '2')[0])
        sigma2pn[i] = len(np.where(fsigma2p[:,i] == '2')[0])
        hm01n[i] = len(np.where(fhm01[:,i] == '2')[0])
        tp1n[i] = len(np.where(ftp1[:,i] == '2')[0])
        dp1n[i] = len(np.where(fdp1[:,i] == '2')[0])
        hm02n[i] = len(np.where(fhm02[:,i] == '2')[0])
        tp2n[i] = len(np.where(ftp2[:,i] == '2')[0])
        dp2n[i] = len(np.where(fdp2[:,i] == '2')[0])

        #suspeitos
        hss[i] = len(np.where(fhs[:,i] == '3')[0])
        h10s[i] = len(np.where(fh10[:,i] == '3')[0])
        hmaxs[i] = len(np.where(fhmax[:,i] == '3')[0])
        tmeds[i] = len(np.where(ftmed[:,i] == '3')[0])
        thmaxs[i] = len(np.where(fthmax[:,i] == '3')[0])
        hm0s[i] = len(np.where(fhm0[:,i] == '3')[0])
        tps[i] = len(np.where(ftp[:,i] == '3')[0])
        dps[i] = len(np.where(fdp[:,i] == '3')[0])
        sigma1ps[i] = len(np.where(fsigma1p[:,i] == '3')[0])
        sigma2ps[i] = len(np.where(fsigma2p[:,i] == '3')[0])
        hm01s[i] = len(np.where(fhm01[:,i] == '3')[0])
        tp1s[i] = len(np.where(ftp1[:,i] == '3')[0])
        dp1s[i] = len(np.where(fdp1[:,i] == '3')[0])
        hm02s[i] = len(np.where(fhm02[:,i] == '3')[0])
        tp2s[i] = len(np.where(ftp2[:,i] == '3')[0])
        dp2s[i] = len(np.where(fdp2[:,i] == '3')[0])

        #dado reprovado
        hsr[i] = len(np.where(fhs[:,i] == '4')[0])
        h10r[i] = len(np.where(fh10[:,i] == '4')[0])
        hmaxr[i] = len(np.where(fhmax[:,i] == '4')[0])
        tmedr[i] = len(np.where(ftmed[:,i] == '4')[0])
        thmaxr[i] = len(np.where(fthmax[:,i] == '4')[0])
        hm0r[i] = len(np.where(fhm0[:,i] == '4')[0])
        tpr[i] = len(np.where(ftp[:,i] == '4')[0])
        dpr[i] = len(np.where(fdp[:,i] == '4')[0])
        sigma1pr[i] = len(np.where(fsigma1p[:,i] == '4')[0])
        sigma2pr[i] = len(np.where(fsigma2p[:,i] == '4')[0])
        hm01r[i] = len(np.where(fhm01[:,i] == '4')[0])
        tp1r[i] = len(np.where(ftp1[:,i] == '4')[0])
        dp1r[i] = len(np.where(fdp1[:,i] == '4')[0])
        hm02r[i] = len(np.where(fhm02[:,i] == '4')[0])
        tp2r[i] = len(np.where(ftp2[:,i] == '4')[0])
        dp2r[i] = len(np.where(fdp2[:,i] == '4')[0])


        #dado faltando
        hsf[i] = len(np.where(fhs[:,i] == '9')[0])
        h10f[i] = len(np.where(fh10[:,i] == '9')[0])
        hmaxf[i] = len(np.where(fhmax[:,i] == '9')[0])
        tmedf[i] = len(np.where(ftmed[:,i] == '9')[0])
        thmaxf[i] = len(np.where(fthmax[:,i] == '9')[0])
        hm0f[i] = len(np.where(fhm0[:,i] == '9')[0])
        tpf[i] = len(np.where(ftp[:,i] == '9')[0])
        dpf[i] = len(np.where(fdp[:,i] == '9')[0])
        sigma1pf[i] = len(np.where(fsigma1p[:,i] == '9')[0])
        sigma2pf[i] = len(np.where(fsigma2p[:,i] == '9')[0])
        hm01f[i] = len(np.where(fhm01[:,i] == '9')[0])
        tp1f[i] = len(np.where(ftp1[:,i] == '9')[0])
        dp1f[i] = len(np.where(fdp1[:,i] == '9')[0])
        hm02f[i] = len(np.where(fhm02[:,i] == '9')[0])
        tp2f[i] = len(np.where(ftp2[:,i] == '9')[0])
        dp2f[i] = len(np.where(fdp2[:,i] == '9')[0])


    # ================================================================================== #
    # Cria e salva relatorio

    regua1 = 50 * '-'
    regua2 = 50 * '='


    #salva relatorio
    print >> f, (

        'Relatorio de Controle de Qualidade de dados de Ondas \n'
        'Laboratorio de Instrumentacao Oceanografica - LIOc \n'
        'COPPE/UFRJ \n \n'

        'Boia Axys - PNBOIA/MB \n'
        'ID Argos: ' + str(idargos) + '\n'
        'ID WMO: ' + str(idwmo) + '\n'
        'Localizacao: ' + local + '\n'
        'Lat/Lon: ' + latlon + '\n'
        'Profundidade: ' + str(h) + ' m \n'
        'Data inicial: ' + listap[0][6:8]+'/'+listap[0][4:6]+'/'+listap[0][0:4]+' - '+listap[0][8:10]+':'+listap[0][10:12] + '\n'
        'Data final: '   + listap[-1][6:8]+'/'+listap[-1][4:6]+'/'+listap[-1][0:4]+' - '+listap[-1][8:10]+':'+listap[-1][10:12] + '\n \n'

        'Numero de arquivos listados no diretorio: ' + str(len(lista)) + '\n'
        'Numero de series analisadas: '              + str(len(listap)) + '\n'
        'Numero de series aprovadas no CQ de Curto-Termo: '          + str(len(listac)) + '\n'
        'Numero de series reprovadas no CQ de Curto-Termo: '          + str(len(listai)) + '\n \n'

        'Numero de Testes de CQ:' '\n'
        '- Brutos: '      + str(len(flagb[0][1])) + '\n'
        '- Processados: ' + str(len(flagp[0][1])) + '\n'


        # ================================================================================== #


        '\n' + regua2 + '\n'
        'Consistencia dos dados brutos'
        '\n' + regua2 + '\n'

        '\n' + regua1 + '\n'
        '** Teste 1 - Mensagem recebida **' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[0])) + '\n'
        'Suspeito: ' + str(int(etas[0])) + '\n'
        'Reprovado: ' + str(int(etar[0])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[0])) + '\n'
        'Suspeito: ' + str(int(etaxs[0])) + '\n'
        'Reprovado: ' + str(int(etaxr[0])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[0])) + '\n'
        'Suspeito: ' + str(int(etays[0])) + '\n'
        'Reprovado: ' + str(int(etayr[0])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 2 - Comprimento da serie ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[1])) + '\n'
        'Suspeito: ' + str(int(etas[1])) + '\n'
        'Reprovado: ' + str(int(etar[1])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[1])) + '\n'
        'Suspeito: ' + str(int(etaxs[1])) + '\n'
        'Reprovado: ' + str(int(etaxr[1])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[1])) + '\n'
        'Suspeito: ' + str(int(etays[1])) + '\n'
        'Reprovado: ' + str(int(etayr[1])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 3 - Lacuna (Gap) ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[2])) + '\n'
        'Suspeito: ' + str(int(etas[2])) + '\n'
        'Reprovado: ' + str(int(etar[2])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[2])) + '\n'
        'Suspeito: ' + str(int(etaxs[2])) + '\n'
        'Reprovado: ' + str(int(etaxr[2])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[2])) + '\n'
        'Suspeito: ' + str(int(etays[2])) + '\n'
        'Reprovado: ' + str(int(etayr[2])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 4 - Spike ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[3])) + '\n'
        'Suspeito: ' + str(int(etas[3])) + '\n'
        'Reprovado: ' + str(int(etar[3])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[3])) + '\n'
        'Suspeito: ' + str(int(etaxs[3])) + '\n'
        'Reprovado: ' + str(int(etaxr[3])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[3])) + '\n'
        'Suspeito: ' + str(int(etays[3])) + '\n'
        'Reprovado: ' + str(int(etayr[3])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 5 - Flat ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[4])) + '\n'
        'Suspeito: ' + str(int(etas[4])) + '\n'
        'Reprovado: ' + str(int(etar[4])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[4])) + '\n'
        'Suspeito: ' + str(int(etaxs[4])) + '\n'
        'Reprovado: ' + str(int(etaxr[4])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[4])) + '\n'
        'Suspeito: ' + str(int(etays[4])) + '\n'
        'Reprovado: ' + str(int(etayr[4])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 6 - Consec. Nulos ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[5])) + '\n'
        'Suspeito: ' + str(int(etas[5])) + '\n'
        'Reprovado: ' + str(int(etar[5])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[5])) + '\n'
        'Suspeito: ' + str(int(etaxs[5])) + '\n'
        'Reprovado: ' + str(int(etaxr[5])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[5])) + '\n'
        'Suspeito: ' + str(int(etays[5])) + '\n'
        'Reprovado: ' + str(int(etayr[1])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 7 - Consec. Iguais ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[6])) + '\n'
        'Suspeito: ' + str(int(etas[6])) + '\n'
        'Reprovado: ' + str(int(etar[6])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[6])) + '\n'
        'Suspeito: ' + str(int(etaxs[6])) + '\n'
        'Reprovado: ' + str(int(etaxr[6])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[6])) + '\n'
        'Suspeito: ' + str(int(etays[6])) + '\n'
        'Reprovado: ' + str(int(etayr[6])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 8 - Faixa ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[7])) + '\n'
        'Suspeito: ' + str(int(etas[7])) + '\n'
        'Reprovado: ' + str(int(etar[7])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[7])) + '\n'
        'Suspeito: ' + str(int(etaxs[7])) + '\n'
        'Reprovado: ' + str(int(etaxr[7])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[7])) + '\n'
        'Suspeito: ' + str(int(etays[7])) + '\n'
        'Reprovado: ' + str(int(etayr[7])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 9 - Shift ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[8])) + '\n'
        'Suspeito: ' + str(int(etas[8])) + '\n'
        'Reprovado: ' + str(int(etar[8])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[8])) + '\n'
        'Suspeito: ' + str(int(etaxs[8])) + '\n'
        'Reprovado: ' + str(int(etaxr[8])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[8])) + '\n'
        'Suspeito: ' + str(int(etays[8])) + '\n'
        'Reprovado: ' + str(int(etayr[8])) + '\n \n'


        # ================================================================================== #

        '\n' + regua2 + '\n'
        'Consistencia dos dados processados'
        '\n' + regua2 + '\n'


        '\n' + regua1 + '\n'
        '** Teste 1 - Faixa **' '\n \n'

        '-- Hs --' '\n'
        'Aprovado: ' + str(int(hsa[0])) + '\n'
        'Faltando: ' + str(int(hsf[0])) + '\n'
        'Suspeito: ' + str(int(hss[0])) + '\n'
        'Reprovado: ' + str(int(hsr[0])) + '\n'
        'Nao avaliado: ' + str(int(hsn[0])) + '\n \n'

        '-- H1/10 --' '\n'
        'Aprovado: ' + str(int(h10a[0])) + '\n'
        'Faltando: ' + str(int(h10f[0])) + '\n'
        'Suspeito: ' + str(int(h10s[0])) + '\n'
        'Reprovado: ' + str(int(h10r[0])) + '\n'
        'Nao avaliado: ' + str(int(h10n[0])) + '\n \n'

        '-- Hmax --' '\n'
        'Aprovado: ' + str(int(hmaxa[0])) + '\n'
        'Faltando: ' + str(int(hmaxf[0])) + '\n'
        'Suspeito: ' + str(int(hmaxs[0])) + '\n'
        'Reprovado: ' + str(int(hmaxr[0])) + '\n'
        'Nao avaliado: ' + str(int(hmaxn[0])) + '\n \n'

        '-- Tmed --' '\n'
        'Aprovado: ' + str(int(tmeda[0])) + '\n'
        'Faltando: ' + str(int(tmedf[0])) + '\n'
        'Suspeito: ' + str(int(tmeds[0])) + '\n'
        'Reprovado: ' + str(int(tmedr[0])) + '\n'
        'Nao avaliado: ' + str(int(tmedn[0])) + '\n \n'

        '-- THmax --' '\n'
        'Aprovado: ' + str(int(thmaxa[0])) + '\n'
        'Faltando: ' + str(int(thmaxf[0])) + '\n'
        'Suspeito: ' + str(int(thmaxs[0])) + '\n'
        'Reprovado: ' + str(int(thmaxr[0])) + '\n'
        'Nao avaliado: ' + str(int(thmaxn[0])) + '\n \n'

        '-- Hm0 --' '\n'
        'Aprovado: ' + str(int(hm0a[0])) + '\n'
        'Faltando: ' + str(int(hm0f[0])) + '\n'
        'Suspeito: ' + str(int(hm0s[0])) + '\n'
        'Reprovado: ' + str(int(hm0r[0])) + '\n'
        'Nao avaliado: ' + str(int(hm0n[0])) + '\n \n'

        '-- Tp --' '\n'
        'Aprovado: ' + str(int(tpa[0])) + '\n'
        'Faltando: ' + str(int(tpf[0])) + '\n'
        'Suspeito: ' + str(int(tps[0])) + '\n'
        'Reprovado: ' + str(int(tpr[0])) + '\n'
        'Nao avaliado: ' + str(int(tpn[0])) + '\n \n'

        '-- Dp --' '\n'
        'Aprovado: ' + str(int(dpa[0])) + '\n'
        'Faltando: ' + str(int(dpf[0])) + '\n'
        'Suspeito: ' + str(int(dps[0])) + '\n'
        'Reprovado: ' + str(int(dpr[0])) + '\n'
        'Nao avaliado: ' + str(int(dpn[0])) + '\n \n'

        '-- Sigma1p --' '\n'
        'Aprovado: ' + str(int(sigma1pa[0])) + '\n'
        'Faltando: ' + str(int(sigma1pf[0])) + '\n'
        'Suspeito: ' + str(int(sigma1ps[0])) + '\n'
        'Reprovado: ' + str(int(sigma1pr[0])) + '\n'
        'Nao avaliado: ' + str(int(sigma1pn[0])) + '\n \n'

        '-- Sigma2p --' '\n'
        'Aprovado: ' + str(int(sigma2pa[0])) + '\n'
        'Faltando: ' + str(int(sigma2pf[0])) + '\n'
        'Suspeito: ' + str(int(sigma2ps[0])) + '\n'
        'Reprovado: ' + str(int(sigma2pr[0])) + '\n'
        'Nao avaliado: ' + str(int(sigma2pn[0])) + '\n \n'

        '-- Hm01 / Hm02 --' '\n'
        'Aprovado: ' + str(int(hm01a[0])) + '\n'
        'Faltando: ' + str(int(hm01f[0])) + '\n'
        'Suspeito: ' + str(int(hm01s[0])) + '\n'
        'Reprovado: ' + str(int(hm01r[0])) + '\n'
        'Nao avaliado: ' + str(int(hm01n[0])) + '\n \n'

        '-- Tp1 / Tp2 --' '\n'
        'Aprovado: ' + str(int(tp1a[0])) + '\n'
        'Faltando: ' + str(int(tp1f[0])) + '\n'
        'Suspeito: ' + str(int(tp1s[0])) + '\n'
        'Reprovado: ' + str(int(tp1r[0])) + '\n'
        'Nao avaliado: ' + str(int(tp1n[0])) + '\n \n'

        '-- Dp1 / Dp2 --' '\n'
        'Aprovado: ' + str(int(dp1a[0])) + '\n'
        'Faltando: ' + str(int(dp1f[0])) + '\n'
        'Suspeito: ' + str(int(dp1s[0])) + '\n'
        'Reprovado: ' + str(int(dp1r[0])) + '\n'
        'Nao avaliado: ' + str(int(dp1n[0])) + '\n \n'

        # '-- Hm02 --' '\n'
        # 'Aprovado: ' + str(int(hm02a[0])) + '\n'
        # 'Faltando: ' + str(int(hm02f[0])) + '\n'
        # 'Suspeito: ' + str(int(hm02s[0])) + '\n'
        # 'Reprovado: ' + str(int(hm02r[0])) + '\n'
        # 'Nao avaliado: ' + str(int(hm02n[0])) + '\n \n'

        # '-- Tp2 --' '\n'
        # 'Aprovado: ' + str(int(tp2a[0])) + '\n'
        # 'Faltando: ' + str(int(tp2f[0])) + '\n'
        # 'Suspeito: ' + str(int(tp2s[0])) + '\n'
        # 'Reprovado: ' + str(int(tp2r[0])) + '\n'
        # 'Nao avaliado: ' + str(int(tp2n[0])) + '\n \n'

        # '-- Dp2 --' '\n'
        # 'Aprovado: ' + str(int(dp2a[0])) + '\n'
        # 'Faltando: ' + str(int(dp2f[0])) + '\n'
        # 'Suspeito: ' + str(int(dp2s[0])) + '\n'
        # 'Reprovado: ' + str(int(dp2r[0])) + '\n'
        # 'Nao avaliado: ' + str(int(dp2n[0])) + '\n \n'


        # ================================================================================== #

        '\n' + regua1 + '\n'
        '** Teste 2 - Variabilidade Temporal ** ' '\n \n'


        '-- Hs --' '\n'
        'Aprovado: ' + str(int(hsa[1])) + '\n'
        'Faltando: ' + str(int(hsf[1])) + '\n'
        'Suspeito: ' + str(int(hss[1])) + '\n'
        'Reprovado: ' + str(int(hsr[1])) + '\n'
        'Nao avaliado: ' + str(int(hsn[1])) + '\n \n'

        '-- H1/10 --' '\n'
        'Aprovado: ' + str(int(h10a[1])) + '\n'
        'Faltando: ' + str(int(h10f[1])) + '\n'
        'Suspeito: ' + str(int(h10s[1])) + '\n'
        'Reprovado: ' + str(int(h10r[1])) + '\n'
        'Nao avaliado: ' + str(int(h10n[1])) + '\n \n'

        '-- Hmax --' '\n'
        'Aprovado: ' + str(int(hmaxa[1])) + '\n'
        'Faltando: ' + str(int(hmaxf[1])) + '\n'
        'Suspeito: ' + str(int(hmaxs[1])) + '\n'
        'Reprovado: ' + str(int(hmaxr[1])) + '\n'
        'Nao avaliado: ' + str(int(hmaxn[1])) + '\n \n'

        '-- Tmed --' '\n'
        'Aprovado: ' + str(int(tmeda[1])) + '\n'
        'Faltando: ' + str(int(tmedf[1])) + '\n'
        'Suspeito: ' + str(int(tmeds[1])) + '\n'
        'Reprovado: ' + str(int(tmedr[1])) + '\n'
        'Nao avaliado: ' + str(int(tmedn[1])) + '\n \n'

        '-- THmax --' '\n'
        'Aprovado: ' + str(int(thmaxa[1])) + '\n'
        'Faltando: ' + str(int(thmaxf[1])) + '\n'
        'Suspeito: ' + str(int(thmaxs[1])) + '\n'
        'Reprovado: ' + str(int(thmaxr[1])) + '\n'
        'Nao avaliado: ' + str(int(thmaxn[1])) + '\n \n'

        '-- Hm0 --' '\n'
        'Aprovado: ' + str(int(hm0a[1])) + '\n'
        'Faltando: ' + str(int(hm0f[1])) + '\n'
        'Suspeito: ' + str(int(hm0s[1])) + '\n'
        'Reprovado: ' + str(int(hm0r[1])) + '\n'
        'Nao avaliado: ' + str(int(hm0n[1])) + '\n \n'

        '-- Tp --' '\n'
        'Aprovado: ' + str(int(tpa[1])) + '\n'
        'Faltando: ' + str(int(tpf[1])) + '\n'
        'Suspeito: ' + str(int(tps[1])) + '\n'
        'Reprovado: ' + str(int(tpr[1])) + '\n'
        'Nao avaliado: ' + str(int(tpn[1])) + '\n \n'

        '-- Dp --' '\n'
        'Aprovado: ' + str(int(dpa[1])) + '\n'
        'Faltando: ' + str(int(dpf[1])) + '\n'
        'Suspeito: ' + str(int(dps[1])) + '\n'
        'Reprovado: ' + str(int(dpr[1])) + '\n'
        'Nao avaliado: ' + str(int(dpn[1])) + '\n \n'

        '-- Sigma1p --' '\n'
        'Aprovado: ' + str(int(sigma1pa[1])) + '\n'
        'Faltando: ' + str(int(sigma1pf[1])) + '\n'
        'Suspeito: ' + str(int(sigma1ps[1])) + '\n'
        'Reprovado: ' + str(int(sigma1pr[1])) + '\n'
        'Nao avaliado: ' + str(int(sigma1pn[1])) + '\n \n'

        '-- Sigma2p --' '\n'
        'Aprovado: ' + str(int(sigma2pa[1])) + '\n'
        'Faltando: ' + str(int(sigma2pf[1])) + '\n'
        'Suspeito: ' + str(int(sigma2ps[1])) + '\n'
        'Reprovado: ' + str(int(sigma2pr[1])) + '\n'
        'Nao avaliado: ' + str(int(sigma2pn[1])) + '\n \n'

        '-- Hm01 / Hm02 --' '\n'
        'Aprovado: ' + str(int(hm01a[1])) + '\n'
        'Faltando: ' + str(int(hm01f[1])) + '\n'
        'Suspeito: ' + str(int(hm01s[1])) + '\n'
        'Reprovado: ' + str(int(hm01r[1])) + '\n'
        'Nao avaliado: ' + str(int(hm01n[1])) + '\n \n'

        '-- Tp1 / Tp2 --' '\n'
        'Aprovado: ' + str(int(tp1a[1])) + '\n'
        'Faltando: ' + str(int(tp1f[1])) + '\n'
        'Suspeito: ' + str(int(tp1s[1])) + '\n'
        'Reprovado: ' + str(int(tp1r[1])) + '\n'
        'Nao avaliado: ' + str(int(tp1n[1])) + '\n \n'

        '-- Dp1 / Dp2 --' '\n'
        'Aprovado: ' + str(int(dp1a[1])) + '\n'
        'Faltando: ' + str(int(dp1f[1])) + '\n'
        'Suspeito: ' + str(int(dp1s[1])) + '\n'
        'Reprovado: ' + str(int(dp1r[1])) + '\n'
        'Nao avaliado: ' + str(int(dp1n[1])) + '\n \n'


        # '-- Hm02 --' '\n'
        # 'Aprovado: ' + str(int(hm02a[1])) + '\n'
        # 'Faltando: ' + str(int(hm02f[1])) + '\n'
        # 'Suspeito: ' + str(int(hm02s[1])) + '\n'
        # 'Reprovado: ' + str(int(hm02r[1])) + '\n'
        # 'Nao avaliado: ' + str(int(hm02n[1])) + '\n \n'

        # '-- Tp2 --' '\n'
        # 'Aprovado: ' + str(int(tp2a[1])) + '\n'
        # 'Faltando: ' + str(int(tp2f[1])) + '\n'
        # 'Suspeito: ' + str(int(tp2s[1])) + '\n'
        # 'Reprovado: ' + str(int(tp2r[1])) + '\n'
        # 'Nao avaliado: ' + str(int(tp2n[1])) + '\n \n'

        # '-- Dp2 --' '\n'
        # 'Aprovado: ' + str(int(dp2a[1])) + '\n'
        # 'Faltando: ' + str(int(dp2f[1])) + '\n'
        # 'Suspeito: ' + str(int(dp2s[1])) + '\n'
        # 'Reprovado: ' + str(int(dp2r[1])) + '\n'
        # 'Nao avaliado: ' + str(int(dp2n[1])) + '\n \n'


        # ================================================================================== #

        '\n' + regua1 + '\n'
        '** Teste 3 - Conec. Iguais **' '\n \n'


        '-- Hs --' '\n'
        'Aprovado: ' + str(int(hsa[2])) + '\n'
        'Faltando: ' + str(int(hsf[2])) + '\n'
        'Suspeito: ' + str(int(hss[2])) + '\n'
        'Reprovado: ' + str(int(hsr[2])) + '\n'
        'Nao avaliado: ' + str(int(hsn[2])) + '\n \n'

        '-- H1/10 --' '\n'
        'Aprovado: ' + str(int(h10a[2])) + '\n'
        'Faltando: ' + str(int(h10f[2])) + '\n'
        'Suspeito: ' + str(int(h10s[2])) + '\n'
        'Reprovado: ' + str(int(h10r[2])) + '\n'
        'Nao avaliado: ' + str(int(h10n[2])) + '\n \n'

        '-- Hmax --' '\n'
        'Aprovado: ' + str(int(hmaxa[2])) + '\n'
        'Faltando: ' + str(int(hmaxf[2])) + '\n'
        'Suspeito: ' + str(int(hmaxs[2])) + '\n'
        'Reprovado: ' + str(int(hmaxr[2])) + '\n'
        'Nao avaliado: ' + str(int(hmaxn[2])) + '\n \n'

        '-- Tmed --' '\n'
        'Aprovado: ' + str(int(tmeda[2])) + '\n'
        'Faltando: ' + str(int(tmedf[2])) + '\n'
        'Suspeito: ' + str(int(tmeds[2])) + '\n'
        'Reprovado: ' + str(int(tmedr[2])) + '\n'
        'Nao avaliado: ' + str(int(tmedn[2])) + '\n \n'

        '-- THmax --' '\n'
        'Aprovado: ' + str(int(thmaxa[2])) + '\n'
        'Faltando: ' + str(int(thmaxf[2])) + '\n'
        'Suspeito: ' + str(int(thmaxs[2])) + '\n'
        'Reprovado: ' + str(int(thmaxr[2])) + '\n'
        'Nao avaliado: ' + str(int(thmaxn[2])) + '\n \n'

        '-- Hm0 --' '\n'
        'Aprovado: ' + str(int(hm0a[2])) + '\n'
        'Faltando: ' + str(int(hm0f[2])) + '\n'
        'Suspeito: ' + str(int(hm0s[2])) + '\n'
        'Reprovado: ' + str(int(hm0r[2])) + '\n'
        'Nao avaliado: ' + str(int(hm0n[2])) + '\n \n'

        '-- Tp --' '\n'
        'Aprovado: ' + str(int(tpa[2])) + '\n'
        'Faltando: ' + str(int(tpf[2])) + '\n'
        'Suspeito: ' + str(int(tps[2])) + '\n'
        'Reprovado: ' + str(int(tpr[2])) + '\n'
        'Nao avaliado: ' + str(int(tpn[2])) + '\n \n'

        '-- Dp --' '\n'
        'Aprovado: ' + str(int(dpa[2])) + '\n'
        'Faltando: ' + str(int(dpf[2])) + '\n'
        'Suspeito: ' + str(int(dps[2])) + '\n'
        'Reprovado: ' + str(int(dpr[2])) + '\n'
        'Nao avaliado: ' + str(int(dpn[2])) + '\n \n'

        '-- Sigma1p --' '\n'
        'Aprovado: ' + str(int(sigma1pa[2])) + '\n'
        'Faltando: ' + str(int(sigma1pf[2])) + '\n'
        'Suspeito: ' + str(int(sigma1ps[2])) + '\n'
        'Reprovado: ' + str(int(sigma1pr[2])) + '\n'
        'Nao avaliado: ' + str(int(sigma1pn[2])) + '\n \n'

        '-- Sigma2p --' '\n'
        'Aprovado: ' + str(int(sigma2pa[2])) + '\n'
        'Faltando: ' + str(int(sigma2pf[2])) + '\n'
        'Suspeito: ' + str(int(sigma2ps[2])) + '\n'
        'Reprovado: ' + str(int(sigma2pr[2])) + '\n'
        'Nao avaliado: ' + str(int(sigma2pn[2])) + '\n \n'

        '-- Hm01 / Hm02--' '\n'
        'Aprovado: ' + str(int(hm01a[2])) + '\n'
        'Faltando: ' + str(int(hm01f[2])) + '\n'
        'Suspeito: ' + str(int(hm01s[2])) + '\n'
        'Reprovado: ' + str(int(hm01r[2])) + '\n'
        'Nao avaliado: ' + str(int(hm01n[2])) + '\n \n'

        '-- Tp1 / Tp2 --' '\n'
        'Aprovado: ' + str(int(tp1a[2])) + '\n'
        'Faltando: ' + str(int(tp1f[2])) + '\n'
        'Suspeito: ' + str(int(tp1s[2])) + '\n'
        'Reprovado: ' + str(int(tp1r[2])) + '\n'
        'Nao avaliado: ' + str(int(tp1n[2])) + '\n \n'

        '-- Dp1 / Dp1 --' '\n'
        'Aprovado: ' + str(int(dp1a[2])) + '\n'
        'Faltando: ' + str(int(dp1f[2])) + '\n'
        'Suspeito: ' + str(int(dp1s[2])) + '\n'
        'Reprovado: ' + str(int(dp1r[2])) + '\n'
        'Nao avaliado: ' + str(int(dp1n[2])) + '\n \n'

        # '-- Hm02 --' '\n'
        # 'Aprovado: ' + str(int(hm02a[2])) + '\n'
        # 'Faltando: ' + str(int(hm02f[2])) + '\n'
        # 'Suspeito: ' + str(int(hm02s[2])) + '\n'
        # 'Reprovado: ' + str(int(hm02r[2])) + '\n'
        # 'Nao avaliado: ' + str(int(hm02n[2])) + '\n \n'

        # '-- Tp2 --' '\n'
        # 'Aprovado: ' + str(int(tp2a[2])) + '\n'
        # 'Faltando: ' + str(int(tp2f[2])) + '\n'
        # 'Suspeito: ' + str(int(tp2s[2])) + '\n'
        # 'Reprovado: ' + str(int(tp2r[2])) + '\n'
        # 'Nao avaliado: ' + str(int(tp2n[2])) + '\n \n'

        # '-- Dp2 --' '\n'
        # 'Aprovado: ' + str(int(dp2a[2])) + '\n'
        # 'Faltando: ' + str(int(dp2f[2])) + '\n'
        # 'Suspeito: ' + str(int(dp2s[2])) + '\n'
        # 'Reprovado: ' + str(int(dp2r[2])) + '\n'
        # 'Nao avaliado: ' + str(int(dp2n[2])) + '\n \n'


        # ================================================================================== #

    )
    f.close()

    # flag com resltado da quantidade de flags (9x9 -- linha=variaveis (ex:l1 = etaa, l2=etas ..) x coluna=testes (ex:c1=t2, c2=t2 ..))
    fflagb = np.concatenate([(etaa, etas, etar, etaxa, etaxs, etaxr, etaya, etays, etayr)])
    fflagp = np.concatenate([(fhs,fh10,fhmax,ftmed,fthmax,fhm0,ftp,fdp,fsigma1p,fsigma2p,fhm01,ftp1,fdp1,fhm02,ftp2,fdp2)])

    return fflagb, fflagp




'''
Espectro de JONSWAP

- Calculo do GAMMA
- Ajusta o Espectro
'''

import numpy as np
from numpy import (inf, atleast_1d, newaxis, any, minimum, maximum, array, #@UnresolvedImport
    asarray, exp, log, sqrt, where, pi, arange, linspace, sin, cos, abs, sinh, #@UnresolvedImport
    isfinite, mod, expm1, tanh, cosh, finfo, ones, ones_like, isnan, #@UnresolvedImport
    zeros_like, flatnonzero, sinc, hstack, vstack, real, flipud, clip) #@UnresolvedImport


def jonswap_peakfact(Hm0, Tp):
    ''' Jonswap peakedness factor, gamma, given Hm0 and Tp

    Parameters
    ----------
    Hm0 : significant wave height [m].
    Tp  : peak period [s]

    Returns
    -------
    gamma : Peakedness parameter of the JONSWAP spectrum

    Details
    -------
    A standard value for GAMMA is 3.3. However, a more correct approach is
    to relate GAMMA to Hm0 and Tp:
         D = 0.036-0.0056*Tp/sqrt(Hm0)
        gamma = exp(3.484*(1-0.1975*D*Tp**4/(Hm0**2)))
    This parameterization is based on qualitative considerations of deep water
    wave data from the North Sea, see Torsethaugen et. al. (1984)
    Here GAMMA is limited to 1..7.

    NOTE: The size of GAMMA is the common shape of Hm0 and Tp.

    Examples
    --------
    import pylab as plb
    Tp,Hs = plb.meshgrid(range(4,8),range(2,6))
    gam = jonswap_peakfact(Hs,Tp)

    Hm0 = plb.linspace(1,20)
    Tp = Hm0
    [T,H] = plb.meshgrid(Tp,Hm0)
    gam = jonswap_peakfact(H,T)
    v = plb.arange(0,8)
    h = plb.contourf(Tp,Hm0,gam,v);h=plb.colorbar()

    Hm0 = plb.arange(1,11)
    Tp  = plb.linspace(2,16)
    T,H = plb.meshgrid(Tp,Hm0)
    gam = jonswap_peakfact(H,T)
    h = plb.plot(Tp,gam.T)
    h = plb.xlabel('Tp [s]')
    h = plb.ylabel('Peakedness parameter')

    >>> plb.close('all')

    See also
    --------
    jonswap
    '''
    Hm0, Tp = atleast_1d(Hm0, Tp)

    x = Tp / sqrt(Hm0)

    gam = ones_like(x)

    k1 = flatnonzero(x <= 5.14285714285714)
    if k1.size > 0: # #limiting gamma to [1 7]
        xk = x.take(k1)
        D = 0.036 - 0.0056 * xk # # approx 5.061*Hm0**2/Tp**4*(1-0.287*log(gam))
        gam.put(k1, minimum(exp(3.484 * (1.0 - 0.1975 * D * xk ** 4.0)), 7.0)) # # gamma

    return gam


def jonswap_gamma(tp):
	'''
	calculo do parametro gamma
	'''

	gam = 6.4 * ( tp ** (-0.491) )

	return gam

def jonswap_spec(hs,tp,f,gam):
	'''
	ajuste do espectro de JONSWAP
	'''

	#frequencia de pico
	fp = 1./tp

	s_js = np.zeros(len(f))

	for i in range(len(f)):

		if f[i] <= fp:

			sigm = 0.07

			s_js[i] = (5./16) * (hs**2) * tp * (fp/f[i])**5 * (1-0.287*np.log(gam)) * np.exp(-1.25*(f[i]/fp)**(-4)) * gam ** ( np.exp(-(f[i]-fp)**2/(2*sigm**2*fp**2)) )

		elif f[i] > fp:

			sigm = 0.09


			s_js[i] = (5./16) * (hs**2) * tp * (fp/f[i])**5 * (1-0.287*np.log(gam)) * np.exp(-1.25*(f[i]/fp)**(-4)) * gam ** ( np.exp(-(f[i]-fp)**2/(2*sigm**2*fp**2)) )

	return s_js











# ================================================================================== #
# Teste 1

def cqbruto_msg(arq,flag):
    
    '''

    VALIDADE DA MENSAGEM RECEBIDA  (Boias Axys)
    * Ex: 200905101100.HNE
    * Verifica se os minutos estao igual a '00'
    * Para dados programados para serem enviados em hora cheia (min=00)
    
    Dados de entrada: arq - nome do arquivo
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Posicao (indice) em 'lista_flag' : 0
    Aprovado  : flag = '1'
    Reprovado : flag = '4'
    
    '''
		
    if arq[10:12] <> '00':

        flag = flag + '4'
        
    else:
        
        flag = flag + '1'
        
    return flag

# ================================================================================== #
# Teste 2

def cqbruto_comp(serie,cs,flag): #modificar a entrada para entrar com qlq tamanho de vetor, devido aos tbm dados meteorologicos
    
    '''

    COMPRIMENTO DA SERIE
    * Verifica se o comprimento da serie eh menor que 1313
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Posicao (indice) em 'lista_flag' : 1
    Aprovado  : flag = '1'
    Reprovado : flag = '4'
    
    '''
    
    #2- verifica comprimento do vetor
    if len(serie) < cs:

        flag = flag + '4'
        
    else:
        
        flag = flag + '1'
        
    return flag

# ================================================================================== #
# Teste 3

def cqbruto_gap(serie,N,flag):
    
    '''

    TESTE DE GAP
    * Verifica valores consecutivos faltando
    
    Dados de entrada: serie - (ex: elevacao, deslocamento ..)
                      N - numero de valores consecutivos aceitaveis para estar
                      faltando
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Aprovado  : flag = '1'
    Reprovado : flag = '4'
    
    '''
    
    for i in range(len(serie)-N):
        
        if np.isnan(serie[i:i+N]).all() == True:

            flag = flag + '4'
            
            #se achou um gap, para o teste
            break

    if flag <> '4':

        flag = flag + '1'

    return flag


# ================================================================================== #
# Teste 4

def cqbruto_spike(serie,med,dp,N,M,P,flag):
    
    '''

    TESTE DE SPIKE
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      med - média da série
                      dp - desvio padrão da série
                      N% - limite total de spikes
                      M - multiplicador do dp
                      P - numero de iteracoes
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Aprovado  : flag = '1'
    Reprovado : flag = '4'
    
    '''

    #retira o primeiro e ultimo valor, caso o spike ocorra nessas
    #posicoes, nao sera editado, pois da erro (melhorar)
    vetc = cp.copy(serie)

    #M1 = 0
    #M2 = 0
    #quantidade maxima de spikes
    N = len(serie) * N / 100 #transforma em %

    #procura valores na serie maior do que o limite
    sp = pl.find(np.abs(serie) > (M * dp) )
    
    #verifica quantidade total de spikes
    M1 = len(sp)

    #valor inicial para numero de spikes (caso tenha spikes sera incrementada durante o programa)
    M2 = 0

    # ----------------#
    # Realiza edicoes #

    #se a quantidade de spikes for maior que zero
    if M1 > 0:

        #numero de vezes que serao realizadas edicoes (retirada de spikes)
        for j in range(P):

            #recalcula o numero de spikes
            sp = pl.find(np.abs(vetc[1:-1]) > (M * dp) )

            #coloca o valor medio no lugar do spike
            for i in range(len(sp)):

                vetc[sp[i]] = np.mean([ vetc[sp[i]-1] , vetc[sp[i]+1] ])

        #verifica se ainda permaneceu com spikes depois das iteracoes
        #Quantidade total de spikes depois das P iteracoes  
        M2 = len(sp)

    if M1 > N or M2 > 0:
    
        flag = flag + '4'
    
    else:
    
        flag = flag + '1'

    return flag, vetc
    
# ================================================================================== #
# Teste 5

def cqbruto_flat(serie,lmin,lmax,flag):
    
    '''

    VALORES FLAT (PROXIMOS DE ZERO)
    * Verifica variacoes menores que 20 cm
    * Verifica se todos os valores de eta sao muito proximos de zero
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Aprovado  : flag = '1'
    Reprovado : flag = '4'
    
    '''

    if ( (serie > lmin).all() and (serie < lmax).all() ):

        flag = flag + '4'
        
    else:
        
        flag = flag + '1'
        
    return flag




# ================================================================================== #
# Teste 6

def cqbruto_nulos(serie,ncn,flag):
    
    '''

    VERIFICA VALORES CONSECUTIVOS NULOS
    * Verifica valores consecutivos nulos
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      ncn - numero de valores consecutivos nulos testados
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Aprovado  : flag = '1'
    Reprovado : flag = '4'
    
    '''
    
    for i in range(len(serie)-ncn):

        if (serie[i:i+ncn] == 0).all():

            flag = flag + '4'
            break

        else:

            flag = flag + '1'
            break

    return flag
            

# ================================================================================== #
# Teste 7

def cqbruto_iguais(serie,nci,flag):
    
    '''

    VERIFICA VALORES CONSECUTIVOS IGUAIS
    * Verifica valores consecutivos iguais
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      nci - numero de valores consecutivos iguais testados
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    
    '''
    
    for i in range(len(serie)-(nci+1)):
        
        if (serie[i:i+nci] == serie[i+1:i+1+nci]).all():

            flag = flag + '4'
            
            break
        
        else:
            
            flag = flag + '1'
            
            break
            
    return flag
            

# ================================================================================== #
# Teste 8

def cqbruto_faixa(serie,imin,imax,flag):
    
    '''

    VERIFICA VALORES QUE EXCEDEM LIMITE DE RANGE
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      imin - limite inferior grosseiro
                      imax - limite superior grosseiro
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    '''
    
    if ( (serie > imax).any() and (serie < imin).any() ):

        flag = flag + '4'
        
    else:
        
        flag = flag + '1'
    
    return flag    
    

# ================================================================================== #
# Teste 9

def cqbruto_shift(serie,m,n,P,flag):
    
    '''

    VERIFICA DESLOCAMENTO DAS MEDIAS DOS SEGMENTOS
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      m - comprimento do segmento (length(serie)/8)
                      n - numero de segmentos (UNESCO = 8)
                      P - deslocamento maximo das medias dos segmentos (UNESCO = 0.20 m)
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    '''

    dmed = []
    a = 0

    for i in range(n-1):

        m1 = np.mean(serie[a:(a+m)])

        m2 = np.mean(serie[(a+m):(a+2*m)])

        dmed.append(m1 - m2)

        a += m

    if abs(max(dmed)) > P:

        flag = flag + '4'

    else:
        
        flag = flag + '1'
    
    return flag    

# ================================================================================== #











# ================================================================================== #

### a) Consitencia dos parâmetros de ondas (Hs, Tp, Dp, ...)

# ================================================================================== #


def cqproc_faixa(var,imin,imax,lmin,lmax,flag):
    
    '''
    
    TESTE DE FAIXA (RANGE)
    
    Dados de entrada: var - variavel sem consistencia
                      var1 - variavel editada
                      linf - limite inferior
                      lsup - limite superior
    
    Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
                    flag - parametro + flag
       
    Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
         O flag utilizado para o teste de range eh: 'A'
         Dados 'consistentes' recebem flag = '0'
    
    '''

    for i in range(len(var)):

      if np.isnan(var[i]):

          flag[i] = flag[i] + '9'

      # A condicao eh realizada na serie bruta
      elif var[i] < imin or var[i] > imax:

          flag[i] = flag[i] + '4'

          #o valor do dado inconsistente editado recebe 'nan'
          # var1[i] = np.nan

      # A condicao eh realizada na serie bruta
      elif var[i] < lmin or var[i] > lmax:

          flag[i] = flag[i] + '3'

          #o valor do dado inconsistente editado recebe 'nan'
          # var1[i] = np.nan

      else:

          flag[i] = flag[i] + '1'


    return flag


# ================================================================================== #

def cqproc_variab(var,lag,lim,flag):
    
    '''
    
    TESTE DE VARIABILDADE TEMPORAL
    
    Dados de entrada: var - variavel
                      var1 - variavel editada
                      lag - delta tempo para o teste (indicado ser de 0 a 3 horas)
                      lim - variacao temporal maxima (para o lag escolhido)
                      flag - matriz de flags
    
    Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
                    flag - data + flag
       
    Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
         O flag utilizado para o teste de range eh: 'B'
         Dados 'consistentes' recebem flag = '0'
    
    '''
    
    #calcula a derivada de acordo com o lag (horas)
    der = var[lag:] - var[:-lag]
    
    for i in range(len(der)):

        if np.isnan(var[i]):

          flag[i] = flag[i] + '9'
                             
        elif der[i] > lim or der[i] < -lim:
            
            flag[i] = flag[i] + '3'
            
            #o valor do dado inconsistente recebe 'nan'
            # var1[i] = np.nan
            
        else:
        
            flag[i] = flag[i] + '1'


    # Coloca flag = '1' nos utlimos dados (nao foram verificados)
    flag[-lag:] = [flag[-i] + '2' for i in range(1,lag+1)]
    # var1[-lag:] = np.nan
                
    return flag
    
    
## ================================================================================== #

def cqproc_iguais(var,nci,flag):
    
    '''
    
    TESTE VALORES CONSECUTIVOS IGUAIS
    
    Dados de entrada: var - variavel
                      var1 - variavel editada
                      nci - numero de valores consecutivos iguais
                      flag - matriz de flags
                          
    Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
                    flag - parametro + flag                    
       
    Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
         O flag utilizado para o teste de range eh: 'C'
         Dados 'consistentes' recebem flag = '0'
    
    '''

    for i in range(len(var)-nci):

        if np.isnan(var[i]):

          flag[i] = flag[i] + '9'
                        
        elif (var[i:i+nci] == var[i+1:i+nci+1]).all():
            
            flag[i] = flag[i]+ '3'
            
            #o valor do dado inconsistente recebe 'nan'
            # var1[i] = np.nan
            
        else:
            
            flag[i] = flag[i]+ '1'


    # Coloca flag = '2' nos dados que nao foram verificados
    flag[-nci:] = [flag[i] + '2' for i in range(-nci,0)]

                
    return flag

# # ================================================================================== #
    
# def t2(var,var1,M,hh,flag):
    
#     '''
    
#     TESTE SPIKE UTILIZANDO MEDIA MOVEL
    
#     Dados de entrada: var - variavel
#                       var1 - variavel editada
#                       M - multiplicador do desvio padrao
#                       despad - desvio padrao da serie
#                       hh - tempo em horas para a media movel
#                       flag - matriz de flags
    
#     Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
#                     flag - parametro + flag
       
#     Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
#          O flag utilizado para o teste de range eh: '1'
#          Dados 'consistentes' recebem flag = '0'
    
#     '''

#     for i in range(len(var)):
        
#         if var[i] < nanmean(var[i-int(hh/2):i+int(hh/2)])-M*nanstd(var[i-int(hh/2):i+int(hh/2)]) or var[i] > nanmean(var[i-hh/2:i+hh/2])+M*nanmean(var[i-int(hh/2):i+int(hh/2)]):
            
#             flag[i] = flag[i] + '1'
            
#             #o valor do dado inconsistente recebe 'nan'
#             var1[i] = nan
            
#         else:
            
#             flag[i] = flag[i] + '0'
            
#     return var1,flag
    
    
# # ================================================================================== #


### ** fazer o teste de consistencia dos parametros processados, indicando se exedeu limite superior ou inferior
# def t6(serie,linf,lsup,flag):
    
#     '''

#     VERIFICA VALORES QUE EXCEDEM LIMITE GROSSEIRO
#     * Verifica valores que excedem limites grosseiros
    
#     Dados de entrada: serie - (eta, dspx, dspy)
#                       linf - limite inferior
#                       lsup - limite superior
#                       flag - vetor de flags a ser preenchido
    
#     Dados de saida: flag = vetor de flag preenchido

#     Posicao (indice) em 'lista_flag' : 6
#     Aprovado  : flag = '0'
#     Reprovado : flag = 'a' - above limit
#                 flag = 'b' - below limit
#                 flag = 'c' - above and below limit
    
#     '''
    
#     if ( (serie > lsup).any() and (serie > lsup).any() ):

#         flag = flag + 'c'

#     elif (serie > lsup).any():

#         flag = flag + 'a'

#     elif (serie < linf).any():
        
#         flag = flag + 'b'
        
#     else:
        
#         flag = flag + '0'
    
#     return flag    
#     


# ================================================================================== #

# def t2(var,med,dp,M,flag):

#     '''

#     TESTE DE SPIKE
    
#     Dados de entrada: var - variavel sem consistencia
#                       med - media da serie
#                       dp - desvio padrão da série
#                       M - multiplicador do dp
#                       flag - vetor de flags a ser preenchido
    
#     Dados de saida: flag = vetor de flag preenchido

#     Aprovado  : flag = '0'
#     Reprovado : flag = '1'
    
#     '''

#     var1 = np.copy(var)

#     for i in range(len(var)):

#         if np.abs(var[i]) > (med + M*dp):

#             var1[i] = np.nan

#             flag[i] = flag[i] + '1'

#         else:

#             flag[i] = flag[i] + '0'

#     return var1,flag


## ================================================================================== #

# def t4(var,var1,hmax,hs,flag):

    
#     '''
    
#     TESTE DE LIMITE DE FREAK-WAVE
    
#     Dados de entrada: var - variavel
#                       var1 - variavel editada
#                       hmax - altura maxima
#                       hs - altura significativa
                          
#     Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
#                     flag - parametro + flag                    
       
#     Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
#          O flag utilizado para o teste de freakwave eh: 'D'
#          Dados 'consistentes' recebem flag = '0'
    
#     '''


#     for i in range(len(var)):

#       if hmax[i] / hs[i] >= 2.1:

#         flag = flag + 'D'

#         #o valor do dado inconsistente recebe 'nan'
#         var1[i] = nan

#       else:

#         flag = flag + '0'

      #flag[-nvc:] = [flag[-i]+'n' for i in range(1,nvc+1)]


    # return var1,flag













































# Rotina processamento dos parametros de ondas
def posproc(local,local1,glib,arq_st,pathname,pathname_ax,pathname_st,matondab,matondap):

	#em florianopolis nao veio dados do site (arq_st = 'pnboia.B69150_argos.dat')

	# pl.close('all')

	# ================================================================================== #  
	# Carrega os dados

	local = 'recife'
	local1 = 'Recife'
	glib = '32'
	arq_st = 'pnboia.B69153_argos.dat'

	#diretorio de onda estao os dados
	pathname = os.environ['HOME'] + '/Dropbox/ww3br/rot/saida/' + local + '/'
	pathname_ax = os.environ['HOME'] + '/Dropbox/pnboia/dados/axys/summary-axys/' + local + '/'
	pathname_st = os.environ['HOME'] + '/Dropbox/pnboia/dados/axys/site/'

	#LIOc (paramwp)
	#   0  1   2   3    4     5    6  7  8    9       10     11  12  13   14  15  16
	# data,hs,h10,hmax,tmed,thmax,hm0,tp,dp,sigma1p,sigma2p,hm01,tp1,dp1,hm02,tp2,dp2
	matondab = np.loadtxt(pathname + 'paramwb_' + glib + '-' + local + '.out', delimiter=',', unpack = False)
	matondap = np.loadtxt(pathname + 'paramwp_' + glib + '-' + local + '.out', delimiter=',', unpack = False)

	#Axys (Summary)
	#  0        1            2          3        4         5         6        7            8            
	#Year/Julian Date/Zero Crossings/Ave. Ht./Ave. Per./Max Ht./Sig. Wave/Sig. Per./Peak Per.(Tp)
	#          9        10     11           12       13      14         15  
	# /Peak Per.(READ)/HM0/Mean Theta/Sigma Theta/ H1/10 / T.H1/10 /Mean Per.(Tz)

	axys = np.loadtxt(pathname_ax + 'Summary_todos.txt',skiprows = 1, usecols = (range(2,18)))
	ax_data = np.loadtxt(pathname_ax + 'Summary_todos.txt',dtype = str, skiprows = 1, usecols = (0,1))


	#Saida site (baixado em 05/10/2014) - site goos/brasil
	#  0   1   2   3     4    5    6   7   8   9
	# ano mes dia hora minuto Hs Hmax Tp Dirm, Df
	site = np.loadtxt(pathname_st + arq_st ,delimiter=',', skiprows = 1, usecols = (2,3,4,5,6,45,46,47,48,49))


	# ================================================================================== #  
	# Formata as datas com datetime

	#lioc
	#formata o vetor de datas pra long e depois string
	data = matondab[:,0].astype(np.long)
	datas = data.astype(np.str)
	datam = [datetime( int(datas[i][0:4]),int(datas[i][4:6]), int(datas[i][6:8]), int(datas[i][8:10]) ) for i in range(len(datas))]


	#axys
	#deixa datas com numeros inteiros
	ano_ax = [int(ax_data[i,0][0:4]) for i in range(len(ax_data))]
	mes_ax = [int(ax_data[i,0][5:7]) for i in range(len(ax_data))]
	dia_ax = [int(ax_data[i,0][8:10]) for i in range(len(ax_data))]
	hora_ax = [int(ax_data[i,1][:2]) for i in range(len(ax_data))]
	min_ax = [int(ax_data[i,1][3:]) for i in range(len(ax_data))]

	datam_ax = []
	for i in range(len(ax_data)):
		datam_ax.append(datetime(ano_ax[i],mes_ax[i],dia_ax[i],hora_ax[i],min_ax[i]))


	# #site
	#deixa os valores com -99999 (erro) com nan
	for i in range(site.shape[1]):
		site[np.where(site[:,i] == -99999),i] = np.nan


	ano_st = site[:,0]
	mes_st = site[:,1]
	dia_st = site[:,2]
	hora_st = site[:,3] 
	min_st = np.zeros(len(site))

	datam_st = []
	for i in range(len(site)):
		datam_st.append(datetime(int(ano_st[i]),int(mes_st[i]),int(dia_st[i]),int(hora_st[i]),int(min_st[i])))


	# # ========================================================================== #
	# #Correcao dos dados (para facilitar na visualizacao dos graficos
	# #*pois tem valores de hs de 1200 no site)

	site[(np.where(site[:,5]>30)),5] = np.nan #hs
	site[(np.where(site[:,6]>30)),5] = np.nan #max


	# ================================================================================== #  
	# Parametros de ondas

	#media
	# medb = np.mean(matondab[:,1:],axis=0)
	# medp = np.mean(matondap[:,1:],axis=0)

	# #desvio padrao
	# desvpadb = np.std(matondab[:,1:],axis=0)
	# desvpadp = np.std(matondap[:,1:],axis=0)


	#graficos

	#lioc
	# variav = ['data','hs','h10','hmax','tmed','thmax','hm0','tp','dp','sigma1p','sigma2p','hm01','tp1','dp1','hm02','tp2','dp2']
	# labs = ['data','m','m','m','s','s','m','s','graus','graus','graus','m','s','graus','m','s','graus']

	# for i in range(1,matondab.shape[1]):

	# 	pl.figure()
	# 	pl.plot(datam,matondab[:,i],'bo')
	# 	pl.plot(datam,matondap[:,i],'r*')
	# 	pl.title(variav[i])
	# 	pl.ylabel(labs[i])
	# 	pl.xticks(rotation=15)

	# hs, tp e dp
	pl.figure()
	pl.subplot(311)
	pl.title('Parametros de Ondas - ' + local1 + ' - LIOc e Axys')
	pl.plot(datam_ax,axys[:,10],'bo')
	pl.plot(datam,matondap[:,6],'r*')
	pl.ylabel('Hm0 (m)')
	pl.grid('on')
	pl.xticks(visible=False)
	pl.subplot(312)
	pl.plot(datam_ax,axys[:,8],'bo')
	pl.plot(datam,matondap[:,7],'r*')
	pl.ylabel('Tp (s)')
	pl.grid('on')
	pl.xticks(visible=False)
	pl.subplot(313)
	pl.plot(datam_ax,axys[:,11],'bo')
	pl.plot(datam,matondap[:,8],'r*')
	pl.ylabel('Dp (g)')
	pl.grid('on')
	pl.xticks(rotation=15)

	# tp, dp1, tp2, dp2

	# pl.figure()
	# pl.plot(datam,matondap[:,12],'bo')
	# pl.plot(datam,matondap[:,15],'r*')
	# pl.title('tp1,tp2')
	# pl.legend(('tp1','tp2'))

	# pl.figure()
	# pl.plot(datam,matondap[:,13],'bo')
	# pl.plot(datam,matondap[:,16],'r*')
	# pl.title('dp1,dp2')
	# pl.legend(('dp1','dp2'))


	# #comparacao lioc, summary e site

	# pl.figure()
	# pl.plot(datam_ax,axys[:,10],'bo')
	# pl.plot(datam,matondap[:,6],'r*')
	# pl.plot(datam_st,site[:,5],'g*')
	# pl.title('Hm0')
	# pl.ylabel('m')
	# pl.legend(('axys','python','site'))
	# pl.xticks(rotation=15)

	# pl.figure()
	# pl.plot(datam_ax,axys[:,13],'bo')
	# pl.plot(datam,matondap[:,2],'r*')
	# # pl.plot(datam_st,site[:,5],'g*')
	# pl.title('H 1/10')
	# pl.ylabel('m')
	# pl.legend(('axys','python','site'))
	# pl.xticks(rotation=15)

	# pl.figure()
	# pl.plot(datam_ax,axys[:,5],'bo')
	# pl.plot(datam,matondap[:,3],'r*')
	# pl.plot(datam_st,site[:,6],'g*')
	# pl.title('Hmax (Max. Ht.)')
	# pl.ylabel('m')
	# pl.legend(('axys','python','site'))
	# pl.xticks(rotation=15)

	# pl.figure()
	# pl.plot(datam_ax,axys[:,8],'bo')
	# pl.plot(datam,matondap[:,7],'r*')
	# pl.plot(datam_st,site[:,7],'g*')
	# pl.title('Tp (Peak Per.)')
	# pl.ylabel('s')
	# pl.legend(('axys','python','site'))
	# pl.xticks(rotation=15)

	# pl.figure()
	# pl.plot(datam_ax,axys[:,11],'bo')
	# pl.plot(datam,matondap[:,8],'r*')
	# pl.plot(datam_st,site[:,8],'g*')
	# pl.title('Dp (Mean Theta)')
	# pl.ylabel('graus')
	# pl.legend(('axys','python','site'))
	# pl.xticks(rotation=15)

	# pl.figure()
	# pl.plot(datam_ax,axys[:,12],'bo')
	# pl.plot(datam,matondap[:,9],'r*')
	# # pl.plot(datam_st,site[:,9],'g*')
	# pl.title('Df (Sigma Theta)')
	# pl.ylabel('graus')
	# pl.legend(('axys','python')) #,'site'))
	# pl.xticks(rotation=15)



	#   0  1   2   3    4     5    6  7  8    9       10     11  12  13   14  15  16
	# data,hs,h10,hmax,tmed,thmax,hm0,tp,dp,sigma1p,sigma2p,hm01,tp1,dp1,hm02,tp2,dp2

	#  0        1            2          3        4         5         6        7            8            
	#Year/Julian Date/Zero Crossings/Ave. Ht./Ave. Per./Max Ht./Sig. Wave/Sig. Per./Peak Per.(Tp)
	#          9        10     11           12       13      14         15  
	# /Peak Per.(READ)/HM0/Mean Theta/Sigma Theta/ H1/10 / T.H1/10 /Mean Per.(Tz)

	#  0   1   2   3     4    5    6   7   8   9
	# ano mes dia hora minuto Hs Hmax Tp Dirm, Df



	# pl.figure()
	# pl.hist(hs,30,color='b',alpha=0.5)
	# pl.hist(hm0,30,color='g',alpha=0.5)
	# pl.title('Altura significativa (tempo e frequencia)')
	# pl.xlabel('metros')
	# pl.ylabel('N de ocorrencias')
	# pl.legend(('Hs','Hm0','Hmax'))
	# pl.axis([0,10,0,2000])

	# pl.figure()
	# pl.hist(h10,50,color='b',alpha=0.5)
	# pl.hist(hmax,50,color='g',alpha=0.5)
	# pl.title('Altura 1/10 e Maxima')
	# pl.xlabel('metros')
	# pl.ylabel('N de ocorrencias')
	# pl.legend(('H10','Hmax'))
	# pl.axis([0,10,0,2000])

	# pl.figure()
	# pl.hist(tmed,35,color='b',alpha=0.5)
	# pl.hist(thmax,35,color='g',alpha=0.5)
	# pl.hist(tp,20,color='r',alpha=0.5)
	# pl.title('Periodo')
	# pl.xlabel('segundos')
	# pl.ylabel('N de ocorrencias')
	# pl.legend(('Tmed','THmax','Tp'))
	# pl.axis([2,18,0,5000])

	# pl.figure()
	# pl.hist(dp,36,color='b',alpha=0.5)
	# pl.title('Direcao do periodo de pico')
	# pl.xlabel('graus')
	# pl.ylabel('N de ocorrencias')
	# pl.legend(['Dp'])
	# pl.axis([0,360,0,1500])

	return

#Graficos do processamento da axys

from pylab import *
from datetime import *

def graficos(mat_onda,eta_mat_cons,dspx_mat_cons,dspy_mat_cons,reg_fw,Hmax_fw,Hs_fw,THmax_fw,rel_fw,ind_fw):
    
    close('all')

    eta_mat_cons = eta_mat_cons[0:1024,:]
    dspx_mat_cons = dspx_mat_cons[0:1024,:]
    dspy_mat_cons = dspy_mat_cons[0:1024,:]

	# 			 0    1     2    3      4     5      6     7    8    9
	# mat_onda: ([Hs, H10, Hmax, Tmed, Tmax, THmax, HTmax, hm0, tp, dirtp])

	# plotagem das alturas de onda

	# figure()

	# plot(mat_onda[:,0])
	# plot(mat_onda[:,7])
	# plot(mat_onda[:,1])
	# plot(mat_onda[:,2])

	# legend(('Hs','hm0','H10','Hmax'))

	# #plotagem dos periodos

	# figure()

	# plot(mat_onda[:,8])
	# plot(mat_onda[:,3])
	# plot(mat_onda[:,4])

	# legend(('tp','Tmed','Tmax'))

	# plotagem de todas as series de elevacao 
	# * a ideia eh verificar de forma rapido se existe algum valores espurio em algumas serie (no periodo selecionado)
	
	# figure ()
	# plot(eta_mat)
	# title('series de elevacao')

	# figure ()
	# plot(dspx_mat)
	# title('series de dspx')

	# figure ()
	# plot(dspy_mat)
	# title('series de dspy')

	# plotagem dos histogramas das series temporais de onda
	
	# cria variaveis em linha para a plotagem do histograma


#	eta_mat1 = reshape(eta_mat_cons,eta_mat_cons.shape[0]*eta_mat_cons.shape[1])
#	dspx_mat1 = reshape(dspx_mat_cons,dspx_mat_cons.shape[0]*dspx_mat_cons.shape[1])
#	dspy_mat1 = reshape(dspy_mat_cons,dspy_mat_cons.shape[0]*dspy_mat_cons.shape[1])

	# figure ()
	# hist(eta_mat1,100)
	# title('series de elevacao')

	# figure ()
	# hist(dspx_mat1,100)
	# title('series de dspx')

	# figure ()
	# hist(dspy_mat1,100)
	# title('series de dspy')

#	figure ()
#	subplot(2,1,1), title('Elevacao')
#	plot(eta_mat_cons)
#	subplot(2,1,2)
#	hist(eta_mat1,100)
#	savefig('hist_eta_RS')
#
#	figure()
#	subplot(2,1,1), title('Deslocamento em x')
#	plot(dspx_mat_cons)
#	subplot(2,1,2)
#	hist(dspx_mat1,100)
#	savefig('hist_dspx_RS')
#
#	figure()
#	subplot(2,1,1), title('Deslocamento em y')
#	plot(dspy_mat_cons)
#	subplot(2,1,2)
#	hist(dspy_mat1,100)
#	savefig('hist_dspy_RS')

	# plot das series de Hs, Hmax, hm0, tp

#	figure ()
#	subplot(2,1,1), title('Altura significativa (Hs)')
#	plot(mat_onda[:,0])
#	subplot(2,1,2)
#	hist(mat_onda[:,0],100)
#	savefig('hist_Hs_RS')
#
#	figure()
#	subplot(2,1,1), title('Altura maxima (Hmax)')
#	plot(mat_onda[:,2])
#	subplot(2,1,2)
#	hist(mat_onda[:,2],100)
#	savefig('hist_Hmax_RS')
#
#	figure()
#	subplot(2,1,1), title('Altura significativa (Hm0)')
#	plot(mat_onda[:,7])
#	subplot(2,1,2)
#	hist(mat_onda[:,7],100)
#	savefig('hist_hm0_RS')
#
#	figure()
#	subplot(2,1,1), title('Periodo de pico (Tp)')
#	plot(mat_onda[:,8])
#	subplot(2,1,2)
#	hist(mat_onda[:,8],100)
#	savefig('hist_tp_RS')
#
#	figure()
#	subplot(2,1,1), title('Direcao associada ao periodo de pico (DirTp)')
#	plot(mat_onda[:,9])
#	subplot(2,1,2)
#	hist(mat_onda[:,9],100)
#	savefig('hist_dirtp_RS')

	
	# #plotagem com 2 eixos y

#	 fig = figure()
#	 ax1 = fig.add_subplot(111) #subplot, da para mudar
#	 t = range(len(mat_onda)) #cria vetor de tempo
#	 ax1.plot(t,mat_onda[:,9],'b-') #direcao de onda
#	 ax1.set_xlabel('tempo (horas)')
#	 ax1.set_ylabel('direcao de onda (graus)',color='b')
#	 ax2 = ax1.twinx()
#	 ax2.plot(t,mat_onda[:,8],'r-') #periodo de pico
#	 ax2.set_ylabel('periodo de pico (s)',color='r')
#	 axis('tight')

	# #plotagem de histograma com 2 eixos y

#    figure()
#    hist(rand(10),color='b')
#    twinx()
#    hist(rand(10),alpha=0.3,color='r')
#    axis([0,1,0,1.5])
    


	# #plotagem com data no eixo x (ainda nao esta funcionando)

	# # exemplo

	# dates_in_string = ['2010-01-01', '2010-01-02', '2010-02-03', '2010-04-05', '2010-07-19']
	# dates_datetime = []
	# for d in dates_in_string:

	#     dates_datetime.append(datetime.datetime.strptime(d, '%Y-%m-%d'))

	# dates_float = date2num(dates_datetime)
	# list1 = [1,2,3,4,5]
	# list2 = [1,2,4,8,16]
	# plot_date(dates_float, list1, linestyle='-', xdate=True, ydate=False)
	# plot_date(dates_float, list2, linestyle='-', xdate=True, ydate=False)


	# dates_in_string = data_hora2
	# dates_datetime = []

	# for d in dates_in_string:

	# 	dates_datetime.append(datetime.datetime.strptime(d, '%d/%m/%Y-%h'))

	# dates_float = date2num(dates_datetime)

	# list1 = mat_onda[:,0]

	# plot_date(dates_float, list1, linestyle='-', xdate=True, ydate=False)

	# #grafico polar
	# import matplotlib as mpl

	# polar_trans = mpl.transforms.Polar.PolarTransform(theta_offset=np.pi/2)
	# ax = plt.axes(projection=polar_trans)
	# ax.plot(np.arange(100)*0.15, np.arange(100)) 

	# import matplotlib.pylab as plt

	# fig = plt.figure()
	# ax = fig.add_axes( [0.1, 0.1, 0.8, 0.8] ,polar = True)
	# ax.set_theta_offset(pi/2)
	# ax.set_theta_direction(-1)
	# ax.set_xticklabels( [ 'N', 'NE', 'L', 'SE', 'S', 'SO', 'O', 'NO', 'N' ] )

	# plt.show()

	# ## aqui voce seta os valores de theta e r
	# #bars = ax.bar( theta (anglo em rad), r (intensidade do vento)  )
	# bars = ax.bar( pi , 1 )
	# #executa de um em um e vai vendo..

	# fig, ax = subplots(subplot_kw=dict(projection='polar'))
 # 	   ax.set_theta_zero_location("N")
 # 	   ax.set_theta_direction(-1)
 # 	   autumn()
 # 	   cax = ax.contourf(pi, 2, values, 30)
 # 	   autumn()
 # 	   cb = fig.colorbar(cax)
 # 	   cb.set_label("Pixel reflectance")


	# N = 150
	# r = 2*rand(N)
	# theta = 2*pi*rand(N)
	# area = 200*r**2*rand(N)
	# colors = theta
	# ax = subplot(111, polar=True)
	# c = scatter(theta, r, c=colors, s=area, cmap=cm.hsv)
	# c.set_alpha(0.75)
	
	# fig, ax = subplots(subplot_kw=dict(projection='polar'))
	# ax.set_theta_zero_location("N")
	# ax.set_theta_direction(-1)

	# plotagem das series de ondas que contem freakwaves

	#   for i in range(len(reg_fw)):
	  	
	#   	figure()

	#   	plot(eta_mat_cons[:,ind_fw[i]])

	#   	title(str(reg_fw[i]) + ', ' + 'Hmax = ' + str(round(Hmax_fw[i],2)) + ', ' + 'Hs = ' + str(round(Hs_fw[i],2)) + ', ' + 'THmax = ' + str(round(THmax_fw[i],2)) + ', ' + 'Rel_fw = ' + str(round(rel_fw[i],2)) )

	#   	savefig('freak'+str(i))

	# figure()

	# plot(Hmax_fw), title('Altua das freakwaves (Alturas maximas das series)')

	# figure()

	# plot(Hs_fw), title('Alturas significativas das series')

	# figure()

	# plot(rel_fw), title('Relacao entre Hmax/Hs')

    #tentar plotar histograma com dois eixos

    #arruma a matriz para fazer o grafico

    eta1 = resize(eta_mat_cons,(size(eta_mat_cons),1))
    dspx1 = resize(dspx_mat_cons,(size(dspx_mat_cons),1))
#
#
#    
    figure()
    hist(eta1,50,color='b')
    ylabel('Num Ocorrencias',color='b')
    xlabel('Elevacao')
    title('Rio Grande do Sul')
    #twinx()
    #hist(eta1,50,color='r',alpha=0.3)
    #axis([-4,4,0,50])    
    #ylabel('n ocorrencias',color='r')


	# dados = loadtxt('/home/hppp/Dropbox/Tese/CQ_Python/Boia_MB_RS/freakwaves/Saida_Param_Axys_RS.txt',skiprows=1)

	# dadosm = loadtxt('/home/hppp/Dropbox/Tese/CQ_Python/Boia_MB_RS/freakwaves/Saida_Param_Axys_Maio_RS.txt',skiprows=1)

	# #          0     1   2    3      4     5    6    7      8     9      10   11   12   13 
	# # dados = ano, mes, dia, hora, minuto, Hs, H10, Hmax, Tmed, THmax, HTmax, Hm0, Tp, DirTp

	# datam = []

	# for i in range(len(dadosm)):

	# datam.append(datetime(int(dadosm[i,0]),int(dadosm[i,1]),int(dadosm[i,2]),int(dadosm[i,3]),int(dadosm[i,4])))

	# plot(mat_onda[:,2]/mat_onda[:,0],mat_onda[:,0],'o')
	# title('Relacao entre a razao Hmax/Hs')
	# xlabel('Razao entre Hmax e Hs')
	# ylabel('Altura significativa (m)')

	return


# DAAT adaptada para o congresso 

#cria matrizes de direcao, espec e energia com 10 linha
#representando 5 faixas, cada uma com 2 direcoes; e 248
#colunas repesentando o tempo (1 mes a cada 3 horas = 
# 24/3*31)


# --------- Separacao da faixa de frequencia ----------
# Espectro calculado com 32 graus de liberdade
#faixa 1    faixa 2 faixa 3     faixa 4  
#3-21.33     6-10.66    10-6.40     16-3.76     
#4-16.00     7-9.14     11-5.81     32-2.00     
#5-12.80     8-8.00     12-4.92
#            9-7.11     13-4.57
#                       14-4.26
#                       15-4.00
#
# ------------------------------------------------------
# aplicados ao ES -- **** perguntar para o parente
#as wavelets serao calculadas para 3 ciclos - cada uma
#correspondendo a um pico do espectro de 1D - para um numero de pontos
#de uma wavelet de 3 ciclos multiplica--se o periodo acima por 3 e
#divide-se por 1 exemplo para 20 segundos.

#preparam-se entao as wavelets para os periodos das 5 faixas - com
#aproximacao para numero inteiro de pontos

#tamanha das wavelets, 3 vezes o periodo da faixa. caso nao tenha pico em
#uma faixa, calcula-se com o periodo central da faixa (dado pelo vetor
#picos1)

# ----------- ES 32 graus -------------------
# faixa 1: 64 48 38 
# faixa 2: 32 27 24 21
# faixa 3: 19 17 16 15 14 13 12
# faixa 4: 11 a 6
# ----------- ES 12 graus -------------------
# faixa 5: 9
# faixa 4: 21 21 20 19 19 18 18 17 17 16 16 15 15 15 14 14 14 13 13 13...
# faixa 3: 25 24 23 22
# faixa 2: 32 30 29 27 26
# faixa 1: 60 55 50 46 43 40 37 35 33


#importa bibliotecas
import time
from numpy import *
from pylab import *
import numpy as np
import matplotlib.pylab as pl
from scipy.signal import lfilter, filtfilt, butter
# import loadhne
import espec


def daat(pathname,listap,nfft,fs,ncol,p0,p1):

	tic = time.clock()

	dire = np.zeros((10,ncol)) #direcao (2 valores, ate 5 faixas)
	espe = np.zeros((10,ncol)) #espectros (2 valores, ate 5 faixas)
	energ = np.zeros((10,ncol)) #Hs + 5 energias (uma por faixa), 4 picos (maiores)
	dire1 = np.copy(dire)
	espe1 = np.copy(espe)

	#tabela de senos e cossenos para o metodo da maxima entropia
	#cria variaveis a23 e a24, com 360 linhas (no matlab eh colunas),
	#que faz um circulo de 1 a -1
	ar, ai, br, bi = np.loadtxt('lyg2.txt', unpack=True)

	a23 = ar + 1j * ai
	a24 = br + 1j * bi

	#mesmo circulo agora com 460 linhas (no matlab eh colunas)
	a26 = np.array( list(a23[310:360]) + list(a23) + list(a23[0:50]) )
	a27 = np.array( list(a24[310:360]) + list(a24) + list(a24[0:50]) )

	#cria vetor de 0 a 360 iniciando em 311 e terminando em 50
	a30 = np.array( range(311,361) + range(1,361) + range(1,51) )

	#??
	grad1 = 0.0175 ; grad2 = 180/pi

	#para o caso de usar matr1 (matriz de ocorrencias)
	# sa=[.5,.5,.5,.5,0.1]

	#o objetivo aqui eh ter wavelets prontas para usa-las de acordo com
	#o pico das faixas; caso nao haja pico em uma faixa, usa-se  wavelets
	#correspondentes a: faixa 1 - 14.28 s (55 pontos), faixa 2 - 9.52 s
	#(37 pontos), faixa 3 - 7.76 s (30 pontos ) e faixa 5- 3 s (12 pontos)
	# ES - 12 graus
	# mm=[60;55;50;46;43;40;38;35;33;32;30;29;27;26;25;24;23;22;21;21;20;19;...
	#     19;18;18;17;17;16;16;15;15;15;14;14;14;13;13;13;12;12;12;12;12;11;...
	#     11;11;11;11;10;10;10;10;10;10;9];
	# ES - 32 graus

	#cria vetor com o tamanho das wavelets
	# mm=[64;50;48;44;38;32;30;27;25;24;21;19;18;17;16;15;14;13;12;11;11;10;10;9;9;8;8;8;7;7;...
	#     7;7;6;6;6];

	mm = range(64,5,-1)
	ms=[];

	#cria vetores de dim 64,34
	wavecos = np.zeros((64,len(mm)))
	wavesen = np.copy(wavecos)

	for i in range(len(mm)):

	    mn = mm[i]
	    ms.append(mn)

	    #cria vetor de -pi a pi do tamanho de mn que eh o tamanho da wavelet
	    out2 = np.array([np.linspace(-3.14,3.14,mn)][:])

	    #cria janela de hanning para o tamanho da wavelet
	    gau = np.hanning(mn) ; gau = resize(gau,(1,len(gau)))

	    #cria wavelet cos
	    out1 = (gau * cos(3 * out2)).T

	    #cria wavelet sen
	    out3 = (gau * sin(3 * out2)).T

	    #coloca em cada coluna a wavelet de determinado
	    #tamanho. cria 34 wavelets?
	    wavecos[0:mn,i] = out1[:,0]
	    wavesen[0:mn,i] = out3[:,0]

	#intervalo de amostragem
	dt = 0.78

	#tempo de amostragem, pq 64? devido ao g.l?
	x = dt * 64

	#carrega lista com o nome dos arquivos
	#z3 = lista com o nomes

	# lista = carrega_axys.lista_hne(pathname)
	lista = listap


	kkl = 0

	#for ik in range(0,len(lista),3):
	# for ik in range(p0,p1,3): #pula 3 arquivos para cada arq processado
	for ik in range(len(listap)):

	    # print ik

	    #for ik in range(1):

	    #atribui o nome do arquivo a variavel 'arq'
	    arq = listap[ik]

	    #atribui as variaveis em 'dados' e a data em 'data'
	    dados = np.loadtxt(pathname+arq[ik])

	    eta = dados[:,1]
	    dspy = dados[:,2]
	    dspx = dados[:,3]

	    co = eta
	    dd = dspx
	    dc = dspy

	    ano = arq[0:4]
	    mes = arq[4:6]
	    dia = arq[6:8]
	    hora = arq[8:10]
	    minuto = arq[10:12]

	    data = [ano, mes, dia, hora, minuto]


	    ano = int(data[0])
	    mes = int(data[1])

	    #limite superior (3db) e limite inferior (3 db)
	    # 1) 20     11.1
	    # 2) 11.1   8.69
	    # 3) 8.69   7.4
	    # 4) 7.4    4.0
	    # 5) 4.0    end

	    # a wavelet sera gerada com as regras acima

	    # serao calculadas as energias em cada faixa mencionada a partir do
	    # espectro de uma dimensao considerando que o espalhamento entre cada
	    # frequencia seja de 1/T

	    #calculo do espectro de uma dimensao

	    ww55 = zeros((10,1))

	    han = 1 #aplicacao da janela: han = 1 hanning ; han = 0 retangular

	    gl = 32

	    qq1 = espec.espec1(co,nfft,fs)

	    f1 = qq1[:,0]

	    qq1 = qq1[:,1] #auto-espectro

	    #faixas em segundos
	    #2     3    4
	    #4     6    7.2
	    #7.14  8    10.8
	    #10.3  16   20.0

	    #intervalo de frequencia
	    df = f1[1] - f1[0]

	    #onda significativa (coloca a altura na primeira linha de ww5)
	    ww55[0] = 4 * sqrt(sum(qq1) * df)

	    #espectros nas 4 faixas - 32 gl
	    ww55[1] = sum(qq1[1:5])
	    ww55[2] = sum(qq1[5:7])
	    ww55[3] = sum(qq1[7:14])
	    ww55[4] = sum(qq1[14:33])

	    #picos1 eh o valor da duracao da wavelet que sera usada
	    #correspondendo a 3 ciclos do periodo de interesse

	    #quando nao ha pico na faixa: 48=16s ; 27=9s ; 
	    #18=6s ; 9=3s
	    picos1 = np.array([48,27,18,9])

	    #calcula a diferenca do vetor qq1 (ex: qq1[2] - qq1[1] = g1[1] )
	    g1 = np.diff(qq1)

	    #coloca 1 p/ valores >1, 0 p/ =0 e -1  <0
	    g1 = np.sign(g1)

	    #calcula a diferenca
	    g1 = np.diff(g1)

	    #acrescenta um valor no inicio de g1
	    g1 = np.array( [0] + list(g1) )

	    #acha indices dos picos
	    g1 = pl.find(g1 == -2)

	    #serao calculados os 4 maiores picos

	    #acha os valores dos picos (g4) e indices dos picos (g5)
	    g4 = sort(qq1[g1])

	    g5 = argsort(qq1[g1])

	    #g5 = range(len(g4)-1,-1,-1)

	    #fica igual ao g1 (matriz com picos em ordem crescente)
	    g6 = flipud(g1[g5])

	    #comeca criando a matriz com picos , pq??
	    #g6 = array( list(g6)+[0,0,0,0] )

	    #escolhe os 4 primeiros maiores?
	    #g6 = g6[0:4]

	    #retira valores maiores que 14 (pra tirar os picos em alta freq?)
	    g7 = g6[g6<14]

	    #cria faixas de frequencia (periodo) - pq nao usa faixa 4?
	    #no matlab esta transposto
	    faixa1 = np.array([3,4])
	    faixa2 = np.array([5,6])
	    faixa3 = np.array(range(7,14))

	    #colocacao dos picos nas primeiras faixas para determinacao das wavelets
	    picos2 = np.zeros((4,1))

	    for gh in range(len(g7)):

	        #se o valor de g7[gh] estiver dentro da faixa1
	        if g7[gh] in array(faixa1):

	            #acha o indice da faixa1 que esta o g7(gh)
	            #g8 = find(g7[gh] == faixa1)

	            picos2[0] = g7[gh]

	            faixa1 = 0        	

	        if g7[gh] in array(faixa2):

	            #acha o indice da faixa1 que esta o g7(gh)
	            #g8 = find(g7[gh] == faixa2)

	            picos2[1] = g7[gh]

	            faixa2 = 0

	        if g7[gh] in array(faixa3):

	            #g8 = find(g7[gh] == faixa3)

	            picos2[2] = g7[gh]

	            faixa3 = 0
	    	# print gh

	    picos3 = picos1

	    # # o que faz isso? (esta dando erro no proc do mes de maio de 2009)
	    # for gh in range(4):

	    #     if picos2[gh] > 0:

	    #         picos1[gh] = round(3 * 1./f1[int(picos2[gh])-1])

	    #valores dos picos para o arquivo final
	    g5 = flipud(g5)
	    g5 = g1[g5]
	    g5 = list(g5) + [0,0,0,0]
	    g5 = array(g5[0:4])
	    g = find(g5 > array(0))

	    #correcao henrique
	    g5aux = []
	    for i in range(len(g)):

	        g5aux.append(64 / float(g5[i]))

	    
	    if len(g5aux) < 4:

	        g5 = array(g5aux + [0,0,0,0])
	        g5 = g5[0:4]

	    #transforma em matriz de 4 col e 1 lin
	    g5 = resize(g5,(len(g5),1))

	    #preparo final do energ
	    ww55[6:11] = g5

	    energ[:,kkl] = ww55[:,0]

	    #serao calculadas 5 faixas com wavelets
	    #para cada wavelet calcula-se uma matriz de direcao
	    #e desvio padrao obtendo-se um D(teta) para cada faixa

	    for iwq in range(4):

	        #acha dentro de mm o indice do valor de picos[iwq]
	        g11 = find(picos1[iwq] == mm)

	        #acha o valor do periodo? da wavelet
	        m = mm[g11[0]]

	        #cria variavel out com a wavelet a ser utilizada (pega
	        #as linhas e colunas da wavelet)

	        out1 = wavecos[0:m,g11[0]]
	        out3 = wavesen[0:m,g11[0]]

	        #cria matriz com valores 1
	        matr1 = ones((20,90))

	        #perguntar p parente??
	        m1 = 1024 - m

	        #parametros para o calculo de tet2 e sp2
	        m3 = m1 ; m1 = m1 - 1 ; m3 = m1
	        m4 = 2 * dt / (m * 0.375) #para corrigir a janela de hanning
	        #como eu ja corrigi em espec1, preciso fazer?

	        m2 = m - 1

	# ==============================================================================#
	#daatRS21_32.m

	        #chama subrotina da daat

	        #CODE daatwaverider21w calculates the main direction
	        #for each segment with wavelet (morlet type);
	        #the formulatuio of Lygre and Krogstad is used

	        #usa-se a convolucao com a wavelet complexa

	        a1 = lfilter((out1 - 1j * out3), 1, co)
	        a2 = lfilter((out1 - 1j * out3), 1, dd)
	        a3 = lfilter((out1 - 1j * out3), 1, dc)

	        m4 = 2*dt / (m*0.375) #precisa fazer?

	        #pq pegar a partir de m?
	        a1 = a1[m-1:1025]
	        a2 = a2[m-1:1025]
	        a3 = a3[m-1:1025]

	        #espectros cruzados
	        z41 = a1
	        z42 = a2
	        z43 = a3

	        #espectros cruzados
	        a4 = m4 * (z41 * conj(z41))
	        a8 = m4 * imag(z41 * (- conj(z42)))
	        a9 = m4 * imag(z41 * (- conj(z43)))

	        a20 = m4 * (z42 * conj(z42))
	        a21 = m4 * (z43 * conj(z43))

	        a25 = a20 + a21
	        a7 = sqrt(a4 * a25)

	        a12 = m4 * real(z42 * conj(z43))

	        # #a8 eh o cosseno, projecao no eixo W-E
	        # #a9 eh o seno, projecao no wixo S-N
	        # #o angulo c0 calculado eh em relacao ao eixo horizontal

	        c0 = a8 + 1j * a9

	        c1 = c0 / a7

	        c01 = cos(c0)
	        c02 = sin(c0)
	        c03 = angle(mean(c01) + 1j * mean(c02))
	        c03 = ceil(c03 * 360 / (2 * pi))

	        c2 = (a20 - a21 + 1j * 2 * a12) / a25
	        c0 = angle(c0) * 360 / (2 * pi)
	        c0 = ceil(c0)

	        # c00 = find(c0<=0)         ##pra que utiliza??
	        # c0[c00] = c0[c00] + 360   ## nenhuma variavel criada aqui esta sendo utilizada
	        # pq = ceil(mean(c0)) ##nao utiliza
	        # pq = c03
	        # g = find(pq <= 0)
	        # pq[g] = pq[g] + 360

	        p1 = (c1 - c2 * conj(c1)) / (1 - abs(c1) ** 2)
	        p2 = c2 - c1 * p1

	        tet2 = zeros((1,m3+2))

	        #in order to avoid the ambiguity caused by 2teta the main 
	        #direction calculated by Fourier techniques is used 
	        #as a reference; the mem value is calculated in an interval
	        #of 100 degrees around this value;

	        for kl in range(m3+2):

	            p3 = ceil(c0[kl])

	            d = list(arange(p3,p3+100))

	            z1 = 1 - p1[kl] * conj(a26[d]) - p2[kl] * conj(a27[d])

	            z1 = z1 * conj(z1)

	            #z1 = array([round(v,7) for v in real(z1)])

	            #minimum of denominator is sufficient to
	            #determine the maximum

	            p5 = find(z1 == min(z1))
	            p5 = p5[0]
	            p7 = a30[p3 + p5 - 1]

	            tet2[0,kl] = grad1 * p7


	        tet2 = tet2.T

	        sp2 = a4

	# # ==============================================================================#
	# #daatRS22_32.m

	        #CODE daatbcampos22.m to select the segments for
	        #the directional spectrum composition
	        ################################################
	        #Prepared by C.E. Parente
	        ################################################

	        it = 2 * (iwq - 1 + 1) + 1 #verificar, que teria que dar 1 e ta dando -1

	        q1 = cos(tet2).T
	        q2 = sin(tet2).T

	        #Preparing ensembles of m segments advancing one sample

	        #fr3 ia a matrix of cos and fr5 of sines of the segments whose direction
	        #stability will be investigated
	        #fr4 is the spectrum matrix

	        pm = len(arange(round(m/2.0),m1-(m-round(m/2.0))))+1

	        fr3 = zeros((round(m/2.0),pm))

	        fr5 = copy(fr3)
	        fr4 = copy(fr3)

	        for ip in arange(round(m/2.0)):

	            fr3[ip,:] = q1[0,ip:m1-(m-ip)+1]
	            fr5[ip,:] = q2[0,ip:m1-(m-ip)+1]
	            fr4[ip,:] = real(sp2[ip:m1-(m-ip)+1])

	        #using the mean and the standard circular deviation
	        #to select the segments with a given stability

	        fr2a = mean(fr3.T, axis=1)
	        fr2b = mean(fr5.T, axis=1)

	        r = sqrt(fr2a ** 2 + fr2b ** 2)

	        #circular deviation
	        fr9 = sqrt(2 * (1 - r))

	        #espectro medio por coluna
	        fr45 = mean(fr4.T, axis=1)

	        fr2 = angle(fr2a + 1j * fr2b)

	        #correcao para os valores ficarem entre 0 e 2pi
	        g = find(fr2 < 0) ; fr2[g] = fr2[g] + 2 * pi
	        g = find(fr2 > 2 * pi) ; fr2[g] = fr2[g] - 2 * pi

	        #g vai ser o comprimento do vetor
	        g = len(fr2)

	        a15 = 0
	        zm = 0.5

	        #segments with values of the standard deviations smaller
	        #than the threshold are selected

	        er5 = copy(fr45)

	        b7 = find(fr9 < zm)

	        a15 = fr2[b7]

	        er4 = mean(fr4[:,b7], axis=0)

	        #Correcting for declination
	        # a15 is the final vector with selected direction values

	        a15 = ceil(a15 * 360 / (2 * pi))

	        #a15 = 90 + a15 - 14 (waverider santa catarina)
	        #a15 = 90 + a15 - 21 (waverider de arraial)
	        #Boia ES dmag -23
	        #usando o EtaEW e EtaNS ja esta descontado a dmag

	        a15 = 270 - a15
	        g = find(a15<0) ; a15[g] = a15[g] + 360
	        g = find(a15>360) ; a15[g] = a15[g] - 350

	        #caixas para acumulo e obtencao de D(teta)

	        w1 = zeros((360,1)) #direcao principal
	        w2 = zeros((360,1)) #ocorrencias

	        a16 = copy(a15)

	        if len(a15) > 1: #caso existam valores selecionados

	            b1 = find(a15<=0) ; a15[b1] = a15[b1] + 360
	            b1 = find(a15>360) ; a15[b1] = a15[b1] - 360

	            #a15 = round(a15)

	            for k in range(len(a15)):

	                bb = a15[k]
	                w1[bb-1] = w1[bb-1] + real(sp2[k])
	                w2[bb-1] = w2[bb-1] + 1

	        [b,t1] = butter(6,0.075)
	        #b = resize(b,(len(b),1))
	        #t1 = resize(t1,(len(t1),1))

	        #filtrando w1 para determinar o D(teta)
	        xx = array(list(w1[321:361]) + list(w1) + list(w1[0:41]))
	        xx = xx[:,0]

	        x = filtfilt(b,t1,xx)
	        x = x[41:401]
	        g = find(x<0)
	        x[g] = 0

	        #calculando as duas direcoes
	        g1 = diff(x)
	        g1 = sign(g1)
	        g1 = diff(g1)
	        g1 = array([0] + list(g1) )
	        g1 = find(g1 == -2)

	        p1 = sort(x[g1])
	        p2 = argsort(x[g1])

	        if len(p1) > 0:

	            p = array(list(flipud(g1[p2])) + [0])
	            p = p[0:2]

	            e = array(list(flipud(p1)) + [0])
	            e = e[0:2]

	        #joga fora valores espacados menos de 50 graus
	        if abs(p[0] - p[1]) < 20:

	            p[1] = 0
	            p[1] = 0

	        elif e[1] < 0.1 * e[0]:

	            e[1] = 0
	            p[1] = 0

	        z1 = ww55[iwq + 1]

	        p = array(list(p) + [0,0,0])
	        p = p[0:2]

	        e = array(list(p) + [0,0,0])
	        e = e[0:2]

	        e = e * z1 / sum(e)

	        dire1[it-1:it+1,kkl] = p
	        espe1[it-1:it+1,kkl] = e

	    kkl = kkl + 1

	toc = time.clock()
	texec = toc - tic

	print 'Tempo de execucao DAAT (s): ', texec

	return espe1, energ, dire1


	
