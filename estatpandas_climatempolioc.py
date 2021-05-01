'''
Calcula RMSE, Correlacao, ...
entre os dados de boias e modelos

Parametros de comparacao:
- Hs, Tp, Dp

Calculos para comparacoes
- Bias (BIAS)
- Erro medio quadratico (ERMS)
- Indice de espalhamento (SI)
- Correlacao (CORR)

Faz os graficos com indices estatisticos do pandas

Data da ultima modificacao: 25/08/2015

'''

import numpy as np
import pylab as pl
import os
import taylor
import pandas as pd

pl.close('all')

#dados
#   0    1     2      3      4     5     6      7      8      9
# data,HsLioc,HsCli,TpLioc,TpCli,DpLioc,DpCli,HsBoia,TpBoia,DpBoia

pathname = os.environ['HOME'] + '/Dropbox/ww3br/rot/out/ww3/'
# izabel Casa
# pathname = os.environ['HOME'] + '/Projetos/Dropbox/lioc/ww3br/Geral/rot/saida/ww3/'

#caso 1 - Rio Grande
# arqv = ['saida2014110400_69153.out','saida2014110500_69153.out',
# 		'saida2014110600_69153.out','saida2014110700_69153.out']

#caso 1 - MIROS P40
# arqv = ['saidaMIROS2014110400.out','saidaMIROS2014110500.out',
# 		'saidaMIROS2014110600.out','saidaMIROS2014110700.out']

#caso 2 - Rio Grande
# arqv = ['saida2014112500_69153.out','saida2014112600_69153.out',
# 		'saida2014112700_69153.out','saida2014112800_69153.out']

#caso 2 - MIROS P40
arqv = ['saidaMIROS2014112500.out','saidaMIROS2014112600.out',
		'saidaMIROS2014112700.out','saidaMIROS2014112800.out']

#dados de entrada

loc = 'p40' #'rio_grande ou 'p40'
caso = '2' #1 ou 2
ii = 25 #dia inicial (caso1 = 4; caso 2 = 25)


#configuracoes para figuras
cor1 = 'b' #lioc
cor2 = 'r' #climtempo
cor12 = cor2+cor1 #bar plot
lsf = 18 #fontsize para as figuras
figsize1 = (15,9)

#vetores com estatisticas
bias_lioc_hs = np.zeros((7,4))
bias_clim_hs = np.zeros((7,4))
bias_lioc_tp = np.zeros((7,4))
bias_clim_tp = np.zeros((7,4))
bias_lioc_dp = np.zeros((7,4))
bias_clim_dp = np.zeros((7,4))

rmse_lioc_hs = np.zeros((7,4))
rmse_clim_hs = np.zeros((7,4))
rmse_lioc_tp = np.zeros((7,4))
rmse_clim_tp = np.zeros((7,4))
rmse_lioc_dp = np.zeros((7,4))
rmse_clim_dp = np.zeros((7,4))

si_lioc_hs = np.zeros((7,4))
si_clim_hs = np.zeros((7,4))
si_lioc_tp = np.zeros((7,4))
si_clim_tp = np.zeros((7,4))
si_lioc_dp = np.zeros((7,4))
si_clim_dp = np.zeros((7,4))

corr_lioc_hs = np.zeros((7,4))
corr_clim_hs = np.zeros((7,4))
corr_lioc_tp = np.zeros((7,4))
corr_clim_tp = np.zeros((7,4))
corr_lioc_dp = np.zeros((7,4))
corr_clim_dp = np.zeros((7,4))

std_lioc_hs = np.zeros((7,4))
std_clim_hs = np.zeros((7,4))
std_boia_hs = np.zeros((7,4))

for j in range(len(arqv)):

	dados = np.loadtxt(pathname + arqv[j],delimiter=',')

	#dia inicial (do arquivo .out)
	t0 = j+ii

	#vetor de datas em string
	datas = dados[:,0].astype(str)

	#vetor de dias
	D = np.array([datas[i][6:8] for i in xrange(len(dados))]).astype(int)

	cont = 0
	for i in range(t0,t0+7):

		if i > 30: i = i - 30 #correcao para mudar o dia (verificar se eh 30 ou 31)

		#indice dos dias
		n = np.where(D==i)[0] 
		
		### DADOS ###
		#hs
		hs_lioc = dados[n,1]
		hs_clim = dados[n,2]
		hs_boia = dados[n,7]
		#tp
		tp_lioc = dados[n,3]
		tp_clim = dados[n,4]
		tp_boia = dados[n,8]
		#dp
		dp_lioc = dados[n,5]
		dp_clim = dados[n,6]
		dp_boia = dados[n,9]


		### BIAS ###
		#hs
		bias_lioc_hs[cont,j] = np.mean(hs_lioc - hs_boia)
		bias_clim_hs[cont,j] = np.mean(hs_clim - hs_boia)
		#tp
		bias_lioc_tp[cont,j] = np.mean(tp_lioc - tp_boia)
		bias_clim_tp[cont,j] = np.mean(tp_clim - tp_boia)
		#dp
		bias_lioc_dp[cont,j] = np.mean(dp_lioc - dp_boia)
		bias_clim_dp[cont,j] = np.mean(dp_clim - dp_boia)

		### ERMS ###
		#hs
		rmse_lioc_hs[cont,j] = np.sqrt( pl.sum( (hs_lioc - hs_boia) ** 2 ) / len(hs_lioc) )
		rmse_clim_hs[cont,j] = np.sqrt( pl.sum( (hs_clim - hs_boia) ** 2 ) / len(hs_clim) )
		#tp
		rmse_lioc_tp[cont,j] = np.sqrt( pl.sum( (tp_lioc - tp_boia) ** 2 ) / len(tp_lioc) )
		rmse_clim_tp[cont,j] = np.sqrt( pl.sum( (tp_clim - tp_boia) ** 2 ) / len(tp_clim) )
		#hs
		rmse_lioc_dp[cont,j] = np.sqrt( pl.sum( (dp_lioc - dp_boia) ** 2 ) / len(dp_lioc) )
		rmse_clim_dp[cont,j] = np.sqrt( pl.sum( (dp_clim - dp_boia) ** 2 ) / len(dp_clim) )
		

		### SI ###
		#hs
		si_lioc_hs[cont,j] = rmse_lioc_hs[cont,j] / np.mean(hs_boia)
		si_clim_hs[cont,j] = rmse_clim_hs[cont,j] / np.mean(hs_boia)
		#tp
		si_lioc_tp[cont,j] = rmse_lioc_tp[cont,j] / np.mean(tp_boia)
		si_clim_tp[cont,j] = rmse_clim_tp[cont,j] / np.mean(tp_boia)
		#dp
		si_lioc_dp[cont,j] = rmse_lioc_dp[cont,j] / np.mean(dp_boia)
		si_clim_dp[cont,j] = rmse_clim_dp[cont,j] / np.mean(dp_boia)

		### Correlacao ###
		#hs
		corr_lioc_hs[cont,j] = np.corrcoef(hs_lioc,hs_boia)[0,1]
		corr_clim_hs[cont,j] = np.corrcoef(hs_clim,hs_boia)[0,1]
		#tp
		corr_lioc_tp[cont,j] = np.corrcoef(tp_lioc,tp_boia)[0,1]
		corr_clim_tp[cont,j] = np.corrcoef(tp_clim,tp_boia)[0,1]
		#dp
		corr_lioc_dp[cont,j] = np.corrcoef(dp_lioc,dp_boia)[0,1]
		corr_clim_dp[cont,j] = np.corrcoef(dp_clim,dp_boia)[0,1]

		### Desvio Padrao ###
		std_lioc_hs[cont,j] = np.std(hs_lioc)
		std_clim_hs[cont,j] = np.std(hs_clim)
		std_boia_hs[cont,j] = np.std(hs_boia)

		cont += 1


#calcula medias diarias
std_boia_hs_med = std_boia_hs.mean(axis=1)
std_lioc_hs_med = std_lioc_hs.mean(axis=1)
std_clim_hs_med = std_clim_hs.mean(axis=1)

corr_lioc_hs_med = corr_lioc_hs.mean(axis=1)
corr_clim_hs_med = corr_clim_hs.mean(axis=1)


#os 7 dias de previsao
dia = range(7)

#bias
pl.figure(figsize=figsize1)
pl.subplot(311)
pl.title('BIAS',fontsize=lsf)
pl.plot(bias_lioc_hs[:,0],'-'+cor1+'d',label='lioc'+str(ii))
pl.plot(bias_lioc_hs[:,1],'-'+cor1+'o',label='lioc'+str(ii+1))
pl.plot(bias_lioc_hs[:,2],'-'+cor1+'s',label='lioc'+str(ii+2))
pl.plot(bias_lioc_hs[:,3],'-'+cor1+'*',label='lioc'+str(ii+3))
pl.plot(bias_clim_hs[:,0],'-'+cor2+'d',label='clim'+str(ii))
pl.plot(bias_clim_hs[:,1],'-'+cor2+'o',label='clim'+str(ii+1))
pl.plot(bias_clim_hs[:,2],'-'+cor2+'s',label='clim'+str(ii+2))
pl.plot(bias_clim_hs[:,3],'-'+cor2+'*',label='clim'+str(ii+3))
pl.ylabel('Hs',fontsize=lsf), pl.grid()
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(bias_lioc_tp[:,0],'-'+cor1+'d',label='lioc'+str(ii))
pl.plot(bias_lioc_tp[:,1],'-'+cor1+'o',label='lioc'+str(ii+1))
pl.plot(bias_lioc_tp[:,2],'-'+cor1+'s',label='lioc'+str(ii+2))
pl.plot(bias_lioc_tp[:,3],'-'+cor1+'*',label='lioc'+str(ii+3))
pl.plot(bias_clim_tp[:,0],'-'+cor2+'d',label='clim'+str(ii))
pl.plot(bias_clim_tp[:,1],'-'+cor2+'o',label='clim'+str(ii+1))
pl.plot(bias_clim_tp[:,2],'-'+cor2+'s',label='clim'+str(ii+2))
pl.plot(bias_clim_tp[:,3],'-'+cor2+'*',label='clim'+str(ii+3))
pl.ylabel('Tp',fontsize=lsf), pl.grid(), pl.legend(loc='center left',bbox_to_anchor=(1,0.5))
pl.xticks(visible=False)
pl.subplot(313)
pl.plot(dia,bias_lioc_dp[:,0],'-'+cor1+'d',label='lioc'+str(ii))
pl.plot(dia,bias_lioc_dp[:,1],'-'+cor1+'o',label='lioc'+str(ii+1))
pl.plot(dia,bias_lioc_dp[:,2],'-'+cor1+'s',label='lioc'+str(ii+2))
pl.plot(dia,bias_lioc_dp[:,3],'-'+cor1+'*',label='lioc'+str(ii+3))
pl.plot(dia,bias_clim_dp[:,0],'-'+cor2+'d',label='clim'+str(ii))
pl.plot(dia,bias_clim_dp[:,1],'-'+cor2+'o',label='clim'+str(ii+1))
pl.plot(dia,bias_clim_dp[:,2],'-'+cor2+'s',label='clim'+str(ii+2))
pl.plot(dia,bias_clim_dp[:,3],'-'+cor2+'*',label='clim'+str(ii+3))
pl.xticks(dia,('+1','+2','+3','+4','+5','+6','+7'))
pl.ylabel('Dp',fontsize=lsf), pl.grid(), pl.xlabel('Dias')

pl.savefig('bias_serie_'+ loc + '_caso_' + caso)

#rmse
pl.figure(figsize=figsize1)
pl.subplot(311)
pl.title('RMSE',fontsize=lsf)
pl.plot(rmse_lioc_hs[:,0],'-'+cor1+'d',label='lioc'+str(ii))
pl.plot(rmse_lioc_hs[:,1],'-'+cor1+'o',label='lioc'+str(ii+1))
pl.plot(rmse_lioc_hs[:,2],'-'+cor1+'s',label='lioc'+str(ii+2))
pl.plot(rmse_lioc_hs[:,3],'-'+cor1+'*',label='lioc'+str(ii+3))
pl.plot(rmse_clim_hs[:,0],'-'+cor2+'d',label='clim'+str(ii))
pl.plot(rmse_clim_hs[:,1],'-'+cor2+'o',label='clim'+str(ii+1))
pl.plot(rmse_clim_hs[:,2],'-'+cor2+'s',label='clim'+str(ii+2))
pl.plot(rmse_clim_hs[:,3],'-'+cor2+'*',label='clim'+str(ii+3))
pl.ylabel('Hs',fontsize=lsf), pl.grid()
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(rmse_lioc_tp[:,0],'-'+cor1+'d',label='lioc'+str(ii))
pl.plot(rmse_lioc_tp[:,1],'-'+cor1+'o',label='lioc'+str(ii+1))
pl.plot(rmse_lioc_tp[:,2],'-'+cor1+'s',label='lioc'+str(ii+2))
pl.plot(rmse_lioc_tp[:,3],'-'+cor1+'*',label='lioc'+str(ii+3))
pl.plot(rmse_clim_tp[:,0],'-'+cor2+'d',label='clim'+str(ii))
pl.plot(rmse_clim_tp[:,1],'-'+cor2+'o',label='clim'+str(ii+1))
pl.plot(rmse_clim_tp[:,2],'-'+cor2+'s',label='clim'+str(ii+2))
pl.plot(rmse_clim_tp[:,3],'-'+cor2+'*',label='clim'+str(ii+3))
pl.ylabel('Tp',fontsize=lsf), pl.grid(), pl.legend(loc='center left',bbox_to_anchor=(1,0.5))
pl.xticks(visible=False)
pl.subplot(313)
pl.plot(dia,rmse_lioc_dp[:,0],'-'+cor1+'d',label='lioc'+str(ii))
pl.plot(dia,rmse_lioc_dp[:,1],'-'+cor1+'o',label='lioc'+str(ii+1))
pl.plot(dia,rmse_lioc_dp[:,2],'-'+cor1+'s',label='lioc'+str(ii+2))
pl.plot(dia,rmse_lioc_dp[:,3],'-'+cor1+'*',label='lioc'+str(ii+3))
pl.plot(dia,rmse_clim_dp[:,0],'-'+cor2+'d',label='clim'+str(ii))
pl.plot(dia,rmse_clim_dp[:,1],'-'+cor2+'o',label='clim'+str(ii+1))
pl.plot(dia,rmse_clim_dp[:,2],'-'+cor2+'s',label='clim'+str(ii+2))
pl.plot(dia,rmse_clim_dp[:,3],'-'+cor2+'*',label='clim'+str(ii+3))
pl.xticks(dia,('+1','+2','+3','+4','+5','+6','+7'))
pl.ylabel('Dp',fontsize=lsf), pl.grid(), pl.xlabel('Dias')

pl.savefig('rmse_serie_'+ loc + '_caso_' + caso)

#si
pl.figure(figsize=figsize1)
pl.subplot(311)
pl.title('SI',fontsize=lsf)
pl.plot(si_lioc_hs[:,0],'-'+cor1+'d',label='lioc'+str(ii))
pl.plot(si_lioc_hs[:,1],'-'+cor1+'o',label='lioc'+str(ii+1))
pl.plot(si_lioc_hs[:,2],'-'+cor1+'s',label='lioc'+str(ii+2))
pl.plot(si_lioc_hs[:,3],'-'+cor1+'*',label='lioc'+str(ii+3))
pl.plot(si_clim_hs[:,0],'-'+cor2+'d',label='clim'+str(ii))
pl.plot(si_clim_hs[:,1],'-'+cor2+'o',label='clim'+str(ii+1))
pl.plot(si_clim_hs[:,2],'-'+cor2+'s',label='clim'+str(ii+2))
pl.plot(si_clim_hs[:,3],'-'+cor2+'*',label='clim'+str(ii+3))
pl.ylabel('Hs',fontsize=lsf), pl.grid()
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(si_lioc_tp[:,0],'-'+cor1+'d',label='lioc'+str(ii))
pl.plot(si_lioc_tp[:,1],'-'+cor1+'o',label='lioc'+str(ii+1))
pl.plot(si_lioc_tp[:,2],'-'+cor1+'s',label='lioc'+str(ii+2))
pl.plot(si_lioc_tp[:,3],'-'+cor1+'*',label='lioc'+str(ii+3))
pl.plot(si_clim_tp[:,0],'-'+cor2+'d',label='clim'+str(ii))
pl.plot(si_clim_tp[:,1],'-'+cor2+'o',label='clim'+str(ii+1))
pl.plot(si_clim_tp[:,2],'-'+cor2+'s',label='clim'+str(ii+2))
pl.plot(si_clim_tp[:,3],'-'+cor2+'*',label='clim'+str(ii+3))
pl.ylabel('Tp',fontsize=lsf), pl.grid(), pl.legend(loc='center left',bbox_to_anchor=(1,0.5))
pl.xticks(visible=False)
pl.subplot(313)
pl.plot(dia,si_lioc_dp[:,0],'-'+cor1+'d',label='lioc'+str(ii))
pl.plot(dia,si_lioc_dp[:,1],'-'+cor1+'o',label='lioc'+str(ii+1))
pl.plot(dia,si_lioc_dp[:,2],'-'+cor1+'s',label='lioc'+str(ii+2))
pl.plot(dia,si_lioc_dp[:,3],'-'+cor1+'*',label='lioc'+str(ii+3))
pl.plot(dia,si_clim_dp[:,0],'-'+cor2+'d',label='clim'+str(ii))
pl.plot(dia,si_clim_dp[:,1],'-'+cor2+'o',label='clim'+str(ii+1))
pl.plot(dia,si_clim_dp[:,2],'-'+cor2+'s',label='clim'+str(ii+2))
pl.plot(dia,si_clim_dp[:,3],'-'+cor2+'*',label='clim'+str(ii+3))
pl.xticks(dia,('+1','+2','+3','+4','+5','+6','+7'))
pl.ylabel('Dp',fontsize=lsf), pl.grid(), pl.xlabel('Dias')

pl.savefig('si_serie_'+ loc + '_caso_' + caso)

#corr
pl.figure(figsize=figsize1)
pl.subplot(311)
pl.title('CORR',fontsize=lsf)
pl.plot(corr_lioc_hs[:,0],'-'+cor1+'d',label='lioc'+str(ii))
pl.plot(corr_lioc_hs[:,1],'-'+cor1+'o',label='lioc'+str(ii+1))
pl.plot(corr_lioc_hs[:,2],'-'+cor1+'s',label='lioc'+str(ii+2))
pl.plot(corr_lioc_hs[:,3],'-'+cor1+'*',label='lioc'+str(ii+3))
pl.plot(corr_clim_hs[:,0],'-'+cor2+'d',label='clim'+str(ii))
pl.plot(corr_clim_hs[:,1],'-'+cor2+'o',label='clim'+str(ii+1))
pl.plot(corr_clim_hs[:,2],'-'+cor2+'s',label='clim'+str(ii+2))
pl.plot(corr_clim_hs[:,3],'-'+cor2+'*',label='clim'+str(ii+3))
pl.ylabel('Hs',fontsize=lsf), pl.grid()
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(corr_lioc_tp[:,0],'-'+cor1+'d',label='lioc'+str(ii))
pl.plot(corr_lioc_tp[:,1],'-'+cor1+'o',label='lioc'+str(ii+1))
pl.plot(corr_lioc_tp[:,2],'-'+cor1+'s',label='lioc'+str(ii+2))
pl.plot(corr_lioc_tp[:,3],'-'+cor1+'*',label='lioc'+str(ii+3))
pl.plot(corr_clim_tp[:,0],'-'+cor2+'d',label='clim'+str(ii))
pl.plot(corr_clim_tp[:,1],'-'+cor2+'o',label='clim'+str(ii+1))
pl.plot(corr_clim_tp[:,2],'-'+cor2+'s',label='clim'+str(ii+2))
pl.plot(corr_clim_tp[:,3],'-'+cor2+'*',label='clim'+str(ii+3))
pl.ylabel('Tp',fontsize=lsf), pl.grid(), pl.legend(loc='center left',bbox_to_anchor=(1,0.5))
pl.xticks(visible=False)
pl.subplot(313)
pl.plot(dia,corr_lioc_dp[:,0],'-'+cor1+'d',label='lioc'+str(ii))
pl.plot(dia,corr_lioc_dp[:,1],'-'+cor1+'o',label='lioc'+str(ii+1))
pl.plot(dia,corr_lioc_dp[:,2],'-'+cor1+'s',label='lioc'+str(ii+2))
pl.plot(dia,corr_lioc_dp[:,3],'-'+cor1+'*',label='lioc'+str(ii+3))
pl.plot(dia,corr_clim_dp[:,0],'-'+cor2+'d',label='clim'+str(ii))
pl.plot(dia,corr_clim_dp[:,1],'-'+cor2+'o',label='clim'+str(ii+1))
pl.plot(dia,corr_clim_dp[:,2],'-'+cor2+'s',label='clim'+str(ii+2))
pl.plot(dia,corr_clim_dp[:,3],'-'+cor2+'*',label='clim'+str(ii+3))
pl.xticks(dia,('+1','+2','+3','+4','+5','+6','+7'))
pl.ylabel('Dp',fontsize=lsf), pl.grid(), pl.xlabel('Dias')

pl.savefig('corr_serie_'+ loc + '_caso_' + caso)


#=============================================#

#bar plots

#desvios padroes e medias dos 4 dias de simulacao para lioc e climatempo
#bias
#hs
med_bias_hs = np.array([np.mean(bias_lioc_hs,axis=1),np.mean(bias_clim_hs,axis=1)]).T
std_bias_hs = np.array([np.std(bias_lioc_hs,axis=1),np.std(bias_clim_hs,axis=1)]).T
#tp
med_bias_tp = np.array([np.mean(bias_lioc_tp,axis=1),np.mean(bias_clim_tp,axis=1)]).T
std_bias_tp = np.array([np.std(bias_lioc_tp,axis=1),np.std(bias_clim_tp,axis=1)]).T
#dp
med_bias_dp = np.array([np.mean(bias_lioc_dp,axis=1),np.mean(bias_clim_dp,axis=1)]).T
std_bias_dp = np.array([np.std(bias_lioc_dp,axis=1),np.std(bias_clim_dp,axis=1)]).T

#rmse
#hs
med_rmse_hs = np.array([np.mean(rmse_lioc_hs,axis=1),np.mean(rmse_clim_hs,axis=1)]).T
std_rmse_hs = np.array([np.std(rmse_lioc_hs,axis=1),np.std(rmse_clim_hs,axis=1)]).T
#tp
med_rmse_tp = np.array([np.mean(rmse_lioc_tp,axis=1),np.mean(rmse_clim_tp,axis=1)]).T
std_rmse_tp = np.array([np.std(rmse_lioc_tp,axis=1),np.std(rmse_clim_tp,axis=1)]).T
#dp
med_rmse_dp = np.array([np.mean(rmse_lioc_dp,axis=1),np.mean(rmse_clim_dp,axis=1)]).T
std_rmse_dp = np.array([np.std(rmse_lioc_dp,axis=1),np.std(rmse_clim_dp,axis=1)]).T

#si
#hs
med_si_hs = np.array([np.mean(si_lioc_hs,axis=1),np.mean(si_clim_hs,axis=1)]).T
std_si_hs = np.array([np.std(si_lioc_hs,axis=1),np.std(si_clim_hs,axis=1)]).T
#tp
med_si_tp = np.array([np.mean(si_lioc_tp,axis=1),np.mean(si_clim_tp,axis=1)]).T
std_si_tp = np.array([np.std(si_lioc_tp,axis=1),np.std(si_clim_tp,axis=1)]).T
#dp
med_si_dp = np.array([np.mean(si_lioc_dp,axis=1),np.mean(si_clim_dp,axis=1)]).T
std_si_dp = np.array([np.std(si_lioc_dp,axis=1),np.std(si_clim_dp,axis=1)]).T

#corr
#hs
med_corr_hs = np.array([np.mean(corr_lioc_hs,axis=1),np.mean(corr_clim_hs,axis=1)]).T
std_corr_hs = np.array([np.std(corr_lioc_hs,axis=1),np.std(corr_clim_hs,axis=1)]).T
#tp
med_corr_tp = np.array([np.mean(corr_lioc_tp,axis=1),np.mean(corr_clim_tp,axis=1)]).T
std_corr_tp = np.array([np.std(corr_lioc_tp,axis=1),np.std(corr_clim_tp,axis=1)]).T
#dp
med_corr_dp = np.array([np.mean(corr_lioc_dp,axis=1),np.mean(corr_clim_dp,axis=1)]).T
std_corr_dp = np.array([np.std(corr_lioc_dp,axis=1),np.std(corr_clim_dp,axis=1)]).T


#cria estrutura para plotagem
ix3 = pd.MultiIndex.from_arrays([['+1','+2','+3','+4','+5','+6','+7']], names=['dias'])

#bias
#hs
df3_bias_hs = pd.DataFrame({'lioc': (med_bias_hs[:,0]), 'clim': (med_bias_hs[:,1])}, index=ix3)
df4_bias_hs = pd.DataFrame({'lioc': (std_bias_hs[:,0]), 'clim': (std_bias_hs[:,1])}, index=ix3)
#tp
df3_bias_tp = pd.DataFrame({'lioc': (med_bias_tp[:,0]), 'clim': (med_bias_tp[:,1])}, index=ix3)
df4_bias_tp = pd.DataFrame({'lioc': (std_bias_tp[:,0]), 'clim': (std_bias_tp[:,1])}, index=ix3)
#dp
df3_bias_dp = pd.DataFrame({'lioc': (med_bias_dp[:,0]), 'clim': (med_bias_dp[:,1])}, index=ix3)
df4_bias_dp = pd.DataFrame({'lioc': (std_bias_dp[:,0]), 'clim': (std_bias_dp[:,1])}, index=ix3)

#rmse
#hs
df3_rmse_hs = pd.DataFrame({'lioc': (med_rmse_hs[:,0]), 'clim': (med_rmse_hs[:,1])}, index=ix3)
df4_rmse_hs = pd.DataFrame({'lioc': (std_rmse_hs[:,0]), 'clim': (std_rmse_hs[:,1])}, index=ix3)
#tp
df3_rmse_tp = pd.DataFrame({'lioc': (med_rmse_tp[:,0]), 'clim': (med_rmse_tp[:,1])}, index=ix3)
df4_rmse_tp = pd.DataFrame({'lioc': (std_rmse_tp[:,0]), 'clim': (std_rmse_tp[:,1])}, index=ix3)
#dp
df3_rmse_dp = pd.DataFrame({'lioc': (med_rmse_dp[:,0]), 'clim': (med_rmse_dp[:,1])}, index=ix3)
df4_rmse_dp = pd.DataFrame({'lioc': (std_rmse_dp[:,0]), 'clim': (std_rmse_dp[:,1])}, index=ix3)

#si
#hs
df3_si_hs = pd.DataFrame({'lioc': (med_si_hs[:,0]), 'clim': (med_si_hs[:,1])}, index=ix3)
df4_si_hs = pd.DataFrame({'lioc': (std_si_hs[:,0]), 'clim': (std_si_hs[:,1])}, index=ix3)
#tp
df3_si_tp = pd.DataFrame({'lioc': (med_si_tp[:,0]), 'clim': (med_si_tp[:,1])}, index=ix3)
df4_si_tp = pd.DataFrame({'lioc': (std_si_tp[:,0]), 'clim': (std_si_tp[:,1])}, index=ix3)
#dp
df3_si_dp = pd.DataFrame({'lioc': (med_si_dp[:,0]), 'clim': (med_si_dp[:,1])}, index=ix3)
df4_si_dp = pd.DataFrame({'lioc': (std_si_dp[:,0]), 'clim': (std_si_dp[:,1])}, index=ix3)

#corr
#hs
df3_corr_hs = pd.DataFrame({'lioc': (med_corr_hs[:,0]), 'clim': (med_corr_hs[:,1])}, index=ix3)
df4_corr_hs = pd.DataFrame({'lioc': (std_corr_hs[:,0]), 'clim': (std_corr_hs[:,1])}, index=ix3)
#tp
df3_corr_tp = pd.DataFrame({'lioc': (med_corr_tp[:,0]), 'clim': (med_corr_tp[:,1])}, index=ix3)
df4_corr_tp = pd.DataFrame({'lioc': (std_corr_tp[:,0]), 'clim': (std_corr_tp[:,1])}, index=ix3)
#dp
df3_corr_dp = pd.DataFrame({'lioc': (med_corr_dp[:,0]), 'clim': (med_corr_dp[:,1])}, index=ix3)
df4_corr_dp = pd.DataFrame({'lioc': (std_corr_dp[:,0]), 'clim': (std_corr_dp[:,1])}, index=ix3)


#figuras
#bias
pl.figure()
df3_bias_hs.plot(ax=pl.subplot(311),yerr=df4_bias_hs,kind='bar',color=cor12,rot=0,title='BIAS',fontsize=14), pl.ylabel('Hs',fontsize=lsf)
pl.title('BIAS',fontsize=lsf)
df3_bias_tp.plot(ax=pl.subplot(312),yerr=df4_bias_tp,kind='bar',color=cor12,rot=0,legend=False,fontsize=14), pl.ylabel('Tp',fontsize=lsf)
df3_bias_dp.plot(ax=pl.subplot(313),yerr=df4_bias_dp,kind='bar',color=cor12,rot=0,legend=False,fontsize=14), pl.ylabel('Dp',fontsize=lsf)

pl.savefig('bias_bar_'+ loc + '_caso_' + caso)

#rmse
pl.figure()
df3_rmse_hs.plot(ax=pl.subplot(311),yerr=df4_rmse_hs,kind='bar',color=cor12,rot=0,title='BIAS',fontsize=14), pl.ylabel('Hs',fontsize=lsf)
pl.title('RMSE',fontsize=lsf)
df3_rmse_tp.plot(ax=pl.subplot(312),yerr=df4_rmse_tp,kind='bar',color=cor12,rot=0,legend=False,fontsize=14), pl.ylabel('Tp',fontsize=lsf)
df3_rmse_dp.plot(ax=pl.subplot(313),yerr=df4_rmse_dp,kind='bar',color=cor12,rot=0,legend=False,fontsize=14), pl.ylabel('Dp',fontsize=lsf)

pl.savefig('rmse_bar_'+ loc + '_caso_' + caso)

#si
pl.figure()
df3_si_hs.plot(ax=pl.subplot(311),yerr=df4_si_hs,kind='bar',color=cor12,rot=0,title='BIAS',fontsize=14), pl.ylabel('Hs',fontsize=18)
pl.title('SI',fontsize=lsf)
df3_si_tp.plot(ax=pl.subplot(312),yerr=df4_si_tp,kind='bar',color=cor12,rot=0,legend=False,fontsize=14), pl.ylabel('Tp',fontsize=18)
df3_si_dp.plot(ax=pl.subplot(313),yerr=df4_si_dp,kind='bar',color=cor12,rot=0,legend=False,fontsize=14), pl.ylabel('Dp',fontsize=18)

pl.savefig('si_bar_'+ loc + '_caso_' + caso)

#corr
pl.figure()
df3_corr_hs.plot(ax=pl.subplot(311),yerr=df4_corr_hs,kind='bar',color=cor12,rot=0,title='BIAS',fontsize=14), pl.ylabel('Hs',fontsize=18)
pl.title('CORR',fontsize=lsf) #, pl.legend(loc=1)
df3_corr_tp.plot(ax=pl.subplot(312),yerr=df4_corr_tp,kind='bar',color=cor12,rot=0,legend=False,fontsize=14), pl.ylabel('Tp',fontsize=18)
df3_corr_dp.plot(ax=pl.subplot(313),yerr=df4_corr_dp,kind='bar',color=cor12,rot=0,legend=False,fontsize=14), pl.ylabel('Dp',fontsize=18)
pl.show()

pl.savefig('corr_bar_'+ loc + '_caso_' + caso)





#=============================================#
#diagrama de taylor

# #cria figura com eixo de referencia do desvio padrao
# dia = taylor.TaylorDiagram(std_boia_hs_med[0])

# dia.add_sample(std_lioc_hs_med[0],corr_lioc_hs_med[0])

# dia.add_rms_contours()

# # for i in range(7):

# 	# dia.add_stddev_contours(std_lioc_hs_med[i],corr_lioc_hs_med[i],corr_clim_hs_med[i],label='1')
# dia.add_stddev_contours(std_lioc_hs_med[0],corr_lioc_hs_med[0],corr_clim_hs_med[0])
# 	# dia.add_stddev_contours(std_lioc_hs_med[0],corr_lioc_hs_med[0],corr_clim_hs_med[0])
# 	# dia.add_stddev_contours(std_lioc_hs_med[0],corr_lioc_hs_med[0],corr_clim_hs_med[0])
# 	# dia.add_stddev_contours(std_lioc_hs_med[0],corr_lioc_hs_med[0],corr_clim_hs_med[0])


# # dia.add_stddev_contours(std_lioc_hs_med[0]+0.1,corr_lioc_hs_med[0],corr_clim_hs_med[0])
# # dia.add_stddev_contours(std_lioc_hs_med[0]+0.15,corr_lioc_hs_med[0]+0.5,corr_clim_hs_med[0])

pl.show()
