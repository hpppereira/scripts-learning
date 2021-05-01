'''
================================================================================== #
PROGRAMA PRINCIPAL PARA PROCESSAMENTO DE DADOS DA BOIA DA BMT-NavCon
Sensor OMDAH
================================================================================== #

Autores: 
Henrique P. P. Pereira
Izabel C M Nogueira
Fabio Nascimento
Carlos Eduardo Parente

Laboratorio de Instrumentacao Oceanografica - COPPE/UFRJ

Data da ultima modificacao: 05/11/2015

================================================================================== #
### Descricao
================================================================================== #
    
Cria uma variavel 'lista' com os arquivos HNE que estao dentro do 'pathname', 
le e processa cada arquivo HNE listado. Passa por uma consitencia, onde sao 
listados os arquivos incosistentes e consistentes atribuindo um flag. Processa
os arquivos consistentes. Chama o modulo 'proc_onda' para processamento dos
dados no dominio do tempo e frequencia. Cria uma variavel 'mat_onda' contendo
os parametros calculados. Cria uma tabela 'saida.txt' com os parametros. Cria
graficos dos parametros.
- Calcula Tp1 (mais energetico) e Tp2
- Calcula Spreading (Tucker) - cos2s?? 

para processar apenas 1 ou poucos arquivos, verificar se o teste de variabildade 
e consecutivos iguais no 'consisteproc.py' estao habilitados, pois pode dar erro

#         0   1   2   3    4     5    6   7   8     9       10       11   12   13   14    15   16   17    18   19
#header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')
        
'''

# ================================================================================== #
# Modulos utilizados
# ================================================================================== #

from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import os
import sys
import numpy as np
import pylab as pl
import time
from datetime import datetime
import proconda
import consistebruto
#import consisteespec
import consisteproc
import relatorio
#import graficos_axys
# import jonswap_wafo #calculo do gamma
import jonswap
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy.stats import norm
import matplotlib.mlab as mlab
import pandas as pd

reload(proconda)
reload(consistebruto)
#reload(consisteespec)
reload(consisteproc)
reload(relatorio)
reload(jonswap)

pl.close('all')


#habilita a daat
#import daat


# ================================================================================== #
# Contador inicial de tempo de execucao

tic = time.clock()

# ================================================================================== #
#### Dados de entrada
# ================================================================================== #


#Escolha a boia (Izabel ou Susana)
boia = 'Izabel'
dmag = -23

print 'Processamento em... ' + boia

#caminho onde estao os arquivos inerciais
pathname = os.environ['HOME'] + '/Dropbox/bmo/dados/' + boia + '/cartao/inercial/'


h = 300 #profundidade 
nfft = 244 #(244-16gl) #numero de dados para a fft (p/ nlin=1312: 32gl;nfft=82, 16gl;nfft=164, 8gl;nfft=328)
fs = 1.28 #freq de amostragem
nlin = 1952 #tem 1952 amostras
gl = (nlin/nfft) * 2

#numero de testes habilitados
#ntb = 9 #brutos
#nte = 3 #espectro
#ntp = 3 #processado

#numero de parametros a serem calculados
#npa = 19

#vetor de tempo

# ================================================================================== #
#DAAT

# espe1, energ, dire1 = daat.daat1(pathname,listap,nfft,fs,ncol,p0,p1)
# np.savetxt('saida/'+'espe1.out',espe1,delimiter=',',fmt='%.1f')
# np.savetxt('saida/'+'dire1.out',dire1,delimiter=',',fmt='%.1f')
# np.savetxt('saida/'+'energ.out',energ,delimiter=',',fmt='%.1f')


#lista arquivos inerciais
lista = []
datat = [] #cria lista com nome dos arquivos
# Lista arquivos do diretorio atual
for f in os.listdir(pathname):
    if f.startswith('Inercial'):
        lista.append(f)
lista=np.sort(lista)

#lista = lista[:50]

#data a partir do nome do arquivo
datat = [datetime.strptime(lista[i][9:13]+lista[i][14:16]+lista[i][17:19]+lista[i][21:23],'%Y%m%d%H') for i in range(len(lista))]

#======================================================================#


#cria variavel 'lista' com nome dos arquivos HNE
#lista = np.array(lista_hne(pathname))
#p0 = 1000
#p1 = 1100 #len(lista)

#numero dos arq para processar (modificar p0=0 e p1=len(lista) para todos)
#p0 = np.where(lista == z0)[0][0]
#p1 = np.where(lista == z1)[0][0]


# ================================================================================== #
#### Incicializacao do programa
# ================================================================================== #

#lista dos arquivos que serao processados
#listap = lista

#listap = [listap[i][0:-4] for i in range(len(listap))]

#numero de arquivos a serem processados
#ncol = len(listap)

#cria vetores de flags das series brutas
#flagb = np.zeros((len(listap),4),dtype='|S32')
#flagb[:,0] = listap

#cria vetores de flags dos parametros espectrais
#flage = np.zeros((1,4),dtype='S32')
#flage1 = np.copy(flage)

#parametros criados no processamento em batelada
matondab = [] #matriz com parametros de onda
listac = [] #lista de arquivos consistentes
listai = [] #lista de arquivos inconsistentes

# ================================================================================== #
#### Processamento em batelada
# ================================================================================== #

#contador
cont = -1
#eta_mat = []
#eta_med = []
#eta_dp = []
#fase_nnx = [] #valor do espec de fase para a fp
#fase_nny = [] #valor do espec de fase para a fp
#fase_nxny = [] #valor do espec de fase para a fp
#coer_nnx = [] #valor do espec de coerencia para a fp
#coer_nny = [] #valor do espec de coerencia para a fp
#coer_nxny = [] #valor do espec de coerencia para a fp
#data frame com parametros

#inicia processamento em batelada
for i in range(len(lista)):

    print 'LH: ' + str(i+1) + ' -- ' + str(datat[i])  

    cont = cont + 1

    #carrega dados
    dd = pd.read_csv(pathname + lista[i], skiprows=5, names=['date','rol','pit','hd1','hv','hd2','st'],
     parse_dates=['date'])

    if len(dd) < 1000:

        listai.append(datat[i])
        pass

    else:

        listac.append(datat[i])

        #vetor de tempo
        dd['t'] = np.linspace(0,len(dd)*1/fs,len(dd))

        #processamento no dominio do tempo
        hs,h10,hmax,tmed,thmax = proconda.ondat(dd.t,dd.hv,h)

        #processamento no dominio da frequencia
        hm0, tp, dp, sigma1, sigma2, sigma1p, sigma2p, freq, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
            dd.hv,dd.pit,dd.rol,h,nfft,fs)

        #corrige a declinacao magnetica
        dp = dp + dmag
        if dp < 0:
            dp = dp + 360

        dire1[pl.find(dire1<0)] = dire1[pl.find(dire1<0)] + 360
        dire2[pl.find(dire2<0)] = dire1[pl.find(dire2<0)] + 360

        #processamento no dominio da frequencia particionado (sea e swell)
        hm01, tp1, dp1, hm02, tp2, dp2 = proconda.ondap(hm0,tp,dp,sn,dire1,df)

        #calculo do parametro gamma - LIOc
        gam = jonswap.gamma(tp)
        gam1 = jonswap.gamma(tp1)
        gam2 = jonswap.gamma(tp2)

        #espectro de jonswap
        s_js = jonswap.spec(hm0,tp,freq,gam)
        s_js2 = jonswap.spec(hm02,tp2,freq,gam2)

         #         0   1   2   3    4     5    6   7   8     9       10       11   12   13   14    15   16   17    18   19
        #header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')
        # * no caso de utilizar a consiste_espec, remover uma identacao no 'matonda'
        #matondab.append(np.concatenate([([int(listac[-1])]),[hs,h10,hmax,tmed,thmax,hm0,tp,dp,sigma1p,sigma2p,hm01,tp1,dp1,hm02,tp2,dp2,gam,gam1,gam2]]))

        matondab.append([hs,h10,hmax,thmax,hm0,tp,dp,hm01,tp1,dp1,hm02,tp2,dp2])
        


dfp = pd.DataFrame(np.array(matondab), index=listac, columns=['hs','h10','hmax','thmax','hm0','tp','dp','hm01','tp1','dp1','hm02','tp2','dp2']) 

#salva arquivo csv
dfp.to_csv('out/omdah_waveparam_comb02_' + str(gl) + 'gl.csv',index_label='date')



'''


    # ================================================================================== #  
    # Testes de consistencia dos dados processados
    
    #Teste 1 - validade da mensagem (apenas axys *.HNE) -  validade do nome do arquivo (ind=0)
    flagb[i,1] = consistebruto.msg(listap[i],flagb[i,1])
    flagb[i,2] = consistebruto.msg(listap[i],flagb[i,2])
    flagb[i,3] = consistebruto.msg(listap[i],flagb[i,3])
    
    #Teste 2 - comprimento do vetor (ind=1)
    flagb[i,1] = consistebruto.comp(eta,1312,flagb[i,1])
    flagb[i,2] = consistebruto.comp(etax,1312,flagb[i,2])
    flagb[i,3] = consistebruto.comp(etay,1312,flagb[i,3])

    #Teste 3 - gap (lacuna)
    flagb[i,1] = consistebruto.gap(eta,10,flagb[i,1])
    flagb[i,2] = consistebruto.gap(etax,10,flagb[i,2])
    flagb[i,3] = consistebruto.gap(etay,10,flagb[i,3])

    #Teste 4 - spike
    flagb[i,1], vet_etai = consistebruto.spike(eta,np.mean(eta),np.std(eta),10,5,2,flagb[i,1])
    flagb[i,2], vet_etaxi = consistebruto.spike(etax,np.mean(etax),np.std(etax),10,5,2,flagb[i,2])
    flagb[i,3], vet_etayi = consistebruto.spike(etay,np.mean(etay),np.std(etay),10,5,2,flagb[i,3])
    
    #Teste 5 - valores flat
    flagb[i,1] = consistebruto.flat(eta,-0.15,0.15,flagb[i,1])
    flagb[i,2] = consistebruto.flat(etax,-0.15,0.15,flagb[i,2])
    flagb[i,3] = consistebruto.flat(etay,-0.15,0.15,flagb[i,3])
    
    #Teste 6 - valores consecutivos nulos
    flagb[i,1] = consistebruto.nulos(eta,10,flagb[i,1])
    flagb[i,2] = consistebruto.nulos(etax,10,flagb[i,2])
    flagb[i,3] = consistebruto.nulos(etay,10,flagb[i,3])
    
    #Teste 7 -valores consecutivos iguais
    flagb[i,1] = consistebruto.iguais(eta,10,flagb[i,1])
    flagb[i,2] = consistebruto.iguais(etax,10,flagb[i,2])
    flagb[i,3] = consistebruto.iguais(etay,10,flagb[i,3])
 
    #Teste 8 -valores que excedem limites de faixa
    flagb[i,1] = consistebruto.faixa(eta,-20,20,flagb[i,1])
    flagb[i,2] = consistebruto.faixa(etax,-20,20,flagb[i,2])
    flagb[i,3] = consistebruto.faixa(etay,-20,20,flagb[i,3])

    #Teste 9 -deslocamento da media (shift)
    flagb[i,1] = consistebruto.shift(eta,164,8,0.3,flagb[i,1])
    flagb[i,2] = consistebruto.shift(etax,164,8,0.3,flagb[i,2])
    flagb[i,3] = consistebruto.shift(etay,164,8,0.3,flagb[i,3])

    # ================================================================================== #
    # Condicao para dados aprovados na consistencia dos dados brutos
    
    if (flagb[i,1:] == [ntb*'1',ntb*'1',ntb*'1']).all():

        t = t[0:nlin]
        eta = eta[0:nlin]
        etax = etax[0:nlin]
        etay = etay[0:nlin]

        #cria matriz com serie de heave (para o calculo do multiplicador do desvio padrao)
        eta_mat.append(eta)
        eta_med.append(np.mean(eta))
        eta_dp.append(np.std(eta))

        #lista nome dos arquivos consistentes 
        listac.append(listap[cont])

        #processamento no dominio do tempo
        hs,h10,hmax,tmed,thmax = proconda.ondat(t,eta,h)

        #processamento no dominio da frequencia
        hm0, tp, dp, sigma1, sigma2, sigma1p, sigma2p, freq, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
            eta,etax,etay,h,nfft,fs)

        #corrige a declinacao magnetica
        dp = dp + dmag
        if dp < 0:
            dp = dp + 360

        dire1[pl.find(dire1<0)] = dire1[pl.find(dire1<0)] + 360
        dire2[pl.find(dire2<0)] = dire1[pl.find(dire2<0)] + 360



        #calcula o espectro de fase (fase e coerencia)
        #acha o indice da fp
        indfp = pl.find(sn[:,0]==sn[sn[:,1]==max(sn[:,1]),0])

        fase_nnx.append(np.real(snnx[indfp,4])[0]) #fase de heave e dspx
        fase_nny.append(np.real(snny[indfp,4])[0]) #fase de heave e dspx
        fase_nxny.append(np.real(snxny[indfp,4])[0]) #fase de heave e dspx

        coer_nnx.append(np.real(snnx[indfp,5])[0]) #coerencia de heave e dspx
        coer_nny.append(np.real(snny[indfp,5])[0]) #coerencia de heave e dspx
        coer_nxny.append(np.real(snxny[indfp,5])[0]) #coerencia de heave e dspx



        #processamento no dominio da frequencia particionado (sea e swell)
        hm01, tp1, dp1, hm02, tp2, dp2 = proconda.ondap(hm0,tp,dp,sn,dire1,df)



        #calculo do parametro gamma - LIOc
        gam = jonswap.gamma(tp)
        gam1 = jonswap.gamma(tp1)
        gam2 = jonswap.gamma(tp2)

        #espectro de jonswap
        s_js = jonswap.spec(hm0,tp,freq,gam)
        s_js2 = jonswap.spec(hm02,tp2,freq,gam2)

 

        #         0   1   2   3    4     5    6   7   8     9       10       11   12   13   14    15   16   17    18   19
        #header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')
        # * no caso de utilizar a consiste_espec, remover uma identacao no 'matonda'
        matondab.append(np.concatenate([([int(listac[-1])]),[hs,h10,hmax,tmed,thmax,hm0,tp,dp,sigma1p,sigma2p,hm01,tp1,dp1,hm02,tp2,dp2,gam,gam1,gam2]]))

    #Condicao para dado inconsistentes
    else:

        #lista nome dos arquivos inconsistentes 
        listai.append(listap[i])

        #coloca NaN nos dados reprovados na consistencia dos dados brutos e espectrais
        matondab.append(np.concatenate([([int(listai[-1])]),npa * [np.nan]]))


# ================================================================================== #  
#### Finalizacao do processamento em batelada
# ================================================================================== #  


# ================================================================================== #  
# Realiza a consistencia dos dados processados

if len(listac) > 0:

    #deixa coluna de dados em string
    # matonda[:,0].astype(int)
    
    #cria array das listas criadas
    matondab = np.array(matondab)
    listac = np.array(listac)
    listaip = np.copy(listai)
    listai = np.array(listai)

    #cria vetor dos parametros calculados
    datap = matondab[:,0]
    hs = matondab[:,1] 
    h10 = matondab[:,2] 
    hmax = matondab[:,3]
    tmed = matondab[:,4] 
    thmax = matondab[:,5] 
    hm0 = matondab[:,6] 
    tp = matondab[:,7] 
    dp = matondab[:,8] 
    sigma1p = matondab[:,9] 
    sigma2p = matondab[:,10] 
    hm01 = matondab[:,11] 
    tp1 = matondab[:,12]
    dp1 = matondab[:,13]
    hm02 = matondab[:,14]
    tp2 = matondab[:,15] 
    dp2 = matondab[:,16]
    gam = matondab[:,17]
    gam1 = matondab[:,18]
    gam2 = matondab[:,19]

    #cria vetores de flags das series processadas (depende das qtdade de variaveis a serem consistidas + data) 
    flagp = np.zeros((len(listap),npa+1),dtype='|S32')
    flagp[:,0] = listap[:]
    
    # ================================================================================== #  
    # Testes de consistencia dos dados processados

    #Teste 1 - faixa
    flagp[:,1] = consisteproc.faixa(hs,0,20,0.25,8,flagp[:,1])
    flagp[:,2] = consisteproc.faixa(h10,0,20,0.25,8,flagp[:,2])
    flagp[:,3] = consisteproc.faixa(hmax,0,35,0.5,20,flagp[:,3])
    flagp[:,4] = consisteproc.faixa(tmed,3,30,4,18,flagp[:,4])
    flagp[:,5] = consisteproc.faixa(thmax,3,30,4,18,flagp[:,5])
    flagp[:,6] = consisteproc.faixa(hm0,0,20,0.25,8,flagp[:,6])
    flagp[:,7] = consisteproc.faixa(tp,3,30,4,18,flagp[:,7])
    flagp[:,8] = consisteproc.faixa(dp,0,360,0,360,flagp[:,8])
    flagp[:,9] = consisteproc.faixa(sigma1p,0,360,0,360,flagp[:,9])
    flagp[:,10] = consisteproc.faixa(sigma2p,0,360,0,360,flagp[:,10])
    flagp[:,11] = consisteproc.faixa(hm01,0,20,0.25,8,flagp[:,11])
    flagp[:,12] = consisteproc.faixa(tp1,3,30,4,18,flagp[:,12])
    flagp[:,13] = consisteproc.faixa(dp1,0,360,0,360,flagp[:,13])
    flagp[:,14] = consisteproc.faixa(hm02,0,20,0.25,8,flagp[:,14])
    flagp[:,15] = consisteproc.faixa(tp2,3,30,4,18,flagp[:,15])
    flagp[:,16] = consisteproc.faixa(dp2,0,360,0,360,flagp[:,16])

    #Teste 2 - Variabilidade temporal
    flagp[:,1] = consisteproc.variab(hs,1,5,flagp[:,1])
    flagp[:,2] = consisteproc.variab(h10,1,5,flagp[:,2])
    flagp[:,3] = consisteproc.variab(hmax,1,5,flagp[:,3])
    flagp[:,4] = consisteproc.variab(tmed,1,20,flagp[:,4])
    flagp[:,5] = consisteproc.variab(thmax,1,20,flagp[:,5])
    flagp[:,6] = consisteproc.variab(hm0,1,5,flagp[:,6])
    flagp[:,7] = consisteproc.variab(tp,1,20,flagp[:,7])
    flagp[:,8] = consisteproc.variab(dp,1,360,flagp[:,8])
    flagp[:,9] = consisteproc.variab(hm01,1,5,flagp[:,9])
    flagp[:,10] = consisteproc.variab(sigma1p,1,360,flagp[:,10])
    flagp[:,11] = consisteproc.variab(sigma2p,1,360,flagp[:,11])
    flagp[:,12] = consisteproc.variab(tp1,1,20,flagp[:,12])
    flagp[:,13] = consisteproc.variab(dp1,1,360,flagp[:,13])
    flagp[:,14] = consisteproc.variab(hm02,1,5,flagp[:,14])
    flagp[:,15] = consisteproc.variab(tp2,1,20,flagp[:,15])
    flagp[:,16] = consisteproc.variab(dp2,1,360,flagp[:,16])

    #Teste 3 - Valores consecutivos iguais (*verificar num de arquivos em 'listac')
    # flagp[:,1] = consisteproc.iguais(hs,5,flagp[:,1])
    # flagp[:,2] = consisteproc.iguais(h10,5,flagp[:,2])
    # flagp[:,3] = consisteproc.iguais(hmax,5,flagp[:,3])
    # flagp[:,4] = consisteproc.iguais(tmed,20,flagp[:,4])
    # flagp[:,5] = consisteproc.iguais(thmax,20,flagp[:,5])
    # flagp[:,6] = consisteproc.iguais(hm0,5,flagp[:,6])
    # flagp[:,7] = consisteproc.iguais(tp,20,flagp[:,7])
    # flagp[:,8] = consisteproc.iguais(dp,20,flagp[:,8])
    # flagp[:,9] = consisteproc.iguais(sigma1p,20,flagp[:,9])
    # flagp[:,10] = consisteproc.iguais(sigma2p,20,flagp[:,10])
    # flagp[:,11] = consisteproc.iguais(hm01,5,flagp[:,11])
    # flagp[:,12] = consisteproc.iguais(tp1,20,flagp[:,12])
    # flagp[:,13] = consisteproc.iguais(dp1,20,flagp[:,13])
    # flagp[:,14] = consisteproc.iguais(hm02,5,flagp[:,14])
    # flagp[:,15] = consisteproc.iguais(tp2,20,flagp[:,15])
    # flagp[:,16] = consisteproc.iguais(dp2,20,flagp[:,16])


    # ================================================================================== #  
    # Coloca nan nos dados reprovados
    
    matondap = np.copy(matondab)

    for c in range(1,flagp.shape[1]):

        for i in range(len(flagp)):

            if '4' in flagp[i,c]:

                matondap[i,c] = np.nan


    # ================================================================================== #  

    #parametros de ondas processados
    # matondap = np.array([datap,hsc,h10c,hmaxc,tmedc,thmaxc,hm0c, tpc, dpc, sigma1pc,
    # sigma2pc, hm01c, tp1c, dp1c, hm02c, tp2c, dp2c]).T

    # ================================================================================== #  
    # Imprime relatorio de controle de qualidade

    # salva relatorio em txt
    # f = open('saida/'+'consistencia_'+str(gl)+'-'+local1+'.out','w')
    # fflagb, fflagp = relatorio.axys(f,lista,listap,listac,listai,flagb,flagp,h,local,latlon,idargos,idwmo)
    

    # ================================================================================== #  
    # ================================================================================== #  
    # Cria saida de dados com savetxt

    #parametros de ondas com cq apenas nos dados brutos
    np.savetxt('out/'+'triaxys_bruto_'+str(gl)+'_'+local1+'.out',matondab,delimiter=',',fmt=['%i']+npa*['%.2f'],
        header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')

    #parametros de ondas com cq nos dados brutos e processados
    np.savetxt('out/'+'triaxys_proc_'+str(gl)+'_'+local1+'.out',matondap,delimiter=',',fmt=['%i']+npa*['%.2f'],
        header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')

    #flags aplicados nos dados brutos
    np.savetxt('out/'+'triaxys_flag_bruto_'+str(gl)+'_'+local1+'.out',flagb,delimiter=',',fmt='%s',
        header='date,eta,etax,etay')

    #flags aplicados nos dados processados
    np.savetxt('out/'+'triaxys_flag_proc_'+str(gl)+'_'+local1+'.out',flagp,delimiter=',',fmt='%s',
        header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2')

    #lista de dados aprovados no cq bruto
    #np.savetxt('out/'+'listacb_'+str(gl)+'-'+local1+'.out',listac,fmt='%s') #lista de dados aprovados no cq bruto

    #lista de dados reprovados no cq bruto
    #np.savetxt('out/'+'listaib_'+str(gl)+'-'+local1+'.out',listai,fmt='%s') #lista de dados reprovados no cq bruto


else:

    print('Todos os arquivos reprovaram em algum teste de Controle de Qualidade' '\n' '\n')

#data com datetime
datat = np.array([datetime.strptime(str(int(matondap[i,0])), '%Y%m%d%H%M') for i in range(len(matondap))])
datatcb = np.array([datetime.strptime(str(int(listac[i])), '%Y%m%d%H%M') for i in range(len(listac))])


# ================================================================================== #  
# Salva saida da daat (espe e dire)



# ================================================================================== #  
# Tempo de execucao da rotina

#contador inicial de tempo de execucao
toc = time.clock()

#tempo de execucao
texec = toc - tic

print 'Tempo de execucao pp_proc + daat_oc (s): ',texec



pl.show()



'''