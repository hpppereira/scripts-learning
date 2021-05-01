#Processamento em batelada dos dados de ondas da BMO da Ambidados
#comparando com os dados da axys
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

#variaveis da axys e gx3
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

# 9 x 1024
acx_gx3 = mat.values()[5]
acy_gx3 = mat.values()[8]
#a acZ da gx3 tem mais datas, ate a hora 18, vamos pegar os registros simultaneos
#multiplica acZ por -9.81 para ficar em m/s2 e ficar idem ao acV
acz_gx3 = mat1[0:9,2:].astype(np.float) * -9.81
acv_gx3 = mat.values()[6] #errada

nfft = 64
fs_ax = 1.28 #freq amostragem axys
fs_gx3 = 1 #freq amostragem gx3

#frequencia de corte (limita a banda entre 4 - 15s)
aux = range(6,12)

# =============================================================================== #
#Processamento em batalada dos arquivos sincronizados

#matriz com parametros de ondas calculados

param_ax = [] #matriz com parametros de ondas da axys
param_gx3 = []
nlin = 1024

pl.figure()

#6 arquivos tem medicoes simultaneas
for i in range(6):

    #contador para o gx3 (o i eh o contador para a axys)
    j = i + 3

    #parametros da axys
    t_ax1 = t_ax[0:nlin]
    eta_ax1 = eta_ax[i,0:nlin]
    dspx_ax1 = dspx_ax[i,0:nlin]
    dspy_ax1 = dspy_ax[i,0:nlin]

    #processamento do dominio da frequencia da axys
    hm0_ax, tp_ax, dp_ax, sigma1p, sigma2p, freq, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
    eta_ax1,dspx_ax1,dspy_ax1,h,nfft,fs_ax)
    # [hm0_ax, tp_ax, dp_ax] = sai_ondaf

    #definicao dos parametros de onda da axys
    param_ax.append([hm0_ax, tp_ax, dp_ax])

    #obter o espectro de heave da gx3 a partir da soma dos espectros de slopes dividido por k^2
    sgx = espec.espec1(acx_gx3[j,:],nfft,fs_gx3) #espectro de acx
    sgy = espec.espec1(acy_gx3[j,:],nfft,fs_gx3) #espectro de acy

    #obter espectro de heave da axys (comparacao no plot)
    sax = espec.espec1(eta_ax1,nfft,fs_ax)
    
    f_gx3 = sgx[:,0] #vetor de frequencia
    df_gx3 = f_gx3[1] - f_gx3[0] #delta de frequencia
    
    sgx = sgx[:,1] #espec de acx
    sgy = sgy[:,1] #espec de acy

    #calculo do numero de onda no dominio da frequencia
    k = np.array(numeronda.numeronda(h,f_gx3,len(f_gx3)))
    k2 = k ** 2 #numero de onda ao quadrado

    #soma dos espectros de pitch e roll da gx3
    sgxy = sgx + sgy

    #espectro de heave da gx3 (calculado a partir dos slopes)
    sn_gx3 = sgxy / k2

    #figura dos espectros
    #*observar que os espectros onde nao tem energia,
    #ocorrem aleatoriedade no calculo da direcao

    pl.subplot(211)
    pl.plot(sax[:,0],sax[:,1])
    pl.axis([0,0.5,0,0.08])
    pl.subplot(212)
    pl.plot(f_gx3,sn_gx3)
    pl.axis([0,0.5,0,0.08])
    
    #indice da frequencia de pico
    aux1 = pl.find(sn_gx3[aux] == max(sn_gx3[aux]))
    ind_fp = pl.find(f_gx3 == f_gx3[aux[aux1]]) 

    #periodo de pico
    tp_gx3 = 1/f_gx3[ind_fp]

    #altura significativa do gx3 (banda limitada)
    hm0_gx3 = 4 * np.sqrt (np.sum(sn_gx3[aux]) * df_gx3)

    # calcula da direcao dividindo o espec ns pelo ew
    dxy_gx3 = sgy / sgx

    #calcula a direcao (apenas para o primeiro quadrante)
    th1 = np.arctan(np.sqrt(dxy_gx3)) * 180 / np.pi

    #calculo da direcao de pico (espec de ns/ew)
    dp1_gx3 = th1[ind_fp] + 90 # * para ficar no quadrante de sudeste, soma 90 graus

    #calculo da direcao para um quadrante utilizando os espectros cruzados 

    #amplitude do espectro cruzado
    asgxy = espec.espec2(acx_gx3[j,:],acy_gx3[j,:],nfft,fs_gx3)[:,1]

    #calcula a direcao (para dois quadrantes?)
    th2 = np.arcsin(asgxy / sgxy) * 180 / np.pi

    #calculo da direcao de pico (forma 2 - espectros cruzados)
    dp2_gx3 = th2[ind_fp] + 180

    #parametros de onda da gx3
    param_gx3.append([hm0_gx3, tp_gx3[0], dp1_gx3[0], dp2_gx3[0]])

#hm0, tp, dp1, dp2
param_ax = np.array(param_ax)

#hm0, tp, dp1, dp2
param_gx3 = np.array(param_gx3)

#figura criada dentro do loop
pl.subplot(211)
pl.title('Espectro de heave - 6 horas - Axys')
pl.ylabel('m^2/Hz')
pl.legend(['0','1','2','3','4','5'])
pl.subplot(212)
pl.title('Espectro de heave - 6 horas - GX3 ((pitch+roll)/k^2)')
pl.xlabel('Frequencia (Hz)')
pl.ylabel('m^2/Hz')
pl.legend(['0','1','2','3','4','5'])


# =============================================================================== #
# Figuras

#figuras dos parametros processados em batelada
pl.figure()
pl.subplot(311)
pl.plot(param_ax[:,0],'b-*')
pl.plot(param_gx3[:,0],'r-*')
pl.ylabel('Metros')
pl.title('Hm0')
pl.legend(['axys','gx3'])
pl.subplot(312)
pl.plot(param_ax[:,1],'b-*')
pl.plot(param_gx3[:,1],'r-*')
pl.title('Periodo de pico')
pl.ylabel('Segundos')
pl.subplot(313)
pl.plot(param_ax[:,2],'b-*')
pl.plot(param_gx3[:,2],'r-*')
pl.title('Direcao do Periodo de pico')
pl.xlabel('Horas')
pl.ylabel('Graus')

pl.show()