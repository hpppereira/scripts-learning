#plot pnboia and nww3 data
#hs, tp, dp, ws, wd

import numpy as np
import matplotlib
matplotlib.use('Agg') #necessario para salvar figura no crontab
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
plt.close('all')

pathname_nww3 = os.environ['HOME'] + '/Dropbox/nww3/data/'
pathname_pnboia = os.environ['HOME'] + '/Dropbox/pnboia/data/realtime/mb/'
pathname_fig = '../fig'

stations_pnboia = ['PNBOIA_BRN','PNBOIA_FTL','PNBOIA_RCF','PNBOIA_PSG',
                   'PNBOIA_VIX','PNBOIA_CFR','PNBOIA_BGA','PNBOIA_SAN',
                   'PNBOIA_FLN','PNBOIA_RIG']

def plotwindwave(pathname, station, date1, hs1, tp1, dp1,
                 ws1, wd1, date2, hs2, tp2, dp2, ws2, wd2,
                 datex1, datex2):

    fig = plt.figure(figsize=(12,12))

    # aux = -128
    aux = -90
    # aux = -72
    # aux = -72
    ax1 = fig.add_subplot(511)
    ax1.plot(date1, ws1, '.b', date2, ws2, '.r')
    ax1.plot([datetime.now(), datetime.now()], [0,30], 'k--')
    ax1.legend(['buoy','nww3'], ncol=2)
    ax1.set_xlim(datex1, datex2)
    ax1.set_ylim(0,30)
    ax1.set_title(station)
    ax1.grid()
    ax1.set_ylabel('Wind Speed (m/s)')
    plt.xticks(visible=False)

    ax2 = fig.add_subplot(512)
    ax2.plot(date1, wd1, '.b', date2, wd2, '.r')
    ax2.plot([datetime.now(), datetime.now()], [0,360], 'k--')
    ax1.set_xlim(datex1, datex2)
    ax2.set_ylim(0,360)
    ax2.grid()
    ax2.set_ylabel('Wind Dir. (deg)')
    plt.xticks(visible=False)

    ax3 = fig.add_subplot(513)
    ax3.plot(date1, hs1, '.b', date2, hs2, '.r')
    ax3.plot([datetime.now(), datetime.now()], [0,10], 'k--')
    ax1.set_xlim(datex1, datex2)
    ax3.set_ylim(0,10)
    ax3.grid()
    ax3.set_ylabel('Hs (m)')
    plt.xticks(visible=False)

    ax4 = fig.add_subplot(514)
    ax4.plot(date1, tp1, '.b', date2, tp2, '.r')
    ax4.plot([datetime.now(), datetime.now()], [0,25], 'k--')
    ax1.set_xlim(datex1, datex2)
    ax4.set_ylim(0,25)
    ax4.grid()
    ax4.set_ylabel('Tp (s)')
    plt.xticks(visible=False)
    
    ax5 = fig.add_subplot(515)
    ax5.plot(date1, dp1, '.b', date2, dp2, '.r')
    ax5.plot([datetime.now(), datetime.now()], [0,360], 'k--')
    ax1.set_xlim(datex1, datex2)
    ax5.set_ylim(0,360)
    ax5.grid()
    ax5.set_ylabel('Dp (deg)')
    plt.xticks(rotation=10)

    fig.savefig(pathname + station + '.png', bbox_inches='tight')


#plot PNBOIA - MB

for s in range(len(stations_pnboia)):

    pathfile = pathname_pnboia + stations_pnboia[s] + '.csv'
    
    nww3 = pd.read_csv(pathname_nww3 + 'NWW3_' + stations_pnboia[s] + '.csv',
        sep=',', parse_dates=['date'], index_col=['date'])

    if os.stat(pathfile).st_size == 0:

        print (stations_pnboia[s] + ' -- Empty file')

        hs1 = np.zeros(len(nww3)),
        tp1 = np.zeros(len(nww3)),
        dp1 = np.zeros(len(nww3)),
        ws1 = np.zeros(len(nww3)),
        wd1 = np.zeros(len(nww3))

    else:

        print (stations_pnboia[s] + ' -- Plotting..')

        pnboia = pd.read_csv(pathfile,
                             sep=',', parse_dates=['date'], index_col=['date'])

        datex1 = '2016-04-01 00:00'
        datex2 = '2016-04-10 00:00'

        plotwindwave(pathname=pathname_fig,
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
                     wd2=nww3.wd,
                     datex1 = datex1,
                     datex2 = datex2)
                     
plt.show()



