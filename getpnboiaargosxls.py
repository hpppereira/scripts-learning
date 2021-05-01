'''
Le dados em .xls do site do PNBOIA

#https://www.mar.mil.br/dhn/chm/meteo/prev/dados/pnboia/JAN_ARGOS_146447_Vitoria.xls

CORRIGE DEC MAG
'''

import os
import xlrd
import numpy as np
from datetime import datetime
import datetime as dt
import consisteproc
import matplotlib.pylab as pl
import pandas as pd
import urllib
import urllib2
import re
import string

reload(consisteproc)

#import getpnboia #baixa dados

#reload(getpnboia)

pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/op/'

boias = ["69153_RioGrande",
		 "146447_Vitoria",
		 "69008_Recife",
		 "69151_Guanabara",
		 "69150_Santos"]

dmag = [-17,-23,-22,-23,-22]

data = dt.datetime.strftime(dt.datetime.now(),'%Y%m%d%H')
meses = ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ']
mes = meses[int(data[4:6])-1]

cont = -1
for boia in boias:

	#contador
	cont += 1

	#diretorio e nome do arquivo de saida
	arq = pathname + 'xls/' + boia + '_' + data + '.xls'

	#carrega arquivo antigo concatenado 
	old = pd.read_table(pathname + 'lioc/' + boia + '_metocean.csv',sep=',',parse_dates=['date'],index_col=['date'])

	#baixa dado
	site_adress = "https://www.mar.mil.br/dhn/chm/meteo/prev/dados/pnboia/"+mes+"_ARGOS_"+boia+".xls"
	site = urllib.urlretrieve(site_adress,arq)
	print 'Baixando dado da ' + boia

	#carrega arquivo de saida
	workbook = xlrd.open_workbook(arq)

	#seleciona planilha por indice (pode ser por nome tbm)
	sheet_0 = workbook.sheet_by_index(0) #planilha 1 - status + vento
	sheet_1 = workbook.sheet_by_index(1) #planilha 2 - meteo + onda

	#pega os valores das celulas selecionadas

	#legenda
	leg0 = np.array([[sheet_0.cell_value(r,c) for r in range(3,4)] for c in range(0,sheet_0.ncols)]).T
	leg1 = np.array([[sheet_1.cell_value(r,c) for r in range(3,4)] for c in range(0,sheet_1.ncols)]).T

	#dados - inverte - flipud
	dd0 = np.flipud(np.array([[sheet_0.cell_value(r,c) for r in range(4,sheet_0.nrows)] for c in range(sheet_0.ncols)]).T)
	dd1 = np.flipud(np.array([[sheet_1.cell_value(r,c) for r in range(4,sheet_1.nrows)] for c in range(sheet_1.ncols)]).T)

	# for c in range(dd0.shape[1]):
	# 	for i in range(dd0.shape[0]):
	# 		#dd0[i,c] = re.sub('[xX ]+', 'NaN', dd0[i,c])
	# 		dd0[i,c] = re.sub('[%s]+' %string.printable[10:70], 'NaN', dd0[i,c])


	#substitui 'xxxx' por nan
	dd0[np.where(dd0=='xxxx')] = np.nan
	dd1[np.where(dd1=='xxxx')] = np.nan
	dd0[np.where(dd0=='xxxxx')] = np.nan
	dd1[np.where(dd1=='xxxxx')] = np.nan
	dd0[np.where(dd0=='xxx')] = np.nan
	dd1[np.where(dd1=='xxx')] = np.nan
	dd0[np.where(dd0=='XXX')] = np.nan
	dd1[np.where(dd1=='XXX')] = np.nan
	dd0[np.where(dd0=='XXXX')] = np.nan
	dd1[np.where(dd1=='XXXX')] = np.nan
	dd0[np.where(dd0=='')] = np.nan
	dd1[np.where(dd1=='')] = np.nan
	dd0[np.where(dd0==' ')] = np.nan
	dd1[np.where(dd1==' ')] = np.nan

	df0 = pd.DataFrame(dd0[:,[1,3,5,6,7,8,9,10]],columns=['date','bat','ws1','wg1','wd1','ws2','wg2','wd2'])
	df1 = pd.DataFrame(dd1[:,[1,2,3,4,5,6,7,8,9,10]],columns=['date','at','rh','dwp','pr','sst','hs','hmax','tp','dp'])
	df0['date'] = pd.to_datetime(df0.date)
	df1['date'] = pd.to_datetime(df1.date)
	df0 = df0.set_index('date')
	df1 = df1.set_index('date')

	#converte os nan em string par nan
	df0[df0 == 'nan'] = np.nan
	df1[df1 == 'nan'] = np.nan

	#converte para float
	df0 = df0.astype(float)
	df1 = df1.astype(float)

	#corrige declinacao magnetica
	df0[['wd1','wd2']] = df0[['wd1','wd2']] + dmag[cont] #corrige a declinacao magnetica para cada boia
	df1['dp'] = df1['dp'] + dmag[cont]

	#reamostra de hora em hora
	df0 = df0.resample('H', how='mean')
	df1 = df1.resample('H', how='mean')

	#junta os dois dados
	df = df1.join(df0)

	df = pd.concat([old,df])

	#retira dados repetidos (verifica a data)
	u, ind = np.unique(df.index, return_index=True)
	df = df.ix[ind]

	df.to_csv(pathname + 'lioc/' + boia + '_metocean.csv',na_rep='nan')

