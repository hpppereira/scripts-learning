'''
Plotagem da pleds de corrente
com dados da boia do siodoc
'''

import os
import pandas as pd
import pleds

reload(pleds)


pathname = os.environ['HOME'] + '/Dropbox/pleds_corrente/dados/'

dd = pd.read_pickle(pathname + 'janis_currents_filter.pkl')
dv = pd.read_pickle(pathname + 'janis_wtsmeta_filter.pkl')

spd = dd.spd['20150101':'20150131'][::3].T.values[::-1]
dire = dd.dir['20150101':'20150131'][::3].T.values[::-1]
ws = dv['wind','spd']['20150101':'20150131'][::3].T.values[::-1]
wd = dv['wind','dir']['20150101':'20150131'][::3].T.values[::-1]

x = pleds.pledscur(spd*100,dire,ws,wd)

