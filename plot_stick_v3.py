# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 11:26:39 2016

@author: b3nd
"""
from plotly import tools
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.plotly as py
import plotly.figure_factory as ff
import numpy as np
from matplotlib.dates import date2num
import pandas as pd
import datetime
import xarray as xr


pathname = 'data/'
filename = 'wrf_d02_2018021700.nc'

# Leitura do arquivo com xarray
ds =  xr.open_dataset(pathname + filename)

# # vai vir da lista de cidades
lt=-20.29
ln=-40.31

# # df = df[-7*24:]
ds = ds.sel(latitude=float(lt),longitude=float(ln),method='nearest')

# lista de variaveis

vars_dict = {'rh2m':     ['Umid. Relativa', '%'],
             'tmp2m':    ['Temp. 2 m', 'ºC'],
             'prmslmsl': ['Pressão Atm.', 'hPa'], 
             'apcpsfc':  ['Precipitação', 'mm / mm/h'], 
             'tcdcclm':  ['Nebulosidade', '%'], 
             # 'ugrd10m':  ['U vento', 'xx'],
             # 'vgrd10m':  ['V vento', 'xx'],
             'windspd':  ['Int. Vento', 'm/s'],
             'winddir':  ['Dir. Vento', 'graus'],
             'hcdchcl':  ['Nuvem alta', '%'],
             'mcdcmcl':  ['Nuvem média', '%'],
             'lcdclcl':  ['Nuvem baixa', '%']}

vv = ['windspd', 'prmslmsl', 'tmp2m', 'rh2m', 'tcdcclm', 'apcpsfc']

# ds1 = ds[['']]


# df = df.set_index('time')

# stop
# stop

# ------------------------------------------------------------------ #
# converte u e v para vel e dir

u_ms = ds['ugrd10m'].data
v_ms = ds['vgrd10m'].data

wind_abs = np.sqrt(u_ms**2 + v_ms**2)
wind_dir_trig_to = np.arctan2(u_ms/wind_abs, v_ms/wind_abs) 
wind_dir_trig_to_degrees = wind_dir_trig_to * 180/np.pi ## -111.6 degrees

# convert this wind vector to the meteorological convention of the direction the wind is coming from:
wind_dir_trig_from_degrees = wind_dir_trig_to_degrees + 180 ## 68.38 degrees

# convert that angle from "trig" coordinates to cardinal coordinates:
wind_dir_cardinal = 90 - wind_dir_trig_from_degrees

# coloca no dataset
ds['windspd'] = (('time'),wind_abs)
ds['windspd'].attrs['long_name'] = '** 10 m above ground wind speed [m/s]'

ds['winddir'] = (('time'), wind_dir_cardinal)
ds['winddir'].attrs['long_name'] = '** 10 m above ground wind direction [degrees]'


# ------------------------------------------------------------------ #

# remove as colunas de U e V
# ds.drop(['ugrd10m', 'vgrd10m'])

# converte dataset para dataframe apenas com as variaveis de interesse
df = ds[vars_dict.keys()].to_dataframe()

# direcao entre a e 360
df.winddir[df.winddir<0] = df.winddir[df.winddir<0] + 360

# pega os ultimos  7 dias de previsao
df = df[-7*24:]

# ------------------------------------------------------------------ #



def to_unix_time(dt):
    epoch =  datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000

# dateparse = lambda x: pd.datetime.strptime(x, '%Y %m %d %H')
# df = pd.read_csv('serie_dados_teste.csv', sep=';', parse_dates={'datetime': ['Year','Month','Day','Hour']}, date_parser=dateparse, index_col = 0)

gust=df.windspd
vvel=df.windspd
vdir=df.winddir
#dtime = [data.to_pydatetime() for data in df.index]
dtime = [data.to_pydatetime().strftime("%b %d") for data in df.index]
#datam=date2num(dtime)
uv=-vvel*np.sin(np.deg2rad(vdir))
vv=-vvel*np.cos(np.deg2rad(vdir))


ymin=0; ymax=np.ceil(max(gust)/0.85) # limites de plotagem
uvnorm=uv[:]/vvel[:]
vvnorm=vv[:]/vvel[:]


fig = ff.create_quiver(np.arange(len(df.index)), 
                       vvel.values-0.065*ymax, 
                       uvnorm.values,
                       vvnorm.values, 
                       scale=1.3, 
                       arrow_scale=.5,
                       line=dict(width=1) )
lines = go.Scatter(
    x = np.arange(len(df.index)),
    y = df['windspd'],
    mode = 'lines',
    name = 'm/s',
    marker = dict(size=10, color = 'rgb(60,60,60)',
                line = dict(width=2, color='rgb(60,60,60'))
    )
fig['data'].append(lines)


# -- Altera o x-stick colocando a data --

custom_xaxis = go.XAxis(
    title="2016",
    range = np.arange(0,len(df.index),24),
    showgrid=True,
    showline=True,
    ticks="", 
    showticklabels=True,
    mirror=True,
    linewidth=2,
    ticktext=dtime[0::24],
    tickvals=np.arange(0,len(df.index),24)
)


layout = go.Layout(
    title="Stick Plot no Plotly",
    autosize=False,
    width=1100,
    height=400,
#    margin=go.Margin(
#        l=50,
#        r=50,
#        b=100,
#        t=100,
#        pad=4
#    ),
#    paper_bgcolor='#7f7f7f',
#    plot_bgcolor='#c7c7c7'
#    xaxis=dict(
#           tickvals=[np.arange(len(df.index))],
#           ticktext=[dtime]
#           ),
    xaxis=custom_xaxis
)




#layout = go.Layout(xaxis = dict(
#                   range = [to_unix_time(datetime.datetime(2013, 10, 17)),
#                            to_unix_time(datetime.datetime(2013, 11, 20))]
#    ))

fig = go.Figure(data=fig['data'], layout=layout)

plot(fig, filename='index.html', show_link=False)

