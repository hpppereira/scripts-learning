# -*- coding: utf-8 -*-
'''
metodologia de particionamento
espectral por krogstad
'''
import numpy as np
import os
import proconda
import pylab as pl
reload(proconda)

pathname = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/partespec/dados/'
#arqname = '200908090600.HNE'
arqname = '200909090600.HNE'
dados = np.loadtxt(pathname + arqname,skiprows=11)

time, eta, etay, etax = dados.T

h = 200 #profundidade 
nfft = 82 #numero de dados para a fft (para nlin=1312 -- p/ 32gl, nfft=82 ; p/8 gl, nfft=328)
fs = 1.28 #freq de amostragem
nlin = 1312 #comprimento da serie temporal a ser processada
gl = (nlin/nfft) * 2


#processamento no dominio da frequencia
hm0, tp, dp, sigma1p, sigma2p, f, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
    eta,etax,etay,h,nfft,fs)

#Particoes do espectro direcional das ondas do oceano em componentes disjuntos.
#determinando quantidades de picos a partir de proconda    
#hm01, tp1, dp1,hm02, tp2, dp2 = proconda.ondap(hm0,tp,dp,sn,dire1,df)
#Passo1: Localizar picos e gerar matriz de indicadores de subida mais íngreme.
NP=0
#########################################################################
#determinar frequencia de pico fp e direção de pico dp
#f = sn[:,0]
#ind = np.where(sn[:,1] == np.max(sn[:,1]))[0]
#fp = sn[ind,0]
# dp importado de proconda

# Verificando se a energia de partição está abaixo de um limiar mínimo.
 
#a e b são escolhidos para eliminar o ruído nas regiões de baixa energia do espectro 
#foi verificado que os valores seguintes de a e b dão resultados razoáveis
#a = 0,1  #parâmetro mais importante
#b = 0,002
#eth = a /(fp**4 + b)