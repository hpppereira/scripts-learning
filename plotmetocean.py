# coding: utf-8

'''Comparison between Buoys and NWW3'''

import numpy as np
import matplotlib
matplotlib.use('Agg') #necessario para salvar figura no crontab
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
plt.close('all')

#data stations
stations_ndbc = ['NDBC_32012','NDBC_41002','NDBC_41013','NDBC_41025',
				 'NDBC_41060','NDBC_41114','NDBC_42058','NDBC_44020',
				 'NDBC_46215','NDBC_46229','NDBC_51202']

stations_pnboia = ['PNBOIA_BRN','PNBOIA_FTL','PNBOIA_RCF','PNBOIA_PSG',
				   'PNBOIA_VIX','PNBOIA_CFR','PNBOIA_BGA','PNBOIA_SAN',
				   'PNBOIA_FLN','PNBOIA_RIG']

stations_remo = ['REMO_CF01','REMO_CF02']

stations_pacific = ['PACIFIC_01']

#pathname of data
pathname = os.environ['HOME'] + '/Dropbox/database/'

#pathname where the figures will be save
pathnamefig = os.environ['HOME'] + '/Dropbox/metocean/fig/forecast/'

#function to plot forecast and data
def plotwindwave(pathname, station, date1, hs1, tp1, dp1, ws1, wd1, date2, hs2, tp2, dp2, ws2, wd2):

	fig = plt.figure(figsize=(12,12))

	aux = -128
	ax1 = fig.add_subplot(511)
	ax1.plot(date1, ws1, '.b', date2, ws2, '.r')
	ax1.plot([datetime.now(), datetime.now()], [0,30], 'k--')
	ax1.legend(['buoy','nww3'], ncol=2)
	ax1.set_xlim(date2[aux], date2[-1])
	ax1.set_ylim(0,30)
	ax1.set_title(station)
	ax1.grid()
	ax1.set_ylabel('Wind Speed (m/s)')
	plt.xticks(visible=False)

	ax2 = fig.add_subplot(512)
	ax2.plot(date1, wd1, '.b', date2, wd2, '.r')
	ax2.plot([datetime.now(), datetime.now()], [0,360], 'k--')
	ax2.set_xlim(date2[aux], date2[-1])
	ax2.set_ylim(0,360)
	ax2.grid()
	ax2.set_ylabel('Wind Dir. (deg)')
	plt.xticks(visible=False)

	ax3 = fig.add_subplot(513)
	ax3.plot(date1, hs1, '.b', date2, hs2, '.r')
	ax3.plot([datetime.now(), datetime.now()], [0,10], 'k--')
	ax3.set_xlim(date2[aux], date2[-1])
	ax3.set_ylim(0,10)
	ax3.grid()
	ax3.set_ylabel('Hs (m)')
	plt.xticks(visible=False)

	ax4 = fig.add_subplot(514)
	ax4.plot(date1, tp1, '.b', date2, tp2, '.r')
	ax4.plot([datetime.now(), datetime.now()], [0,25], 'k--')
	ax4.set_xlim(date2[aux], date2[-1])
	ax4.set_ylim(0,25)
	ax4.grid()
	ax4.set_ylabel('Tp (s)')
	plt.xticks(visible=False)
	
	ax5 = fig.add_subplot(515)
	ax5.plot(date1, dp1, '.b', date2, dp2, '.r')
	ax5.plot([datetime.now(), datetime.now()], [0,360], 'k--')
	ax5.set_ylim(0,360)
	ax5.grid()
	ax5.set_ylabel('Dp (deg)')
	ax5.set_xlim(date2[aux], date2[-1])
	plt.xticks(rotation=10)

	fig.savefig(pathname + station + '.png', bbox_inches='tight')

#################################################################################################
#################################################################################################

#plot NDBC
for s in range(len(stations_ndbc)):

	print (stations_ndbc[s])
	
	ndbc = pd.read_csv(pathname + 'realtime/buoys/ndbc/' + stations_ndbc[s] + '.csv',
		sep=',', parse_dates=['date'], index_col=['date'])

	nww3 = pd.read_csv(pathname + 'forecast/nww3/NWW3_' + stations_ndbc[s] + '.csv',
		sep=',', parse_dates=['date'], index_col=['date'])

	plotwindwave(pathname=pathnamefig,
				 station=stations_ndbc[s], 
				  date1=ndbc.index,
				  hs1=ndbc.WVHT,
				  tp1=ndbc.DPD,
				  dp1=ndbc.MWD,
				  ws1=np.zeros(len(ndbc)),
				  wd1=np.zeros(len(ndbc)), 
				  date2=nww3.index,
				  hs2=nww3.hs,
				  tp2=nww3.tp,
				  dp2=nww3.dp,
				  ws2=nww3.ws,
				  wd2=nww3.wd)

#################################################################################################
#################################################################################################

#plot PNBOIA
for s in range(len(stations_pnboia)):

	print (stations_pnboia[s])
	
	nww3 = pd.read_csv(pathname + 'forecast/nww3/NWW3_' + stations_pnboia[s] + '.csv',
		sep=',', parse_dates=['date'], index_col=['date'])

	#points with pnboia buoy data
	if stations_pnboia[s] in ['PNBOIA_RIG','PNBOIA_SAN','PNBOIA_VIX','PNBOIA_PSG']:

		# pnboia = pd.read_csv(pathname + 'Realtime/Buoys/PNBOIA/Argos/' + stations_pnboia[s] + '.csv',
		# sep=',', parse_dates=['date'], index_col=['date'])

		pnboia = pd.read_csv(pathname + 'realtime/buoys/pnboia/xls/' + stations_pnboia[s] + '_xls.csv',
		sep=',', parse_dates=['date'], index_col=['date'])

		plotwindwave(pathname=pathnamefig,
					 station=stations_pnboia[s], 
					 date1=pnboia.index,
					 hs1=pnboia.hs,
					 tp1=pnboia.tp,
					 dp1=pnboia.dp,
					 ws1=pnboia.ws1,
					 wd1=pnboia.wd1, 
					 date2=nww3.index,
					 hs2=nww3.hs,
					 tp2=nww3.tp,
					 dp2=nww3.dp,
					 ws2=nww3.ws,
					 wd2=nww3.wd)

	#zeros for buoys hs, tp and dp (plot only forecast)
	else:

		plotwindwave(pathname=pathnamefig,
					 station=stations_pnboia[s], 
					 date1=nww3.index,
					 hs1=np.zeros(len(nww3)),
					 tp1=np.zeros(len(nww3)),
					 dp1=np.zeros(len(nww3)),
					 ws1=np.zeros(len(nww3)),
					 wd1=np.zeros(len(nww3)), 
					 date2=nww3.index,
					 hs2=nww3.hs,
					 tp2=nww3.tp,
					 dp2=nww3.dp,
					 ws2=nww3.ws,
					 wd2=nww3.wd)

#################################################################################################
#################################################################################################

#plot REMO
for s in range(len(stations_remo)):

	print (stations_remo[s])

	nww3 = pd.read_csv(pathname + 'forecast/nww3/NWW3_' + stations_remo[s] + '.csv',
		sep=',', parse_dates=['date'], index_col=['date'])

	if stations_remo[s] == 'REMO_CF01':

		cf1 = pd.read_csv(pathname + 'realtime/buoys/remo/CF1_BMOBR05_2016Nov/cf1nov16.csv',
		 index_col='date', parse_dates=True)

		cf1 = cf1['2016-11-05 20:00':]

		plotwindwave(pathname=pathnamefig,
					 station=stations_remo[s], 
					 date1=cf1.index,
					 hs1=cf1.hs,
					 tp1=cf1.tp,
					 dp1=cf1.dp,
					 ws1=cf1.ws,
					 wd1=cf1.wd, 
					 date2=nww3.index,
					 hs2=nww3.hs,
					 tp2=nww3.tp,
					 dp2=nww3.dp,
					 ws2=nww3.ws,
					 wd2=nww3.wd)

#################################################################################################
#################################################################################################

#plot PACIFIC
for s in range(len(stations_pacific)):

	print (stations_pacific[s])
	
	# pnboia = pd.read_csv(pathname + 'pnboia/realtime/' + stations_pnboia[s] + '.csv',
	# 	sep=',', parse_dates=['date'], index_col=['date'])

	nww3 = pd.read_csv(pathname + 'forecast/nww3/NWW3_' + stations_pacific[s] + '.csv',
		sep=',', parse_dates=['date'], index_col=['date'])

	plotwindwave(pathname=pathnamefig,
				 station=stations_pacific[s], 
				 date1=np.zeros(len(nww3)),
				 hs1=np.zeros(len(nww3)),
				 tp1=np.zeros(len(nww3)),
				 dp1=np.zeros(len(nww3)),
				 ws1=np.zeros(len(nww3)),
				 wd1=np.zeros(len(nww3)), 
				 date2=nww3.index,
				 hs2=nww3.hs,
				 tp2=nww3.tp,
				 dp2=nww3.dp,
				 ws2=nww3.ws,
				 wd2=nww3.wd)

plt.show()