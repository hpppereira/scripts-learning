# -*- coding: utf-8 -*-


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
from plotly.graph_objs import *
import pandas as pd
from plotly import tools
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.plotly as py
import plotly.figure_factory as ff
import numpy as np
from matplotlib.dates import date2num
import pandas as pd
import datetime

def to_unix_time(dt):
  epoch =  datetime.datetime.utcfromtimestamp(0)
  return (dt - epoch).total_seconds() * 1000

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

vars_dict = {'rh2m':     ['Umid. Relativa', '%'],
             'tmp2m':    ['Temp. 2 m', 'ºC'],
             'prmslmsl': ['Pressão Atm.', 'hPa'], 
             'apcpsfc':  ['Precipitação', 'mm / mm/h'], 
             'tcdcclm':  ['Nebulosidade', '%'], 
             'ugrd10m':  ['U vento', 'xx'],
             'vgrd10m':  ['V vento', 'xx'],
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
#ds.drop(['ugrd10m', 'vgrd10m'])

# converte dataset para dataframe apenas com as variaveis de interesse
df = ds[vars_dict.keys()].to_dataframe()

# direcao entre a e 360
df.winddir[df.winddir<0] = df.winddir[df.winddir<0] + 360

# pega os ultimos  7 dias de previsao
df = df[-7*24:]

# ------------------------------------------------------------------ #
# calculo da precipitacao instantanea

df['precinst'] = df.apcpsfc.diff()
df.precinst[df.precinst<0] = 0

# ------------------------------------------------------------------ #
# moficia pressao para hPa
df['prmslmsl'] = df.prmslmsl / 100

# ------------------------------------------------------------------ #

titles = tuple([vars_dict[vv[i]][0] for i in range(len(vv))])

fig = tools.make_subplots(rows=len(vars_dict), cols=1, shared_xaxes=False,
                          # subplot_titles=(titles),
                          vertical_spacing = .02)

fig['layout'].update(title='Cidade / Estado')
# fig['layout'].update(height=1800, width=1000, margin=go.Margin(
        # l=300,
        # r=50,
        # b=100,
        # t=100,
        # pad=4
        # ))
fig['layout'].update(height=1850, width=1100)
fig['layout'].update(hovermode= 'closest')
fig['layout'].update(showlegend=False)

ll = 0
# for v in vars_dict.keys():
for v in vv:

    ll += 1

    if v == 'windspd':


      # dateparse = lambda x: pd.datetime.strptime(x, '%Y %m %d %H')
      # df = pd.read_csv('serie_dados_teste.csv', sep=';', parse_dates={'datetime': ['Year','Month','Day','Hour']}, date_parser=dateparse, index_col = 0)

      gust=df.windspd
      vvel=df.windspd
      vdir=df.winddir
      #dtime = [data.to_pydatetime() for data in df.index]
      dtime = [data.to_pydatetime().strftime("%b %d") for data in df.index]
      #datam=date2num(dtime)
      # uv=-vvel*np.sin(np.deg2rad(vdir))
      # vv=-vvel*np.cos(np.deg2rad(vdir))

      ymin=0; ymax=np.ceil(max(gust)/0.85) # limites de plotagem
      uvnorm=df['ugrd10m'].values/df.windspd[:]
      vvnorm=df['vgrd10m'].values/df.windspd[:]


      # fig.append_trace(trace0, ll, 1)
      quiver = ff.create_quiver(np.arange(len(df.index)), 
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
      quiver['data'].append(lines)


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
          xaxis=custom_xaxis
      )


      layout = go.Layout(xaxis = dict(
                        range = [to_unix_time(datetime.datetime(2013, 10, 17)),
                                 to_unix_time(datetime.datetime(2013, 11, 20))]
         ))

      # fig.append_trace(quiver['data'], ll, 1)

#      quiver['data'][0].append(layout)
#      quiver['layout']['xaxis'] = layout['xaxis']
 
    # plot(quiver['data'], filename='index1.html', show_link=False)


      for i in range(len(quiver.data)):
          quiver.data[i].xaxis='x1'
          quiver.data[i].yaxis='y1'

      quiver.layout.xaxis1.update({'anchor': 'y1'})
      quiver.layout.yaxis1.update({'anchor': 'x1', 'domain': [.55, 1]})

      #for i in range(len(fig2.data)):
      #    fig2.data[i].xaxis='x2'
      #    fig2.data[i].yaxis='y2'

      #fig2.layout.xaxis2.update({'anchor': 'y2'})
      #fig2.layout.yaxis2.update({'anchor': 'x2', 'domain': [0, .45]})


      #stop
      fig.append_trace(quiver, ll, 1)

    if v == 'tcdcclm': #nebulosidade

      alta = df['hcdchcl'].resample('6H').max()
      media = df['mcdcmcl'].resample('6H').max()
      baixa = df['lcdclcl'].resample('6H').max()

      # Create traces
      trace0 = go.Bar(
          x = alta.index,
          y = alta,
          # mode = 'lines',
          name = '% - Alta',
          # marker = dict(size=10, color = 'rgb(60,60,60)',
          #               line = dict(width=2, color='rgb(60,60,60'))
      )

      trace1 = go.Bar(
          x = media.index,
          y = media,
          # text = 'aaa',
          # mode = 'lines',
          name = '% Media',
          # marker = dict(size=10, color = 'rgb(120,120,120)',
          #               line = dict(width=2, color='rgb(120,120,120'))
      )

      trace2 = go.Bar(
          x = baixa.index,
          y = baixa,
          # mode = 'lines',
          name = '% - Baixa',
          # marker = dict(size=10, color = 'rgb(180,180,180)',
          #               line = dict(width=2, color='rgb(180,180,180)'))
      )

      data = [trace0, trace1, trace2]

      fig.append_trace(trace0, ll, 1)
      fig.append_trace(trace1, ll, 1)
      fig.append_trace(trace2, ll, 1)

      # fig['layout'].update(showlegend=True)
      # fig['layout']['yaxis%s' %ll].update(title=titles[ll-1] + ' (%s)' %vars_dict[v][1], tickformat=".2f")
      fig['layout']['yaxis%s' %ll].update(title=titles[ll-1], tickformat=".2f")

    # ------------------------------------------------------------------ #

    elif v == 'apcpsfc': 

      trace0 = go.Bar(
           x = df.index,
           y = df['precinst'],
           # mode = 'lines',
           name = 'mm/h - Inst.',
           xaxis=df.index,
           marker=dict(color='rgb(26, 118, 255)')
           )

      trace1 = go.Scatter(
          x = df.index,
          y = df['apcpsfc'],
          mode = 'lines',
          name = 'mm - Acum.')

      fig.append_trace(trace0, ll, 1)
      fig.append_trace(trace1, ll, 1)

      # fig['layout']['yaxis%s' %ll].update(title=titles[ll-1] + ' (%s)' %vars_dict[v][1], tickformat=".2f")
      fig['layout']['yaxis%s' %ll].update(title=titles[ll-1], tickformat=".2f")

    # ------------------------------------------------------------------ #


    else:

      plott = go.Scatter(
          x = df.index,
          y = df[v],
          mode = 'lines',
          name = vars_dict[v][1],
          xaxis=df.index
          )

      # plot2 = go.Scatter(
      #    x = xx,
      #    y = yy,
      #    mode = 'lines',
      #    name = 'lines')

      fig.append_trace(plott, ll, 1)
      # fig.append_trace(plot2, 2, 1)

      # fig['layout']['yaxis%s' %ll].update(title=titles[ll-1] + ' (%s)' %vars_dict[v][1], tickformat=".2f")
      fig['layout']['yaxis%s' %ll].update(title=titles[ll-1], tickformat=".2f")
      # fig['layout']['yaxis%s' %ll].update(title=titles[ll-1] + ' (%s)' %vars_dict[v][1])
      # fig['layout']['xaxis2'].update(title='xaxis 2 title')#, range=[10, 50])
      # fig['layout']['xaxis3'].update(title='xaxis 3 title', showgrid=False)
      # fig['layout']['xaxis4'].update(title='xaxis 4 title', type='log')
      # fig['layout']['yaxis1'].update(title='yaxis 1 title')
      # fig['layout']['yaxis2'].update(title='yaxis 2 title')#, range=[40, 80])
      # fig['layout']['yaxis3'].update(title='yaxis 3 title', showgrid=False)
      # fig['layout']['yaxis4'].update(title='yaxis 4 title')
      # fig['layout']['yaxis4'].update(showlegend=True)
      fig['data'][0]['showlegend']=True




# py.iplot(fig, filename='simple-subplot')

# config={'showLink': False}

plot(fig, filename='index.html', show_link=False)

#plotly.offline.plot({
#     "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
#     "layout": Layout(title="hello world")
#})


# ------------------------------------------------------------------ #





