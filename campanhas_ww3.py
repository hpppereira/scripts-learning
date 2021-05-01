'''
Processamento dos resultados do
ww3 para as campanhas de campo
relatorio ww3seal
'''

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import netCDF4 as nc
import matplotlib as mpl
import pylab as pl
import matplotlib.dates as mdates

pl.close('all')


#carrega resultados do WW3

pathname = os.environ['HOME'] + '/Dropbox/ww3seal/modelagem/campanhas/dir/'

#lista dos diretorios da modelagem
direm = np.sort(os.listdir(pathname))#[2:-1]

#carrega dado do primeiro diretorio (apenas Hs, Tp e Dp)  - para depois ser concatenado
parse1 = lambda x: datetime.strptime(x, '%Y %m %d %H') #formato dos arquivos .txt
parse2 = lambda x: datetime.strptime(x, '%Y%m%d %H') #formato dos arquivos .txt

#carrega dados do modelo (2 formatos)
ddd = {}
for i in range(len(direm)):

	if i < 2:
		print str(i+1) + ' Carregando ' + str(direm[i])
		ddd['dd' + str(i)] = pd.read_table(pathname + direm[i] + '/southatl.tab',sep='\s*',header=None,names=['year','month','day','hour','min','hs','tp','dp','spr'],parse_dates=[[0,1,2,3]],date_parser=parse1,index_col=['year_month_day_hour'])
		#ddd['dd' + str(i)]['tp'] = 1. / ddd['dd' + str(i)]['fp'] #cria variavel de tp
	
	else:
		print str(i+1) + ' Carregando ' + str(direm[i])
		ddd['dd' + str(i)] = pd.read_table(pathname + direm[i] + '/southatl.tab',skiprows=3,sep='\s*',names=['ymd','h','m','s','hs','L','Tr','dp','spr','fp','p_dir','p_spr'],parse_dates=[[0,1]],date_parser=parse2,index_col=['ymd_h'])
		ddd['dd' + str(i)]['tp'] = 1. / ddd['dd' + str(i)]['fp']

#concatena os dados com hs, tp e dp
dd = pd.concat([ddd['dd0'][['hs','tp','dp']],ddd['dd1'][['hs','tp','dp']],ddd['dd2'][['hs','tp','dp']],ddd['dd3'][['hs','tp','dp']],
	ddd['dd4'][['hs','tp','dp']],ddd['dd5'][['hs','tp','dp']],ddd['dd6'][['hs','tp','dp']],ddd['dd7'][['hs','tp','dp']],ddd['dd8'][['hs','tp','dp']],
			   ddd['dd9'][['hs','tp','dp']],ddd['dd10'][['hs','tp','dp']],ddd['dd11'][['hs','tp','dp']],ddd['dd12'][['hs','tp','dp']]])

#cria variaveis com as campanhas
dc = {}
dc['c1'] = dd.loc['2010-11-25':'2010-12-27'] #evento 1
dc['c2'] = dd.loc['2011-06-13':'2011-06-23'] #evento 2
dc['c3'] = dd.loc['2014-05-22':'2014-06-20'] #evento 3
dc['c4'] = dd.loc['2014-11-28':'2015-01-06'] #evento 4
dc['c5'] = dd.loc['2013-03-12':'2013-04-05'] #evento 5
dc['c6'] = dd.loc['2013-10-08':'2013-11-29'] #evento 6

#carrega dados do ECMWF

pathname_ecmwf = os.environ['HOME'] + '/Dropbox/ww3seal/ECMWF/'

ecmwf = nc.Dataset(pathname_ecmwf + 'Ondas_ECMWF_SEAL_2010_2015.nc')

time = ecmwf.variables['time'][:]
lats = ecmwf.variables['latitude'][:]
lons = - (360 - ecmwf.variables['longitude'][:])
hs = ecmwf.variables['swh'][:]
tp = ecmwf.variables['mwp'][:]
dp = ecmwf.variables['mwd'][:]

#converte datas (divide por 24 para passar para dias)
date = np.array(mpl.dates.num2date(time/24.0 + mpl.dates.date2num(datetime(1900,01,01,00))))

#monta dataframe
de = pd.DataFrame(np.array([date,hs[:,6,0],tp[:,6,0],dp[:,6,0]]).T, columns=['date','hs','tp','dp'])
de = de.set_index('date')


#calcula estatisticas

est = {}
for c in dc.keys():
	est['tab_' + c] = [ 
					   [dc[c].hs.mean(),dc[c].tp.mean(),dc[c].dp.mean()],
	   				   [np.percentile(dc[c].hs,90),np.percentile(dc[c].tp,90),np.percentile(dc[c].dp,90)],
	   				   [dc[c].hs.max(),dc[c].tp.max(),dc[c].dp.max()]
	   				 ]


fig = (15,10)

#tamanho da janela para plotagem
tj0 = de.index[0]
tj1 = de.index[-1]

pl.figure(figsize=fig)
pl.subplot(111)
pl.plot(de.index,de.hs,'b',dc['c1'].index,dc['c1'].hs,'r',dc['c2'].index,dc['c2'].hs,'r',dc['c3'].index,dc['c3'].hs,'r',dc['c4'].index,dc['c4'].hs,'r',dc['c5'].index,dc['c5'].hs,'r',dc['c6'].index,dc['c6'].hs,'r')
pl.text(dc['c1'].index[0],0.6,'1',fontsize=20)
pl.text(dc['c2'].index[0],0.6,'2',fontsize=20)
pl.text(dc['c3'].index[0],0.6,'3',fontsize=20)
pl.text(dc['c4'].index[0],0.6,'4',fontsize=20)
pl.text(dc['c5'].index[0],0.6,'5',fontsize=20)
pl.text(dc['c6'].index[0],0.6,'6',fontsize=20)
pl.ylabel('Hs (m)'), pl.grid(), pl.ylim(0.5,3.5), pl.xlim(tj0,tj1), pl.xticks(visible=True)
pl.legend(['ECMWF','WW3'],loc=9,ncol=2)
pl.savefig('camp_ecmwf_ww3.png')


pl.figure(figsize=fig)
pl.subplot(311)
pl.title('Campanha 01 - SED 01')
pl.plot(dc['c1'].index,dc['c1'].hs,'r')
pl.ylabel('Hs (m)'), pl.grid(), pl.ylim(0.5,3.5)
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(dc['c1'].index,dc['c1'].tp,'r.')
pl.ylabel('Tp (s)'), pl.grid(), pl.ylim(4,20)
pl.xticks(visible=False)
pl.subplot(313)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
pl.plot(dc['c1'].index,dc['c1'].dp,'r.')
pl.ylabel('Dp (graus)'), pl.grid(), pl.yticks(range(0,360+45,45))
pl.savefig('camp1.png')


pl.figure(figsize=fig)
pl.subplot(311)
pl.title('Campanha 02 - SED 02')
pl.plot(dc['c2'].index,dc['c2'].hs,'r')
pl.ylabel('Hs (m)'), pl.grid(), pl.ylim(0.5,3.5)
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(dc['c2'].index,dc['c2'].tp,'r.')
pl.ylabel('Tp (s)'), pl.grid(), pl.ylim(4,20)
pl.xticks(visible=False)
pl.subplot(313)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
pl.plot(dc['c2'].index,dc['c2'].dp,'r.')
pl.ylabel('Dp (graus)'), pl.grid(), pl.yticks(range(0,360+45,45))
pl.savefig('camp2.png')


pl.figure(figsize=fig)
pl.subplot(311)
pl.title('Campanha 03 - MARSEAL Agua 01')
pl.plot(dc['c3'].index,dc['c3'].hs,'r')
pl.ylabel('Hs (m)'), pl.grid(), pl.ylim(0.5,3.5)
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(dc['c3'].index,dc['c3'].tp,'r.')
pl.ylabel('Tp (s)'), pl.grid(), pl.ylim(4,20)
pl.xticks(visible=False)
pl.subplot(313)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
pl.plot(dc['c3'].index,dc['c3'].dp,'r.')
pl.ylabel('Dp (graus)'), pl.grid(), pl.yticks(range(0,360+45,45))
pl.savefig('camp3.png')


pl.figure(figsize=fig)
pl.subplot(311)
pl.title('Campanha 04 - MARSEAL Agua 02')
pl.plot(dc['c4'].index,dc['c4'].hs,'r')
pl.ylabel('Hs (m)'), pl.grid(), pl.ylim(0.5,3.5)
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(dc['c4'].index,dc['c4'].tp,'r.')
pl.ylabel('Tp (s)'), pl.grid(), pl.ylim(4,20)
pl.xticks(visible=False)
pl.subplot(313)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
pl.plot(dc['c4'].index,dc['c4'].dp,'r.')
pl.ylabel('Dp (graus)'), pl.grid(), pl.yticks(range(0,360+45,45))
pl.savefig('camp4.png')


pl.figure(figsize=fig)
pl.subplot(311)
pl.title('Campanha 05 - MARSEAL SED 03')
pl.plot(dc['c5'].index,dc['c5'].hs,'r')
pl.ylabel('Hs (m)'), pl.grid(), pl.ylim(0.5,3.5)
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(dc['c5'].index,dc['c5'].tp,'r.')
pl.ylabel('Tp (s)'), pl.grid(), pl.ylim(4,20)
pl.xticks(visible=False)
pl.subplot(313)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
pl.plot(dc['c5'].index,dc['c5'].dp,'r.')
pl.ylabel('Dp (graus)'), pl.grid(), pl.yticks(range(0,360+45,45))
pl.savefig('camp5.png')



pl.figure(figsize=fig)
pl.subplot(311)
pl.title('Campanha 06 - MARSEAL SED 04')
pl.plot(dc['c6'].index,dc['c6'].hs,'r')
pl.ylabel('Hs (m)'), pl.grid(), pl.ylim(0.5,3.5)
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(dc['c6'].index,dc['c6'].tp,'r.')
pl.ylabel('Tp (s)'), pl.grid(), pl.ylim(4,20)
pl.xticks(visible=False)
pl.subplot(313)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
pl.plot(dc['c6'].index,dc['c6'].dp,'r.')
pl.ylabel('Dp (graus)'), pl.grid(), pl.yticks(range(0,360+45,45))
pl.savefig('camp6.png')



pl.show()