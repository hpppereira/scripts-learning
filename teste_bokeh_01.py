from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource

TOOLS = "tap"
p = figure(title="Some Figure", tools=TOOLS)

source = ColumnDataSource(dict(x=[[1, 3, 2], [3, 4, 6, 6]], y=[[2, 1, 4], [4, 7, 8, 5]], alphas = [0.8, 0.3], colors=["firebrick", "navy"], name=['A', 'B']))

pglyph = p.patches(xs='x', ys='y', source=source, line_width=2, alpha = 'alphas', color='colors')

def callback_fcn(attr, old, new):
    # The index of the selected glyph is : new['1d']['indices'][0]
    patch_name =  source.data['name'][new['1d']['indices'][0]]
    print("TapTool callback executed on Patch {}".format(patch_name))

pglyph.data_source.on_change('selected',callback_fcn)

curdoc().add_root(column(p))