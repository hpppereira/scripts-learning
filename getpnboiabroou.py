'''
#
# 	Santos
#			https://www.mar.mil.br/dhn/chm/meteo/prev/dados/pnboia/topo_st.htm
# 	Santa Catarina
#			https://www.mar.mil.br/dhn/chm/meteo/prev/dados/pnboia/topo_st.htm
#
#
#
#		LC_ALL=C sed -i.bak 's/,/./g' sheet002.html

<table border=0 cellpadding=0 cellspacing=0 width=1118 style='border-collapse:collapse;table-layout:fixed;width:841pt'>

site = https://www.mar.mil.br/dhn/chm/meteo/prev/dados/pnboia/

boia = sc

data_pn = 1506

planilha = sheet002.htm

'''

import numpy as np
import sys
import subprocess
import os
import time
import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import math

import warnings
warnings.filterwarnings("ignore")
# Matplotlib
import matplotlib
import matplotlib.pyplot as plt
try:
	os.environ["DISPLAY"]
except:
	matplotlib.use('Agg')

import pandas as pd
import xray

import wget

#
#
#
#


def down_pnboia(site,boia,data,plani):

	url = site+boia+data+'_ficheiros/'+plani

	filename = wget.download(url)

	command = '''cat sheet002.htm | grep -n \"<table\" | awk -F: '{{print $1}}' | sed -n \'1p\' | \
						xargs -I {{}} sed -n \"{{}},`cat sheet002.htm | wc -l`p\" sheet002.htm | LC_ALL=C sed -e \'s/,/./g\' > sheet002.html '''

	subprocess.call(command,shell=True)

	if os.stat('sheet002.html').st_size == 0:
		print("Arquivo PNBOIA boia: {0} \n".format(boia))
		print("               data: {0} \n".format(data))
		print("#### CORROMPIDO #### \n")		
		return None

	print (url)
	df = pd.read_html('sheet002.html')

	df2 = np.array(df[0])

	# Excluir valores errados
	#
	df2 = df2[4:,0:11]

	matrix_PN = {}

	matrix_PN['argos_id']=df2[1:,0]
	matrix_PN['air_temp']=df2[1:,2]
	matrix_PN['humidity']=df2[1:,3]
	matrix_PN['dew_point']=df2[1:,4]
	matrix_PN['pressure']=df2[1:,5]
	matrix_PN['sst']=df2[1:,6]
	matrix_PN['wave_hs']=df2[1:,7]
	matrix_PN['wave_hs_max']=df2[1:,8]
	matrix_PN['wave_tp']=df2[1:,9]
	matrix_PN['wave_dir']=df2[1:,10]

	fmt   = "%Y-%m-%d %H:%M"
	fmt2   = "%Y/%m/%d %H:%M:%S"
	fmt22   = "%Y/%d/%m %H:%M:%S"

	date_pn = []

	for dt in df2[1:,1]:
		if 'nan' in str(dt):
			dt = "1970/01/01 01:00:00"
			datetime_dt = datetime.datetime.strptime(str(dt),fmt2)
			date_pn.append(datetime.datetime.strftime(datetime_dt,fmt))
		else:
			# print dt
			try:
				datetime_dt = datetime.datetime.strptime(str(dt),fmt2)
			except:
				datetime_dt = datetime.datetime.strptime(str(dt),fmt22)
			date_pn.append(datetime.datetime.strftime(datetime_dt,fmt))

	df3 = pd.DataFrame(matrix_PN, index=date_pn)
	df3 = df3[pd.notnull(df3['wave_hs'])]

	df3.loc[df3['wave_hs'] == 'xxxx'] = np.nan

	subprocess.call("mkdir -p {}".format(boia),shell=True)

	pandas_file = boia+'/'+boia+'_'+data+'.csv'
	df3.to_csv(pandas_file, sep=',', encoding='utf-8', index=True, index_label='time')

def main():
	site = 'https://www.mar.mil.br/dhn/chm/meteo/prev/dados/pnboia/'

	# boias = ['rg']

	boias = [ 'rg', 'sc', 'st', 'rc', 'ps', 'vt', 'bg' ]

	plani = 'sheet002.htm'

	first_month = datetime.datetime(2011,01,01,0,0)

	today = datetime.datetime.today()

	diff = (today - first_month)

	total_moths = round((diff.days/365.)*12)

	fmt3 = "%y%m"

	# sys.exit()

	for boia in boias:
		for i in range(0,int(total_moths)):

			after_month = first_month + relativedelta(months=i)
			data=datetime.datetime.strftime(after_month,fmt3)
			print(data)

			if os.path.isfile(plani):
				subprocess.call("rm "+plani,shell=True)

			if os.path.isfile('sheet002.html'):
				subprocess.call("rm sheet002.html",shell=True)

			down_pnboia(site,boia,data,plani)

if __name__ == '__main__':

	main()

#
#	Retirar NAN (xxxx)
#
#	teste.loc[teste['wave_hs'] == 'xxxx'] = 'nan'
#
#	df3['wave_hs'].convert_objects(convert_numeric=True).describe()
#
#plt.plot(df.index,df['wave_hs'].convert_objects(convert_numeric=True))






