"""
To run: bokeh serve main.py

    # plotar em linha todas as variaveis
    # se a variavel for  4d (tiver nivel),  plotar
    # todos os niveis na mesma figura

"""


# from os.path import join, dirname
# import datetime

# import pandas as pd
# from scipy.signal import savgol_filter

# from bokeh.io import curdoc
# from bokeh.layouts import row, column
# from bokeh.models import ColumnDataSource, DataRange1d, Select
# from bokeh.palettes import Blues4
# from bokeh.plotting import figure
# from bokeh.io import output_file, show


import os
import xarray as xr
# import pandas as pd
from bokeh.plotting import figure
from bokeh.io import output_file, show, curdoc
# from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot, row, column
# from bokeh.models import ColumnDataSource, CDSView, BooleanFilter
# import pandas as pd
# import bokeh.plotting as bp
from bokeh.models import HoverTool, DatetimeTickFormatter, ColumnDataSource, Select

# ------------------------------------------------------------------ #

output_file("incaper.html")


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
ds = ds.sel(latitude=float(lt),longitude=float(ln),levels=2,method='nearest')

# # converte para dataframe
df = ds.to_dataframe()

# # lista de variaveis
list_vars = df.columns


# # cria variavel de data
df['date'] = df.index

# # cria columns datasource
dsource = ColumnDataSource(data=df)

# # lista de figuras
# figures = []

# # varia as variaveis
# for v in list_vars:

#     # tira o unicode
#     v = v.encode()

#     print ('Variavel: %s' %v)

#     units = ds[v].long_name.split()[-1].encode()[1:-1]

#     ptitle='%s' %(ds[v].long_name)

#     hover = HoverTool(tooltips=[('data', '@time{%F %T UTC}'),
#                                 ('valor', "@{} {}".format(v,units))],
#                      formatters={'time' : 'datetime'},
#                      mode='vline')

#     # se for a primeira figura
#     if len(figures) == 0:

#         p1 = figure(height = 200,
#                     width = 900,
#                     x_axis_type='datetime',
#                     tools=["pan,wheel_zoom,box_zoom,reset,save,box_select"],
#                     active_scroll = 'wheel_zoom',
#                     title = ptitle,
#                     # x_axis_label="tempo",
#                     y_axis_label = units)

#         p1.add_tools(hover)

#         # p1.xaxis.formatter = DatetimeTickFormatter(days=[str('%d/%m/%Y')])

#         p1.line(source=dsource, x="date", y=v, line_color='blue')

#     else:

#         p1 = figure(height = 200,
#                     width = 900,
#                     x_axis_type = 'datetime',
#                     # tools = ["pan,wheel_zoom,box_zoom,reset,save,box_select"],
#                     active_scroll = 'wheel_zoom',
#                     title = ptitle,
#                     # x_axis_label="tempo",
#                     y_axis_label = units,
#                     x_range=p1.x_range)


#         p1.line(source=dsource, x="date", y=v, line_color='blue')


#     p1.xaxis.formatter = DatetimeTickFormatter(days=[str('%d/%m/%Y')])
#     p1.add_tools(hover)

#     figures.append(p1)

# show(column(figures))


# ------------------------------------------------------------------ #
# Cria Menu

def update_plot(attrname, old, new):
    city = city_select.value
    plot.title.text = "Weather data for " + cities[city]['title']

    src = get_dataset(df, cities[city]['airport'], distribution_select.value)
    source.data.update(src.data)


v = list_vars[0]

city = 'Austin'
distribution = 'Discrete'

cities = {
    'Austin': {
        'airport': 'AUS',
        'title': 'Austin, TX',
    },
    'Boston': {
        'airport': 'BOS',
        'title': 'Boston, MA',
    },
    'Seattle': {
        'airport': 'SEA',
        'title': 'Seattle, WA',
    }
}


p1 = figure(height = 200,

            width = 900,
            x_axis_type='datetime',
            tools=["pan,wheel_zoom,box_zoom,reset,save,box_select"],
            active_scroll = 'wheel_zoom',
            title = 'ptitle',
            # x_axis_label="tempo",
            y_axis_label = 'units')

p1.line(source=dsource, x="date", y=v, line_color='blue')


city_select = Select(value=city, title='City', options=sorted(cities.keys()))

distribution_select = Select(value=distribution, title='Distribution', options=['Discrete', 'Smoothed'])


city_select.on_change('value', update_plot)
distribution_select.on_change('value', update_plot)

controls = column(city_select, distribution_select)

curdoc().add_root(row(p1, controls))
curdoc().title = "Weather"


show(p1)