
# coding: utf-8

# In[38]:

'''
Avaliacao operacional da previsao para os dados
do PNBOIA

Programa que compara os dados baixados do
PNBOIA e a previsao

Data da ultima modificacao: 25/08/2015
'''

import matplotlib
matplotlib.use('Agg') #necessario para salvar figura no crontab
import os
import numpy as np
import matplotlib.pylab as pl
from pandas import Series, DataFrame
import pandas as pd
import datetime as dt

pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/LIOc/'
pathnamep = os.environ['HOME'] + '/Dropbox/Previsao/pnboia/resultados/'

prevs = np.sort(os.listdir(pathnamep))


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

#reamostra os dados horarios
rg = rg.resample('H')
fg = fl.resample('H')
sa = sa.resample('H')

#carrega os resultados do modelo

#previsao dia -7
rgp7 = pd.read_table(pathnamep + prevs[-7] + '/PNBOIA_riogrande.txt',sep='\s*',
                     names=['ano','mes','dia','hora','minu','hs','tp','dp','spr'])

flp7 = pd.read_table(pathnamep + prevs[-7] + '/PNBOIA_floripa.txt',sep='\s*',
                     names=['ano','mes','dia','hora','minu','hs','tp','dp','spr'])

sap7 = pd.read_table(pathnamep + prevs[-7] + '/PNBOIA_santos.txt',sep='\s*',
                     names=['ano','mes','dia','hora','minu','hs','tp','dp','spr'])

#previsao dia -4
rgp4 = pd.read_table(pathnamep + prevs[-4] + '/PNBOIA_riogrande.txt',sep='\s*',
                     names=['ano','mes','dia','hora','minu','hs','tp','dp','spr'])

flp4 = pd.read_table(pathnamep + prevs[-4] + '/PNBOIA_floripa.txt',sep='\s*',
                     names=['ano','mes','dia','hora','minu','hs','tp','dp','spr'])

sap4 = pd.read_table(pathnamep + prevs[-4] + '/PNBOIA_santos.txt',sep='\s*',
                     names=['ano','mes','dia','hora','minu','hs','tp','dp','spr'])

#previsao dia -3
rgp3 = pd.read_table(pathnamep + prevs[-3] + '/PNBOIA_riogrande.txt',sep='\s*',
                     names=['ano','mes','dia','hora','minu','hs','tp','dp','spr'])

flp3 = pd.read_table(pathnamep + prevs[-3] + '/PNBOIA_floripa.txt',sep='\s*',
                     names=['ano','mes','dia','hora','minu','hs','tp','dp','spr'])

sap3 = pd.read_table(pathnamep + prevs[-3] + '/PNBOIA_santos.txt',sep='\s*',
                     names=['ano','mes','dia','hora','minu','hs','tp','dp','spr'])

##previsao dia atual (-1)
rgp1 = pd.read_table(pathnamep + prevs[-1] + '/PNBOIA_riogrande.txt',sep='\s*',
                     names=['ano','mes','dia','hora','minu','hs','tp','dp','spr'])

flp1 = pd.read_table(pathnamep + prevs[-1] + '/PNBOIA_floripa.txt',sep='\s*',
                     names=['ano','mes','dia','hora','minu','hs','tp','dp','spr'])

sap1 = pd.read_table(pathnamep + prevs[-1] + '/PNBOIA_santos.txt',sep='\s*',
                     names=['ano','mes','dia','hora','minu','hs','tp','dp','spr'])

#cria data com datetime

#dia -7
rgp7['data'] = pd.to_datetime(rgp7.ano.astype(str) + rgp7.mes.astype(str) + rgp7.dia.astype(str) + rgp7.hora.astype(str) ,format="%Y%m%d%H")
flp7['data'] = pd.to_datetime(flp7.ano.astype(str) + flp7.mes.astype(str) + flp7.dia.astype(str) + flp7.hora.astype(str) ,format="%Y%m%d%H")
sap7['data'] = pd.to_datetime(sap7.ano.astype(str) + sap7.mes.astype(str) + sap7.dia.astype(str) + sap7.hora.astype(str) ,format="%Y%m%d%H")

#dia -4
rgp4['data'] = pd.to_datetime(rgp4.ano.astype(str) + rgp4.mes.astype(str) + rgp4.dia.astype(str) + rgp4.hora.astype(str) ,format="%Y%m%d%H")
flp4['data'] = pd.to_datetime(flp4.ano.astype(str) + flp4.mes.astype(str) + flp4.dia.astype(str) + flp4.hora.astype(str) ,format="%Y%m%d%H")
sap4['data'] = pd.to_datetime(sap4.ano.astype(str) + sap4.mes.astype(str) + sap4.dia.astype(str) + sap4.hora.astype(str) ,format="%Y%m%d%H")

#dia -3
rgp3['data'] = pd.to_datetime(rgp3.ano.astype(str) + rgp3.mes.astype(str) + rgp3.dia.astype(str) + rgp3.hora.astype(str) ,format="%Y%m%d%H")
flp3['data'] = pd.to_datetime(flp3.ano.astype(str) + flp3.mes.astype(str) + flp3.dia.astype(str) + flp3.hora.astype(str) ,format="%Y%m%d%H")
sap3['data'] = pd.to_datetime(sap3.ano.astype(str) + sap3.mes.astype(str) + sap3.dia.astype(str) + sap3.hora.astype(str) ,format="%Y%m%d%H")

#dia -1
rgp1['data'] = pd.to_datetime(rgp1.ano.astype(str) + rgp1.mes.astype(str) + rgp1.dia.astype(str) + rgp1.hora.astype(str) ,format="%Y%m%d%H")
flp1['data'] = pd.to_datetime(flp1.ano.astype(str) + flp1.mes.astype(str) + flp1.dia.astype(str) + flp1.hora.astype(str) ,format="%Y%m%d%H")
sap1['data'] = pd.to_datetime(sap1.ano.astype(str) + sap1.mes.astype(str) + sap1.dia.astype(str) + sap1.hora.astype(str) ,format="%Y%m%d%H")


#deixa a data como indice

#dia -7
rgp7 = rgp7.set_index('data')
flp7 = flp7.set_index('data')
sap7 = sap7.set_index('data')

#dia -4
rgp4 = rgp4.set_index('data')
flp4 = flp4.set_index('data')
sap4 = sap4.set_index('data')

#dia -3
rgp3 = rgp3.set_index('data')
flp3 = flp3.set_index('data')
sap3 = sap3.set_index('data')

#dia -1
rgp1 = rgp1.set_index('data')
flp1 = flp1.set_index('data')
sap1 = sap1.set_index('data')


#remove as colunas de ano, mes, dia hora e minu

#dia -7
rgp7 = rgp7.ix[:,['hs','tp','dp']]
flp7 = flp7.ix[:,['hs','tp','dp']]
sap7 = sap7.ix[:,['hs','tp','dp']]

#dia -4
rgp4 = rgp4.ix[:,['hs','tp','dp']]
flp4 = flp4.ix[:,['hs','tp','dp']]
sap4 = sap4.ix[:,['hs','tp','dp']]

#dia -3
rgp3 = rgp3.ix[:,['hs','tp','dp']]
flp3 = flp3.ix[:,['hs','tp','dp']]
sap3 = sap3.ix[:,['hs','tp','dp']]

#dia -1
rgp1 = rgp1.ix[:,['hs','tp','dp']]
flp1 = flp1.ix[:,['hs','tp','dp']]
sap1 = sap1.ix[:,['hs','tp','dp']]



# In[39]:

pl.close('all')

#figuras

#plota figuras de dados e previsao

hoje = dt.datetime.strftime(dt.datetime.today(),'%Y%m%d')

#tamanho da janela
tj = 7 * 24


pl.figure(figsize=(16,10))
pl.subplot(311)
pl.plot(rg.index[-168:],rg.hs[-168:],'bo',fl.index[-168:],fl.hs[-168:],'ro',sa.index[-168:],sa.hs[-168:],'go')
pl.title('PNBOIA-SE \n' + str(dt.datetime.now())[:-16])
pl.xticks(visible=False), pl.grid(), pl.ylabel('Hs (m)')
pl.ylim(0,6)
pl.subplot(312)
pl.plot(rg.index[-168:],rg.tp[-168:],'bo',fl.index[-168:],fl.tp[-168:],'ro',sa.index[-168:],sa.tp[-168:],'go')
pl.xticks(visible=False), pl.grid(), pl.ylabel('Tp (s)')
pl.ylim(0,20)
pl.subplot(313)
pl.plot(rg.index[-168:],rg.dp[-168:],'bo',fl.index[-168:],fl.dp[-168:],'ro',sa.index[-168:],sa.dp[-168:],'go')
pl.grid(), pl.ylabel('Dp (graus)')
pl.yticks(np.arange(0,360+45,45))
pl.ylim(0,360)
pl.legend(['Rio Grande','Florian.','Santos'], ncol=3, loc='upper center',bbox_to_anchor=(0.5, -0.17) )

pl.savefig(os.environ['HOME'] + '/Dropbox/Previsao/pnboia/fig/pnboia_SE_' + hoje + '.png')


pl.figure(figsize=(16,10))
pl.subplot(311)
pl.title('Rio Grande/RS \n' + str(dt.datetime.now())[:-16])
pl.plot(rg.index[-tj:],rg.hs[-tj:],'o')
pl.plot(rgp7.index,rgp7.hs,rgp4.index,rgp4.hs,rgp1.index,rgp1.hs,linewidth=3)
pl.ylim(0,6)
pl.xticks(visible=False), pl.grid(), pl.ylabel('Hs (m)')
pl.subplot(312)
pl.plot(rg.index[-tj:],rg.tp[-tj:],'o')
pl.plot(rgp7.index,rgp7.tp,rgp4.index,rgp4.tp,rgp1.index,rgp1.tp,linewidth=3)
pl.ylim(0,20)
pl.xticks(visible=False), pl.grid(), pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(rg.index[-tj:],rg.dp[-tj:],'o')
pl.plot(rgp7.index,rgp7.dp,rgp4.index,rgp4.dp,rgp1.index,rgp1.dp,linewidth=3)
pl.grid(), pl.ylabel('Dp (graus)')
pl.yticks(np.arange(0,360+45,45))
pl.ylim(0,360)
pl.legend(['BMO','WW3-7','WW3-4','WW3-1'], ncol=4, loc='upper center',bbox_to_anchor=(0.5, -0.17) )

pl.savefig(os.environ['HOME'] + '/Dropbox/Previsao/pnboia/fig/pnboiaprev_rio_grande_' + hoje + '.png')


pl.figure(figsize=(16,10))
pl.subplot(311)
pl.plot(fl.index[-tj:],fl.hs[-tj:],'o')
pl.title('Florianopolis/SC \n' + str(dt.datetime.now())[:-16])
pl.plot(flp7.index,flp7.hs,flp4.index,flp4.hs,flp1.index,flp1.hs,linewidth=3)
pl.ylim(0,6)
pl.xticks(visible=False), pl.grid(), pl.ylabel('Hs (m)')
pl.subplot(312)
pl.plot(fl.index[-tj:],fl.tp[-tj:],'o')
pl.plot(flp7.index,flp7.tp,flp4.index,flp4.tp,flp1.index,flp1.tp,linewidth=3)
pl.xticks(visible=False), pl.grid(), pl.ylabel('Tp (s)')
pl.ylim(0,20)
pl.subplot(313)
pl.plot(fl.index[-tj:],fl.dp[-tj:],'o')
pl.plot(flp7.index,flp7.dp,flp4.index,flp4.dp,flp1.index,flp1.dp,linewidth=3)
pl.grid(), pl.ylabel('Dp (graus)')
pl.yticks(np.arange(0,360+45,45))
pl.ylim(0,360)
pl.legend(['BMO','WW3-7','WW3-4','WW3-1'], ncol=4, loc='upper center',bbox_to_anchor=(0.5, -0.17) )

pl.savefig(os.environ['HOME'] + '/Dropbox/Previsao/pnboia/fig/pnboiaprev_florianopolis_' + hoje + '.png')


pl.figure(figsize=(16,10))
pl.subplot(311)
pl.plot(sa.index[-tj:],sa.hs[-tj:],'o')
pl.title('Santos/SP \n' + str(dt.datetime.now())[:-16])
pl.plot(sap7.index,sap7.hs,sap4.index,sap4.hs,sap1.index,sap1.hs,linewidth=3)
pl.ylim(0,6)
pl.xticks(visible=False), pl.grid(), pl.ylabel('Hs (m)')
pl.subplot(312)
pl.plot(sa.index[-tj:],sa.tp[-tj:],'o')
pl.plot(sap7.index,sap7.tp,sap4.index,sap4.tp,sap1.index,sap1.tp,linewidth=3)
pl.xticks(visible=False), pl.grid(), pl.ylabel('Tp (s)')
pl.ylim(0,20)
pl.subplot(313)
pl.plot(sa.index[-tj:],sa.dp[-tj:],'o')
pl.plot(sap7.index,sap7.dp,sap4.index,sap4.dp,sap1.index,sap1.dp,linewidth=3)
pl.grid(), pl.ylabel('Dp (graus)')
pl.yticks(np.arange(0,360+45,45))
pl.ylim(0,360)
pl.legend(['BMO','WW3-7','WW3-4','WW3-1'], ncol=4, loc='upper center',bbox_to_anchor=(0.5, -0.17) )

pl.savefig(os.environ['HOME'] + '/Dropbox/Previsao/pnboia/fig/pnboiaprev_santos_' + hoje + '.png')



pl.show()


# In[ ]:



