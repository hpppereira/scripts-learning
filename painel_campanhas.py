

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

def make_panel(df, tit):
    """
    Plot panel
    """

    fig = plt.figure(figsize=(19,12), facecolor='w')

    #------
    ax1 = fig.add_subplot(3,3,1)
    ax1.plot(df.wspd1, '-', markersize=3, label='Mean')
    ax1.plot(df.gust1, '-', markersize=3, label='Gust')
    ax1.set_ylabel('Wind Spd. (m/s)', color='k')
    ax1.grid()
    ax1.legend(fontsize=7)
    plt.xticks(rotation=20, visible=True)

    #------
    ax1 = fig.add_subplot(3,3,4)
    ax1.plot(df.wdir1, '-', markersize=3)
    ax1.set_ylabel('Wind Dir. (º)', color='k')
    plt.yticks(np.arange(0,360+45,45))
    ax1.grid()
    plt.xticks(rotation=20, visible=True)

    ax1 = fig.add_subplot(3,3,7)
    ax1.plot(df.pres, '-', markersize=3)
    ax1.set_ylabel('Atm. Pressure (hPa)', color='k')
    ax1.grid()
    plt.xticks(rotation=20, visible=True)

    ax1 = fig.add_subplot(3,3,2)
    ax1.plot(df.lon, df.lat, 'o')
    ax1.plot(df.lon[-1], df.lat[-1], 'ro')
    ax1.set_ylabel('Latitude (Déc. graus)', color='k')
    ax1.set_xlabel('Longitude (Déc. graus)', color='k')
    ax1.set_title('AtmosMarine \n PNBOIA - {}'.format(tit))
    ax1.grid()
#    plt.xlim(0.05,0.4)
    ax1.legend(fontsize=7)
    plt.xticks(rotation=0, visible=True)

    ax1 = fig.add_subplot(3,3,5)
    ax1.plot(df.atmp, '-', markersize=3, label='Air')
    ax1.plot(df.dewp, '-', markersize=3, label='Dew')
    ax1.set_ylabel('Air Temp. (ºC)', color='k')
    ax1.grid()
    ax1.legend(fontsize=7)
    plt.xticks(rotation=20, visible=True)

    ax1 = fig.add_subplot(3,3,8)
    ax1.plot(df.humi, '-', markersize=3, label='Inst.')
    #ax1.plot(df.umid_med, '-o', markersize=3, label='Mean')
    ax1.set_ylabel('Rel. Umid. (%)', color='k')
    ax1.grid()
    ax1.legend(fontsize=7)
    plt.xticks(rotation=20, visible=True)

    ax1 = fig.add_subplot(3,3,3)
    ax1.plot(df.wvht, '-', markersize=3, label='Hs')
    ax1.plot(df.wmax, '-', markersize=3, label='Hmax')
    ax1.set_ylabel('Wave Height (m)', color='k')
    ax1.grid()
    ax1.legend(fontsize=7)
    plt.xticks(rotation=20, visible=True)

    ax1 = fig.add_subplot(3,3,6)
    ax1.plot(df.dpd, '-', markersize=3, label='Tp')
    ax1.set_ylabel('Wave Period (m)', color='k')
    ax1.grid()
    plt.xticks(rotation=20, visible=True)

    ax1 = fig.add_subplot(3,3,9)
    ax1.plot(df.mwd, '-', markersize=3, label='Dp')
    ax1.set_ylabel('Wave Direction (º)', color='k')
    ax1.grid()
    plt.yticks(np.arange(0,360+45,45))
    plt.xticks(rotation=20, visible=True)

    return fig

if __name__ == '__main__':

    pathname = os.environ['HOME'] + '/gdrive/pnboia/dados/historico_campanhas/'

    for p in np.sort(glob(pathname + '*qc_c*.csv')):

        nome = p.split('/')[-1].split('.')[0]

        df = pd.read_csv(p, index_col='date', parse_dates=True)

        fig = make_panel(df, tit=nome)

        fig.savefig(pathname + '{}.png'.format(nome), bbox_inches='tight')
