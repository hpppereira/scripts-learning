'''
Processa dados validados pelo PNBOIA

link
http://www.goosbrasil.org/login/?next=/pnboia/dados/downloadvalid/


Year	Month	Day	Hour	Minute	lon	lat	wspd	wspdflag
wspdflagid	gust	gustflag	gustflagid	wdir	wdirflag
wdirflagid	atmp	atmpflag	atmpflagid	humi	humiflag
humiflagid	dewp	dewpflag	dewpflagid	pres	presflag
presflagid	wtmp	wtmpflag	wtmpflagid	bhead	arad
cvel01	cvel01flag	cvel01flagid	cdir01	cdir01flag
cdir01flagid	cvel02	cvel02flag	cvel02flagid
cdir02	cdir02flag	cdir02flagid	cvel03	cvel03flag	cvel03flagid	
cdir03	cdir03flag	cdir03flagid	wvht	wvhtflag	wvhtflagid	wmax	
wmaxflag	wmaxflagid	dpd	dpdflag	dpdflagid	mwd	mwdflag	mwdflagid	spred

'''

import pandas as pd
import os
import datetime as dt
import numpy as np
import pylab as pl
import matplotlib.dates as mdates



pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/validados/'

dd = pd.read_excel(pathname + 'historico_dados_validados.xlsx', sheetname=['METADADOS','santos','santacatarina',
	'riogrande','recife','portoseguro','cabofrio'])

rg = dd['riogrande']
re = dd['recife']
sa = dd['santos']
fl = dd['santacatarina']
ps = dd['portoseguro']
cf = dd['cabofrio']

rg['date'] = [dt.datetime(rg.Year[i],rg.Month[i],rg.Day[i],rg.Hour[i],rg.Minute[i]) for i in range(len(rg))]
fl['date'] = [dt.datetime(fl.Year[i],fl.Month[i],fl.Day[i],fl.Hour[i],fl.Minute[i]) for i in range(len(fl))]
sa['date'] = [dt.datetime(sa.Year[i],sa.Month[i],sa.Day[i],sa.Hour[i],sa.Minute[i]) for i in range(len(sa))]
re['date'] = [dt.datetime(re.Year[i],re.Month[i],re.Day[i],re.Hour[i],re.Minute[i]) for i in range(len(re))]
ps['date'] = [dt.datetime(ps.Year[i],ps.Month[i],ps.Day[i],ps.Hour[i],ps.Minute[i]) for i in range(len(ps))]
cf['date'] = [dt.datetime(cf.Year[i],cf.Month[i],cf.Day[i],cf.Hour[i],cf.Minute[i]) for i in range(len(cf))]

#consistencia dos dados validados
rg = rg.loc[(rg.wvht < 10) & (rg.wvht > 0) & (rg.dpd < 25)]
fl = fl.loc[(fl.wvht < 10) & (fl.wvht > 0) & (fl.dpd < 25)]
sa = sa.loc[(sa.wvht < 10) & (sa.wvht > 0) & (sa.dpd < 25)]
cf = cf.loc[(cf.wvht < 10) & (cf.wvht > 0) & (cf.dpd < 25)]
ps = ps.loc[(ps.wvht < 10) & (ps.wvht > 0) & (ps.dpd < 25)]
re = re.loc[(re.wvht < 10) & (re.wvht > 0) & (re.dpd < 25)]

rg.index = rg.date
fl.index = fl.date
sa.index = sa.date

#salva arquivos do periodo de dados simultaneos nas 3 boias com data, hs, tp, dp, ws, wd
#rg.loc['2012-02-01 01:21:00':'2012-06-30 23:21:00',['wvht','dpd','mwd','wspd','wdir']].to_csv('out/wavewind_rg_2012.csv', header=['hs','tp','dp','ws','wd'])
#fl.loc['2012-02-01 01:21:00':'2012-06-30 23:21:00',['wvht','dpd','mwd','wspd','wdir']].to_csv('out/wavewind_fl_2012.csv', header=['hs','tp','dp','ws','wd'])
#sa.loc['2012-02-01 01:21:00':'2012-06-30 23:21:00',['wvht','dpd','mwd','wspd','wdir']].to_csv('out/wavewind_sa_2012.csv', header=['hs','tp','dp','ws','wd'])

rg.loc['2013':,['wvht','dpd','mwd','wspd','wdir']].to_csv('out/jonas/wavewind_rg_2013.csv', header=['hs','tp','dp','ws','wd'])
fl.loc['2013':,['wvht','dpd','mwd','wspd','wdir']].to_csv('out/jonas/wavewind_fl_2013.csv', header=['hs','tp','dp','ws','wd'])
sa.loc['2013':,['wvht','dpd','mwd','wspd','wdir']].to_csv('out/jonas/wavewind_sa_2013.csv', header=['hs','tp','dp','ws','wd'])



nrg = np.ones(len(rg)) * 1
nfl = np.ones(len(fl)) * 2
nsa = np.ones(len(sa)) * 3
ncf = np.ones(len(cf)) * 4
nps = np.ones(len(ps)) * 5
nre = np.ones(len(re)) * 6


#periodo de medicao
pl.figure(figsize=(11,6))
pl.plot(rg.date,nrg,'k.',fl.date,nfl,'k.',sa.date,nsa,'k.',cf.date,ncf,'k.',ps.date,nps,'k.',re.date,nre,'k.',markersize=15)
pl.yticks([1,2,3,4,5,6],['Rio Grande','Florianop.','Santos','Cabo Frio','Porto Seg.','Recife'])
pl.ylim(0,7)
pl.grid()


#posicao
#pl.figure()
#pl.plot(rg.lon,rg.lat,'.',fl.lon,fl.lat,'.',sa.lon,sa.lat,'.',ps.lon,ps.lat,'.',re.lon,re.lat,'.',)


pl.figure()
pl.subplot(211)
pl.title('Rio Grande/RS')
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(rg.date,rg.wspd,'.')
pl.ylabel('Wind Spd. (m/s)')
pl.ylim(0,20)
pl.subplot(212)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(rg.date,rg.wdir,'.')
pl.ylabel('Wind Dir. (deg.)')
pl.yticks(np.arange(0,360+45,45))
pl.ylim(0,360)


pl.figure()
pl.subplot(211)
pl.title('Florianopolis/SC')
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(fl.date,fl.wspd,'.')
pl.ylabel('Wind Spd. (m/s)')
pl.ylim(0,20)
pl.subplot(212)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(fl.date,fl.wdir,'.')
pl.ylabel('Wind Dir. (deg.)')
pl.yticks(np.arange(0,360+45,45))
pl.ylim(0,360)


pl.figure()
pl.subplot(211)
pl.title('Santos/SP')
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(sa.date,sa.wspd,'.')
pl.ylabel('Wind Spd. (m/s)')
pl.ylim(0,20)
pl.subplot(212)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(sa.date,sa.wdir,'.')
pl.ylabel('Wind Dir. (deg.)')
pl.yticks(np.arange(0,360+45,45))
pl.ylim(0,360)




#hs, tp e dp

#rio grande
pl.figure()
pl.subplot(311)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.title('Rio Grande/RS')
pl.plot(rg.date,rg.wvht,'.')
pl.ylabel('Hm0 (m)')
pl.subplot(312)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(rg.date,rg.dpd,'.')
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(rg.date,rg.mwd,'.')
pl.ylabel('Dp (deg)')

#florian
pl.figure()
pl.subplot(311)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.title('Florianopolis/SC')
pl.plot(fl.date,fl.wvht,'.')
pl.ylabel('Hm0 (m)')
pl.subplot(312)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(fl.date,fl.dpd,'.')
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(fl.date,fl.mwd,'.')
pl.ylabel('Dp (deg)')

#santos
pl.figure()
pl.subplot(311)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.title('Santos/SP')
pl.plot(sa.date,sa.wvht,'.')
pl.ylabel('Hm0 (m)')
pl.subplot(312)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(sa.date,sa.dpd,'.')
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(sa.date,sa.mwd,'.')
pl.ylabel('Dp (deg)')

#cabo frio
pl.figure()
pl.subplot(311)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.title('Cabo Frio/RJ')
pl.plot(cf.date,cf.wvht,'.')
pl.ylabel('Hm0 (m)')
pl.subplot(312)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(cf.date,cf.dpd,'.')
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(cf.date,cf.mwd,'.')
pl.ylabel('Dp (deg)')

#porto seguro
pl.figure()
pl.subplot(311)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.title('Porto Seguro/BA')
pl.plot(ps.date,ps.wvht,'.')
pl.ylabel('Hm0 (m)')
pl.subplot(312)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(ps.date,ps.dpd,'.')
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(ps.date,ps.mwd,'.')
pl.ylabel('Dp (deg)')

#recife
pl.figure()
pl.subplot(311)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.title('Recife/PE')
pl.plot(re.date,re.wvht,'.')
pl.ylabel('Hm0 (m)')
pl.subplot(312)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(re.date,re.dpd,'.')
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
pl.plot(re.date,re.mwd,'.')
pl.ylabel('Dp (deg)')

pl.show()


# carregar dados brutos de rg, sc, sp e re

# carregar dados do siodoc

# verificar se nesses dados tem o periodo simultaneo dos dados brutos de ondas

