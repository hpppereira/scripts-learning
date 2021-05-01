'''
================================================================================== #
PROGRAMA PRINCIPAL PARA PROCESSAMENTO DE DADOS DA BOIA AXYS
================================================================================== #

Autores: 
Henrique P. P. Pereira
Izabel C. M. Nogueira
Ricardo M. Campos
Carlos E. Parente
Fabio Nascimento

Laboratorio de Instrumentacao Oceanografica - COPPE/UFRJ

Data da ultima modificacao: 03/10/2014

================================================================================== #
### Descricao

Boia: Axys 3M - Rio Grande/RS - PNBOIA

Cria uma variavel 'lista' com os arquivos HNE que estao dentro do 'pathname', 
le e processa cada arquivo HNE listado. Passa por uma consitencia, onde sao 
listados os arquivos incosistentes e consistentes atribuindo um flag. Processa
os arquivos consistentes. Chama o modulo 'proc_onda' para processamento dos
dados no dominio do tempo e frequencia. Cria uma variavel 'mat_onda' contendo
os parametros calculados. Cria uma tabela 'saida.txt' com os parametros. Cria
graficos dos parametros.
- Calcula Tp1 (mais energetico) e Tp2
- Calcula Spreading (Tucker) - cos2s??

Para processar apenas 1 ou poucos arquivos, verificar se o teste de variabildade 
e consecutivos iguais no 'consiste_proc.py' estao habilitados, pois pode dar erro

================================================================================== #
### Processamento

Processamento dos dados brutos da boia Wavescan do projeto SIODOC
Processamento dos dados da boia do SIODOC com a DAAT/PLEDS

Dados brutos: heave, pitch, roll e compass

a) Verificar a necessidade da correcao
das series de heave, pitch e roll

b) Verificar com Parente ou Candella como corrige as series de pitch 
e roll com o compass (manual ndbc96 ?? )
c) As matrizes tem dimensao de 3020x1030 - as series estao em linha??

              0  1   2  3  4   5       6,7,8, ...
d) Formato: YYYY,MM,DD,hh,mm?,ss?, --> serie ....
'''

# ================================================================================== #
#### Modulos utilizados
# ================================================================================== #

import os
import sys
import numpy as np
import pylab as pl
import scipy.io
import time
from datetime import datetime
# import loadhne
import proconda
import consiste_bruto
# import consiste_espec
import consiste_proc
# import daat
# import relatorio
# import graficos_axys
import jonswap

reload(proconda)
reload(consiste_bruto)
# reload(consiste_espec)
reload(consiste_proc)
# reload(daat)
# reload(relatorio)
# reload(graficos_axys)
reload(jonswap)

# pl.close('all')

# ================================================================================== #
# Contador inicial de tempo de execucao

tic = time.clock()

# ================================================================================== #
#### Dados de entrada
# ================================================================================== #

#localizacao
local = 'Arraial do cabo/RJ' # relatorio
local1 = 'arrcabo_siodoc' #nome do arquivo salvo
latlon = '-22.995 / -42.187 ' #relatorio
idargos = '--'
idwmo = '--'

#caminho onde estao os arquivos brutos (.mat)
pathname = os.environ['HOME'] + '/Dropbox/siodoc/dados/bruto/'

#carrega arquivos .mat
hvmat = scipy.io.loadmat(pathname + 'heave.mat')
ptmat = scipy.io.loadmat(pathname + 'pitch.mat')
rlmat = scipy.io.loadmat(pathname + 'roll.mat')
cpmat = scipy.io.loadmat(pathname + 'compass.mat')

#  0    1    2    3     4    5  
# ano, mes, dia, hora, min, seg
data_all = hvmat.values()[1][:,[0,1,2,3,4,5]]

#data de todos os arquivos com datetime
datat_all = [datetime(int(data_all[i,0]),int(data_all[i,1]),int(data_all[i,2]),
    int(data_all[i,3])) for i in range(len(data_all))]
datat_all = np.array(datat_all) #coloca datat em array

#cria vetor de data em str (ex: '2014-07-16 16:00:00')
data_allstr = datat_all.astype(str) 

hv_all = hvmat.values()[1][:,6:]
pt_all = ptmat.values()[0][:,6:]
rl_all = rlmat.values()[0][:,6:]
cp_all = cpmat.values()[0][:,6:]

#escolhe a data inicial e final para ser processada (opcional, no 'p0' e 'p1')
z0 = '2014-10-01 00:00:00' #ini: '2014-07-16 16:00:00' (brutos: 2014-07)
z1 = '2014-11-01 00:00:00' #fim: '2014-11-19 11:00:00'

# #numero dos arq para processar (modificar p0=0 e p1=len(lista) para todos)
p0 = np.where(data_allstr == z0)[0][0]
p1 = np.where(data_allstr == z1)[0][0]

#datas apenas dos arquivos processados

#  0    1    2    3     4    5  
# ano, mes, dia, hora, min, seg
datavet = hvmat.values()[1][p0:p1,[0,1,2,3,4,5]]

#data com datetime
datat = [datetime(int(datavet[i,0]),int(datavet[i,1]),int(datavet[i,2]),
    int(datavet[i,3]),int(datavet[i,4])) for i in range(len(datavet))]

#coloca datat em array
datat = np.array(datat)

#cria vetor de data em str (ex: '2014-07-16 16:00:00')
datastr = datat.astype(str) 

#lista dos arquivos que serao processados - data em numero (AAAAMMDDHHMM)
listap = np.array([ int(datastr[i][0:4]+datastr[i][5:7]+datastr[i][8:10]+datastr[i][11:13]+
    datastr[i][14:16]) for i in range(len(datastr))])

# listap = [str(int(datavec[i,0]))+str(int(datavec[i,1]))+str(int(datavec[i,2]))+
#     str(int(datavec[i,3]))+str(int(datavec[i,4])) for i in range(len(datavec))]

# listap = np.array(listap)
listap = list(listap.astype(str))

#lista dos arquivos que serao processados
# listap = dataint[p0:p1+1]

hv = hvmat.values()[1][p0:p1+1,6:] #heave
pt = ptmat.values()[0][p0:p1+1,6:] #pitch
rl = rlmat.values()[0][p0:p1+1,6:] #roll
cp = cpmat.values()[0][p0:p1+1,6:] #compass

# #faz a correcao de pitch e roll em slpEW e slpNS

# valores do compass em radianos
cp_rad = cp * (np.pi/180)

#?? teste
cp_rad = np.arctan(np.sin(cp_rad) / np.cos(cp_rad))

#correcao do compass (NDBC 96, pg.14)

#pitch
pitch_EW = ( (np.sin(cp_rad) * np.sin(pt)) / np.cos(pt) ) -  ( (np.cos(cp_rad) * np.sin(rl)) / (np.cos(pt) * np.cos(rl)) )

#roll
roll_NS = ( (np.cos(cp_rad) * np.sin(pt)) / np.cos(pt) ) +  ( (np.sin(cp_rad) * np.sin(rl)) / (np.cos(pt) * np.cos(rl)) )

pt = pitch_EW
rl = roll_NS

#parametros para processamento

h = 60 #profundidade 
nfft = 256 #numero de dados para a fft (para nlin=1312 -- p/ 32gl, nfft=82 ; p/8 gl, nfft=328)
fs = 1 #freq de amostragem
nlin = 1024 #comprimento da serie temporal a ser processada
gl = (nlin/nfft) * 2 #graus de liberdade
t = range(1,1025) ##vetor de tempo

#numero de testes habilitados
ntb = 8 #brutos
#nte = 3 #espectro
ntp = 3 #processado

#numero de parametros a serem calculados
npa = 19

# ================================================================================== #
#### Incicializacao do programa
# ================================================================================== #

# listap = [listap[i][0:-4] for i in range(len(listap))]

#numero de arquivos a serem processados
ncol = len(listap)

#cria vetores de flags das series brutas
flagb = np.zeros((len(listap),4),dtype='|S32')
flagb[:,0] = listap

#cria vetores de flags dos parametros espectrais
# flage = np.zeros((1,4),dtype='S32')
# flage1 = np.copy(flage)

#parametros criados no processamento em batelada
matondab = [] #matriz com parametros de onda
listac = [] #lista de arquivos consistentes
listai = [] #lista de arquivos inconsistentes

# ================================================================================== #
#### Processamento em batelada
# ================================================================================== #

# ================================================================================== #
#DAAT

# espe1, energ, dire1 = daat.daat1(pathname,listap,nfft,fs,ncol,p0,p1)

# ================================================================================== #
    
#contador
cont = -1

for i in range(len(listap)):

    # print 'LH: ' + str(i+1)   

    cont = cont + 1

    #carrega dados e data
    # dados, data = dados_hne(pathname,listap[i]+'.HNE')

    #define variaveis
    eta = hv[i,:] #heave
    etax = pt[i,:] #pitch
    etay = rl[i,:] #roll
    buss = cp[i,:] #bussola

    # ================================================================================== #  
    # Testes de consistencia dos dados processados
    
    #Teste 1 - validade da mensagem (apenas axys *.HNE) -  validade do nome do arquivo (ind=0)
    # flagb[i,1] = consiste_bruto.msg(listap[i],flagb[i,1])
    # flagb[i,2] = consiste_bruto.msg(listap[i],flagb[i,2])
    # flagb[i,3] = consiste_bruto.msg(listap[i],flagb[i,3])
    
    #Teste 2 - comprimento do vetor (ind=1)
    flagb[i,1] = consiste_bruto.comp(eta,1024,flagb[i,1])
    flagb[i,2] = consiste_bruto.comp(etax,1024,flagb[i,2])
    flagb[i,3] = consiste_bruto.comp(etay,1024,flagb[i,3])

    #Teste 3 - gap (lacuna)
    flagb[i,1] = consiste_bruto.gap(eta,10,flagb[i,1])
    flagb[i,2] = consiste_bruto.gap(etax,10,flagb[i,2]) 
    flagb[i,3] = consiste_bruto.gap(etay,10,flagb[i,3])

    #Teste 4 - spike
    flagb[i,1], vet_etai = consiste_bruto.spike(eta,np.mean(eta),np.std(eta),10,5,2,flagb[i,1])
    flagb[i,2], vet_etaxi = consiste_bruto.spike(etax,np.mean(etax),np.std(etax),10,5,2,flagb[i,2]) 
    flagb[i,3], vet_etayi = consiste_bruto.spike(etay,np.mean(etay),np.std(etay),10,5,2,flagb[i,3])
    
    #Teste 5 - valores flat
    flagb[i,1] = consiste_bruto.flat(eta,-0.10,0.10,flagb[i,1]) #verificar que eh pitch e roll
    flagb[i,2] = consiste_bruto.flat(etax,-0.05,0.05,flagb[i,2])
    flagb[i,3] = consiste_bruto.flat(etay,-0.05,0.05,flagb[i,3])
    
    #Teste 6 - valores consecutivos nulos
    flagb[i,1] = consiste_bruto.nulos(eta,10,flagb[i,1])
    flagb[i,2] = consiste_bruto.nulos(etax,10,flagb[i,2])
    flagb[i,3] = consiste_bruto.nulos(etay,10,flagb[i,3])
    
    #Teste 7 -valores consecutivos iguais
    flagb[i,1] = consiste_bruto.iguais(eta,10,flagb[i,1])
    flagb[i,2] = consiste_bruto.iguais(etax,10,flagb[i,2])
    flagb[i,3] = consiste_bruto.iguais(etay,10,flagb[i,3])
 
    #Teste 8 -valores que excedem limites de faixa
    flagb[i,1] = consiste_bruto.faixa(eta,-20,20,flagb[i,1])
    flagb[i,2] = consiste_bruto.faixa(etax,-20,20,flagb[i,2])
    flagb[i,3] = consiste_bruto.faixa(etay,-20,20,flagb[i,3])

    #Teste 9 -deslocamento da media (shift)
    flagb[i,1] = consiste_bruto.shift(eta,164,8,0.2,flagb[i,1])
    flagb[i,2] = consiste_bruto.shift(etax,164,8,0.2,flagb[i,2])
    flagb[i,3] = consiste_bruto.shift(etay,164,8,0.2,flagb[i,3])

    # ================================================================================== #
    # Condicao para dados aprovados na consistencia dos dados brutos
    
    if (flagb[i,1:] == [ntb*'1',ntb*'1',ntb*'1']).all():

        eta = eta[0:nlin]
        etax = etax[0:nlin]
        etay = etay[0:nlin]

        #lista nome dos arquivos consistentes 
        listac.append(listap[cont])

        #processamento no dominio do tempo
        hs,h10,hmax,tmed,thmax = proconda.ondat(t,eta,h)

        #processamento no dominio da frequencia
        hm0, tp, dp, sigma1p, sigma2p, freq, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
            eta,etax,etay,h,nfft,fs)

        # #parametros de ondas instantaneos
        # Hm0 = pondaf[0]
        # Tp = pondaf[1]
        # Dp = pondaf[2]

        #plota o espectro
        # pl.figure()
        # pl.plot(f,sn[:,1])
        # pl.title(listac[-1])

        #processamento no dominio da frequencia particionado (sea e swell)
        hm01, tp1, dp1, hm02, tp2, dp2 = proconda.ondap(hm0,tp,dp,sn,dire1,df)

        #calculo do parametro gamma - WAFO
        # gam = jonswap.jonswap_peakfact(hm0,tp)
        # gam1 = jonswap.jonswap_peakfact(hm01,tp1)
        # gam2 = jonswap.jonswap_peakfact(hm02,tp2)

        #calculo do parametro gamma - LIOc
        gam = jonswap.gamma(tp)
        gam1 = jonswap.gamma(tp1)
        gam2 = jonswap.gamma(tp2)

        #espectro de jonswap
        s_js = jonswap.spec(hm0,tp,freq,gam)
        s_js2 = jonswap.spec(hm02,tp2,freq,gam2)

        # pl.figure()
        # pl.plot(freq,sn[:,1],freq,s_js,freq,s_js2)
        # pl.legend(['LIOc','JS-1','JS-2'])
        # pl.title('Espectro de Energia - LIOc')
        # pl.xlabel('Frequencia (Hz)')
        # pl.ylabel('m^2/Hz')
        # pl.grid()
        
        #                       0  1   2   3    4     5    6   7   8     9         10     11   12   13    14   15   16
        #parametros de onda = data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2
        # * no caso de utilizar a consiste_espec, remover uma identacao no 'matonda'
        # matondab.append([np.concatenate((listap[i],hs,h10,hmax,tmed,thmax,hm0,tp,dp,sigma1p,sigma2p,hm01,tp1,dp1,hm02,tp2,dp2,gam,gam1,gam2))])

        # matondab.append(np.concatenate([([int(listac[-1])]),[hs,h10,hmax,tmed,thmax,hm0,tp,dp,sigma1p,sigma2p,hm01,tp1,dp1,hm02,tp2,dp2,gam,gam1,gam2]]))
        matondab.append(np.concatenate([([int(listac[-1])]),[hs,h10,hmax,tmed,thmax,hm0,tp,dp,sigma1p,sigma2p,hm01,tp1,dp1,hm02,tp2,dp2,gam,gam1,gam2]]))

        
        print 'LH: ' + str(i+1) + ' | ' + datastr[i] + ' | CQ-CT: OK | Flag-CT: ' + str(flagb[i,:])
        

    #Condicao para dado inconsistentes
    else:

        #lista nome dos arquivos inconsistentes 
        listai.append(listap[i])

        #coloca NaN nos dados reprovados na consistencia dos dados brutos e espectrais
        matondab.append(np.concatenate([([int(listai[-1])]),npa * [np.nan]]))

        print 'LH: ' + str(i+1) + ' | ' + datastr[i] + ' | CQ-CT: -- | Flag-CT: ' + str(flagb[i,:])

# ================================================================================== #  
#### Finalizacao do processamento em batelada
# ================================================================================== #  

#retira a ultima linha do flage
# flage = flage[:-1,:]

# ================================================================================== #  
# Realiza a consistencia dos dados processados

if len(listac) > 0:

    #deixa coluna de dados em string
    # matonda[:,0].astype(int)
    
    #cria array das listas criadas
    matondab = np.array(matondab)
    listac = np.array(listac)
    listaip = np.copy(listai) #lista dos inconsistntes dos no cq de lt?
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
    # flagp = np.zeros((len(listap),npa+1),dtype='|S32')

    # ================================================================================== #  
    # Testes de consistencia dos dados processados

    #Teste 1 - faixa
    flagp[:,1] = consiste_proc.faixa(hs,0,20,0.25,8,flagp[:,1])
    flagp[:,2] = consiste_proc.faixa(h10,0,20,0.25,8,flagp[:,2])
    flagp[:,3] = consiste_proc.faixa(hmax,0,35,0.5,20,flagp[:,3])
    flagp[:,4] = consiste_proc.faixa(tmed,3,30,4,18,flagp[:,4])
    flagp[:,5] = consiste_proc.faixa(thmax,3,30,4,18,flagp[:,5])
    flagp[:,6] = consiste_proc.faixa(hm0,0,20,0.25,8,flagp[:,6])
    flagp[:,7] = consiste_proc.faixa(tp,3,30,4,18,flagp[:,7])
    flagp[:,8] = consiste_proc.faixa(dp,0,360,0,360,flagp[:,8])
    flagp[:,9] = consiste_proc.faixa(sigma1p,0,360,0,360,flagp[:,9])
    flagp[:,10] = consiste_proc.faixa(sigma2p,0,360,0,360,flagp[:,10])
    flagp[:,11] = consiste_proc.faixa(hm01,0,20,0.25,8,flagp[:,11])
    flagp[:,12] = consiste_proc.faixa(tp1,3,30,4,18,flagp[:,12])
    flagp[:,13] = consiste_proc.faixa(dp1,0,360,0,360,flagp[:,13])
    flagp[:,14] = consiste_proc.faixa(hm02,0,20,0.25,8,flagp[:,14])
    flagp[:,15] = consiste_proc.faixa(tp2,3,30,4,18,flagp[:,15])
    flagp[:,16] = consiste_proc.faixa(dp2,0,360,0,360,flagp[:,16])

    #Teste 2 - Variabilidade temporal
    flagp[:,1] = consiste_proc.variab(hs,1,5,flagp[:,1])
    flagp[:,2] = consiste_proc.variab(h10,1,5,flagp[:,2])
    flagp[:,3] = consiste_proc.variab(hmax,1,5,flagp[:,3])
    flagp[:,4] = consiste_proc.variab(tmed,1,20,flagp[:,4])
    flagp[:,5] = consiste_proc.variab(thmax,1,20,flagp[:,5])
    flagp[:,6] = consiste_proc.variab(hm0,1,5,flagp[:,6])
    flagp[:,7] = consiste_proc.variab(tp,1,20,flagp[:,7])
    flagp[:,8] = consiste_proc.variab(dp,1,360,flagp[:,8])
    flagp[:,9] = consiste_proc.variab(hm01,1,5,flagp[:,9])
    flagp[:,10] = consiste_proc.variab(sigma1p,1,360,flagp[:,10])
    flagp[:,11] = consiste_proc.variab(sigma2p,1,360,flagp[:,11])
    flagp[:,12] = consiste_proc.variab(tp1,1,20,flagp[:,12])
    flagp[:,13] = consiste_proc.variab(dp1,1,360,flagp[:,13])
    flagp[:,14] = consiste_proc.variab(hm02,1,5,flagp[:,14])
    flagp[:,15] = consiste_proc.variab(tp2,1,20,flagp[:,15])
    flagp[:,16] = consiste_proc.variab(dp2,1,360,flagp[:,16])

    #Teste 3 - Valores consecutivos iguais (*verificar num de arquivos em 'listac')
    # flagp[:,1] = consiste_proc.iguais(hs,5,flagp[:,1])
    # flagp[:,2] = consiste_proc.iguais(h10,5,flagp[:,2])
    # flagp[:,3] = consiste_proc.iguais(hmax,5,flagp[:,3])
    # flagp[:,4] = consiste_proc.iguais(tmed,20,flagp[:,4])
    # flagp[:,5] = consiste_proc.iguais(thmax,20,flagp[:,5])
    # flagp[:,6] = consiste_proc.iguais(hm0,5,flagp[:,6])
    # flagp[:,7] = consiste_proc.iguais(tp,20,flagp[:,7])
    # flagp[:,8] = consiste_proc.iguais(dp,20,flagp[:,8])
    # flagp[:,9] = consiste_proc.iguais(sigma1p,20,flagp[:,9])
    # flagp[:,10] = consiste_proc.iguais(sigma2p,20,flagp[:,10])
    # flagp[:,11] = consiste_proc.iguais(hm01,5,flagp[:,11])
    # flagp[:,12] = consiste_proc.iguais(tp1,20,flagp[:,12])
    # flagp[:,13] = consiste_proc.iguais(dp1,20,flagp[:,13])
    # flagp[:,14] = consiste_proc.iguais(hm02,5,flagp[:,14])
    # flagp[:,15] = consiste_proc.iguais(tp2,20,flagp[:,15])
    # flagp[:,16] = consiste_proc.iguais(dp2,20,flagp[:,16])


    # ================================================================================== #  
    # Coloca nan nos dados reprovados
    
    matondap = np.copy(matondab)

    #varia cada variavel (eta, etax e etay)
    for c in range(1,flagp.shape[1]):

        #varia os dias
        for i in range(len(flagp)):

            #varia o string do vetor de flag
            if '4' in flagp[i,c]:

                matondap[i,c] = np.nan

            # print 'LH: ' + str(i+1) + ' / ' + listap[i] + ' / CQ-LT -- Aprovado'


            # else:

            # print 'LH: ' + str(i+1) + ' / ' + listap[i] + ' / CQ-LT -- Reprovado'


    # ================================================================================== #  

    #parametros de ondas processados
    # matondap = np.array([datap,hsc,h10c,hmaxc,tmedc,thmaxc,hm0c, tpc, dpc, sigma1pc,
    #  sigma2pc, hm01c, tp1c, dp1c, hm02c, tp2c, dp2c]).T

    # ================================================================================== #  
    # Imprime relatorio de controle de qualidade

    #salva relatorio em txt
    f = open('saida/'+'consistencia_'+str(gl)+'-'+local1+'.out','w')
    # fflagb, fflagp = relatorio.axys(f,lista,listap,listac,listai,flagb,flagp,h,local,latlon,idargos,idwmo)
    
    # ================================================================================== #  
    # Cria saida de dados com savetxt

    #parametros de ondas com cq apenas nos dados brutos
    np.savetxt('saida/'+'paramwb_'+str(gl)+'-'+local1+'.out',matondab,delimiter=',',fmt=['%i']+npa*['%.1f'],
        header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')

    #parametros de ondas com cq nos dados brutos e processados
    np.savetxt('saida/'+'paramwp_'+str(gl)+'-'+local1+'.out',matondap,delimiter=',',fmt=['%i']+npa*['%.1f'],
        header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')

    #flags aplicados nos dados brutos
    np.savetxt('saida/'+'flagbw_'+str(gl)+'-'+local1+'.out',flagb,delimiter=',',fmt='%s',
        header='date,eta,etax,etay')

    #flags aplicados nos dados brutos
    np.savetxt('saida/'+'flagpw_'+str(gl)+'-'+local1+'.out',flagp,delimiter=',',fmt='%s',
        header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2')

    #lista de dados aprovados no cq bruto
    np.savetxt('saida/'+'listacb_'+str(gl)+'-'+local1+'.out',listac,fmt='%s') #lista de dados aprovados no cq bruto

    #lista de dados reprovados no cq bruto
    np.savetxt('saida/'+'listaib_'+str(gl)+'-'+local1+'.out',listai,fmt='%s') #lista de dados reprovados no cq bruto


else:

    print('Todos os arquivos reprovaram em algum teste de Controle de Qualidade' '\n' '\n')



# ================================================================================== #  
# Salva saida da daat (espe e dire)

# np.savetxt('saida/'+'espe1.out',espe1,delimiter=',',fmt='%.1f')
# np.savetxt('saida/'+'dire1.out',dire1,delimiter=',',fmt='%.1f')
# np.savetxt('saida/'+'energ.out',energ,delimiter=',',fmt='%.1f')

# ================================================================================== #  
# Tempo de execucao da rotina

#contador inicial de tempo de execucao
toc = time.clock()

#tempo de execucao
texec = toc - tic

print 'Tempo de execucao pp_proc + daat_oc (s): ',texec

# ================================================================================== #  
# Graficos

# graficos_axys.graf(mat_onda,eta_mat_cons,dspx_mat_cons,dspy_mat_cons,reg_fw,Hmax_fw,Hs_fw,THmax_fw,rel_fw,ind_fw)


# ================================================================================== #  
# Fim

# mostra figuras
pl.show()
