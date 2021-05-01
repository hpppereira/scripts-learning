"""
Gera HTML para as boias BMOBR da REMO
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotly import tools
import plotly.graph_objs as go
from plotly.offline import plot


# --------------------------------------------------------------------------------------------- #

def make_figs(station, vars_dict, html_name):


	"""
	fig = fig object plotly
	vars_dics = structure with var name, xlabel and unit
	html_name = output filename with .html
	"""	

	titles = tuple([vars_dict[vars_dict.keys()[i]][0] for i in range(len(vars_dict))])

	fig = tools.make_subplots(rows=len(vars_dict), cols=1, shared_xaxes=True,
	                          vertical_spacing = .02)

	fig['layout'].update(title=station)
	fig['layout'].update(height=1800, width=1250)
	fig['layout'].update(showlegend= False)

	ll = 0
	for v in vars_dict.keys():

	    ll += 1

	    xx = df.index
	    yy = df[v]

	    plott = go.Scatter(
	        x = xx,
	        y = yy,
	        mode = 'lines',
	        name = vars_dict[v][1]
	        )

	    fig.append_trace(plott, ll, 1)

	    fig['layout']['yaxis%s' %ll].update(title=titles[ll-1] + ' (%s)' %vars_dict[v][1])

	plot(fig, filename=html_name)

# --------------------------------------------------------------------------------------------- #
## CF01_201503_BMOBR03

pathname = os.environ['HOME'] + '/Dropbox/BMOP/Processamento/data/CF01_201503_BMOP03/telemetria/'
filename = 'CF01_201503_BMOP03.csv'

dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%Y %H:%M:%S')

df = pd.read_csv(pathname + filename, header=0,
                 parse_dates=['ExprDataHoraBMOP'],
                 date_parser=dateparse,
                 index_col=['ExprDataHoraBMOP'])

df = df[:'2015-05']

cf01_201503 = {'velocidadeVento': ['Intensidade do Vento', 'm/s'],
               'direcaoVento':    ['Direcao do Vento', 'graus'],
		       'umidadeRelativa': ['Umidade Relativa', '%'],
               'temperaturaAr':   ['Temperatura do Ar', 'gC'],
               'pressao':         ['Pressao Atmosferica', 'hPa'], 
               'alturaOnda':      ['Altura Significativa', 'm'], 
               'periodoPico':     ['Periodo de Pico', 'seg'], 
               'direcaoPico':     ['Direcao de Pico', 'graus']}			 

make_figs('CF01 - Mar/2015', cf01_201503, 'cf01_201503_graphs.html')

df.to_html('cf01_201503_table.html')

# --------------------------------------------------------------------------------------------- #
## CF01_201602_BMOBR03

pathname = os.environ['HOME'] + '/Dropbox/BMOP/Processamento/data/CF01_201602_BMOP05/telemetria/'
filename = 'CF01_201602_BMOP05.csv'

#carrega os dados da boia
df = pd.read_csv(pathname + filename, index_col='date', parse_dates=True)

#pega dados quando a boia foi para agua
df = df['2016-03':'2016-05']

# retira valores negativos
df.ate[df.ate<0] = np.nan
df.rh[df.rh<0] = np.nan

cf01_201602 = {'ws': ['Intensidade do Vento', 'm/s'],
               'wd':    ['Direcao do Vento', 'graus'],
		       'rh': ['Umidade Relativa', '%'],
               'ate':   ['Temperatura do Ar', 'gC'],
               'bp':         ['Pressao Atmosferica', 'hPa'], 
               'hs':      ['Altura Significativa', 'm'], 
               'tp':     ['Periodo de Pico', 'seg'], 
               'dp':     ['Direcao de Pico', 'graus']}			 

make_figs('CF01 - Fev/2016', cf01_201602, 'cf01_201602_graphs.html')

df.to_html('cf01_201602_table.html')

# --------------------------------------------------------------------------------------------- #
## CF01_201611_BMOBR05

pathname = os.environ['HOME'] + '/Dropbox/BMOP/Processamento/data/CF01_201611_BMOP05/telemetria/'
filename = 'CF01_201611_BMOP05.csv'

#carrega os dados da boia
df = pd.read_csv(pathname + filename, index_col='date', parse_dates=True)


cf01_201611 = {'ws': ['Intensidade do Vento', 'm/s'],
               'wd':    ['Direcao do Vento', 'graus'],
		       'rh': ['Umidade Relativa', '%'],
               'ate':   ['Temperatura do Ar', 'gC'],
               'bp':         ['Pressao Atmosferica', 'hPa'], 
               'hs':      ['Altura Significativa', 'm'], 
               'tp':     ['Periodo de Pico', 'seg'], 
               'dp':     ['Direcao de Pico', 'graus']}			 

make_figs('CF01 - Nov/2016', cf01_201611, 'cf01_201611_graphs.html')

df.to_html('cf01_201511_table.html')

# --------------------------------------------------------------------------------------------- #
## CF03_201606_BMOBR06

pathname = os.environ['HOME'] + '/Dropbox/BMOP/Processamento/data/CF03_201606_BMOP06/telemetria/'
filename = 'CF03_201606_BMOP06.csv'

#carrega os dados da boia
df = pd.read_csv(pathname + filename, index_col='date', parse_dates=True)

cf03_201606 = {'ws': ['Intensidade do Vento', 'm/s'],
               'wd':    ['Direcao do Vento', 'graus'],
		       'rh': ['Umidade Relativa', '%'],
               'ate':   ['Temperatura do Ar', 'gC'],
               'bp':         ['Pressao Atmosferica', 'hPa'], 
               'hs':      ['Altura Significativa', 'm'], 
               'tp':     ['Periodo de Pico', 'seg'], 
               'dp':     ['Direcao de Pico', 'graus']}			 

make_figs('CF03 - Jun/2016', cf03_201606, 'cf03_201606_graphs.html')

df.to_html('cf03_201606_table.html')
