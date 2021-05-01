#!/usr/bin/python
# -*- coding: UTF-8 -*-
# ================================================================================== #
# Desenvolvido por: Henrique P. P. Pereira - heniqueppp@oceanica.ufrj.br
# Data da ultima modificacao: 08/04/2014
# ================================================================================== #
# Boia Axys 3M - Rio Grande/RS - PNBOIA
# ================================================================================== #
# Programa principal para o processamento de dados de onda
# da BMO Axys no RS para o mês de Maio de 2009 (744 arquivos)
# na placa microprocessadora ARM ...
#
# a) Sera contabilizado o tempo de processamento para 1 arquivo
# e para o mês inteiro (com o objetivo de realizar um controle de qualidade
# em dados de longo termo)
# os dados na placa A
#
# b) fara os calculos dos parametros de Hs, Tp e Dp e tambem a tecnica
# DAAT, a qual possibilitara o envio de parametros extras que podem
# complementar a informacao direcional das ondas.
#
# Para cada medicao, a DAAT fornece uma matriz espe1 e dire1 e energ
# a primeira linha do energ eh o Hs
#
# Por enquanto estamos enviado toda a informacao produzida pela daat,
# posteriormente, poderemos selecionar, de acordo com o estado de mar, 
# quais os parametros necessarios ou importantes que a daat pode enviar.
# ================================================================================== #

import os
import numpy as np
import time
import datetime
import carrega_axys
import proconda
import consiste_bmo_bruto
import consiste_bmo_proc
import daat_oc
import relatorio
import pylab as pl
import espec
import numeronda

reload(daat_oc)
reload(carrega_axys)
reload(proconda)
reload(consiste_bmo_bruto)
reload(consiste_bmo_proc)
reload(relatorio)

pl.close('all')

#contador inicial de tempo de execucao
tic = time.clock()

# ================================================================================== #
## Dados de entrada

#carregar arquivo com o nome dos arquivos .HNE

#caminho onde estao os arquivos .HNE
#pathname = os.environ['HOME'] + '/Google Drive/oceans/electrum/dados/'
pathname = 'C:\Users\henrique\Google Drive\oceans\electrum\dados/'

lista = np.array(carrega_axys.lista_hne(pathname))

#escolhe a data inicial e final para ser processada (opcional, no 'p0' e 'p1')
z0 = '200905090600.HNE'
z1 = '200905091000.HNE'

#numero dos arq para processar (modificar p0=0 e p1=len(lista) para todos)
p0 = np.where(lista == z0)[0][0]
p1 = np.where(lista == z1)[0][0]

h = 200 #profundidade
nfft = 64 #numero de dados para a fft
fs = 1.28 #freq de amostragem
nlin = 1024 #comprimento da serie temporal a ser processada

#define as faixas de frequencia para a LH
f1 = range(2,4) #16.6 - 12.5
f2 = range(4,7) #10 - 7.14
f3 = range(7,11) #6.25 - 4.6
f4 = range(11,15) #4.16 - 3.3

# ================================================================================== #
## Incicializacao do programa

#lista dos arquivos que serao processados
listap = lista[p0:p1+1]
# listap = listap[0:20]

#numero de arquivos a serem processados
ncol = len(listap)

    #cria vetores de flags das series brutas
flagb = np.zeros((len(listap),4),dtype='|S32')
flagb[:,0] = [ listap[i][0:-4] for i in range(len(listap)) ]

#parametros criados no processamento em batelada
matonda = [] #matriz com parametros de onda
listac = [] #lista de arquivos consistentes
listai = [] #lista de arquivos inconsistentes

#eixo para plotagem com datas
aux_ax = [733528.0, 733558.95833333337, 0.0, 360.0]

# ================================================================================== #
# Processamento em batelada

#DAAT
espe1, energ, dire1 = daat_oc.daat1(pathname,listap,nfft,fs,ncol,p0,p1)

matonda = []
datat = []
dp1 = []
dp2 = []
dp3 = []
dp4 = []


for i in range(len(listap)):

    print 'LH: ' + str(i)

    # cont = cont + 1

    #carrega dados e data
    dados, data = carrega_axys.dados_hne(pathname,listap[i])

    datat.append(datetime.datetime(int(data[0]),int(data[1]),int(data[2]),int(data[3])))

    #define variaveis
    t = dados[:,0]
    eta = dados[:,1]
    etax = dados[:,3]
    etay = dados[:,2]

    #Consistencia dos dados brutos      
    #Teste 1hne (apenas axys *.HNE) -  validade do nome do arquivo (ind=0)
    flagb[i,1] = consiste_bmo_bruto.t1hne(listap[i],flagb[i,1])
    flagb[i,2] = consiste_bmo_bruto.t1hne(listap[i],flagb[i,2])
    flagb[i,3] = consiste_bmo_bruto.t1hne(listap[i],flagb[i,3])
    
#     #Teste 2hne (apenas axys *.HNE) - comprimento do vetor (ind=1)
    flagb[i,1] = consiste_bmo_bruto.t2hne(eta,flagb[i,1])
    flagb[i,2] = consiste_bmo_bruto.t2hne(etax,flagb[i,2])
    flagb[i,3] = consiste_bmo_bruto.t2hne(etay,flagb[i,3])
#
#     #Teste 1 - gap (lacuna)
#     flagb[i,1] = consiste_bmo_bruto.t1(eta,10,flagb[i,1])
#     flagb[i,2] = consiste_bmo_bruto.t1(etax,10,flagb[i,2])
#     flagb[i,3] = consiste_bmo_bruto.t1(etay,10,flagb[i,3])
#
#     #Teste 2 - spike
#     flagb[i,1], vet_etai = consiste_bmo_bruto.t2(eta,np.mean(eta),np.std(eta),10,7,2,flagb[i,1])
#     flagb[i,2], vet_etaxi = consiste_bmo_bruto.t2(etax,np.mean(etax),np.std(etax),10,7,2,flagb[i,2])
#     flagb[i,3], vet_etayi = consiste_bmo_bruto.t2(etay,np.mean(etay),np.std(etay),10,7,2,flagb[i,3])
#    
#     #Teste 3- valores proximos a zero
#     flagb[i,1] = consiste_bmo_bruto.t3(eta,flagb[i,1])
#     flagb[i,2] = consiste_bmo_bruto.t3(etax,flagb[i,2])
#     flagb[i,3] = consiste_bmo_bruto.t3(etay,flagb[i,3])
#    
#     #Teste 4 - valores consecutivos nulos
#     flagb[i,1] = consiste_bmo_bruto.t4(eta,5,flagb[i,1])
#     flagb[i,2] = consiste_bmo_bruto.t4(etax,5,flagb[i,2])
#     flagb[i,3] = consiste_bmo_bruto.t4(etay,5,flagb[i,3])
#    
#     #Teste 5 -valores consecutivos iguais / (serie,nci,flag):
#     flagb[i,1] = consiste_bmo_bruto.t5(eta,5,flagb[i,1])
#     flagb[i,2] = consiste_bmo_bruto.t5(etax,5,flagb[i,2])
#     flagb[i,3] = consiste_bmo_bruto.t5(etay,5,flagb[i,3])
# 
#     #Teste 6 -valores que excedem limites grosseiros
#     flagb[i,1] = consiste_bmo_bruto.t6(eta,-15,15,flagb[i,1])
#     flagb[i,2] = consiste_bmo_bruto.t6(etax,-15,15,flagb[i,2])
#     flagb[i,3] = consiste_bmo_bruto.t6(etay,-15,15,flagb[i,3])

    #Condicao para qualificar a serie como inconsistente
    #verifica se o vetor de flags eh igual a zero
    # if [ int(flagb[i,1]), int(flagb[i,2]), int(flagb[i,3]) ] <> [0,0,0]:
        
    #     #lista nome dos arquivos inconsistentes 
    #     listai.append(listap[i][0:-4])

    #Condicao para dado consistentes
    # elif [ int(flagb[i,1]), int(flagb[i,2]), int(flagb[i,3]) ] == [0,0,0]:

    #lista nome dos arquivos inconsistentes 
    listac.append(listap[i][0:-4])

    #processamento no dominio do tempo
    pondat = proconda.ondat(t,eta,h)

    #processamento no dominio da frequencia
    pondaf = proconda.ondaf(eta,etax,etay,h,nfft,fs)

    #parametros de onda = [Hs,H10,Hmax,Tmed,THmax,Hm0,Tp,Dp]
    matonda.append(np.concatenate([pondat,pondaf]))

    #espectro simples
    sn = espec.espec1(eta,nfft,fs)
    sny = espec.espec1(etax,nfft,fs)
    snz = espec.espec1(etay,nfft,fs)

    #calculo dos espectros cruzados
    snnx = espec.espec2(eta,etax,nfft,fs)
    snny = espec.espec2(eta,etay,nfft,fs)
    snxny = espec.espec2(etax,etay,nfft,fs)

    #vetor de frequencia
    f = sn[:,0]

    #calculo do numero de onda
    k = numeronda.k(h,f,len(f))
    k = np.array(k)

    #calculo dos coeficientes de fourier
    a1 = snnx[:,3] / (k * np.pi * sn[:,1])
    b1 = snny[:,3] / (k * np.pi * sn[:,1])

    #calcula direcao de onda
    dire = np.array([np.angle(np.complex(b1[i],a1[i]),deg=True) for i in range(len(a1))])

    #condicao para valores maiores que 360 e menores que 0
    dire[np.where(dire < 0)] = dire[np.where(dire < 0)] + 360
    dire[np.where(dire > 360)] = dire[np.where(dire > 360)] - 360

    #indice da frequencia de pico para as 4 bandas (32 gl)
    aux1 = pl.find(sn[f1,1] == max(sn[f1,1]))
    aux2 = pl.find(sn[f2,1] == max(sn[f2,1]))
    aux3 = pl.find(sn[f3,1] == max(sn[f3,1]))
    aux4 = pl.find(sn[f4,1] == max(sn[f4,1]))

    #direcao do periodo de pico (para 32 gl)
    dp1.append( dire[np.where(f == f[f1][aux1])] )
    dp2.append( dire[np.where(f == f[f2][aux2])] )
    dp3.append( dire[np.where(f == f[f3][aux3])] )
    dp4.append( dire[np.where(f == f[f4][aux4])] )

    #figura
    pl.figure()
    pl.subplot(211)
    pl.plot(f,sn[:,1])
    pl.title('Power Spectrum\nRio Grande/RS - 05-09-2009 06:00h')
    pl.ylabel('m^2/Hz')
    pl.text(0.4,1.1,'Hm0 = 2 m\nTp1 = 12.5 sec\nTp2 = 4.2 sec\nDp1 = 215 deg\nDp2 = '
        '100 deg\nDp-1 (DAAT) = 213 deg\nDp-4 (DAAT) = 100 deg')
    pl.axis('tight'), pl.grid('on')
    pl.subplot(212)
    pl.plot(f,dire)
    pl.title('Principal Direction')
    pl.ylabel('degrees')
    pl.xlabel('Frequency (Hz)')
    pl.axis([0,max(f),0,360]), pl.grid('on')
    


matonda = np.array(matonda)


# ================================================================================== #  
# Realiza a consistencia dos dados processados

# if len(listac) > 0:

#     #cria array das listas criadas
#     matonda = np.array(matonda)
#     listac = np.array(listac)
#     listai = np.array(listai)

#     #cria vetor dos parametros calculados
#     hs = matonda[:,0]
#     h10 = matonda[:,1]
#     hmax = matonda[:,2]
#     tmed = matonda[:,4]
#     thmax = matonda[:,3]
#     hm0 = matonda[:,5]
#     tp = matonda[:,6]
#     dp = matonda[:,7]

#     #cria vetores de flags das series processadas (depende das qtdade de variaveis a serem consistidas + data) 
#     # flagp = np.zeros((len(listac),matonda.shape[1]),dtype='|S32')
#     flagp = np.zeros((len(listac),4),dtype='|S32')
#     flagp[:,0] = listac[:]
    
#     # Consistencia dos dados processados

#     #Teste 1 - Faixa regional
#     hm0c,flagp[:,1] = consiste_bmo_proc.t1(hm0,0.25,10,flagp[:,1])
#     tpc,flagp[:,2] = consiste_bmo_proc.t1(tp,2,20,flagp[:,2])
#     dpc,flagp[:,3] = consiste_bmo_proc.t1(dp,0,360,flagp[:,3])

#     #Teste 2 - Spike
#     hm0c,flagp[:,1] = consiste_bmo_proc.t2(hm0,np.mean(hm0),np.std(hm0),7,flagp[:,1])
#     tpc,flagp[:,2] = consiste_bmo_proc.t2(tp,np.mean(tp),np.std(tp),7,flagp[:,2])
#     dpc,flagp[:,3] = consiste_bmo_proc.t2(dp,np.mean(dp),np.std(dp),7,flagp[:,3])

#     #Teste 3 - Variabilidade temporal
#     hm0c,flagp[:,1] = consiste_bmo_proc.t3(hm0,1,3,flagp[:,1])
#     tpc,flagp[:,2] = consiste_bmo_proc.t3(tp,1,10,flagp[:,2])
#     dpc,flagp[:,3] = consiste_bmo_proc.t3(dp,1,180,flagp[:,3])

#     #Teste 4 - Valores consecutivos iguais
#     hm0c,flagp[:,1] = consiste_bmo_proc.t4(hm0,10,flagp[:,1])
#     tpc,flagp[:,2] = consiste_bmo_proc.t4(tp,10,flagp[:,2])
#     dpc,flagp[:,3] = consiste_bmo_proc.t4(dp,10,flagp[:,3])

# else:

#     print('Todos os arquivos reprovaram em algum teste de Controle de Qualidade' '\n' '\n')

# #imprime relatorio de controle de qualidade
# relatorio.rel(lista,listap,listac,listai,flagb,flagp,hm0c,tpc,dpc,h)

#contador inicial de tempo de execucao
toc = time.clock()

#tempo de execucao
texec = toc - tic

#criar saida de dados com savetxt
# np.savetxt('paramw_rs.out',matonda,delimiter=',',fmt='%.2f',header='Hs,H10,Hmax,Tmed,THmax,Hm0,Tp,Dp')
# np.savetxt('flagbw_rs.out',flagb,delimiter=',',fmt='%s',header='date,eta,etax,etay')
# np.savetxt('flagpw_rs.out',flagb,delimiter=',',fmt='%s',header='date,eta,etax,etay')

# #salva saida da daat (espe e dire)
# np.savetxt('espe1.out',espe1,delimiter=',',fmt='%.2f')
# np.savetxt('dire1.out',dire1,delimiter=',',fmt='%.2f')
# np.savetxt('energ.out',energ,delimiter=',',fmt='%.2f')

print 'Tempo de execucao pp_oc + daat_oc (s): ',texec


#correcao da direcao para ficar parecido com o LH (perguntar para o parente)

dire1[2,np.where(dire1[2,:]>300)] = dire1[2,np.where(dire1[2,:]>300)] - 300
dire1[4,np.where(dire1[4,:]>300)] = dire1[4,np.where(dire1[4,:]>300)] - 300
dire1[6,np.where(dire1[6,:]>300)] = dire1[6,np.where(dire1[6,:]>300)] - 300

dire1[2,np.where(dire1[2,:]<45)] = dire1[2,np.where(dire1[2,:]<45)] + 45
dire1[4,np.where(dire1[4,:]<45)] = dire1[4,np.where(dire1[4,:]<45)] + 45
dire1[6,np.where(dire1[6,:]<45)] = dire1[6,np.where(dire1[6,:]<45)] + 45


# pl.figure()
# pl.subplot(311), pl.grid('on')
# pl.plot(datat,matonda[:,-3],'o'), pl.tick_params(labelbottom='off')
# pl.subplot(312), pl.grid('on')
# pl.plot(matonda[:,-2],'o'), pl.tick_params(labelbottom='off')
# pl.subplot(313), pl.grid('on')
# pl.plot(datat,matonda[:,-1],'o')
# pl.xticks(rotation=10)

# pl.figure()
# pl.subplot(411), pl.grid('on')
# pl.plot(datat,matonda[:,-1],'o'),pl.tick_params(labelbottom='off')
# pl.plot(datat,dire1[0,:],'ro'),pl.tick_params(labelbottom='off')
# pl.subplot(412), pl.grid('on')
# pl.plot(datat,matonda[:,-1],'o'),pl.tick_params(labelbottom='off')
# pl.plot(datat,dire1[2,:],'ro'), pl.tick_params(labelbottom='off')
# pl.subplot(413), pl.grid('on')
# pl.plot(datat,matonda[:,-1],'o'), pl.tick_params(labelbottom='off')
# pl.plot(datat,dire1[4,:],'ro'), pl.tick_params(labelbottom='off')
# pl.subplot(414), pl.grid('on')
# pl.plot(datat,matonda[:,-1],'o')#, pl.axis([0,len(matonda),0,360])
# pl.plot(datat,dire1[5,:],'ro')#, pl.axis([0,len(matonda),0,360])
# pl.xticks(rotation=10)


# pl.figure()
# pl.subplot(311), pl.grid('on')
# pl.plot(datat,matonda[:,-3],'o'), pl.tick_params(labelbottom='off')
# pl.title('Significant Wave Height (Hm0)'), pl.ylabel('meters')
# pl.axis('tight')
# pl.subplot(312), pl.grid('on')
# pl.plot(datat,matonda[:,-2],'o'), pl.tick_params(labelbottom='off')
# pl.title('Peak Period (Tp)'), pl.ylabel('seconds')
# pl.axis('tight')
# pl.subplot(313), pl.grid('on')
# pl.plot(datat,matonda[:,-1],'o')
# pl.axis(aux_ax)
# pl.title('Peak Direction (Dp)'), pl.ylabel('degrees')
# pl.axis(aux_ax), pl.xticks(rotation=15)

# pl.figure()
# pl.subplot(411), pl.grid('on')
# pl.plot(datat,dp1,'o'),pl.tick_params(labelbottom='off')
# pl.plot(datat,dire1[0,:],'ro'),pl.tick_params(labelbottom='off')
# pl.axis(aux_ax)
# pl.title('Peak Direction (Dp)\n Frequency Band - 1'), pl.ylabel('degrees')
# pl.legend(['LH','DAAT'],loc=4,prop={'size':6.5})
# # pl.axis([aux_ax])
# pl.subplot(412), pl.grid('on')
# pl.plot(datat,dp2,'o'),pl.tick_params(labelbottom='off')
# pl.plot(datat,dire1[2,:],'ro'), pl.tick_params(labelbottom='off')
# pl.axis(aux_ax)
# pl.title('Frequency Band - 2'), pl.ylabel('degrees')
# # pl.axis([aux_ax])
# pl.subplot(413), pl.grid('on')
# pl.plot(datat,dp3,'o'), pl.tick_params(labelbottom='off')
# pl.plot(datat,dire1[4,:],'ro'), pl.tick_params(labelbottom='off')
# pl.axis(aux_ax)
# pl.title('Frequency Band - 3'), pl.ylabel('degrees')
# # pl.axis([aux_ax])
# pl.subplot(414), pl.grid('on')
# pl.plot(datat,dp4,'o')
# pl.plot(datat,dire1[6,:],'ro')
# pl.title('Frequency Band - 4'), pl.ylabel('degrees')
# pl.axis(aux_ax), pl.xticks(rotation=15)

pl.show()

