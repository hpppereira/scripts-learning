# coding: utf-8

'''
http://opendap.saltambiental.com.br:8080/pnboia/

Henrique P P Pereira

Variaveis:

avg_radiation   
rel_humid       
wave_period     
cm_dir1         
temp_air        
wave_dir        
battery         
latitude        
wind_dir1       
cm_int1         
cm_int3         
cm_int2         
wave_hs         
sst             
wind_gust1_f2   
pressure        
wave_h_max      
wind_dir1_f2    
dew_point       
avg_wind_int1_f2
cm_dir3         
cm_dir2         
longitude       
avg_wind_int1   
avg_wind_int2   
wind_gust2      
avg_dir2        
wind_gust1      

'''


import os
import matplotlib
import pandas as pd
import numpy as np
from datetime import datetime
import xray
try:
	os.environ["DISPLAY"]
except:
	matplotlib.use('Agg')

#paths
pathfile = os.environ['HOME'] + '/Dropbox/database/PNBOIA/realtime/goosbr/'

urls = {
        # 'http://opendap.saltambiental.com.br:8080/pnboia/Brio_grande.nc', #erro
        # 'http://opendap.saltambiental.com.br:8080/pnboia/Bsanta_catarina.nc', #erro
        # 'FLN': 'http://opendap.saltambiental.com.br:8080/pnboia/Bsanta_catarina2.nc',
        # 'http://opendap.saltambiental.com.br:8080/pnboia/Bsantos.nc', #erro
        # 'http://opendap.saltambiental.com.br:8080/pnboia/Bguanabara.nc', #erro
        'CFR': 'http://opendap.saltambiental.com.br:8080/pnboia/Bcabo_frio.nc',
        # 'http://opendap.saltambiental.com.br:8080/pnboia/B69009_cabofrio.nc', #erro
        'VIX': 'http://opendap.saltambiental.com.br:8080/pnboia/Bvitoria.nc',
        # 'http://opendap.saltambiental.com.br:8080/pnboia/Bporto_seguro.nc', #erro
        # 'http://opendap.saltambiental.com.br:8080/pnboia/Brecife.nc', #erro
        'FTL': 'http://opendap.saltambiental.com.br:8080/pnboia/Bfortaleza.nc'
        }

dic = {}
for url in urls.items():

    try:
    
        print url

        aux = xray.open_dataset(url[1])

        print aux.time.data[-1]

        # monta arquivo de dados
        df = aux.to_dataframe()

        # coloca nan no lugar de -99999
        df[df==-99999.000000] = np.nan

        # salva arquivo csv
        df.to_csv(pathfile + 'PNBOIA_' + url[0] + '.csv', na_rep='NaN')

    except Exception as e: print (e)
























# pathname = os.environ['HOME'] + '/Dropbox/pnboia/data/realtime/mb/'
# anomes = datetime.now().strftime('%y%m')
# boias = ['rg', 'sc', 'st', 'bg', 'cf', 'vt', 'ps', 'rc', 'fo']
# boias1 = ['PNBOIA_RIG','PNBOIA_FLN','PNBOIA_SAN','PNBOIA_BGA','PNBOIA_CFR','PNBOIA_VIX','PNBOIA_PSG','PNBOIA_RCF','PNBOIA_FTL']
				       
# dd = {}

# cont = -1
# for boia in boias:

# 	print boia


# 	cont += 1

# 	try:

# 		for sheet in ['sheet001', 'sheet002']:

# 			url = 'https://www.mar.mil.br/dhn/chm/meteo/prev/dados/pnboia/' + boia + anomes + '_ficheiros/' + sheet + '.htm'

# 			print url

# 			aux = pd.read_html(url, thousands='.')[0][5:].astype(str)

# 			aux = np.array([aux.ix[:,i].apply(lambda x: x.replace(',','.')) for i in aux.columns]).T

# 			aux[np.where(aux == 'xxx')] = np.nan
# 			aux[np.where(aux == 'xxxx')] = np.nan
# 			aux[np.where(aux == 'xxxxx')] = np.nan
# 			aux[np.where(aux == 'nan')] = np.nan

# 			if sheet == 'sheet001':

# 				dd1 = pd.DataFrame(aux[:,:11], columns=['argos_id', 'date', 'position', 'battery', 'flooding', 'ws1', 'wg1', 'wd1', 'ws2', 'wg2', 'wd2'])
# 				dd1['date'] = pd.to_datetime(dd1.date)
# 				dd1 = dd1.loc[dd1.date.isnull()==False]
# 				dd1 = dd1.set_index('date')
# 				dd1 = dd1.astype(float)
# 				dd1 = dd1.resample('H').mean()

# 			elif sheet == 'sheet002':

# 				dd2 = pd.DataFrame(aux[:,1:11], columns=['date', 'at', 'rh', 'dew_point', 'pr', 'sst', 'hs', 'hmax', 'tp', 'dp'])
# 				dd2['date'] = pd.to_datetime(dd2.date)
# 				dd2 = dd2.loc[dd2.date.isnull()==False]
# 				dd2 = dd2.set_index('date')
# 				dd2 = dd2.astype(float)
# 				dd2 = dd2.resample('H').mean()

# 		new = pd.concat((dd1,dd2),axis=1)

# 		old = pd.read_csv(pathname + boias1[cont] + '.csv', sep=',', parse_dates=['date'], index_col=['date'])

# 		#concatena dado antigo com novo
# 		dd[boia] = pd.concat([old,new])

# 		#retira dados repetidos (verifica a data)
# 		u, ind = np.unique(dd[boia].index, return_index=True)
# 		dd[boia] = dd[boia].ix[ind]

# 		#inverte os dados
# 		# dd[boia] = dd[boia][-1:0:-1]

# 		# dd[boia] = new
# 		dd[boia].to_csv(pathname + boias1[cont] + '.csv', na_rep='NaN')

# 	except Exception as e: print (e)