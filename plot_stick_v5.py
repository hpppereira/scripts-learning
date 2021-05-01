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

def to_unix_time(dt):
    epoch =  datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000

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
             'tmp2m':    ['Temp. 2 m', 'gC'],
             'prmslmsl': ['Pressao Atm.', 'hPa'], 
             'apcpsfc':  ['Precipitacao', 'mm'], 
             'tcdcclm':  ['Nebulosidade', '%'], 
             'ugrd10m':  ['U vento', 'xx'],
             'vgrd10m':  ['V vento', 'xx'],
             'windspd':  ['Int. Vento', 'm/s'],
             'winddir':  ['Dir. Vento', 'graus'],
             'hcdchcl':  ['Nuvem alta', '%'],
             'mcdcmcl':  ['Nuvem media', '%'],
             'lcdclcl':  ['Nuvem baixa', '%']}

# vv = ['windspd', 'winddir', 'prmslmsl', 'tmp2m', 'rh2m', 'tcdcclm', 'apcpsfc']

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

df = ds[vars_dict.keys()].to_dataframe()

df = df[-7*24:]

df['prmslmsl'] = df.prmslmsl / 100

# kelvin para celsius
df['tmp2m'] = df['tmp2m'] -273.15

df['precinst'] = df.apcpsfc.diff()
df.precinst[df.precinst<0] = 0

# dateparse = lambda x: pd.datetime.strptime(x, '%Y %m %d %H')
# df = pd.read_csv('serie_dados_teste.csv', sep=';', parse_dates={'datetime': ['Year','Month','Day','Hour']}, date_parser=dateparse, index_col = 0)

gust=df.windspd
vvel=df.windspd
vdir=df.winddir
#dtime = [data.to_pydatetime() for data in df.index]

#datam=date2num(dtime)
uv=-vvel*np.sin(np.deg2rad(vdir))
vv=-vvel*np.cos(np.deg2rad(vdir))


ymin=0; ymax=np.ceil(max(gust)/0.85) # limites de plotagem
uvnorm=uv[:]/vvel[:]
vvnorm=vv[:]/vvel[:]

# --- PLOTA QUIVER E LINHA ---
figure = ff.create_quiver(np.arange(len(df.index)), 
                       vvel.values-0.065*ymax, 
                       uvnorm.values,
                       vvnorm.values, 
                       scale=1.3, 
                       arrow_scale=.5,
                       line=dict(width=1),
                       name='')
#figure['data'].append(quiver)   # Plota no mesmo subplot

lines = go.Scatter(
    #x = df.index,
    x = np.arange(len(df.index)),
    y = df['windspd'],
    xaxis='x1',
    yaxis='y1',
    mode = 'lines',
    name = 'm/s',
    marker = dict(size=10, color = 'rgb(60,60,60)',
                line = dict(width=2, color='rgb(60,60,60'))
    ) 
#figure = go.Figure(data=[lines])
figure['data'].append(lines)   # Plota no mesmo subplot

# -- Altera o x-stick do Quiver colocando a data --
dtime = [data.to_pydatetime().strftime("%b %d") for data in df.index[df.index.hour==0]]
dtime_vals = df.reset_index().index[df.index.hour==0]

custom_xaxis = {"range":np.arange(0,len(df.index),24),
                "showgrid":True,
                #"showline":True,
                #"ticks":"", 
                "showticklabels":True,
                #"mirror":True,
                "linewidth":2,
                "ticktext":dtime,
                "tickvals":dtime_vals,
                #"tickmode":"auto"
                }


# --- PLOTA GRAFICO 2 - Presso atm.
lines1 = go.Scatter(
    x = df.index,
    y = df['prmslmsl'],
    xaxis='x2',
    yaxis='y2',
    mode = 'lines',
    name = 'hPa',    
    marker = dict(size=10, color = 'rgb(60,60,60)',
                line = dict(width=2, color='rgb(60,60,60'))
    )
figure['data'].extend(go.Data([lines1])) # Cria um novo cubplot


# --- PLOTA GRAFICO 3 - temperatura
lines2 = go.Scatter(
    x = df.index,
    y = df['tmp2m'],
    xaxis='x3',
    yaxis='y3',
    mode = 'lines',
    #fill='tozeroy',
    #mode= 'none',
    name = 'ºC',    
    marker = dict(size=10, color = 'rgb(60,60,60)',
                line = dict(width=2, color='rgb(60,60,60'))
    )
figure['data'].extend(go.Data([lines2])) # Cria um novo cubplot


# --- PLOTA GRAFICO 4 - umidade relativa
lines3 = go.Scatter(
    x = df.index,
    y = df['rh2m'],
    xaxis='x4',
    yaxis='y4',
    mode = 'lines',
    #fill='tozeroy',
    #mode= 'none',
    name = '%',    
    marker = dict(size=10, color = 'rgb(60,60,60)',
                line = dict(width=2, color='rgb(60,60,60'))
    )
figure['data'].extend(go.Data([lines3])) # Cria um novo cubplot



# --- PLOTA GRAFICO 5 - nuvem

alta = df['hcdchcl'].resample('6H').max()
media = df['mcdcmcl'].resample('6H').max()
baixa = df['lcdclcl'].resample('6H').max()

# Create traces
trace0 = go.Bar(
    x = alta.index,
    y = alta,
    xaxis='x5',
    yaxis='y5',
      # mode = 'lines',
    name = '% - Alta',
    # marker = dict(size=10, color = 'rgb(60,60,60)',
    #               line = dict(width=2, color='rgb(60,60,60'))
)

trace1 = go.Bar(
    x = media.index,
    y = media,
    xaxis='x5',
    yaxis='y5',
  # text = 'aaa',
    # mode = 'lines',
    name = '% Media',
    # marker = dict(size=10, color = 'rgb(120,120,120)',
    #               line = dict(width=2, color='rgb(120,120,120'))
)

trace2 = go.Bar(
    x = baixa.index,
    y = baixa,
    xaxis='x5',
    yaxis='y5',
      # mode = 'lines',
    name = '% - Baixa',
    # marker = dict(size=10, color = 'rgb(180,180,180)',
    #               line = dict(width=2, color='rgb(180,180,180)'))
)

  
data = [trace0, trace1, trace2]

figure['data'].extend(go.Data(data)) # Cria um novo cubplot


# --- PLOTA GRAFICO 6 - precipitacao


trace0 = go.Bar(
     x = df.index,
     y = df['precinst'],
     xaxis='x6',
     yaxis='y6',
     # mode = 'lines',
     name = 'mm/h - Inst.',
     # xaxis=df.index,
     marker=dict(color='rgb(26, 118, 255)')
     )

trace1 = go.Scatter(
    x = df.index,
    y = df['apcpsfc'],
    xaxis='x6',
    yaxis='y6',
    mode = 'lines',
    name = 'mm - Acum.')


data = [trace0, trace1]

figure['data'].extend(go.Data(data)) # Cria um novo cubplot


# Edit layout for subplots

figure.layout.xaxis.update({'anchor': 'y1',"zeroline":False,"showline":True})
figure.layout.xaxis.update(custom_xaxis)

# stick plot - vel e dir vento
# The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
figure.layout.yaxis.update({'anchor': 'x1',"zeroline":False,"showline":True})
figure.layout.yaxis.update({'domain': [0, 0.16]})
figure.layout.yaxis.update({'title': 'Int. Dir. Vento (m/s)'})

# pressao atm
figure.layout.yaxis2.update({'anchor': 'x2'})
figure.layout.xaxis2.update({'anchor': 'y2'})
figure.layout.yaxis2.update({'domain': [0.18, 0.34]})
figure.layout.yaxis2.update({'title': 'Pressão Atm. (hPa)'})

# temp. 2 m
figure.layout.yaxis3.update({'domain': [0.36, 0.50]})
figure.layout.yaxis3.update({'anchor': 'x3',"zeroline":False,"showline":True})
figure.layout.xaxis3.update({'anchor': 'y3',"showline":True})
figure.layout.yaxis3.update({'title': 'Temp. 2 m (ºC)'})

# umidade relativa
figure.layout.yaxis4.update({'domain': [0.52, 0.66]})
figure.layout.yaxis4.update({'anchor': 'x4',"zeroline":False,"showline":True})
figure.layout.xaxis4.update({'anchor': 'y4',"showline":True})
figure.layout.yaxis4.update({'title': 'Umid. Rel. (%)'})

# nebulosidade
figure.layout.yaxis5.update({'domain': [0.7, 0.83]})
figure.layout.yaxis5.update({'anchor': 'x5',"zeroline":False,"showline":True})
figure.layout.xaxis5.update({'anchor': 'y5',"showline":True})
figure.layout.yaxis5.update({'title': 'Nebulosidade (%)'})

# precipitacao
figure.layout.yaxis6.update({'domain': [0.87, 1]})
figure.layout.yaxis6.update({'anchor': 'x6',"zeroline":False,"showline":True})
figure.layout.xaxis6.update({'anchor': 'y6',"showline":True})
figure.layout.yaxis6.update({'title': 'Precipitação (mm / mm/h)'})


# Update the margins to add a title and see graph x-labels. 
figure.layout.margin.update({'t':75, 'l':50})
figure.layout.update({'title': 'Cidade / Estado'})

# Update the height because adding a graph vertically will interact with
# the plot height calculated for the table
figure.layout.update({'height':1300})
figure.layout.update({'showlegend':False})


figure.layout.annotations.update({'x':0.5,
                                  'y':0.5,
                                  'showarrow':False,
                                  'text':'Custom x-axis title',
                                  'xref':'paper',
                                  'yref':'paper'
                                  })




# layout = go.Layout(
#     title="Stick Plot no Plotly",
#     autosize=False,
#     width=1100,
#     height=400,
# #    margin=go.Margin(
# #        l=50,
# #        r=50,
# #        b=100,
# #        t=100,
# #        pad=4
# #    ),
# #    paper_bgcolor='#7f7f7f',
# #    plot_bgcolor='#c7c7c7'
# #    xaxis=dict(
# #           tickvals=[np.arange(len(df.index))],
# #           ticktext=[dtime]
# #           ),
#     xaxis=custom_xaxis
# )


#layout = go.Layout(xaxis = dict(
#                   range = [to_unix_time(datetime.datetime(2013, 10, 17)),
#                            to_unix_time(datetime.datetime(2013, 11, 20))]
#    ))

#fig = go.Figure(data=fig['data'], layout=layout)

plot(figure, filename='index.html', show_link=False)

