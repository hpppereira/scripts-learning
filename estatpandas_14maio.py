'''
Calcula RMSE, Correlacao, ...
entre as diferentes configuracoes do ww3
para reconstituir o evento do dia 14 de maio de 2015

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
import datetime as dt

pl.close('all')

pathname_ww3 = os.environ['HOME'] + '/Dropbox/ww3vale/TU/Previsao/Previsao_14maio/'
pathname_pnboia = os.environ['HOME'] + '/Dropbox/pnboia/dados/LIOc/'

#carrega dados do PNBOIA
df_sa = pd.read_csv(pathname_pnboia + 'B69150_onda.csv',parse_dates=['date'])
df_fl = pd.read_csv(pathname_pnboia + 'B69152_onda.csv',parse_dates=['date'])
df_rg = pd.read_csv(pathname_pnboia + 'B69153_onda.csv',parse_dates=['date'])

df_sa = df_sa.set_index('date')
df_fl = df_fl.set_index('date')
df_rg = df_rg.set_index('date')

#conf:      01                  02                 03                 04                  05                 06
confs = ['ww3v314st2gfs05', 'ww3v418st2gfs05', 'ww3v418st4gfs05', 'ww3v418st4mgfs25', 'ww3v418st4mgfs25', 'ww3v418st6gfs25',]
#confs = ['ww3v314st2gfs05', 'ww3v418st4gfs05', 'ww3v418st4mgfs25', 'ww3v418st6gfs25',]

colorb = 'brgycm'
#dprev = '20150514'
#cor = ['k','b','g'] #cores para plotagem

lsf = 18 #fontsize para as figuras

#### escolha a boia #######
boia = 'Boiasantos.txt' ; df_boia1 = df_sa
boia = 'BoiaFl.txt' ; df_boia1 = df_fl
boia = 'BoiaRS.txt' ; df_boia1 = df_rg


#figure size
fs = (11,9.5)


#estatisticas

bias_hs_med = []
bias_tp_med = []
bias_dp_med = []
bias_hs_std = []
bias_tp_std = []
bias_dp_std = []

rmse_hs_med = []
rmse_tp_med = []
rmse_dp_med = []
rmse_hs_std = []
rmse_tp_std = []
rmse_dp_std = []

si_hs_med = []
si_tp_med = []
si_dp_med = []
si_hs_std = []
si_tp_std = []
si_dp_std = []

corr_hs_med = []
corr_tp_med = []
corr_dp_med = []
corr_hs_std = []
corr_tp_std = []
corr_dp_std = []


for conf in confs:

	print conf

	dias = ['20150508', '20150509', '20150510', '20150511', '20150512', '20150513', '20150514']

	#vetores com estatisticas (um dicionario para cada indice e variavel)
	bias = {'hs' : np.zeros((7,7)),
			'tp' : np.zeros((7,7)),
			'dp' : np.zeros((7,7))}

	rmse = {'hs' : np.zeros((7,7)),
			'tp' : np.zeros((7,7)),
			'dp' : np.zeros((7,7))}

	si = {'hs' : np.zeros((7,7)),
		  'tp' : np.zeros((7,7)),
		  'dp' : np.zeros((7,7))}

	corr = {'hs' : np.zeros((7,7)),
			'tp' : np.zeros((7,7)),
			'dp' : np.zeros((7,7))}


	for d in range(len(dias)):

		#varia os dias
		dia = dias[d]

		#carrega dados do ww3
		dd_ww3 = np.loadtxt(pathname_ww3 + conf + '/' + dia + '/' + boia)[:-1]

		print dia

		dtt = np.array([dt.datetime(int(dd_ww3[i,0]),int(dd_ww3[i,1]),int(dd_ww3[i,2]),
			int(dd_ww3[i,3])) for i in range(len(dd_ww3))])

		#cria um dicionario
		dw = {'date' : dtt,
			  'hs'   : dd_ww3[:,5],
		 	  'tp'   : dd_ww3[:,6],
		 	  'dp'   : dd_ww3[:,7]}

		#cria dataframe com os dados do ww3
		df_ww3 = pd.DataFrame(dw)

		#deixa a data como indice
		df_ww3 = df_ww3.set_index('date')

		#subconjunto para os dados da boia idem aos dados do modelo
		df_boia = df_boia1[pl.find(df_boia1.index == df_ww3.index[0])[0]:pl.find(df_boia1.index == df_ww3.index[-1])[0]+1]

		#pega os dados de 24 em 24 horas

		cont = -1
		for m in np.arange(0,7*24,24):

			cont += 1
			print cont

			df_ww3d = df_ww3[m:m+24]
			df_boiad = df_boia[m:m+24]

			#seleciona os valores do ww3 e boia somente onde tem valores da boia (exclui os nan)
			df_boiad = df_boiad.iloc[pl.find(np.isnan(df_boiad['hs'])==False)]
			df_ww3d  = df_ww3d.iloc[pl.find(np.isnan(df_boiad['hs'])==False)]

			print df_boiad
			print df_ww3d


			#####
			#calculos estatisticos (calcula para cada dia)

			### BIAS ###
			bias['hs'][d,cont] = np.mean((df_ww3d['hs'] - df_boiad['hs']))
			bias['tp'][d,cont] = np.mean((df_ww3d['tp'] - df_boiad['tp']))
			bias['dp'][d,cont] = np.mean((df_ww3d['dp'] - df_boiad['dp']))

			### ERMS ###
			rmse['hs'][d,cont] = np.sqrt( pl.sum( (df_ww3d['hs'] - df_boiad['hs']) ** 2 ) / len(df_ww3d) )
			rmse['tp'][d,cont] = np.sqrt( pl.sum( (df_ww3d['tp'] - df_boiad['tp']) ** 2 ) / len(df_ww3d) )
			rmse['dp'][d,cont] = np.sqrt( pl.sum( (df_ww3d['dp'] - df_boiad['dp']) ** 2 ) / len(df_ww3d) )

	 		### SI ###
			si['hs'][d,cont] = rmse['hs'][d,cont] / np.mean(df_boiad['hs'])
			si['tp'][d,cont] = rmse['tp'][d,cont] / np.mean(df_boiad['tp'])
			si['dp'][d,cont] = rmse['dp'][d,cont] / np.mean(df_boiad['dp'])

			### Correlacao ###
			corr['hs'][d,cont] = np.corrcoef(df_ww3d['hs'],df_boiad['hs'])[0,1]
			corr['tp'][d,cont] = np.corrcoef(df_ww3d['tp'],df_boiad['tp'])[0,1]
			corr['dp'][d,cont] = np.corrcoef(df_ww3d['dp'],df_boiad['dp'])[0,1]

	#calcula medias para cada dia
	bias_med = {'hs' : bias['hs'].mean(0),
				'tp' : bias['tp'].mean(0),
				'dp' : bias['dp'].mean(0)}

	bias_std = {'hs' : bias['hs'].std(0),
				'tp' : bias['tp'].std(0),
				'dp' : bias['dp'].std(0)}

	rmse_med = {'hs' : rmse['hs'].mean(0),
				'tp' : rmse['tp'].mean(0),
				'dp' : rmse['dp'].mean(0)}

	rmse_std = {'hs' : rmse['hs'].std(0),
				'tp' : rmse['tp'].std(0),
				'dp' : rmse['dp'].std(0)}

	si_med = {'hs' : si['hs'].mean(0),
			  'tp' : si['tp'].mean(0),
			  'dp' : si['dp'].mean(0)}

	si_std = {'hs' : si['hs'].std(0),
			  'tp' : si['tp'].std(0),
			  'dp' : si['dp'].std(0)}

	corr_med = {'hs' : corr['hs'].mean(0),
			  'tp' : corr['tp'].mean(0),
			  'dp' : corr['dp'].mean(0)}

	corr_std = {'hs' : corr['hs'].std(0),
			  'tp' : corr['tp'].std(0),
			  'dp' : corr['dp'].std(0)}


	bias_hs_med.append(list(bias_med['hs']))
	bias_tp_med.append(list(bias_med['tp']))
	bias_dp_med.append(list(bias_med['dp']))
	bias_hs_std.append(list(bias_std['hs']))
	bias_tp_std.append(list(bias_std['tp']))
	bias_dp_std.append(list(bias_std['dp']))

	rmse_hs_med.append(list(rmse_med['hs']))
	rmse_tp_med.append(list(rmse_med['tp']))
	rmse_dp_med.append(list(rmse_med['dp']))
	rmse_hs_std.append(list(rmse_std['hs']))
	rmse_tp_std.append(list(rmse_std['tp']))
	rmse_dp_std.append(list(rmse_std['dp']))

	si_hs_med.append(list(si_med['hs']))
	si_tp_med.append(list(si_med['tp']))
	si_dp_med.append(list(si_med['dp']))
	si_hs_std.append(list(si_std['hs']))
	si_tp_std.append(list(si_std['tp']))
	si_dp_std.append(list(si_std['dp']))

	corr_hs_med.append(list(corr_med['hs']))
	corr_tp_med.append(list(corr_med['tp']))
	corr_dp_med.append(list(corr_med['dp']))
	corr_hs_std.append(list(corr_std['hs']))
	corr_tp_std.append(list(corr_std['tp']))
	corr_dp_std.append(list(corr_std['dp']))

# #=============================================#

#subsutitui conf para as configuracoes
confs = ['conf.01','conf.02','conf.03','conf.04','conf.05','conf.06']

#cria estrutura para plotagem
ix3 = pd.MultiIndex.from_arrays([['+1','+2','+3','+4','+5','+6','+7']], names=['dias'])

#######################################################
#indices com 4 configuracoes
#bias
#hs
# dfm_bias_hs = pd.DataFrame({confs[0]: (bias_hs_med[0]), confs[1]: (bias_hs_med[1]), confs[2]: (bias_hs_med[2]), confs[3]: (bias_hs_med[3])}, index=ix3)
# dfs_bias_hs = pd.DataFrame({confs[0]: (bias_hs_std[0]), confs[1]: (bias_hs_std[1]), confs[2]: (bias_hs_std[2]), confs[3]: (bias_hs_std[3])}, index=ix3)
# #tp
# dfm_bias_tp = pd.DataFrame({confs[0]: (bias_tp_med[0]), confs[1]: (bias_tp_med[1]), confs[2]: (bias_tp_med[2]), confs[3]: (bias_tp_med[3])}, index=ix3)
# dfs_bias_tp = pd.DataFrame({confs[0]: (bias_tp_std[0]), confs[1]: (bias_tp_std[1]), confs[2]: (bias_tp_std[2]), confs[3]: (bias_tp_std[3])}, index=ix3)
# #dp
# dfm_bias_dp = pd.DataFrame({confs[0]: (bias_dp_med[0]), confs[1]: (bias_dp_med[1]), confs[2]: (bias_dp_med[2]), confs[3]: (bias_dp_med[3])}, index=ix3)
# dfs_bias_dp = pd.DataFrame({confs[0]: (bias_dp_std[0]), confs[1]: (bias_dp_std[1]), confs[2]: (bias_dp_std[2]), confs[3]: (bias_dp_std[3])}, index=ix3)

# #rmse
# #hs
# dfm_rmse_hs = pd.DataFrame({confs[0]: (rmse_hs_med[0]), confs[1]: (rmse_hs_med[1]), confs[2]: (rmse_hs_med[2]), confs[3]: (rmse_hs_med[3])}, index=ix3)
# dfs_rmse_hs = pd.DataFrame({confs[0]: (rmse_hs_std[0]), confs[1]: (rmse_hs_std[1]), confs[2]: (rmse_hs_std[2]), confs[3]: (rmse_hs_std[3])}, index=ix3)
# #tp
# dfm_rmse_tp = pd.DataFrame({confs[0]: (rmse_tp_med[0]), confs[1]: (rmse_tp_med[1]), confs[2]: (rmse_tp_med[2]), confs[3]: (rmse_tp_med[3])}, index=ix3)
# dfs_rmse_tp = pd.DataFrame({confs[0]: (rmse_tp_std[0]), confs[1]: (rmse_tp_std[1]), confs[2]: (rmse_tp_std[2]), confs[3]: (rmse_tp_std[3])}, index=ix3)
# #dp
# dfm_rmse_dp = pd.DataFrame({confs[0]: (rmse_dp_med[0]), confs[1]: (rmse_dp_med[1]), confs[2]: (rmse_dp_med[2]), confs[3]: (rmse_dp_med[3])}, index=ix3)
# dfs_rmse_dp = pd.DataFrame({confs[0]: (rmse_dp_std[0]), confs[1]: (rmse_dp_std[1]), confs[2]: (rmse_dp_std[2]), confs[3]: (rmse_dp_std[3])}, index=ix3)

# #si
# #hs
# dfm_si_hs = pd.DataFrame({confs[0]: (si_hs_med[0]), confs[1]: (si_hs_med[1]), confs[2]: (si_hs_med[2]), confs[3]: (si_hs_med[3])}, index=ix3)
# dfs_si_hs = pd.DataFrame({confs[0]: (si_hs_std[0]), confs[1]: (si_hs_std[1]), confs[2]: (si_hs_std[2]), confs[3]: (si_hs_std[3])}, index=ix3)
# #tp
# dfm_si_tp = pd.DataFrame({confs[0]: (si_tp_med[0]), confs[1]: (si_tp_med[1]), confs[2]: (si_tp_med[2]), confs[3]: (si_tp_med[3])}, index=ix3)
# dfs_si_tp = pd.DataFrame({confs[0]: (si_tp_std[0]), confs[1]: (si_tp_std[1]), confs[2]: (si_tp_std[2]), confs[3]: (si_tp_std[3])}, index=ix3)
# #dp
# dfm_si_dp = pd.DataFrame({confs[0]: (si_dp_med[0]), confs[1]: (si_dp_med[1]), confs[2]: (si_dp_med[2]), confs[3]: (si_dp_med[3])}, index=ix3)
# dfs_si_dp = pd.DataFrame({confs[0]: (si_dp_std[0]), confs[1]: (si_dp_std[1]), confs[2]: (si_dp_std[2]), confs[3]: (si_dp_std[3])}, index=ix3)

# #corr
# #hs
# dfm_corr_hs = pd.DataFrame({confs[0]: (corr_hs_med[0]), confs[1]: (corr_hs_med[1]), confs[2]: (corr_hs_med[2]), confs[3]: (corr_hs_med[3])}, index=ix3)
# dfs_corr_hs = pd.DataFrame({confs[0]: (corr_hs_std[0]), confs[1]: (corr_hs_std[1]), confs[2]: (corr_hs_std[2]), confs[3]: (corr_hs_std[3])}, index=ix3)
# #tp
# dfm_corr_tp = pd.DataFrame({confs[0]: (corr_tp_med[0]), confs[1]: (corr_tp_med[1]), confs[2]: (corr_tp_med[2]), confs[3]: (corr_tp_med[3])}, index=ix3)
# dfs_corr_tp = pd.DataFrame({confs[0]: (corr_tp_std[0]), confs[1]: (corr_tp_std[1]), confs[2]: (corr_tp_std[2]), confs[3]: (corr_tp_std[3])}, index=ix3)
# #dp
# dfm_corr_dp = pd.DataFrame({confs[0]: (corr_dp_med[0]), confs[1]: (corr_dp_med[1]), confs[2]: (corr_dp_med[2]), confs[3]: (corr_dp_med[3])}, index=ix3)
# dfs_corr_dp = pd.DataFrame({confs[0]: (corr_dp_std[0]), confs[1]: (corr_dp_std[1]), confs[2]: (corr_dp_std[2]), confs[3]: (corr_dp_std[3])}, index=ix3)

#######################################################

#######################################################
#indices com 6 configuracoes
#bias
#hs
dfm_bias_hs = pd.DataFrame({confs[0]: (bias_hs_med[0]), confs[1]: (bias_hs_med[1]), confs[2]: (bias_hs_med[2]), confs[3]: (bias_hs_med[3]), confs[4]: (bias_hs_med[4]), confs[5]: (bias_hs_med[5])}, index=ix3)
dfs_bias_hs = pd.DataFrame({confs[0]: (bias_hs_std[0]), confs[1]: (bias_hs_std[1]), confs[2]: (bias_hs_std[2]), confs[3]: (bias_hs_std[3]), confs[4]: (bias_hs_std[4]), confs[5]: (bias_hs_std[5])}, index=ix3)
#tp
dfm_bias_tp = pd.DataFrame({confs[0]: (bias_tp_med[0]), confs[1]: (bias_tp_med[1]), confs[2]: (bias_tp_med[2]), confs[3]: (bias_tp_med[3]), confs[4]: (bias_tp_med[4]), confs[5]: (bias_tp_med[5])}, index=ix3)
dfs_bias_tp = pd.DataFrame({confs[0]: (bias_tp_std[0]), confs[1]: (bias_tp_std[1]), confs[2]: (bias_tp_std[2]), confs[3]: (bias_tp_std[3]), confs[4]: (bias_tp_std[4]), confs[5]: (bias_tp_std[5])}, index=ix3)
#dp
dfm_bias_dp = pd.DataFrame({confs[0]: (bias_dp_med[0]), confs[1]: (bias_dp_med[1]), confs[2]: (bias_dp_med[2]), confs[3]: (bias_dp_med[3]), confs[4]: (bias_dp_med[4]), confs[5]: (bias_dp_med[5])}, index=ix3)
dfs_bias_dp = pd.DataFrame({confs[0]: (bias_dp_std[0]), confs[1]: (bias_dp_std[1]), confs[2]: (bias_dp_std[2]), confs[3]: (bias_dp_std[3]), confs[4]: (bias_dp_std[4]), confs[5]: (bias_dp_std[5])}, index=ix3)

#rmse
#hs
dfm_rmse_hs = pd.DataFrame({confs[0]: (rmse_hs_med[0]), confs[1]: (rmse_hs_med[1]), confs[2]: (rmse_hs_med[2]), confs[3]: (rmse_hs_med[3]), confs[4]: (rmse_hs_med[4]), confs[5]: (rmse_hs_med[5])}, index=ix3)
dfs_rmse_hs = pd.DataFrame({confs[0]: (rmse_hs_std[0]), confs[1]: (rmse_hs_std[1]), confs[2]: (rmse_hs_std[2]), confs[3]: (rmse_hs_std[3]), confs[4]: (rmse_hs_std[4]), confs[5]: (rmse_hs_std[5])}, index=ix3)
#tp
dfm_rmse_tp = pd.DataFrame({confs[0]: (rmse_tp_med[0]), confs[1]: (rmse_tp_med[1]), confs[2]: (rmse_tp_med[2]), confs[3]: (rmse_tp_med[3]), confs[4]: (rmse_tp_med[4]), confs[5]: (rmse_tp_med[5])}, index=ix3)
dfs_rmse_tp = pd.DataFrame({confs[0]: (rmse_tp_std[0]), confs[1]: (rmse_tp_std[1]), confs[2]: (rmse_tp_std[2]), confs[3]: (rmse_tp_std[3]), confs[4]: (rmse_tp_std[4]), confs[5]: (rmse_tp_std[5])}, index=ix3)
#dp
dfm_rmse_dp = pd.DataFrame({confs[0]: (rmse_dp_med[0]), confs[1]: (rmse_dp_med[1]), confs[2]: (rmse_dp_med[2]), confs[3]: (rmse_dp_med[3]), confs[4]: (rmse_dp_med[4]), confs[5]: (rmse_dp_med[5])}, index=ix3)
dfs_rmse_dp = pd.DataFrame({confs[0]: (rmse_dp_std[0]), confs[1]: (rmse_dp_std[1]), confs[2]: (rmse_dp_std[2]), confs[3]: (rmse_dp_std[3]), confs[4]: (rmse_dp_std[4]), confs[5]: (rmse_dp_std[5])}, index=ix3)

#si
#hs
dfm_si_hs = pd.DataFrame({confs[0]: (si_hs_med[0]), confs[1]: (si_hs_med[1]), confs[2]: (si_hs_med[2]), confs[3]: (si_hs_med[3]), confs[4]: (si_hs_med[4]), confs[5]: (si_hs_med[5])}, index=ix3)
dfs_si_hs = pd.DataFrame({confs[0]: (si_hs_std[0]), confs[1]: (si_hs_std[1]), confs[2]: (si_hs_std[2]), confs[3]: (si_hs_std[3]), confs[4]: (si_hs_std[4]), confs[5]: (si_hs_std[5])}, index=ix3)
#tp
dfm_si_tp = pd.DataFrame({confs[0]: (si_tp_med[0]), confs[1]: (si_tp_med[1]), confs[2]: (si_tp_med[2]), confs[3]: (si_tp_med[3]), confs[4]: (si_tp_med[4]), confs[5]: (si_tp_med[5])}, index=ix3)
dfs_si_tp = pd.DataFrame({confs[0]: (si_tp_std[0]), confs[1]: (si_tp_std[1]), confs[2]: (si_tp_std[2]), confs[3]: (si_tp_std[3]), confs[4]: (si_tp_std[4]), confs[5]: (si_tp_std[5])}, index=ix3)
#dp
dfm_si_dp = pd.DataFrame({confs[0]: (si_dp_med[0]), confs[1]: (si_dp_med[1]), confs[2]: (si_dp_med[2]), confs[3]: (si_dp_med[3]), confs[4]: (si_dp_med[4]), confs[5]: (si_dp_med[5])}, index=ix3)
dfs_si_dp = pd.DataFrame({confs[0]: (si_dp_std[0]), confs[1]: (si_dp_std[1]), confs[2]: (si_dp_std[2]), confs[3]: (si_dp_std[3]), confs[4]: (si_dp_std[4]), confs[5]: (si_dp_std[5])}, index=ix3)

#corr
#hs
dfm_corr_hs = pd.DataFrame({confs[0]: (corr_hs_med[0]), confs[1]: (corr_hs_med[1]), confs[2]: (corr_hs_med[2]), confs[3]: (corr_hs_med[3]), confs[4]: (corr_hs_med[4]), confs[5]: (corr_hs_med[5])}, index=ix3)
dfs_corr_hs = pd.DataFrame({confs[0]: (corr_hs_std[0]), confs[1]: (corr_hs_std[1]), confs[2]: (corr_hs_std[2]), confs[3]: (corr_hs_std[3]), confs[4]: (corr_hs_std[4]), confs[5]: (corr_hs_std[5])}, index=ix3)
#tp
dfm_corr_tp = pd.DataFrame({confs[0]: (corr_tp_med[0]), confs[1]: (corr_tp_med[1]), confs[2]: (corr_tp_med[2]), confs[3]: (corr_tp_med[3]), confs[4]: (corr_tp_med[4]), confs[5]: (corr_tp_med[5])}, index=ix3)
dfs_corr_tp = pd.DataFrame({confs[0]: (corr_tp_std[0]), confs[1]: (corr_tp_std[1]), confs[2]: (corr_tp_std[2]), confs[3]: (corr_tp_std[3]), confs[4]: (corr_tp_std[4]), confs[5]: (corr_tp_std[5])}, index=ix3)
#dp
dfm_corr_dp = pd.DataFrame({confs[0]: (corr_dp_med[0]), confs[1]: (corr_dp_med[1]), confs[2]: (corr_dp_med[2]), confs[3]: (corr_dp_med[3]), confs[4]: (corr_dp_med[4]), confs[5]: (corr_dp_med[5])}, index=ix3)
dfs_corr_dp = pd.DataFrame({confs[0]: (corr_dp_std[0]), confs[1]: (corr_dp_std[1]), confs[2]: (corr_dp_std[2]), confs[3]: (corr_dp_std[3]), confs[4]: (corr_dp_std[4]), confs[5]: (corr_dp_std[5])}, index=ix3)

#######################################################





#figuras

#bias
pl.figure(figsize=fs)
dfm_bias_hs.plot(ax=pl.subplot(311),yerr=dfs_bias_hs,kind='bar',color=colorb,rot=0,fontsize=14,legend=None,title='BIAS'), pl.ylabel('Hs (m)',fontsize=lsf)
pl.xticks(visible='False')
dfm_bias_tp.plot(ax=pl.subplot(312),yerr=dfs_bias_tp,kind='bar',color=colorb,rot=0,fontsize=14,legend=None), pl.ylabel('Tp (s)',fontsize=lsf)
dfm_bias_dp.plot(ax=pl.subplot(313),yerr=dfs_bias_dp,kind='bar',color=colorb,rot=0,fontsize=14,legend=None), pl.ylabel('Dp (graus)',fontsize=lsf)
pl.legend(ncol=6, loc='upper center',bbox_to_anchor=(0.5, -0.17) )

pl.savefig('fig/bias_' + boia[:-4] + '.png')

#rmse
pl.figure(figsize=fs)
dfm_rmse_hs.plot(ax=pl.subplot(311),yerr=dfs_rmse_hs,kind='bar',color=colorb,rot=0,fontsize=14,legend=None,title='RMSE'), pl.ylabel('Hs (m)',fontsize=lsf)
pl.xticks(visible='False')
dfm_rmse_tp.plot(ax=pl.subplot(312),yerr=dfs_rmse_tp,kind='bar',color=colorb,rot=0,fontsize=14,legend=None), pl.ylabel('Tp (s)',fontsize=lsf)
dfm_rmse_dp.plot(ax=pl.subplot(313),yerr=dfs_rmse_dp,kind='bar',color=colorb,rot=0,fontsize=14,legend=None), pl.ylabel('Dp (graus)',fontsize=lsf)
pl.legend(ncol=6, loc='upper center',bbox_to_anchor=(0.5, -0.17) )

pl.savefig('fig/rmse_' + boia[:-4] + '.png')

#si
pl.figure(figsize=fs)
dfm_si_hs.plot(ax=pl.subplot(311),yerr=dfs_si_hs,kind='bar',color=colorb,rot=0,fontsize=14,legend=None,title='SI'), pl.ylabel('Hs (m)',fontsize=lsf)
pl.xticks(visible='False')
dfm_si_tp.plot(ax=pl.subplot(312),yerr=dfs_si_tp,kind='bar',color=colorb,rot=0,fontsize=14,legend=None), pl.ylabel('Tp (s)',fontsize=lsf)
dfm_si_dp.plot(ax=pl.subplot(313),yerr=dfs_si_dp,kind='bar',color=colorb,rot=0,fontsize=14,legend=None), pl.ylabel('Dp (graus)',fontsize=lsf)
pl.legend(ncol=6, loc='upper center',bbox_to_anchor=(0.5, -0.17) )

pl.savefig('fig/si_' + boia[:-4] + '.png')

#corr
pl.figure(figsize=fs)
dfm_corr_hs.plot(ax=pl.subplot(311),yerr=dfs_corr_hs,kind='bar',color=colorb,rot=0,fontsize=14,legend=None,title='CORR'), pl.ylabel('Hs (m)',fontsize=lsf)
pl.xticks(visible='False')
dfm_corr_tp.plot(ax=pl.subplot(312),yerr=dfs_corr_tp,kind='bar',color=colorb,rot=0,fontsize=14,legend=None), pl.ylabel('Tp (s)',fontsize=lsf)
dfm_corr_dp.plot(ax=pl.subplot(313),yerr=dfs_corr_dp,kind='bar',color=colorb,rot=0,fontsize=14,legend=None), pl.ylabel('Dp (graus)',fontsize=lsf)
pl.legend(ncol=6, loc='upper center',bbox_to_anchor=(0.5, -0.17) )

pl.savefig('fig/corr_' + boia[:-4] + '.png')



pl.show()
