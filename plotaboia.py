'''
Reamostrar os dados do PNBOIA baixados
do site interpolando os dados e deixando eles
de hora em hora (em horas cheias)

Avaliacao operacional da previsao para os dados
do PNBOIA

Programa que compara os dados baixados do
PNBOIA e a previsao

Data da ultima modificacao: 25/08/2015
'''

import os
import numpy as np
import pylab as pl
from pandas import Series, DataFrame
import pandas as pd
import datetime as dt

pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/LIOc/'

#carrega os dados em data frame
rg = pd.read_table(pathname + 'B69153_onda.out',sep=',',header=0,names=['date','hs','tp','dp','hmax'])
fl = pd.read_table(pathname + 'B69152_onda.out',sep=',',header=0,names=['date','hs','tp','dp','hmax'])
sa = pd.read_table(pathname + 'B69150_onda.out',sep=',',header=0,names=['date','hs','tp','dp','hmax'])

#cria coluna de data com datetime
rg['date'] = [dt.datetime.strptime(str(int(rg['date'][i])), '%Y%m%d%H%M') for i in range(len(rg))]
fl['date'] = [dt.datetime.strptime(str(int(fl['date'][i])), '%Y%m%d%H%M') for i in range(len(fl))]
sa['date'] = [dt.datetime.strptime(str(int(sa['date'][i])), '%Y%m%d%H%M') for i in range(len(sa))]

rg = rg.set_index('date')
fl = fl.set_index('date')
sa = sa.set_index('date')


#figuras
pl.figure(figsize=(16,10))
pl.subplot(311)
pl.plot(rg.index[-168:],rg.hs[-168:],'bo',fl.index[-168:],fl.hs[-168:],'ro',sa.index[-168:],sa.hs[-168:],'go')
pl.title(str(dt.datetime.now())[:-10]+'h')
pl.xticks(visible=False), pl.grid(), pl.ylabel('Hs (m)')
pl.subplot(312)
pl.plot(rg.index[-168:],rg.tp[-168:],'bo',fl.index[-168:],fl.tp[-168:],'ro',sa.index[-168:],sa.tp[-168:],'go')
pl.xticks(visible=False), pl.grid(), pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(rg.index[-168:],rg.dp[-168:],'bo',fl.index[-168:],fl.dp[-168:],'ro',sa.index[-168:],sa.dp[-168:],'go')
pl.grid(), pl.ylabel('Dp (graus)')
pl.yticks(np.arange(0,360+45,45))
pl.ylim(0,360)
pl.legend(['Rio Grande','Florian.','Santos'], ncol=3, loc='upper center',bbox_to_anchor=(0.5, -0.17) )

pl.savefig('fig/pnboia_se.png')

pl.show()
