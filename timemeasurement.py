'''
Grafico com periodos de medicoes das boias

dados de entrada: ano, mes, dia, hora
*matriz de parametros calculados
'''

import numpy as np
from datetime import datetime
import os
import matplotlib.pylab as pl

# pl.close('all')

#carrega arquivos 'lista'

pathname = os.environ['HOME'] + '/Dropbox/tese/rot/out/'

#  0  1   2  3  4  5  6  7  8  9 10
#date,ws,wg,wd,at,rh,pr,wt,hs,tp,dp
re = np.loadtxt(pathname + 'argos_opendap_cq_recife.out',delimiter=',') 
# ac = np.loadtxt(pathname + 'siodoc_janis_arraial_cabo.out',delimiter=',') 
sa = np.loadtxt(pathname + 'argos_opendap_cq_santos.out',delimiter=',') 
fl = np.loadtxt(pathname + 'argos_opendap_cq_florianopolis.out',delimiter=',') 
rg = np.loadtxt(pathname + 'argos_opendap_cq_rio_grande.out',delimiter=',') 

#consistencia manual
re[1995:6995,1:] = np.nan ; re[11411:15932,1:] = np.nan
fl[2352:4118,1:] = np.nan #florianopolis

#plotar apenas os dados consistentes
re = re[pl.find(np.isnan(re[:,1])==False),:]
sa = sa[pl.find(np.isnan(sa[:,1])==False),:]
fl = fl[pl.find(np.isnan(fl[:,1])==False),:]
rg = rg[pl.find(np.isnan(rg[:,1])==False),:]


#triaxys
rew = np.loadtxt(pathname + 'triaxys_cp_8_recife.out',delimiter=',') 
saw = np.loadtxt(pathname + 'triaxys_cp_8_santos.out',delimiter=',') 
flw = np.loadtxt(pathname + 'triaxys_cp_8_florianopolis.out',delimiter=',') 
rgw = np.loadtxt(pathname + 'triaxys_cp_8_rio_grande.out',delimiter=',') 

#plotar apenas os dados consistentes
rew = rew[pl.find(np.isnan(rew[:,1])==False),:]
saw = saw[pl.find(np.isnan(saw[:,1])==False),:]
flw = flw[pl.find(np.isnan(flw[:,1])==False),:]
rgw = rgw[pl.find(np.isnan(rgw[:,1])==False),:]


#datas
dre = np.array([datetime.strptime(str(int(re[i,0])), '%Y%m%d%H%M') for i in range(len(re))])
# dac = np.array([datetime.strptime(str(int(ac[i,0])), '%Y%m%d%H%M') for i in range(len(ac))])
dsa = np.array([datetime.strptime(str(int(sa[i,0])), '%Y%m%d%H%M') for i in range(len(sa))])
dfl = np.array([datetime.strptime(str(int(fl[i,0])), '%Y%m%d%H%M') for i in range(len(fl))])
drg = np.array([datetime.strptime(str(int(rg[i,0])), '%Y%m%d%H%M') for i in range(len(rg))])

#datas triaxys
drew = np.array([datetime.strptime(str(int(rew[i,0])), '%Y%m%d%H%M') for i in range(len(rew))])
dsaw = np.array([datetime.strptime(str(int(saw[i,0])), '%Y%m%d%H%M') for i in range(len(saw))])
dflw = np.array([datetime.strptime(str(int(flw[i,0])), '%Y%m%d%H%M') for i in range(len(flw))])
drgw = np.array([datetime.strptime(str(int(rgw[i,0])), '%Y%m%d%H%M') for i in range(len(rgw))])

#valores para plotagem
vre = np.linspace(4,4,len(re))
# vac = np.linspace(4,4,len(ac))
vsa = np.linspace(3,3,len(sa))
vfl = np.linspace(2,2,len(fl))
vrg = np.linspace(1,1,len(rg))

#valores para plotagem - triaxys
vrew = np.linspace(3.75,3.75,len(rew))
vsaw = np.linspace(2.75,2.75,len(saw))
vflw = np.linspace(1.75,1.75,len(flw))
vrgw = np.linspace(0.75,0.75,len(rgw))


pl.figure(); pl.hold('on')
# pl.title('Periodo medicao das boias meteo-oceanograficas - PNBOIA',fontsize=18)
pl.plot(dre,vre,'b.',markersize=25)
pl.plot(drew,vrew,'b.',markersize=15,label='Recife')
# pl.plot(dac,vac,'m.',markersize=25)
pl.plot(dsa,vsa,'r.',markersize=25)
pl.plot(dsaw,vsaw,'r.',markersize=15,label='Santos')
pl.plot(dfl,vfl,'g.',markersize=25)
pl.plot(dflw,vflw,'g.',markersize=15,label='Florian')
pl.plot(drg,vrg,'k.',markersize=25)
pl.plot(drgw,vrgw,'k.',markersize=15,label='RioGrande')

pl.xticks(rotation=0,fontsize=14)
pl.yticks(visible=False)
pl.xlabel('Data',fontsize=18)
pl.legend(loc=0,fontsize=18)
pl.ylim([0,4.75])
pl.grid('on')
pl.hold('off')

#xlim([731217  734139]); ylim([0 6]); grid();

pl.show()
