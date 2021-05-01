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
from plotly.graph_objs import Layout
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

# ds1 = ds[['']]

df = ds.to_dataframe()
# df = df.set_index('time')

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

# lista de variaveis
list_vars = ['rh2m', #umidade relativa
             'tmp2m', # temperatura
             'prmslmsl', # pressao atm
             'apcpsfc', # precipitacao
             'tcdcclm', #nebulosidade
             'ugrd10m', #U wind
             'vgrd10m', #V wind
             'windspd', # wind speed
             'winddir'] # wind direction


# converte para dataframe
df = ds[list_vars].to_dataframe()

df = df[-7*24:]

# date = df.index.to_series().values

# stop
# cria variavel de data
# df['date'] = df.index

xx = df.index
yy = df.rh2m

# ------------------------------------------------------------------ #


# ------------------------------------------------------------------ #

plot1 = go.Scatter(
    x = xx,
    y = yy,
    mode = 'lines',
    name = 'lines')

plot2 = go.Scatter(
   x = xx,
   y = yy,
   mode = 'lines',
   name = 'lines')

# fig = ff.create_quiver(np.arange(len(df)), np.ones(len(df)), df.ugrd10m, df.ugrd10m)
# fig = ff.create_quiver(ds.time.values[:len(df)], np.ones(len(df)), df.ugrd10m, df.ugrd10m)
# fig = ff.create_quiver(np.array(a), np.ones(len(a)), b, b)
# fig = ff.create_quiver(date.astype(str), np.ones(len(date)).astype(str), df.ugrd10m, df.ugrd10m)

fig = tools.make_subplots(rows=2, cols=1,  shared_xaxes=True)

fig.append_trace(plot1, 1, 1)
fig.append_trace(plot2, 2, 1)


fig['layout'].update(height=600, width=800, title='i <3 subplots')

layout = Layout(images=[dict(
       source="https://www.atmosmarine.com/wp-content/uploads/2016/08/logo-atmosmarine.png",
       xref="paper", yref="paper",
       x=0.1, y=1.05,
       sizex=0.4, sizey=0.4,
       xanchor="center", yanchor="bottom"
     )])



# py.iplot(fig, filename='simple-subplot')

plot(fig, filename='teste.html')

#plotly.offline.plot({
#     "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
#     "layout": Layout(title="hello world")
#})




# ------------------------------------------------------------------ #





