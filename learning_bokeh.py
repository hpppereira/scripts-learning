"""
Plot INCAPER

- Plota dados NC do do modelo WRF
- Gera HTML com graficos feitos no Bokeh
"""

# ------------------------------------------------------------------ #
# Import bibliotecas

import os
import xarray as xr
import pandas as pd
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, CDSView, BooleanFilter
import pandas as pd
import bokeh.plotting as bp
from bokeh.models import HoverTool, DatetimeTickFormatter

# ------------------------------------------------------------------ #
# Leitura do arquivo netCDF

pathname = os.environ['HOME'] + '/git/svarqueiro/'
filename = 'meteo_sva_davis.csv'

dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%y %H:%M')

df = pd.read_csv(pathname + filename, index_col='date', parse_dates=True)

# Leitura do arquivo com xarray
# ds =  xr.open_dataset(pathname + filename)

# # Converte para dataframe
# df = ds.to_dataframe()

# # Data com indice
# df = df.set_index('date')

# df = df[-7*24:]

# ------------------------------------------------------------------ #
# Plotagem 01

# x = df.index
# y = df.hm0

# p = figure(title="simple line example",
# 		   x_axis_label='x',
# 		   y_axis_label='y')

# p.line(x, y, legend="Temp.", line_width=2)

# output_file("teste1.html")
# show(p)

# ------------------------------------------------------------------ #
# Plotagem 02

# # Create a ColumnDataSource object
# mySource = ColumnDataSource(df)

# # Formata data para aparecer como datetime
# mySource.add(df.index.to_series().apply(lambda d: d.strftime('%Y-%m-%d %H:%M:%S')), 'event_date_formatted')


# # Create your plot as a bokeh.figure object
# myPlot = bp.figure(height = 200,
#                width = 800,
#                x_axis_type = 'datetime',
#                title = 'ColumnDataSource',
#                y_range=(0,10))

# # Format your x-axis as datetime.
# myPlot.xaxis[0].formatter = DatetimeTickFormatter(days='%b %d')

# # Draw the plot on your plot object, identifying the source as your Column Data Source object.
# myPlot.circle("date",
#           "hm0",
#           source=mySource,
#           color='red',
#           size = 25)

# # Add your tooltips
# myPlot.add_tools( HoverTool(tooltips= [("date","@event_date_formatted"),
#                                        ("hm0","@hm0")]
#                             # mode='vline'
#                             )
# 				)


# # Create an output file
# bp.output_file('columnDataSource.html', title = 'ColumnDataSource')
# bp.show(myPlot) 


# ------------------------------------------------------------------ #
# Plotagem 03 - Exemplo Ronaldo

# dsource=ColumnDataSource(data=df)

# ptitle='Titulo da figura' #%s (%s)' %(var[varname].long_name,var[varname].units)            

# hover = HoverTool(tooltips=[('data', '@time{%F %T UTC}'),
#     ('valor', "@{} {}".format('parametro','unidade'))],
#     formatters={'time' : 'datetime'},mode='vline')

# p1 = figure(x_axis_type='datetime',
# 		    tools=["pan,wheel_zoom,box_zoom,reset,save,box_select"],
#     		active_scroll='wheel_zoom',
#     		title=ptitle,
#     		x_axis_label="tempo",
#     		y_axis_label='unidade' )

# p1.add_tools(hover)

# p1.xaxis.formatter = DatetimeTickFormatter(days=[str('%d/%m/%Y')])

# p1.line(source=dsource, x="date", y='hm0', line_color='blue')

# ###p1.x_range=p[listaVars[0]].x_range

# # plots Multi-div as a single PlotObject

# plots = gridplot([p1], ncols=1, plot_width=1000, plot_height=250)


# bp.output_file("meteograma.html")

# bp.show(p1)

# ------------------------------------------------------------------ #
# Plotagem 04 - Subplot

dsource=ColumnDataSource(data=df)

ptitle='Titulo da figura' #%s (%s)' %(var[varname].long_name,var[varname].units)            

hover = HoverTool(tooltips=[('data', '@time{%F %T UTC}'),
    ('valor', "@{} {}".format('parametro','unidade'))],
    formatters={'time' : 'datetime'},mode='vline')

p1 = figure(x_axis_type='datetime',
		    tools=["pan,wheel_zoom,box_zoom,reset,save,box_select"],
    		active_scroll='wheel_zoom',
    		title=ptitle,
    		x_axis_label="tempo",mode='vline'
    		y_axis_label='unidade' )

p1.add_tools(hover)

p1.xaxis.formatter = DatetimeTickFormatter(days=[str('%d/%m/%Y')])

p1.line(source=dsource, x="date", y='hm0', line_color='blue')

#figure 2

p2 = figure(x_axis_type='datetime',
		    tools=["pan,wheel_zoom,box_zoom,reset,save,box_select"],
    		active_scroll='wheel_zoom',
    		title=ptitle,
    		# x_axis_label="tempo",
    		y_axis_label='unidade',
            x_range=p1.x_range)

p2.add_tools(hover)

p2.xaxis.formatter = DatetimeTickFormatter(days=[str('%d/%m/%Y')])

p2.line(source=dsource, x="date", y='tp', line_color='blue')


# p2.line(source=dsource, x="date", y='tp', line_color='red')

###p1.x_range=p[listaVars[0]].x_range

# plots Multi-div as a single PlotObject

plots = gridplot([p1,p2], ncols=1, plot_width=1000, plot_height=250)


bp.output_file("teste04.html")

bp.show(plots)
