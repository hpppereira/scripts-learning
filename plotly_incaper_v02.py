"""
plotar em linha todas as variaveis
se a variavel for  4d (tiver nivel),  plotar
todos os niveis na mesma figura

variaveis:
ugrd10m ** 10 m above ground u wind [m/s]
vgrd10m ** 10 m above ground v wind [m/s]
rh2m ** 2 m above ground Relative humidity [%]
tmp2m ** 2 m above ground Temp. [K]
prmslmsl ** mean-sea level Pressure reduced to MSL [Pa]
apcpsfc ** surface Total precipitation [kg/m^2]
tcdcclm ** atmos column Total cloud cover [%]
"""

import os
import xarray as xr
# import pandas as pd
import numpy as np

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot
# from plotly.graph_objs import Layout
import plotly.figure_factory as ff
from datetime import datetime

# ------------------------------------------------------------------ #
# Leitura do arquivo netCDF

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

vars_dict = {'rh2m':     ['Umidade Relativa', '%'],
             'tmp2m':    ['Temperatura a 2 m', 'gC'],
             'prmslmsl': ['Pressao Atmosferica', 'hPa'], 
             'apcpsfc':  ['Precipitacao', 'mm'], 
             'tcdcclm':  ['Nebulosidade', 'xx'], 
             # 'ugrd10m':  ['U vento', 'xx'],
             # 'vgrd10m':  ['V vento', 'xx'],
             'windspd':  ['Intensidade do Vento', 'm/s'],
             'winddir':  ['Direcao do Vento', 'graus']}

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
ds.drop(['ugrd10m', 'vgrd10m'])

# converte dataset para dataframe apenas com as variaveis de interesse
df = ds[vars_dict.keys()].to_dataframe()

# direcao entre a e 360
df.winddir[df.winddir<0] = df.winddir[df.winddir<0] + 360

# pega os ultimos  7 dias de previsao
df = df[-7*24:]

# moficia pressao para hPa
df['prmslmsl'] = df.prmslmsl / 100

titles = aa = tuple([vars_dict[vars_dict.keys()[i]][0] for i in range(len(vars_dict))])

fig = tools.make_subplots(rows=len(vars_dict), cols=1, shared_xaxes=True,
                          # subplot_titles=(titles),
                          vertical_spacing = .02)

fig['layout'].update(title='Cidade / Estado')
fig['layout'].update(height=1800, width=1250)
# fig['layout'].update(hovermode= 'closest')
fig['layout'].update(showlegend= False)


ll = 0
for v in vars_dict.keys():

    ll += 1

    # converte para dataframe
    # df = ds[v].to_dataframe()


    # date = df.index.to_series().values

    # stop
    # cria variavel de data
    # df['date'] = df.index

    xx = df.index
    yy = df[v]

    # ------------------------------------------------------------------ #


    # ------------------------------------------------------------------ #

    plott = go.Scatter(
        x = xx,
        y = yy,
        mode = 'lines',
        name = vars_dict[v][1]
        )

    # plot2 = go.Scatter(
    #    x = xx,
    #    y = yy,
    #    mode = 'lines',
    #    name = 'lines')

    fig.append_trace(plott, ll, 1)
    # fig.append_trace(plot2, 2, 1)

    fig['layout']['yaxis%s' %ll].update(title=titles[ll-1] + ' (%s)' %vars_dict[v][1])
    # fig['layout']['xaxis2'].update(title='xaxis 2 title')#, range=[10, 50])
    # fig['layout']['xaxis3'].update(title='xaxis 3 title', showgrid=False)
    # fig['layout']['xaxis4'].update(title='xaxis 4 title', type='log')
    # fig['layout']['yaxis1'].update(title='yaxis 1 title')
    # fig['layout']['yaxis2'].update(title='yaxis 2 title')#, range=[40, 80])
    # fig['layout']['yaxis3'].update(title='yaxis 3 title', showgrid=False)
    # fig['layout']['yaxis4'].update(title='yaxis 4 title')



# py.iplot(fig, filename='simple-subplot')

plot(fig, filename='teste.html')

#plotly.offline.plot({
#     "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
#     "layout": Layout(title="hello world")
#})


# ------------------------------------------------------------------ #





