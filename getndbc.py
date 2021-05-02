'''
Open Realtime data from NDBC website and concatenate with
the existing file

date,WDIR,WSPD,GST,WVHT,DPD,APD,MWD,PRES,ATMP,WTMP,DEWP,VIS,PTDY,TIDE

'''

import matplotlib
matplotlib.use('Agg') #necessario para salvar figura no crontab
import os
import numpy as np
# from urllib.request import urlopen
from urllib import urlopen
import pandas as pd
import matplotlib.pyplot as plt

#pathname and station names
pathname = os.environ['HOME'] + '/Dropbox/database/NDBC/realtime/'

stations = [
            '32012', #pacifico - southwest peru
            '41002',
            '41013',
            '41025',
            # '41060',
            # '41114',
            # '42058',
            # '44020',
            # '46215',
            # '46229',
            # '51202'
            ]

for station in stations:

    print (station)

    #open realtime data
    url = 'http://www.ndbc.noaa.gov/data/realtime2/' + station + '.txt'
    data = urlopen(url).read().decode('utf-8')

    data = data.split('\n')

    #create dataframe
    df = pd.DataFrame()
    for line in data[2:]:
        df = pd.concat([df, pd.Series(line.split())], axis=1)
    df = df.T
    df.index = range(len(df))
    df.columns = ['YY'] + data[0].split()[1:]
    df['date'] = pd.to_datetime(df.YY+df.MM+df.DD+df.hh+df.mm, format='%Y%m%d%H%M')
    df = df.drop(['YY','DD','MM','hh','mm'], axis=1)
    df = df.set_index('date')
    df = df.replace('MM','NaN')
    df = df.astype(float)
    df = df.iloc[::-1][1:] #inverte - flipud e retira o primeio valor (nan)

    #feet to meters (WVHT)
    df.WVHT = df.WVHT #* 0.3048

    #load exist file
    old = pd.read_csv(pathname + 'NDBC_' + station + '.csv', sep=',', parse_dates=['date'], index_col=['date'])

    #concatenate new and old file
    df = pd.concat([old, df], axis=0)

    #remove duplicated lines
    df = df.drop_duplicates()

    #save new (concatated) file
    df.to_csv(pathname + 'NDBC_' + station + '.csv', na_rep='NaN')