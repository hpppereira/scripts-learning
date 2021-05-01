'''
Plota previsao para cada configuracao e cada dia de previsao

Data da ultima modificacao: 28/08/2015

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

#df_sa = df_sa.set_index('date')
#df_fl = df_fl.set_index('date')
#df_rg = df_rg.set_index('date')

#confs = ['ww3v314gfs05', 'ww3v418st4gfs05', 'ww3v418st4mgfs25', 'ww3v418st6gfs25']
confs = ['ww3v314st2gfs05', 'ww3v418st4gfs05', 'ww3v418st4mgfs25', 'ww3v418st6gfs25',]

#dprev = '20150508'

dias = ['20150508', '20150509', '20150510', '20150511', '20150512', '20150513', '20150514']
dias = ['20150511']
cor = ['b','g', 'c', 'm'] #cores para plotagem

lsf = 18 #fontsize para as figuras


#####################################################################################

for dprev in dias:


	#plotagem dos dados da boia
	pl.figure(figsize=(14,10))

	pl.subplot(3,3,1)
	pl.plot(df_rg['date'],df_rg['hs'],'ro'), pl.grid()
	pl.subplot(3,3,4)
	pl.plot(df_rg['date'],df_rg['tp'],'ro'), pl.grid()
	pl.subplot(3,3,7)
	pl.plot(df_rg['date'],df_rg['dp'],'ro'), pl.grid()

	pl.subplot(3,3,2)
	pl.plot(df_fl['date'],df_fl['hs'],'ro'), pl.grid()
	pl.subplot(3,3,5)
	pl.plot(df_fl['date'],df_fl['tp'],'ro'), pl.grid()
	pl.subplot(3,3,8)
	pl.plot(df_fl['date'],df_fl['dp'],'ro'), pl.grid()

	pl.subplot(3,3,3)
	pl.plot(df_sa['date'],df_sa['hs'],'ro'), pl.grid()
	pl.subplot(3,3,6)
	pl.plot(df_sa['date'],df_sa['tp'],'ro'), pl.grid()
	pl.subplot(3,3,9)
	pl.plot(df_sa['date'],df_sa['dp'],'ro'), pl.grid()
       
	c = -1
	for conf in confs:

		#varia cores para cada configuracao
		c += 1

		#carrega dados do ww3
		dd_wsa = np.loadtxt(pathname_ww3 + conf + '/' + dprev + '/Boiasantos.txt')
		dd_wfl = np.loadtxt(pathname_ww3 + conf + '/' + dprev + '/BoiaFl.txt')
		dd_wrg = np.loadtxt(pathname_ww3 + conf + '/' + dprev + '/BoiaRS.txt')

		#cria data em datetime com swan
		dtt = np.array([dt.datetime(int(dd_wsa[i,0]),int(dd_wsa[i,1]),int(dd_wsa[i,2]),
			int(dd_wsa[i,3])) for i in range(len(dd_wsa))])

		#cria um dicionario
		dsa = {'date' : dtt,
			   'hs'   : dd_wsa[:,5],
		 	   'tp'   : dd_wsa[:,6],
		 	   'dp'   : dd_wsa[:,7]}

		dfl = {'date' : dtt,
			   'hs'   : dd_wfl[:,5],
		 	   'tp'   : dd_wfl[:,6],
		 	   'dp'   : dd_wfl[:,7]}

		drg = {'date' : dtt,
			   'hs'   : dd_wrg[:,5],
		 	   'tp'   : dd_wrg[:,6],
		 	   'dp'   : dd_wrg[:,7]}

		#cria dataframe com os dados do ww3
		df_wsa = pd.DataFrame(dsa)
		df_wfl = pd.DataFrame(dfl)
		df_wrg = pd.DataFrame(drg)

		#plota as linhas da modelgam para cada configuracao (cada configuracao eh um loop)	
		pl.subplot(3,3,1)
		pl.title('Rio Grande/RS')
		pl.plot(df_wrg['date'],df_wrg['hs'],cor[c],linewidth=2)
		pl.xlim(df_rg['date'][1600], df_rg['date'][1950])
		pl.xticks(visible=False), pl.ylabel('Hs (m)'), pl.grid(), pl.ylim(0,7)
		pl.subplot(3,3,4)
		pl.plot(df_wrg['date'],df_wrg['tp'],cor[c],linewidth=2)
		pl.xlim(df_rg['date'][1600], df_rg['date'][1950])
		pl.xticks(visible=False), pl.ylabel('Tp (s)'), pl.grid(), pl.ylim(0,20)
		pl.subplot(3,3,7)
		pl.plot(df_wrg['date'],df_wrg['dp'],cor[c],linewidth=2)
		pl.xlim(df_rg['date'][1600], df_rg['date'][1950])
		pl.xticks(rotation=20), pl.ylabel('Dp (graus)')
		pl.yticks([0,45,90,135,180,225,270,315,360]), pl.ylim(0,360), pl.grid()

		pl.subplot(3,3,2)
		pl.title(dprev[0:4]+'-'+dprev[4:6]+'-'+dprev[6:8] + '\n Florianopolis/SC')
		pl.plot(df_wfl['date'],df_wfl['hs'],cor[c],linewidth=2)
		pl.xlim(df_fl['date'][1600], df_fl['date'][1950])
		pl.xticks(visible=False), pl.ylabel('Hs (m)'), pl.grid(), pl.ylim(0,7)
		pl.subplot(3,3,5)
		pl.plot(df_wfl['date'],df_wfl['tp'],cor[c],linewidth=2)
		pl.xlim(df_fl['date'][1600], df_fl['date'][1950])
		pl.xticks(visible=False), pl.ylabel('Tp (s)'), pl.grid(), pl.ylim(0,20)
		pl.subplot(3,3,8)
		pl.plot(df_wfl['date'],df_wfl['dp'],cor[c],linewidth=2)
		pl.xlim(df_fl['date'][1600], df_fl['date'][1950])
		pl.xticks(rotation=20), pl.ylabel('Dp (graus)')
		pl.yticks([0,45,90,135,180,225,270,315,360]), pl.ylim(0,360),  pl.grid()

		pl.subplot(3,3,3)
		pl.title('Santos/SP')
		pl.plot(df_wsa['date'],df_wsa['hs'],cor[c],linewidth=2)
		pl.xlim(df_sa['date'][1600], df_sa['date'][1950])
		pl.xticks(visible=False), pl.ylabel('Hs (m)'), pl.grid(), pl.ylim(0,7)
		pl.subplot(3,3,6)
		pl.plot(df_wsa['date'],df_wsa['tp'],cor[c],linewidth=2)
		pl.xlim(df_sa['date'][1600], df_sa['date'][1950])
		pl.xticks(visible=False), pl.ylabel('Tp (s)'), pl.grid(), pl.ylim(0,20)
		pl.subplot(3,3,9)
		pl.plot(df_wsa['date'],df_wsa['dp'],cor[c],linewidth=2)
		pl.xlim(df_sa['date'][1600], df_sa['date'][1950])
		pl.xticks(rotation=20), pl.ylabel('Dp (graus)')
		pl.yticks([0,45,90,135,180,225,270,315,360]), pl.ylim(0,360), pl.grid()

	pl.savefig('fig/' + dprev + '.png')

	pl.show()
