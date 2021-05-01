'''
Baixa dados utilizando a rotina
telnetpnboia.py

Funcao
telnetpnboia.Asaos(boia,'fileout')
'''

import datetime as dt
import numpy as np
import telnetpnboia
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg') #necessario para salvar figura no crontab
import matplotlib.pylab as pl

reload(telnetpnboia)

pl.close('all')


#carrega dados antigos

#abre arquivos argos da boia onde estao sendo
#concatenados os arquivos baixados


pathname = os.environ['HOME'] + '/Dropbox/pnboia/rot/out/argos/'

old_rg = pd.read_csv(pathname + 'Argos_RioGran_B69153.csv',sep=',',parse_dates=['date'],index_col=['date'])
#old_fl = pd.read_csv(pathname + 'Argos_Florian_B69152.csv',sep=',',parse_dates=['date'],index_col=['date'])
old_sa = pd.read_csv(pathname + 'Argos_Santos_B69150.csv',sep=',',parse_dates=['date'],index_col=['date'])
old_bg = pd.read_csv(pathname + 'Argos_BGuan_B69151.csv',sep=',',parse_dates=['date'],index_col=['date'])
old_vi = pd.read_csv(pathname + 'Argos_Vitoria_B146447.csv',sep=',',parse_dates=['date'],index_col=['date'])
old_ps = pd.read_csv(pathname + 'Argos_PortSeg_B146448.csv',sep=',',parse_dates=['date'],index_col=['date'])
old_re = pd.read_csv(pathname + 'Argos_Recife_B69008.csv',sep=',',parse_dates=['date'],index_col=['date'])

#salva arquivos
old_rg.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/rot/out/argos/bkp/Argos_RioGran_B69153_' + str(dt.datetime.today())[0:10] + '.csv')
old_sa.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/rot/out/argos/bkp/Argos_Santos_B691501_' + str(dt.datetime.today())[0:10] + '.csv')
old_bg.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/rot/out/argos/bkp/Argos_BGuan_B69151_' + str(dt.datetime.today())[0:10] + '.csv')
old_vi.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/rot/out/argos/bkp/Argos_Vitoria_B146447_' + str(dt.datetime.today())[0:10] + '.csv')
old_ps.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/rot/out/argos/bkp/Argos_PortSeg_B146448_' + str(dt.datetime.today())[0:10] + '.csv')
old_re.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/rot/out/argos/bkp/Argos_Recife_B69008_' + str(dt.datetime.today())[0:10] + '.csv')

#baixa dados atuais (caso nao tenha o arquivo )

print '1 - Baixando dados da boia 69153 - Rio Grande/RS'
telnetpnboia.Argos(69153,pathname + 'Argos_RioGran_B69153')

#print '4 - Baixando dados da boia 69152 - Florianopolis/SC'
#telnetpnboia.Argos(69152,'out/argos/Argos_Florian_B69152')

print '2 - Baixando dados da boia 69150 - Santos/SP'
telnetpnboia.Argos(69150,pathname + 'Argos_Santos_B69150')

print '3 - Baixando dados da boia 69151 - BGuan/RJ'
telnetpnboia.Argos(69151,pathname + 'Argos_BGuan_B69151')

print '4 - Baixando dados da boia 146447 - Vitoria/ES'
telnetpnboia.Argos(146447,pathname + 'Argos_Vitoria_B146447')

print '5 - Baixando dados da boia 146448 - Porto Seguro/BA'
telnetpnboia.Argos(146448,pathname + 'Argos_PortSeg_B146448')

print '6 - Baixando dados da boia 69008 - Recife/PE'
telnetpnboia.Argos(69008,pathname + 'Argos_Recife_B69008')

#carrega dados atuais

new_rg = pd.read_csv(pathname + 'Argos_RioGran_B69153.csv',sep=',',parse_dates=['date'],index_col=['date'])
#new_fl = pd.read_csv(pathname + 'Argos_Florian_B69152.csv',sep=',',parse_dates=['date'],index_col=['date'])
new_sa = pd.read_csv(pathname + 'Argos_Santos_B69150.csv',sep=',',parse_dates=['date'],index_col=['date'])
new_bg = pd.read_csv(pathname + 'Argos_BGuan_B69151.csv',sep=',',parse_dates=['date'],index_col=['date'])
new_vi = pd.read_csv(pathname + 'Argos_Vitoria_B146447.csv',sep=',',parse_dates=['date'],index_col=['date'])
new_ps = pd.read_csv(pathname + 'Argos_PortSeg_B146448.csv',sep=',',parse_dates=['date'],index_col=['date'])
new_re = pd.read_csv(pathname + 'Argos_Recife_B69008.csv',sep=',',parse_dates=['date'],index_col=['date'])


#concatena os dados

concat_rg = pd.concat([old_rg, new_rg])
#concat_fl = pd.concat([old_fl, new_fl])
concat_sa = pd.concat([old_sa, new_sa])
concat_bg = pd.concat([old_bg, new_bg])
concat_vi = pd.concat([old_vi, new_vi])
concat_ps = pd.concat([old_ps, new_ps])
concat_re = pd.concat([old_re, new_re])


#retira dados repetidos (verifica a data)

u, ind = np.unique(concat_rg.index, return_index=True)
concat_rg = concat_rg.ix[ind]

#u, ind = np.unique(concat_fl.index, return_index=True)
#concat_fl = concat_fl.ix[ind]

u, ind = np.unique(concat_sa.index, return_index=True)
concat_sa = concat_sa.ix[ind]

u, ind = np.unique(concat_bg.index, return_index=True)
concat_bg = concat_bg.ix[ind]

u, ind = np.unique(concat_vi.index, return_index=True)
concat_vi = concat_vi.ix[ind]

u, ind = np.unique(concat_ps.index, return_index=True)
concat_ps = concat_ps.ix[ind]

u, ind = np.unique(concat_re.index, return_index=True)
concat_re = concat_re.ix[ind]


#salva arquivos concatenados

concat_rg.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/rot/out/argos/Argos_RioGran_B69153.csv')
concat_rg.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/dados/operacional/argos/Argos_RioGran_B69153.csv')

#concat_fl.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/rot/out/argos/Argos_Florian_B69152.csv')
#concat_fl.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/dados/operacional/argos/Argos_Florian_B69152.csv')

concat_sa.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/rot/out/argos/Argos_Santos_B69150.csv')
concat_sa.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/dados/operacional/argos/Argos_Santos_B69150.csv')

concat_bg.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/rot/out/argos/Argos_BGuan_B69151.csv')
concat_bg.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/dados/operacional/argos/Argos_BGuan_B69151.csv')

concat_vi.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/rot/out/argos/Argos_Vitoria_B146447.csv')
concat_vi.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/dados/operacional/argos/Argos_Vitoria_B146447.csv')

concat_ps.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/rot/out/argos/Argos_PortSeg_B146448.csv')
concat_ps.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/dados/operacional/argos/Argos_PortSeg_B146448.csv')

concat_re.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/rot/out/argos/Argos_Recife_B69008.csv')
concat_re.to_csv(os.environ['HOME'] + '/Dropbox/pnboia/dados/operacional/argos/Argos_Recife_B69008.csv')


#coloca -9999 nos parametros de temp do ar - para nao dar erro na plotagem
concat_rg.airt[pd.isnull(concat_rg.airt)] = -9999
#concat_fl.airt[pd.isnull(concat_fl.airt)] = -9999
concat_sa.airt[pd.isnull(concat_sa.airt)] = -9999
concat_bg.airt[pd.isnull(concat_bg.airt)] = -9999
concat_vi.airt[pd.isnull(concat_vi.airt)] = -9999
concat_ps.airt[pd.isnull(concat_ps.airt)] = -9999
concat_re.airt[pd.isnull(concat_re.airt)] = -9999


#plota os parametros baixados

#bateria
pl.figure()
pl.plot(concat_rg.index,concat_rg.bat,'-o',label='RioGran')
pl.plot(concat_sa.index,concat_sa.bat,'-o',label='Santos')
pl.plot(concat_bg.index,concat_bg.bat,'-o',label='BGuana')
pl.plot(concat_vi.index,concat_vi.bat,'-o',label='Vitoria')
pl.plot(concat_ps.index,concat_ps.bat,'-o',label='PortSeg')
pl.plot(concat_re.index,concat_re.bat,'-o',label='Recife')
pl.legend(ncol=3,loc=3)
pl.xticks(rotation=12)
pl.ylim(0,15)
pl.grid()
pl.xlabel('Time (UTC)')
pl.ylabel('Battery (V)')
pl.savefig(pathname + 'fig/batttery.png')


#ondas

#rio grande
pl.figure()
pl.subplot(311)
pl.plot(concat_rg.index,concat_rg.hs,'b-o',concat_rg.index,concat_rg.hmax,'r--o')
pl.title('Rio Grande - ' + str(concat_rg.index[-1])[:-9])
pl.ylim(0,7), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Hs, Hmax (m)')
pl.subplot(312)
pl.plot(concat_rg.index,concat_rg.tp,'-o')
pl.ylim(0,20), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(concat_rg.index,concat_rg.dp-17,'-o')
pl.yticks(np.arange(0,360+45,45)), pl.ylim(0,360), pl.grid()
pl.xticks(rotation=12)
pl.ylabel('Dp (deg)')
pl.xlabel('Time (UTC)')
pl.savefig(pathname + 'fig/waves_rg.png')

#santos
pl.figure()
pl.subplot(311)
pl.plot(concat_sa.index,concat_sa.hs,'b-o',concat_sa.index,concat_sa.hmax,'r--o')
pl.title('Santos - ' + str(concat_sa.index[-1])[:-9])
pl.ylim(0,7), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Hs, Hmax (m)')
pl.subplot(312)
pl.plot(concat_sa.index,concat_sa.tp,'-o')
pl.ylim(0,20), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(concat_sa.index,concat_sa.dp-22,'-o')
pl.yticks(np.arange(0,360+45,45)), pl.ylim(0,360), pl.grid()
pl.xticks(rotation=12)
pl.ylabel('Dp (deg)')
pl.xlabel('Time (UTC)')
pl.savefig(pathname + 'fig/waves_sa.png')


#baia de guanabara
pl.figure()
pl.subplot(311)
pl.plot(concat_bg.index,concat_bg.hs,'b-o',concat_bg.index,concat_bg.hmax,'r--o')
pl.title('Baia de Guanabara - ' + str(concat_bg.index[-1])[:-9])
pl.ylim(0,7), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Hs, Hmax (m)')
pl.subplot(312)
pl.plot(concat_bg.index,concat_bg.tp,'-o')
pl.ylim(0,20), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(concat_bg.index,concat_bg.dp-22,'-o')
pl.yticks(np.arange(0,360+45,45)), pl.ylim(0,360), pl.grid()
pl.xticks(rotation=12)
pl.ylabel('Dp (deg)')
pl.xlabel('Time (UTC)')
pl.savefig(pathname + 'fig/waves_bg.png')


#vitoria
pl.figure()
pl.subplot(311)
pl.plot(concat_vi.index,concat_vi.hs,'b-o',concat_vi.index,concat_vi.hmax,'r--o')
pl.title('Vitoria - ' + str(concat_vi.index[-1])[:-9])
pl.ylim(0,7), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Hs, Hmax (m)')
pl.subplot(312)
pl.plot(concat_vi.index,concat_vi.tp,'-o')
pl.ylim(0,20), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(concat_vi.index,concat_vi.dp-22,'-o')
pl.yticks(np.arange(0,360+45,45)), pl.ylim(0,360), pl.grid()
pl.xticks(rotation=12)
pl.ylabel('Dp (deg)')
pl.xlabel('Time (UTC)')
pl.savefig(pathname + 'fig/waves_vi.png')


#porto seguro
pl.figure()
pl.subplot(311)
pl.plot(concat_ps.index,concat_ps.hs,'b-o',concat_ps.index,concat_ps.hmax,'r--o')
pl.title('Porto Seguro - ' + str(concat_ps.index[-1])[:-9])
pl.ylim(0,7), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Hs, Hmax (m)')
pl.subplot(312)
pl.plot(concat_ps.index,concat_ps.tp,'-o')
pl.ylim(0,20), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(concat_ps.index,concat_ps.dp-22,'-o')
pl.yticks(np.arange(0,360+45,45)), pl.ylim(0,360), pl.grid()
pl.xticks(rotation=12)
pl.ylabel('Dp (deg)')
pl.xlabel('Time (UTC)')
pl.savefig(pathname + 'fig/waves_ps.png')


#recife
pl.figure()
pl.subplot(311)
pl.plot(concat_re.index,concat_re.hs,'b-o',concat_re.index,concat_re.hmax,'r--o')
pl.title('Recife - ' + str(concat_re.index[-1])[:-9])
pl.ylim(0,7), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Hs, Hmax (m)')
pl.subplot(312)
pl.plot(concat_re.index,concat_re.tp,'-o')
pl.ylim(0,20), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(concat_re.index,concat_re.dp-22,'-o')
pl.yticks(np.arange(0,360+45,45)), pl.ylim(0,360), pl.grid()
pl.xticks(rotation=12)
pl.ylabel('Dp (deg)')
pl.xlabel('Time (UTC)')
pl.savefig(pathname + 'fig/waves_re.png')


#meteorologicos


#rio grande
pl.figure(figsize=(11,9))
pl.subplot(321)
pl.plot(concat_rg.index,concat_rg.ws1,'b-o',concat_rg.index,concat_rg.wg1,'r--o')
pl.title('Rio Grande - ' + str(concat_rg.index[-1])[:-9])
pl.ylim(0,20), pl.grid()
pl.xticks(visible=False)
pl.ylabel('WS, WG (m/s)')
pl.subplot(322)
pl.plot(concat_rg.index,concat_rg.wd1,'-o')
pl.title('Rio Grande - ' + str(concat_rg.index[-1])[:-9])
pl.ylim(0,360), pl.grid()
pl.xticks(visible=False)
pl.ylabel('WD (deg)')
pl.subplot(323)
pl.plot(concat_rg.index,concat_rg.airt,'-o')
pl.ylim(0,35), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Air Temp (C)')
pl.subplot(324)
pl.plot(concat_rg.index,concat_rg.rh,'-o')
pl.ylim(0,100), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Rel. Humid')
pl.subplot(325)
pl.plot(concat_rg.index,concat_rg.pr,'-o')
pl.ylim(990,1030), pl.grid()
pl.ylabel('Pressure (hPa)')
pl.xlabel('Time (UTC)')
pl.xticks(rotation=18)
pl.subplot(326)
pl.plot(concat_rg.index,concat_rg.sst,'-o')
pl.ylim(15,35), pl.grid()
pl.ylabel('SST (deg)')
pl.xlabel('Time (UTC)')
pl.xticks(rotation=18)
pl.savefig(pathname + 'fig/meteo_rg.png')


#santos
pl.figure(figsize=(11,9))
pl.subplot(321)
pl.plot(concat_sa.index,concat_sa.ws1,'b-o',concat_sa.index,concat_sa.wg1,'r--o')
pl.title('Santos - ' + str(concat_sa.index[-1])[:-9])
pl.ylim(0,20), pl.grid()
pl.xticks(visible=False)
pl.ylabel('WS, WG (m/s)')
pl.subplot(322)
pl.plot(concat_sa.index,concat_sa.wd1,'-o')
pl.title('Santos - ' + str(concat_sa.index[-1])[:-9])
pl.ylim(0,360), pl.grid()
pl.xticks(visible=False)
pl.ylabel('WD (deg)')
pl.subplot(323)
pl.plot(concat_sa.index,concat_sa.airt,'-o')
pl.ylim(0,35), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Air Temp (C)')
pl.subplot(324)
pl.plot(concat_sa.index,concat_sa.rh,'-o')
pl.ylim(0,100), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Rel. Humid')
pl.subplot(325)
pl.plot(concat_sa.index,concat_sa.pr,'-o')
pl.ylim(990,1030), pl.grid()
pl.ylabel('Pressure (hPa)')
pl.xlabel('Time (UTC)')
pl.xticks(rotation=18)
pl.subplot(326)
pl.plot(concat_sa.index,concat_sa.sst,'-o')
pl.ylim(15,35), pl.grid()
pl.ylabel('SST (deg)')
pl.xlabel('Time (UTC)')
pl.xticks(rotation=18)
pl.savefig(pathname + 'fig/meteo_sa.png')


#baia de guanabara
pl.figure(figsize=(11,9))
pl.subplot(321)
pl.plot(concat_bg.index,concat_bg.ws1,'b-o',concat_bg.index,concat_bg.wg1,'r--o')
pl.title('Santos - ' + str(concat_bg.index[-1])[:-9])
pl.ylim(0,20), pl.grid()
pl.xticks(visible=False)
pl.ylabel('WS, WG (m/s)')
pl.subplot(322)
pl.plot(concat_bg.index,concat_bg.wd1,'-o')
pl.title('Santos - ' + str(concat_bg.index[-1])[:-9])
pl.ylim(0,360), pl.grid()
pl.xticks(visible=False)
pl.ylabel('WD (deg)')
pl.subplot(323)
pl.plot(concat_bg.index,concat_bg.airt,'-o')
pl.ylim(0,35), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Air Temp (C)')
pl.subplot(324)
pl.plot(concat_bg.index,concat_bg.rh,'-o')
pl.ylim(0,100), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Rel. Humid')
pl.subplot(325)
pl.plot(concat_bg.index,concat_bg.pr,'-o')
pl.ylim(990,1030), pl.grid()
pl.ylabel('Pressure (hPa)')
pl.xlabel('Time (UTC)')
pl.xticks(rotation=18)
pl.subplot(326)
pl.plot(concat_bg.index,concat_bg.sst,'-o')
pl.ylim(15,35), pl.grid()
pl.ylabel('SST (deg)')
pl.xlabel('Time (UTC)')
pl.xticks(rotation=18)
pl.savefig(pathname + 'fig/meteo_bg.png')



#vitoria
pl.figure(figsize=(11,9))
pl.subplot(321)
pl.plot(concat_vi.index,concat_vi.ws1,'b-o',concat_vi.index,concat_vi.wg1,'r--o')
pl.title('Vitoria - ' + str(concat_vi.index[-1])[:-9])
pl.ylim(0,20), pl.grid()
pl.xticks(visible=False)
pl.ylabel('WS, WG (m/s)')
pl.subplot(322)
pl.plot(concat_vi.index,concat_vi.wd1,'-o')
pl.title('Vitoria - ' + str(concat_vi.index[-1])[:-9])
pl.ylim(0,360), pl.grid()
pl.xticks(visible=False)
pl.ylabel('WD (deg)')
pl.subplot(323)
pl.plot(concat_vi.index,concat_vi.airt,'-o')
pl.ylim(0,35), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Air Temp (C)')
pl.subplot(324)
pl.plot(concat_vi.index,concat_vi.rh,'-o')
pl.ylim(0,100), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Rel. Humid')
pl.subplot(325)
pl.plot(concat_vi.index,concat_vi.pr,'-o')
pl.ylim(990,1030), pl.grid()
pl.ylabel('Pressure (hPa)')
pl.xlabel('Time (UTC)')
pl.xticks(rotation=18)
pl.subplot(326)
pl.plot(concat_vi.index,concat_vi.sst,'-o')
pl.ylim(15,35), pl.grid()
pl.ylabel('SST (deg)')
pl.xlabel('Time (UTC)')
pl.xticks(rotation=18)
pl.savefig(pathname + 'fig/meteo_vi.png')


#porto seguro
pl.figure(figsize=(11,9))
pl.subplot(321)
pl.plot(concat_ps.index,concat_ps.ws1,'b-o',concat_ps.index,concat_ps.wg1,'r--o')
pl.title('Porto Seguro - ' + str(concat_ps.index[-1])[:-9])
pl.ylim(0,20), pl.grid()
pl.xticks(visible=False)
pl.ylabel('WS, WG (m/s)')
pl.subplot(322)
pl.plot(concat_ps.index,concat_ps.wd1,'-o')
pl.title('Porto Seguro - ' + str(concat_ps.index[-1])[:-9])
pl.ylim(0,360), pl.grid()
pl.xticks(visible=False)
pl.ylabel('WD (deg)')
pl.subplot(323)
pl.plot(concat_ps.index,concat_ps.airt,'-o')
pl.ylim(0,35), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Air Temp (C)')
pl.subplot(324)
pl.plot(concat_ps.index,concat_ps.rh,'-o')
pl.ylim(0,100), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Rel. Humid')
pl.subplot(325)
pl.plot(concat_ps.index,concat_ps.pr,'-o')
pl.ylim(990,1030), pl.grid()
pl.ylabel('Pressure (hPa)')
pl.xlabel('Time (UTC)')
pl.xticks(rotation=18)
pl.subplot(326)
pl.plot(concat_ps.index,concat_ps.sst,'-o')
pl.ylim(15,35), pl.grid()
pl.ylabel('SST (deg)')
pl.xlabel('Time (UTC)')
pl.xticks(rotation=18)
pl.savefig(pathname + 'fig/meteo_ps.png')



#recife
pl.figure(figsize=(11,9))
pl.subplot(321)
pl.plot(concat_re.index,concat_re.ws1,'b-o',concat_re.index,concat_re.wg1,'r--o')
pl.title('Recife - ' + str(concat_re.index[-1])[:-9])
pl.ylim(0,20), pl.grid()
pl.xticks(visible=False)
pl.ylabel('WS, WG (m/s)')
pl.subplot(322)
pl.plot(concat_re.index,concat_re.wd1,'-o')
pl.title('Recife - ' + str(concat_re.index[-1])[:-9])
pl.ylim(0,360), pl.grid()
pl.xticks(visible=False)
pl.ylabel('WD (deg)')
pl.subplot(323)
pl.plot(concat_re.index,concat_re.airt,'-o')
pl.ylim(0,35), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Air Temp (C)')
pl.subplot(324)
pl.plot(concat_re.index,concat_re.rh,'-o')
pl.ylim(0,100), pl.grid()
pl.xticks(visible=False)
pl.ylabel('Rel. Humid')
pl.subplot(325)
pl.plot(concat_re.index,concat_re.pr,'-o')
pl.ylim(990,1030), pl.grid()
pl.ylabel('Pressure (hPa)')
pl.xlabel('Time (UTC)')
pl.xticks(rotation=18)
pl.subplot(326)
pl.plot(concat_re.index,concat_re.sst,'-o')
pl.ylim(15,35), pl.grid()
pl.ylabel('SST (deg)')
pl.xlabel('Time (UTC)')
pl.xticks(rotation=18)
pl.savefig(pathname + 'fig/meteo_re.png')



#### gera boletim ####

#pathname_template = os.environ['HOME'] + '/Dropbox/pnboia/boletim/'
#os.system("cd " + pathname_template + " ; /usr/bin/pdflatex " + pathname_template + 'boletim_argos_PNBOIA.tex')




#pl.show()



