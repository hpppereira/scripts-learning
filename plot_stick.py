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


dateparse = lambda x: pd.datetime.strptime(x, '%Y %m %d %H')
df = pd.read_csv('serie_dados_teste.csv', sep=';', parse_dates={'datetime': ['Year','Month','Day','Hour']}, date_parser=dateparse, index_col = 0)

gust=df.gust
vvel=df.wspd
vdir=df.wdir
datam=date2num([data.to_datetime() for data in df.index])
uv=-vvel*np.sin(np.deg2rad(vdir))
vv=-vvel*np.cos(np.deg2rad(vdir))


ymin=0; ymax=np.ceil(max(gust)/0.85) # limites de plotagem
uvnorm=uv[:]/vvel[:]
vvnorm=vv[:]/vvel[:]


layout = go.Layout(
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
)


fig = ff.create_quiver(np.arange(len(df.index)), 
                       vvel.values-0.065*ymax, 
                       uvnorm.values,
                       vvnorm.values, 
                       scale=1.3, 
                       arrow_scale=.5,
                       line=dict(width=1) )
data = fig


lines = go.Scatter(
    x = np.arange(len(df.index)),
    y = df['wspd'],
    mode = 'lines',
    name = 'm/s',
    marker = dict(size=10, color = 'rgb(60,60,60)',
                line = dict(width=2, color='rgb(60,60,60'))
    )

fig['data'].append(lines)

fig = go.Figure(data=fig['data'], layout=layout)


# -- Altera o x-stick colocando a data --
#layout = go.Layout(xaxis = dict(
#                   range = [to_unix_time(datetime.datetime(2013, 10, 17)),
#                            to_unix_time(datetime.datetime(2013, 11, 20))]
#    ))


plot(fig, filename='index.html', show_link=False)

