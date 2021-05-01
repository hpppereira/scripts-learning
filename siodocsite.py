#!/usr/bin/python
# -*- coding: utf-8 -*-

# Laboratorio de Instrumentacao Oceanografica - LIOc-COPPE/UFRJ

#baixar dados meteo-oceanograficos
#do siodoc

# 1 - baixar os dados 1 vez por dia, e enviar a mensagem as 6 hrs da manha
# 1.1 - rodar o programa em shell, chamando o python no crontab
# 2 - criar um programa para listar os arquivos do diretorio e trabalhar
# com o utlimo arquivo baixado
# 3 - mandar as estatisticas de onda
# 3.1 -  corrigir a declinacao

#baixar dados em shell - terminal
# /usr/bin/wget http://metocean.fugrogeos.com/marinha/Members/Data_month.csv -O /home/hp/Google\ Drive/siodoc/dados/boia_wavescan_`date +\%Y\%m\%d`.txt

import numpy as np
import pylab as pl
import datetime as dt
import os

# pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/siodoc/dados/proc/'

#data = time, hm0, tp, dp, at=2,hmax=25,wt=53,wd=61,ws=63 

dados = np.loadtxt(pathname + 'Data_month.csv', delimiter=',', unpack=False, dtype=str)

data = dados[2:,0]
hm0, hm0a, hm0b, hmax = dados[2:,range(22,26)].T.astype('float')
mdir, mdira, mdirb = dados[2:,range(33,36)].T.astype('float')
sprtp, thhf, thmax, thtp, tm01, tm02, tm02a, tp = dados[2:,range(45,53)].T.astype('float')
bp, at, wt, wd, wg, ws,  = dados[2:,[1,2,53,61,62,63]].T.astype('float')

#corrige declinacao magnetica (-24 graus)
dire = np.array([wd, mdir, mdira, mdirb])
dire = dire - 23
#
dire[np.where(dire > 360)] = dire[np.where(dire > 360)] - 360
dire[np.where(dire < 0)] = dire[np.where(dire < 0)] + 360

wd, mdir, mdira, mdirb = dire

#data com datetime
data1 = [dt.datetime.strptime(data[i], '%d.%m.%Y %H:%M:%S') for i in range(len(data))]

#figuras

# -- figura 1 -- #

pl.figure()
pl.subplot(211)
pl.title('Dados Meteorologicos - SIODOC')
pl.plot(data1,bp,'b',label='bp'), pl.xticks(visible=False)
pl.ylabel('Pressao - mbar'), pl.legend(loc=2)
pl.grid('on')
pl.twinx()
pl.plot(data1,ws,'r',label='ws')
pl.plot(data1,wg,'g',label='wg')
pl.ylabel('Vel e Raj. Vento - m/s'), pl.legend(loc=1)


pl.subplot(212)
pl.plot(data1,wd,'b',label='wd'), pl.xticks(rotation=15)
pl.ylabel('Dir. Vento - gr'), pl.legend(loc=2)
pl.axis([data1[0],data1[-1],0,360])
pl.grid('on')
pl.twinx()
pl.plot(data1,wt,'r',label='wt')
pl.ylabel('Temp. agua - gr'), pl.legend(loc=1)


# -- figura 2 -- #

pl.figure()
pl.subplot(311)
pl.title('Dados de Ondas  - SIODOC')
pl.plot(data1,hm0,'bo',label='hm0'), pl.xticks(visible=False)
pl.ylabel('Hm0 - m'), pl.legend(loc=2)
pl.grid('on')
pl.twinx()
pl.plot(data1,ws,'r',label='ws')
pl.ylabel('Vel. Vento - m/s'), pl.legend(loc=1)

pl.subplot(312)
pl.plot(data1,tp,'bo',label='tp')
pl.xticks(visible=False), pl.grid('on')
pl.ylabel('Tp - s'), pl.legend(loc=2)


pl.subplot(313)
pl.plot(data1,mdir,'bo',label='dp'), pl.xticks(rotation=15)
pl.ylabel('Dp - gr'), pl.legend(loc=2)
pl.axis([data1[0],data1[-1],0,360])
pl.grid('on')
pl.twinx()
pl.plot(data1,wd,'r',label='wd'), 
pl.ylabel('Dir. Vento - m/s'), pl.legend(loc=1)
pl.axis([data1[0],data1[-1],0,360])

pl.show()
