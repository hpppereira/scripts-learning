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

def to_unix_time(dt):
    epoch =  datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000

dateparse = lambda x: pd.datetime.strptime(x, '%Y %m %d %H')
df = pd.read_csv('serie_dados_teste.csv', sep=';', parse_dates={'datetime': ['Year','Month','Day','Hour']}, date_parser=dateparse, index_col = 0)

gust=df.gust
vvel=df.wspd
vdir=df.wdir
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
                       line=dict(width=1) )
#figure['data'].append(quiver)   # Plota no mesmo subplot

lines = go.Scatter(
    #x = df.index,
    x = np.arange(len(df.index)),
    y = df['wspd'],
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


# --- PLOTA GRAFICO 2
lines1 = go.Scatter(
    x = df.index,
    y = df['gust'],
    xaxis='x2',
    yaxis='y2',
    mode = 'lines',
    name = 'm/s',    
    marker = dict(size=10, color = 'rgb(60,60,60)',
                line = dict(width=2, color='rgb(60,60,60'))
    )
figure['data'].extend(go.Data([lines1])) # Cria um novo cubplot


# --- PLOTA GRAFICO 3
lines2 = go.Scatter(
    x = df.index,
    y = df['wdir'],
    xaxis='x3',
    yaxis='y3',
    mode = 'lines',
    #fill='tozeroy',
    #mode= 'none',
    name = 'm/s',    
    marker = dict(size=10, color = 'rgb(60,60,60)',
                line = dict(width=2, color='rgb(60,60,60'))
    )
figure['data'].extend(go.Data([lines2])) # Cria um novo cubplot



# Edit layout for subplots


figure.layout.yaxis.update({'domain': [0.0, 0.25]})
figure.layout.yaxis2.update({'domain': [0.32, 0.65]})
figure.layout.yaxis3.update({'domain': [0.70, 0.90]})

# The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
figure.layout.yaxis.update({'anchor': 'x1',"zeroline":False,"showline":True})
figure.layout.xaxis.update({'anchor': 'y1',"zeroline":False,"showline":True})
figure.layout.xaxis.update(custom_xaxis)

figure.layout.yaxis.update({'title': '(m/s)'})

figure.layout.yaxis2.update({'anchor': 'x2'})
figure.layout.xaxis2.update({'anchor': 'y2'})
figure.layout.yaxis2.update({'title': '(m/s)'})


figure.layout.yaxis3.update({'anchor': 'x3',"zeroline":False,"showline":True})
figure.layout.xaxis3.update({'anchor': 'y3',"showline":True})
figure.layout.yaxis3.update({'title': '(m/s)'})

# Update the margins to add a title and see graph x-labels. 
figure.layout.margin.update({'t':75, 'l':50})
figure.layout.update({'title': '2016 Hockey Stats'})
# Update the height because adding a graph vertically will interact with
# the plot height calculated for the table
figure.layout.update({'height':750})
figure.layout.update({'showlegend':False})


figure.layout.annotations.update({'x':0.5,
                                  'y':0.5,
                                  'showarrow':False,
                                  'text':'Custom x-axis title',
                                  'xref':'paper',
                                  'yref':'paper'
                                  })




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

#fig = go.Figure(data=fig['data'], layout=layout)

plot(figure, filename='index.html', show_link=False)

