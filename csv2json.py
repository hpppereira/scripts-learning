'''
Load .csv file and converto to json
'''


import os
import pandas as pd
import numpy as np
import pandas_highcharts
import pandas as pd
import datetime
import os
import numpy as np
from pandas.compat import StringIO
from pandas.io.common import urlopen
from IPython.display import display, display_pretty, Javascript, HTML
from pandas_highcharts.core import serialize
from pandas_highcharts.display import display_charts
import matplotlib.pyplot as plt



pathname = os.environ['HOME'] + '/Dropbox/projetos/BMOP/Sistemas-BMOP/Processamento/dados/BMOBR05_CF1/op/'

#carrega arquivo antigo concatenado 
df = pd.read_table(pathname + 'Dados_BMOBR05.csv',sep=',',parse_dates=['date'],index_col=['date'])

display_charts(df, title="Germany inflation rate")

plt.show()