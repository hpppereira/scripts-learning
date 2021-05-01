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
================================================================================== #
    
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

para processar apenas 1 ou poucos arquivos, verificar se o teste de variabildade 
e consecutivos iguais no 'consiste_proc.py' estao habilitados, pois pode dar erro

- Rio Grande:
latlon = '-31.56667 / -49.86667' #relatorio
idargos = '69153'
idwmo = '31053'

- Florianopolis:
latlon = '-28.50000 / -47.36667'
idargos = '69150'
idwmo = '31374'

- Santos:
latlon = '-25.28334 / -44.93334'
idargos = '69151'
idwmo = '31051'

- Porto Seguro:
latlon = '-18.151 / -37.94367'
idargos = '69007'
idwmo = '31260'

- Recife:
latlon = '-8.149 / -34.56' #relatorio
idargos = '69154'
idwmo = '31052'
'''
# ================================================================================== #
#### Modulos utilizados
# ================================================================================== #

import os
import sys
import numpy as np
import pylab as pl
import time
from datetime import datetime
# import loadhne
import proconda
import consiste_bruto
import consiste_espec
import consiste_proc
#import daat
#import relatorio
#import graficos_axys
#import jonswap

reload(proconda)
reload(consiste_bruto)
reload(consiste_espec)
reload(consiste_proc)
#reload(daat)
#reload(relatorio)
#reload(graficos_axys)
#reload(jonswap)

pl.close('all')

#define funcoes

#carrega axys


# ================================================================================== #
# Contador inicial de tempo de execucao

tic = time.clock()

# ================================================================================== #
#### Dados de entrada
# ================================================================================== #


#localizacao
#local = 'Rio Grande/RS' # relatorio
#local1 = 'rio_grande' #nome do arquivo salvo
#latlon = '-31.56667 / -49.86667' #relatorio
#idargos = '69153'
#idwmo = '31053'

#caminho onde estao os arquivos .HNE
pathname = os.environ['HOME'] + '/Documents/pnboia/dados/axys/rio_grande/hne/'

#escolhe a data inicial e final para ser processada (opcional, no 'p0' e 'p1')
#z0 = '200905010000.HNE'
#z1 = '200901010000.HNE'

#para processar todos os arquivos (comentao o p0 e p1 abaixo)
#p0 = 500
#p1 = 550# len(lista)

h = 6 #profundidade 
nfft = 82 #numero de dados para a fft (para nlin=1312 -- p/ 32gl, nfft=82 ; p/8 gl, nfft=328)
fs = 1 #freq de amostragem
nlin = 1024 #comprimento da serie temporal a ser processada
gl = (nlin/nfft) * 2

#numero de testes habilitados
ntb = 9 #brutos
#nte = 3 #espectro
ntp = 3 #processado

#numero de parametros a serem calculados
npa = 19


#define funcoes
#======================================================================#

#def lista_hne(pathname):
#
#    ''' Lista arquivos com extensao .HNE 
#    que estao dentro do diretorio 'pathname' 
#
#    Entrada: pathname - diretorio que estao os arquivos
#    Saida: arq - variavel com o nome dos arquivos
#
#    '''
#
#    lista = []
#    # Lista arquivos do diretorio atual
#    for f in os.listdir(pathname):
#        if f.endswith('.HNE'):
#            lista.append(f)
#    lista=np.sort(lista)
#
#    return lista
#
#def dados_hne(pathname,arq):
#
#    ''' Retorna os dados de tempo, elevacao e
#    deslocamentos norte e leste
#
#    Entrada: nome do arquivo com extensao -exemplo: 200907060200.HNE
#
#    Saida: t - tempo
#           eta - elevacao
#           dspy - deslocamento norte
#           dspx - deslocamento leste
#           data - ano, mes, dia, hora, minuto
# '''
#
#    #le os dados a partir da 11 linha que sao numeros
#    dados=np.loadtxt(pathname+arq, skiprows = 11)
#
#    ano = arq[0:4]
#    mes = arq[4:6]
#    dia = arq[6:8]
#    hora = arq[8:10]
#    minuto = arq[10:12]
#
#    data = [ano, mes, dia, hora, minuto]
#
#    return dados,data

#======================================================================#


#cria variavel 'lista' com nome dos arquivos HNE
#lista = np.array(lista_hne(pathname))

#numero dos arq para processar (modificar p0=0 e p1=len(lista) para todos)
# p0 = np.where(lista == z0)[0][0]
# p1 = np.where(lista == z1)[0][0]





# ================================================================================== #
#### Incicializacao do programa
# ================================================================================== #

#lista dos arquivos que serao processados
listap = lista[p0:p1+1]
listap = [listap[i][0:-4] for i in range(len(listap))]

#numero de arquivos a serem processados
ncol = len(listap)

#cria vetores de flags das series brutas
flagb = np.zeros((len(listap),4),dtype='|S32')
flagb[:,0] = listap

#cria vetores de flags dos parametros espectrais
flage = np.zeros((1,4),dtype='S32')
flage1 = np.copy(flage)

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

    print 'LH: ' + str(i+1)   

    cont = cont + 1

    #carrega dados e data
    dados, data = dados_hne(pathname,listap[i]+'.HNE')

    #define variaveis
    t = dados[:,0]
    eta = dados[:,1]
    etax = dados[:,3]
    etay = dados[:,2]

    # ================================================================================== #  
    # Testes de consistencia dos dados processados
    
    #Teste 1 - validade da mensagem (apenas axys *.HNE) -  validade do nome do arquivo (ind=0)
    flagb[i,1] = consiste_bruto.msg(listap[i],flagb[i,1])
    flagb[i,2] = consiste_bruto.msg(listap[i],flagb[i,2])
    flagb[i,3] = consiste_bruto.msg(listap[i],flagb[i,3])
    
    #Teste 2 - comprimento do vetor (ind=1)
    flagb[i,1] = consiste_bruto.comp(eta,1312,flagb[i,1])
    flagb[i,2] = consiste_bruto.comp(etax,1312,flagb[i,2])
    flagb[i,3] = consiste_bruto.comp(etay,1312,flagb[i,3])

    #Teste 3 - gap (lacuna)
    flagb[i,1] = consiste_bruto.gap(eta,10,flagb[i,1])
    flagb[i,2] = consiste_bruto.gap(etax,10,flagb[i,2])
    flagb[i,3] = consiste_bruto.gap(etay,10,flagb[i,3])

    #Teste 4 - spike
    flagb[i,1], vet_etai = consiste_bruto.spike(eta,np.mean(eta),np.std(eta),10,5,2,flagb[i,1])
    flagb[i,2], vet_etaxi = consiste_bruto.spike(etax,np.mean(etax),np.std(etax),10,5,2,flagb[i,2])
    flagb[i,3], vet_etayi = consiste_bruto.spike(etay,np.mean(etay),np.std(etay),10,5,2,flagb[i,3])
    
    #Teste 5 - valores flat
    flagb[i,1] = consiste_bruto.flat(eta,-0.15,0.15,flagb[i,1])
    flagb[i,2] = consiste_bruto.flat(etax,-0.15,0.15,flagb[i,2])
    flagb[i,3] = consiste_bruto.flat(etay,-0.15,0.15,flagb[i,3])
    
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
        

        # ================================================================================== #
        # Consistencia dos parametros espectrais
        
    #     #coloca data na primeira coluna do flage
    #     flage[-1,0] = listac[-1]

        # ================================================================================== #
        # Testes de consistencia dos parametros espectrais

    #     #Teste 1 - check-ratio (coloca flag em heave, dspx e dspy)
    #     flage[-1,[1,2,3]], kf, rf, rf_med = consiste_espec.checkratio(h,k,snn,snxnx,snyny,flage[-1,[1,2,3]])

    #     #Teste 2 - faixa de frequencia operacional
    #     flage[-1,1] = consiste_espec.freq_range(1/Tp,1,0.333,1,0.1,flage[-1,1])

        # ================================================================================== #

    #     #monta vetor de flag na iteracao
    #     flage = np.concatenate((flage,flage1))

        # ================================================================================== #  
        # Condicao para dados aprovados na consistencia dos parametros espectrais

    #     if (flage[-2,1:] == [nte*'1',nte*'1',nte*'1']).all():

        #                       0  1   2   3    4     5    6   7   8     9         10     11   12   13    14   15   16
        #parametros de onda = data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2
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

    for c in range(1,flagp.shape[1]):

        for i in range(len(flagp)):

            if '4' in flagp[i,c]:

                matondap[i,c] = np.nan


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
