"plot map with energy potential for some places"

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import xarray as xr

def make2dplot(names, hs, tp, mydate):
    """
    2d map for wave energy flux
    """

    # wave height
    h = np.arange(0,5,.1)

    # wave period
    t = np.arange(0,20,.1)

    # matrix for wave height and period
    H, T = np.meshgrid(h, t)

    # water density kg/m3
    p = 1025

    # gravity acceleration m/s2
    g = 9.81

    # wave energy flux (/s)
    P = (p * g ** 2 / (32 * np.pi)) * H ** 2 * T

    # wave energy flux (kW/h ??)
    P = P / 3600

    plt.figure(figsize=(8,6))
    plt.contourf(H, T, P, 50)
    plt.title('Wave Energy Flux - {}'.format(mydate))
    plt.xlabel('Significant Wave Height (m)')
    plt.ylabel('Peak Period (sec)')
    cbar = plt.colorbar()
    cbar.set_label('kW/h', rotation=270)


    for i in range(len(names)):
        # plt.text(hs[i], tp[i], names[i])
        plt.plot(hs[i], tp[i], 'o', label=names[i])

    plt.legend()
    plt.show()

    return

def calculate_energy_flux(H, T):

    # water density kg/m3
    p = 1025

    # gravity acceleration m/s2
    g = 9.81

    # wave energy flux (/s)
    P = (p * g ** 2 / (32 * np.pi)) * H ** 2 * T

    # wave energy flux (kW/h ??)
    P = P / 3600

    # wave energy
    #E = (p * g ** 2 / (64 * np.pi)) * H ** 2 * T

    return P

def read_data_points(pathname, filename):
    """
    Read data file with lat and lon in dec degrees
    """

    points = pd.read_csv(pathname + filename)

    # valid points
    pp = np.array([ 0,  1,  2,  3,  7, 12, 17, 18, 20, 22, 24, 26, 27, 32, 38, 39, 43, 45])

    points = points.loc[pp,:]

    points['Longitud'].loc[points['Longitud']<0] = points['Longitud'].loc[points['Longitud']<0] + 360

    names, lat, lon = points[['Nombre', 'Latitud', 'Longitud']].values.T

    return points, names, lat, lon

def near(array,value):
    """
    Function to find index to nearest point
    """

    idx=(abs(array-value)).argmin()

    return idx

def create_url_nww3():

    mydate = datetime.now()# - dt.timedelta(days=1)
    mydate = mydate.strftime('%Y%m%d')

    url = 'http://nomads.ncep.noaa.gov:9090/dods/wave/nww3/nww3'+mydate+'/nww3'+mydate+'_00z'

    return url, mydate

def read_data_nww3(url):

    ds = xr.open_dataset(url)

    return ds

def find_wave_point(lat, lon):

    point = ds.sel(time=0, lon=lon, lat=lat, method='nearest')
    hs = float(point['htsgwsfc'])
    tp = float(point['perpwsfc'])
    dp = float(point['dirpwsfc'])

    return hs, tp, dp

if __name__ == '__main__':

    pathname = './'
    filename = 'puntos_analizar.csv'

    points, names, lat, lon = read_data_points(pathname, filename)

    url, mydate = create_url_nww3()

    ds = read_data_nww3(url)

    hs, tp, dp = np.array([find_wave_point(lat[i], lon[i]) for i in range(len(lon))]).T

    idx = np.where(np.isnan(hs)==False)[0]

    make2dplot(names[idx], hs[idx], tp[idx], mydate)
    # P = calculate_energy_flux(H=2, T=10)
    # print ("Energy Flux (kW/h): {}".format(P))

    #
