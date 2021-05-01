'''
Programa principal para gerar as pleds
do SWAN e WW3
'''

import os
import pleds
import pandas as pd
reload(pleds)

#carrega dados de vento
pathnamew = os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/'

wind = pd.read_table(pathnamew + 'vento.txt', parse_dates=[0], header=None, names=['date','int','dir'])

wind = wind.set_index('date')
wind = wind.resample('H', how='mean')

wind = wind['2013-02-01 00:00':'2013-02-28 23:00']

pathname = os.environ['HOME'] + '/Dropbox/ww3vale/trocas/msc_isa/Espectros/201302/SWAN_uns/'

filename = 'spec_point_ADCP01.out'

espe, dire = pleds.preppledsSWAN(pathname,filename)

espe1 = espe[:,::3]
dire1 = dire[:,::3]
wind = wind[::3]

tit = 'teste'
namefig = 'testepleds_201302_uns1.png'

pleds.pleds(espe1,dire1, wind.int.values , wind.dir.values, tit,namefig)