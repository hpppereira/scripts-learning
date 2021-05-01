# coding: utf-8

'''Comparison between Buoys and NWW3

Henrique P P Pereira'''

import numpy as np
import matplotlib
matplotlib.use('Agg') #necessario para salvar figura no crontab
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
plt.close('all')

#data stations
stations_ndbc = ['NDBC_32012',
				# 'NDBC_41002',
				# 'NDBC_41013',
				# 'NDBC_41025',
				# 'NDBC_41060',
				# 'NDBC_41114',
				# 'NDBC_42058',
				# 'NDBC_44020',
				# 'NDBC_46215',
				# 'NDBC_46229',
				# 'NDBC_51202'
				]

stations_pnboia = ['PNBOIA_BRN','PNBOIA_FTL','PNBOIA_RCF','PNBOIA_PSG',
			       'PNBOIA_VIX','PNBOIA_CFR','PNBOIA_BGA','PNBOIA_SAN',
			       'PNBOIA_FLN','PNBOIA_RIG']

# stations_remo = ['REMO_CF01','REMO_CF02']

# stations_pacific = ['PACIFIC_01']

#pathname of data
pathname_ndbc = os.environ['HOME'] + '/Dropbox/database/NDBC/realtime/'
pathname_pnboia = os.environ['HOME'] + '/Dropbox/database/PNBOIA/realtime/goosbr/'
pathname_nww3 = os.environ['HOME'] + '/Dropbox/database/NWW3/realtime/'
pathname_fig = os.environ['HOME'] + '/Dropbox/metocean/web/img/'

#function to plot forecast and data
def plotwindwave(pathname, station, date1, hs1, tp1, dp1, ws1, wd1, date2, hs2, tp2, dp2, ws2, wd2):

	fig = plt.figure(figsize=(12,12))

	lim1 = date2[0]
	# lim1 = date2[-1] - timedelta(days=10)
	lim2 = date2[-1c  ]

	ax1 = fig.add_subplot(511)
	ax1.plot(date1, ws1, '.b', date2, ws2, '.r')
	ax1.plot([datetime.now(), datetime.now()], [0,30], 'k--')
	ax1.legend(['buoy','nww3'], ncol=2)
	ax1.set_xlim(lim1, lim2)
	ax1.set_ylim(0,30)
	ax1.set_title(station)
	ax1.grid()
	ax1.set_ylabel('Wind Speed (m/s)')
	plt.xticks(visible=False)

	ax2 = fig.add_subplot(512)
	ax2.plot(date1, wd1, '.b', date2, wd2, '.r')
	ax2.plot([datetime.now(), datetime.now()], [0,360], 'k--')
	ax2.set_xlim(lim1, lim2)
	ax2.set_ylim(0,360)
	ax2.grid()
	ax2.set_ylabel('Wind Dir. (deg)')
	plt.xticks(visible=False)

	ax3 = fig.add_subplot(513)
	ax3.plot(date1, hs1, '.b', date2, hs2, '.r')
	ax3.plot([datetime.now(), datetime.now()], [0,10], 'k--')
	ax3.set_xlim(lim1, lim2)
	ax3.set_ylim(0,10)
	ax3.grid()
	ax3.set_ylabel('Hs (m)')
	plt.xticks(visible=False)

	ax4 = fig.add_subplot(514)
	ax4.plot(date1, tp1, '.b', date2, tp2, '.r')
	ax4.plot([datetime.now(), datetime.now()], [0,25], 'k--')
	ax4.set_xlim(lim1, lim2)
	ax4.set_ylim(0,25)
	ax4.grid()
	ax4.set_ylabel('Tp (s)')
	plt.xticks(visible=False)
	
	ax5 = fig.add_subplot(515)
	ax5.plot(date1, dp1, '.b', date2, dp2, '.r')
	ax5.plot([datetime.now(), datetime.now()], [0,360], 'k--')
	ax5.set_xlim(lim1, lim2)
	ax5.set_ylim(0,360)
	ax5.grid()
	ax5.set_ylabel('Dp (deg)')
	plt.xticks(rotation=10)

	fig.savefig(pathname + station + '.png', bbox_inches='tight')

#################################################################################################

#plot NDBC

for s in range(len(stations_ndbc)):

	print (stations_ndbc[s])
	
	nww3 = pd.read_csv(pathname_nww3 + 'NWW3_' + stations_ndbc[s] + '.csv',
		sep=',', parse_dates=['date'], index_col=['date'])

	ndbc = pd.read_csv(pathname_ndbc + stations_ndbc[s] + '.csv',
		sep=',', parse_dates=['date'], index_col=['date'])

	plotwindwave(pathname=pathname_fig,
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
#plot PNBOIA - MB

# for s in range(len(stations_pnboia)):

# 	print (stations_pnboia[s])
	
# 	nww3 = pd.read_csv(pathname_nww3 + 'NWW3_' + stations_pnboia[s] + '.csv',
# 		sep=',', parse_dates=['date'], index_col=['date'])

# 	#points with pnboia buoy data
# 	if stations_pnboia[s] in ['PNBOIA_FTL','PNBOIA_VIX','PNBOIA_CFR']:

# 		pnboia = pd.read_csv(pathname_pnboia + stations_pnboia[s] + '.csv',
# 		sep=',', parse_dates=['time'], index_col=['time'])

# 		plotwindwave(pathname=pathname_fig,
# 					 station=stations_pnboia[s], 
# 					 date1=pnboia.index,
# 					 hs1=pnboia.wave_hs,
# 					 tp1=pnboia.wave_period,
# 					 dp1=pnboia.wave_dir,
# 					 ws1=pnboia.avg_wind_int1,
# 					 wd1=pnboia.wind_dir1, 
# 					 date2=nww3.index,
# 					 hs2=nww3.hs,
# 					 tp2=nww3.tp,
# 					 dp2=nww3.dp,
# 					 ws2=nww3.ws,
# 					 wd2=nww3.wd)

# 	# zeros for buoys hs, tp and dp (plot only forecast)
# 	else:

# 		plotwindwave(pathname=pathname_fig,
# 					 station=stations_pnboia[s], 
# 					 date1=nww3.index,
# 					 hs1=np.zeros(len(nww3)),
# 					 tp1=np.zeros(len(nww3)),
# 					 dp1=np.zeros(len(nww3)),
# 					 ws1=np.zeros(len(nww3)),
# 					 wd1=np.zeros(len(nww3)), 
# 					 date2=nww3.index,
# 					 hs2=nww3.hs,
# 					 tp2=nww3.tp,
# 					 dp2=nww3.dp,
# 					 ws2=nww3.ws,
# 					 wd2=nww3.wd)


#################################################################################################


plt.show()