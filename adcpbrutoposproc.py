'''
pos processamento dos dados da vale dos dados brutos
processados pelo LIOc

LIOc - Laboratorio de Instrumentacao Oceanografica
Henrique P P Pereira
Izabel C M Nogueira
Isabel Cabral
Talitha Lourenco
Tamiris Alfama

Ultima modificacao: 14/08/2015
'''

import numpy as np
from datetime import datetime
import pylab as pl
import os

#  0    1     2    3   4   5 
# data, hs, hmax, hm0, tp, dp

pathname = os.environ['HOME'] + '/Dropbox/ww3vale_hp/TU/rot/out/bruto/parametros/'

dd1 = np.loadtxt(pathname + 'adcp01_lioc_vel1.out',delimiter=',')
dd2 = np.loadtxt(pathname + 'adcp02_lioc_vel1.out',delimiter=',')
dd3 = np.loadtxt(pathname + 'adcp03_lioc_vel1.out',delimiter=',')
dd4 = np.loadtxt(pathname + 'adcp04_lioc_vel1.out',delimiter=',')

dd1 = np.loadtxt(pathname + 'adcp01_lioc.out',delimiter=',')
dd2 = np.loadtxt(pathname + 'adcp02_lioc.out',delimiter=',')
dd3 = np.loadtxt(pathname + 'adcp03_lioc.out',delimiter=',')
dd4 = np.loadtxt(pathname + 'adcp04_lioc.out',delimiter=',')

# datas com datetime

data1 = [ datetime.strptime(str(int(dd1[i,0])), '%Y%m%d%H%M') for i in range(len(dd1)) ]
data2 = [ datetime.strptime(str(int(dd2[i,0])), '%Y%m%d%H%M') for i in range(len(dd2)) ]
data3 = [ datetime.strptime(str(int(dd3[i,0])), '%Y%m%d%H%M') for i in range(len(dd3)) ]
data4 = [ datetime.strptime(str(int(dd4[i,0])), '%Y%m%d%H%M') for i in range(len(dd4)) ]


pl.figure()
pl.subplot(311)
pl.title('ADCP-1')
pl.plot(data1,dd1[:,1],'o',label='Hs')
pl.plot(data1,dd1[:,3],'o',label='Hm0')
pl.plot(data1,dd1[:,2],'o',label='Hmax')
pl.legend()
pl.subplot(312)
pl.plot(data1,dd1[:,4],'o',label='Tp')
pl.legend()
pl.subplot(313)
pl.plot(data1,dd1[:,5],'o',label='Dp')
pl.legend()	

pl.figure()
pl.subplot(311)
pl.title('ADCP-2')
pl.plot(data2,dd2[:,1],'o',label='Hs')
pl.plot(data2,dd2[:,3],'o',label='Hm0')
pl.plot(data2,dd2[:,2],'o',label='Hmax')
pl.legend()
pl.subplot(312)
pl.plot(data2,dd2[:,4],'o',label='Tp')
pl.legend()
pl.subplot(313)
pl.plot(data2,dd2[:,5],'o',label='Dp')
pl.legend()	

pl.figure()
pl.subplot(311)
pl.title('ADCP-3')
pl.plot(data3,dd3[:,1],'o',label='Hs')
pl.plot(data3,dd3[:,3],'o',label='Hm0')
pl.plot(data3,dd3[:,2],'o',label='Hmax')
pl.legend()
pl.subplot(312)
pl.plot(data3,dd3[:,4],'o',label='Tp')
pl.legend()
pl.subplot(313)
pl.plot(data3,dd3[:,5],'o',label='Dp')
pl.legend()	

pl.figure()
pl.subplot(311)
pl.title('ADCP-4')
pl.plot(data4,dd4[:,1],'o',label='Hs')
pl.plot(data4,dd4[:,3],'o',label='Hm0')
pl.plot(data4,dd4[:,2],'o',label='Hmax')
pl.legend()
pl.subplot(312)
pl.plot(data4,dd4[:,4],'o',label='Tp')
pl.legend()
pl.subplot(313)
pl.plot(data4,dd4[:,5],'o',label='Dp')
pl.legend()	

pl.show()