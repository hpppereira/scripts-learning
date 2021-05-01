'''
Baixa dados operacionalmente do geoforce
Username: pereira.henriquep@gmail.com
Password: l%FS1MKt


wget --user pereira.henriquep@gmail.com --password l%FS1MKt https://app.geoforce.com/feeds/asset_inventory.xml

'''

import os
import xml.etree.ElementTree as ET
import datetime
import pandas as pd
import numpy as np

#caminho de onde vai ser salvo
filename = 'asset_inventory.xml'
pathname_geoforce = os.environ['HOME'] + '/Dropbox/projects/BMOP/Processamento/dados/BMOBR05_CF1/op/'

#carrega arquivo antigo concatenado 
old_a = pd.read_csv(pathname_geoforce + 'Geoforce_BMOBR05_A.csv',sep=',',parse_dates=['date'],index_col=['date'])
old_b = pd.read_csv(pathname_geoforce + 'Geoforce_BMOBR05_B.csv',sep=',',parse_dates=['date'],index_col=['date'])

#baixa os dados
os.system('cd ' + pathname_geoforce + '\n' + 
	'rm ' + filename + '\n'
	'wget --user pereira.henriquep@gmail.com --password l%FS1MKt https://app.geoforce.com/feeds/' + filename)

#carrega o dado xml
tree = ET.parse(pathname_geoforce + filename)

#??
root = tree.getroot()

date = []
lat = []
lon = []

for a in root.iter('locations'):
	b = a.attrib
	date.append(datetime.datetime.strptime(b.values()[0],'%Y-%m-%dT%H:%M:%SZ'))
	
for a in root.iter('latitude'):
	lat.append(a.text)

for a in root.iter('longitude'):
	lon.append(a.text)

geoa = {'date' : date[0],
		'lat'  : lat[0] ,
		'lon'  : lon[0]
		}
ga = pd.DataFrame(geoa, index=[0])
ga = ga.set_index('date')

geob = {'date' : date[1],
		'lat'  : lat[1] ,
		'lon'  : lon[1]
		}
gb = pd.DataFrame(geob, index=['date'])
gb = gb.set_index('date')

#concatena o dado antigo com o novo
ga = pd.concat([old_a,ga])
gb = pd.concat([old_b,gb])

#retira dados repetidos (verifica a data)
u_a, ind_a = np.unique(ga.index, return_index=True)
u_b, ind_b = np.unique(gb.index, return_index=True)

ga = ga.ix[ind_a]
gb = gb.ix[ind_b]

#salva dataframes
ga.to_csv(pathname_geoforce + 'Geoforce_BMOBR05_A.csv')
gb.to_csv(pathname_geoforce + 'Geoforce_BMOBR05_B.csv')