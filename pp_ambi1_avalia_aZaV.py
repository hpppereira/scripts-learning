'''
#Processamento dos dados de ondas da BMO da Ambidados
#
# a) Obter o espectro de heave a partir da soma dos espectros de slopes dividido por k^2
# b) Calcular a direcao dividindo o espec de ac. NS pelo dspEW da GX3 (apenas para o primeiro quadrante (arctg**2))
# c) Calcular a direcao para 2 quadrantes utilizando as ampl. dos espectros cruzados  (arcsin)
# d) Processamento em batalada dos arquivos sincronizados
# e) Comparar os espectros de heave da axys com os da GX3
# f) Fazer a conta com a acZ da gx3
#
#Observacoes:
# - Foram colocados simultaneamente um sensor GX3 e um miniTriaxys.
# - Foram coletados 9 horas
# - Os dados do GX3 esta 3 horas adiantado (verificar para comparacao,
#   existem 6 horas de dados coincidentes)
# - Verificar se o dspx e dspy estao invertidos
# - Precisa fazer os calculos com w ou pode ser com f?.
# - Direcao das ondas no TBIG geralmente de SE
#
#Dados: bmo.dat
'''

import numpy as np
import pylab as pl
import scipy.io
import os
import proconda
import espec
import numeronda

reload(numeronda)
reload(espec)
reload(proconda)

pl.close('all')

# =============================================================================== #
# Definicao das variaveis

pathname = os.environ['HOME'] + '/Dropbox/ambid/dados/TEBIG_gx3_triaxys/'
# pathname = 'C:/Users/henrique/Dropbox/ambid/TEBIG-axys_gx3_20140522/'

#variaveis da axys e gx3 (as aceleracoes horizontais sao em verdade pitch e roll)
mat = scipy.io.loadmat(pathname + 'bmo.mat')

#aceleracao z do gx3 (brutos)
mat1 = np.loadtxt(pathname + 'CR1000_microstrain_stbacelZ_2014_05_22_15_17_00.dat',
    delimiter=',',skiprows=4,dtype=str)

h = 22 #profundidade

#Axys
t_ax = mat.values()[0][0]
data_ax = mat.values()[1]

# 9 x 1382
eta_ax = mat.values()[7]
dspx_ax = mat.values()[4] #verificar se nao eh invertido
dspy_ax = mat.values()[9]

#GX3
t = range(1,1025) #vetor de tempo (1Hz)
data_gx3 = mat.values()[11]

# 9 x 1024 (acx e acy = pitch e roll)
acx_gx3 = mat.values()[5]
acy_gx3 = mat.values()[8]
acv_gx3 = mat.values()[6] #errada (media de 9.81 - m/s2)

#a acZ da gx3 tem mais datas, ate a hora 18, vamos pegar os registros simultaneos
#a ac_Z esta em unidade 'g', multiplicar por -9.81 para ficar em m/s2 (idem acV)
acz_gx3 = mat1[0:9,2:].astype(np.float)

acz_gx3 = acz_gx3 * -9.81 #passa para m/s2


# =============================================================================== #
# Espectros (apenas para o arquivo 1 da axys e 4 da gx3 (primeiro arquivo simultaneo))

nfft = 64
fs_ax = 1.28 #freq amostragem axys
fs_gx3 = 1 #freq amostragem gx3

#Axys
aa_ax = espec.espec1(eta_ax[0,0:1024],nfft,fs_ax)
f_ax = aa_ax[:,0]
df_ax = f_ax[1] - f_ax[0]
sn_ax = aa_ax[:,1]

#GX3
# 1 - Obter o espectro de heave a partir da soma dos espectros de slopes dividido por k^2
#calculo dos espectros de slpx e slpy
sgx = espec.espec1(acx_gx3[3,:],nfft,fs_gx3) #espectro de acx
sgy = espec.espec1(acy_gx3[3,:],nfft,fs_gx3) #espectro de acy
sgz = espec.espec1(acz_gx3[3,:],nfft,fs_gx3)
sgv = espec.espec1(acv_gx3[3,:],nfft,fs_gx3)

#frequencia de corte, depende do gl (limita a banda entre 4 - 15s)
aux = range(6,len(sgx))

f_gx3 = sgx[:,0] #vetor de frequencia
df_gx3 = f_gx3[1] - f_gx3[0] #delta de frequencia
w4_gx3 = (2 * np.pi * f_gx3) ** 4 #omega a quarta

sgx = sgx[:,1] #auto-espectro roll?
sgy = sgy[:,1] #auto-espectro pitch?
sgz = sgz[:,1] #auto-espectro ac.z
sgv = sgv[:,1] #auto-espectro ac.v

#espectro de heave a partir da ac. z
sgn = sgz / w4_gx3

#os espectros possuem muita energia em alta e baixa frequencia.
#precisa utilizar uma frequencia de corte inferior e superior 
#antes de calcular o periodo de pico e hs

#periodo de pico obtido pelo gx3 (utilizando no numero de onda)
#utiliza um corte de banda para o calculo do periodo de pico
#pois a energia em baixa e alta freq mascara o periodo de pico
#real 

#periodo de pico calculado dentro da banda escolhida
T = 1/f_gx3[aux][pl.find(sgz[aux]==max(sgz[aux]))]

#calculo do numero de onda do dominio da frequencia
k = np.array(numeronda.numeronda(h,f_gx3,len(f_gx3)))
k2 = k ** 2 #numero de onda ao quadrado

#soma dos espectros de pitch e roll
sgxy = sgx + sgy

#espectro de heave (calculado a partir de pitch e roll)
sgn1 = sgxy / k2

# 2 - Obter as direcoes a partir de pitch e roll

# tan(theta) - calcula a direcao dividindo o espec ns pelo ew
dsgxy = sgy / sgx

# 2a - thetha - calcula a direcao (apenas para o primeiro quadrante)
th1 = np.arctan(np.sqrt(dsgxy)) * 180 / np.pi

# 2b - calculo da direcao para um (ou 2?) quadrantes utilizando os
#espectros cruzados 

#calcula a amplitude do espec cruzado
asgxy = espec.espec2(acx_gx3[3,:],acy_gx3[3,:],nfft,fs_gx3)[:,1]
# asgxy = asgxy[3:18]

#calcula a direcao atraves dos espectros cruzados
th2 = np.arcsin(asgxy / sgxy) * 180 / np.pi

# =============================================================================== #
# Figuras

#plotagem das series temporais de acZ, acV
pl.figure()
pl.title('Series temporais de aceleracoes mast-down e vertical')
pl.plot(acz_gx3[3,:],'b',label='acZ_gx3')
pl.plot(acv_gx3[3,:],'r',label='acV_gx3')
pl.ylabel('m/s^2')
pl.axis('tight')
pl.legend()

# figura do espectro do primeiro registro simultaneo
pl.figure()
pl.title('Espectros de heave do primeiro registro simultaneo')
pl.plot(f_ax,sn_ax,'b',label='axys')
pl.plot(f_gx3,sgn,'g',label='gx3 (acz/w^4)')
pl.plot(f_gx3,sgn1,'r',label='gx3 (pitch+roll)/k2')
pl.axis([0,0.5,0,0.2])
pl.xlabel('Frequencia (Hz)')
pl.ylabel('m^2/Hz')
pl.legend()

pl.show()