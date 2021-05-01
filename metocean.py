"""
Baixar, plotar e atualizar o site metocean


"""

import matplotlib
matplotlib.use('Agg') #necessario para salvar figura no crontab
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import netCDF4
import pandas as pd
import datetime as dt
import os


def near(array,value):
    """
    Function to find index to nearest point
    """

    idx = (abs(array - value)).argmin()

    return idx


def read_nww3():
    """
    """
    mydate = dt.datetime.now()# - dt.timedelta(days=1)
    mydate = mydate.strftime('%Y%m%d')
    url = 'http://nomads.ncep.noaa.gov:9090/dods/wave/nww3/nww3'+mydate+'/nww3'+mydate+'_00z'

    # Extract the significant wave height of combined wind waves and swell

    nc = netCDF4.Dataset(url)
    lat = nc.variables['lat'][:]
    lon = nc.variables['lon'][:]
    data_hs = nc.variables['htsgwsfc'][0, :, :]
    data_tp = nc.variables['perpwsfc'][0,:,:]
    time_var = nc.variables['time']
    dtime = netCDF4.num2date(time_var[:],time_var.units)
    nc.close()

    return


if __name__ == '__main__':

    mydate = dt.datetime.now()# - dt.timedelta(days=1)
    mydate = mydate.strftime('%Y%m%d')
    url = 'http://nomads.ncep.noaa.gov:9090/dods/wave/nww3/nww3'+mydate+'/nww3'+mydate+'_00z'


#     stat  = {
#              'PNBOIA_BRN':   [+01.094, -046.350 + 360], #barra norte/am 
#              'PNBOIA_FTL':   [-02.987, -038.819 + 360], #fortaleza/ce
#              'PNBOIA_RCF':   [-08.149, -034.560 + 360], #recife/pe
#              'PNBOIA_PSG':   [-18.151, -037.944 + 360], #porto seguro/ba
#              'PNBOIA_VIX':   [-20.278, -039.727 + 360], #vitoria/es
#              'PNBOIA_CFR':   [-22.995, -042.187 + 360], #cabo frio/rj
#              'PNBOIA_BGA':   [-22.924, -043.150 + 360], #baia de guanabara/rj
#              'PNBOIA_SAN':   [-25.283, -044.933 + 360], #santos/sp
#              'PNBOIA_FLN':   [-28.500, -047.366 + 360], #florianopolis/sc
#              'PNBOIA_RIG':   [-31.566, -049.966 + 360], #rio grande/rs
#              }


# #retrieve time series of a point
# for st in np.sort(list(stat.keys())):

#     print (st)

#     # Find nearest point to desired location (no interpolation)
#     ix = near(lon, stat[st][1])
#     iy = near(lat, stat[st][0])
#     print (ix,iy)

#     # Get all time records of variable [vname] at indices [iy,ix]
#     hs = nc.variables['htsgwsfc'][:,iy,ix]
#     tp = nc.variables['perpwsfc'][:,iy,ix]
#     dp = nc.variables['dirpwsfc'][:,iy,ix]
#     ws = nc.variables['windsfc'][:,iy,ix]
#     wd = nc.variables['wdirsfc'][:,iy,ix]
#     tim = dtime[:]

#     # Create Pandas time series object
#     df = pd.DataFrame(np.array([hs, tp, dp, ws, wd]).T,
#                       index=pd.Series(tim, name='date'),
#                       columns=['hs', 'tp', 'dp', 'ws', 'wd'])
