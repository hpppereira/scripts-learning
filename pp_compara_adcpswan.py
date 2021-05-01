'''
Comparacao dos parametros de ondas calculados
pela Vale (planilhas), pelo lioc (dados brutos)
e os resultados do SWAN

Data da ultima modificacao: 15/07/2015

'''

import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pylab as pl
import os
from datetime import datetime


plt.close('all')

pathname_lioc = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/rot/out/bruto/parametros/'
pathname_vale  = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/rot/out/proc/parametros/'
pathname_swan = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/hindcast/ADCP/201304/'

#carrega dados processados pelo lioc
#  0    1     2    3   4   5 
# data, hs, hmax, hm0, tp, dp
ddl1 = np.loadtxt(pathname_lioc + 'lioc_adcp1.out',delimiter=',')
ddl2 = np.loadtxt(pathname_lioc + 'lioc_adcp2.out',delimiter=',')
ddl3 = np.loadtxt(pathname_lioc + 'lioc_adcp3.out',delimiter=',')
ddl4 = np.loadtxt(pathname_lioc + 'lioc_adcp4.out',delimiter=',')

# datas com datetime
datal1 = np.array([ datetime.strptime(str(int(ddl1[i,0])), '%Y%m%d%H%M') for i in range(len(ddl1)) ])
datal2 = np.array([ datetime.strptime(str(int(ddl2[i,0])), '%Y%m%d%H%M') for i in range(len(ddl2)) ])
datal3 = np.array([ datetime.strptime(str(int(ddl3[i,0])), '%Y%m%d%H%M') for i in range(len(ddl3)) ])
datal4 = np.array([ datetime.strptime(str(int(ddl4[i,0])), '%Y%m%d%H%M') for i in range(len(ddl4)) ])

#carrega parametros de ondas dos dados processados pela vale
#   0    1    2     3     4      5       6      7   8
# data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02'
ddv1 = np.loadtxt(pathname_vale + 'vale_adcp1.out',delimiter=',')
ddv2 = np.loadtxt(pathname_vale + 'vale_adcp2.out',delimiter=',')
ddv3 = np.loadtxt(pathname_vale + 'vale_adcp3.out',delimiter=',')
ddv4 = np.loadtxt(pathname_vale + 'vale_adcp4.out',delimiter=',')

#data com datetime
datav1 = np.array([ datetime.strptime(str(int(ddv1[i,0])), '%Y%m%d%H%M') for i in range(len(ddv1)) ])
datav2 = np.array([ datetime.strptime(str(int(ddv2[i,0])), '%Y%m%d%H%M') for i in range(len(ddv2)) ])
datav3 = np.array([ datetime.strptime(str(int(ddv3[i,0])), '%Y%m%d%H%M') for i in range(len(ddv3)) ])
datav4 = np.array([ datetime.strptime(str(int(ddv4[i,0])), '%Y%m%d%H%M') for i in range(len(ddv4)) ])

#correcao da direcao - convencao (+90) e declinacao magnetica (-23.5)
corr = + 90 - 23.5

ddl1[:,5] = ddl1[:,5] + corr
ddl2[:,5] = ddl2[:,5] + corr
ddl3[:,5] = ddl3[:,5] + corr
ddl4[:,5] = ddl4[:,5] + corr

ddl1[pl.find(ddl1[:,5] > 360)] = ddl1[pl.find(ddl1[:,5] > 360)] - 360
ddl2[pl.find(ddl2[:,5] > 360)] = ddl2[pl.find(ddl2[:,5] > 360)] - 360
ddl3[pl.find(ddl3[:,5] > 360)] = ddl3[pl.find(ddl3[:,5] > 360)] - 360
ddl4[pl.find(ddl4[:,5] > 360)] = ddl4[pl.find(ddl4[:,5] > 360)] - 360

#carrega parametros de ondas dos dados processados pela vale
#  0    1     2       3       4        5        6       7       
#Time, Hsig, PkDir, RTpeak, X-Windv, Y-Windv, Hswell, Dspr
# [ ]   [m]  [degr]  [sec]     [m/s], [m/s],    [m],  [degr]

swn1 = np.loadtxt(pathname_swan + 'table_point_ADCP01.out',comments='%')
swn2 = np.loadtxt(pathname_swan + 'table_point_ADCP02.out',comments='%')
swn3 = np.loadtxt(pathname_swan + 'table_point_ADCP03.out',comments='%')
swn4 = np.loadtxt(pathname_swan + 'table_point_ADCP04.out',comments='%')

#data com datetime
datas1 = np.array([ datetime.strptime(str(swn1[i,0]*100),'%Y%m%d%H.0') for i in range(len(swn1)) ])
datas2 = np.array([ datetime.strptime(str(swn2[i,0]*100),'%Y%m%d%H.0') for i in range(len(swn2)) ])
datas3 = np.array([ datetime.strptime(str(swn3[i,0]*100),'%Y%m%d%H.0') for i in range(len(swn3)) ])
datas4 = np.array([ datetime.strptime(str(swn4[i,0]*100),'%Y%m%d%H.0') for i in range(len(swn4)) ])


############################################################################
#figuras


###correca para > 360 
#limitar janela para plotagem
ini = pl.find(datal1.astype(str) == '2013-04-01 00:00:00')[0]
fim = pl.find(datal1.astype(str) == '2013-04-30 23:00:00')[0]

#ADCP 1
plt.figure()
plt.subplot(311)
plt.title('ADCP 1')
plt.plot(datal1,ddl1[:,3],'.b',label='lioc')
plt.plot(datav1,ddv1[:,1],'.r',label='vale')
plt.plot(datas1,swn1[:,1],'.g',label='swan')
plt.legend(ncol=3,loc=0)
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,3)
plt.xticks(visible=False)
plt.ylabel('Hm0 (m)'), plt.grid('on')
plt.subplot(312)
plt.plot(datal1,ddl1[:,4],'.b',label='lioc')
plt.plot(datav1,ddv1[:,7],'.r',label='vale')
plt.plot(datas1,swn1[:,3],'.g',label='swan')
plt.ylabel('Tp (s)'), plt.grid('on')
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,20)
plt.xticks(visible=False)
plt.subplot(313)
plt.plot(datal1,ddl1[:,5],'.b',label='lioc')
plt.plot(datav1,ddv1[:,4],'.r',label='vale')
plt.plot(datas1,swn1[:,2],'.g',label='swan')
plt.ylabel('Dp (graus)'), plt.grid('on')
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,360)
plt.xticks(visible=True)

#ADCP 2
plt.figure()
plt.subplot(311)
plt.title('ADCP 2')
plt.plot(datal2,ddl2[:,3],'.b',label='lioc')
plt.plot(datav2,ddv2[:,1],'.r',label='vale')
plt.plot(datas2,swn2[:,1],'.g',label='swan')
plt.legend(ncol=3,loc=0)
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,3)
plt.xticks(visible=False)
plt.ylabel('Hm0 (m)'), plt.grid('on')
plt.subplot(312)
plt.plot(datal2,ddl2[:,4],'.b',label='lioc')
plt.plot(datav2,ddv2[:,7],'.r',label='vale')
plt.plot(datas2,swn2[:,3],'.g',label='swan')
plt.ylabel('Tp (s)'), plt.grid('on')
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,20)
plt.xticks(visible=False)
plt.subplot(313)
plt.plot(datal2,ddl2[:,5],'.b',label='lioc')
plt.plot(datav2,ddv2[:,4],'.r',label='vale')
plt.plot(datas2,swn2[:,2],'.g',label='swan')
plt.ylabel('Dp (graus)'), plt.grid('on')
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,360)
plt.xticks(visible=True)


#ADCP 3
plt.figure()
plt.subplot(311)
plt.title('ADCP 3')
plt.plot(datal3,ddl3[:,3],'.b',label='lioc')
plt.plot(datav3,ddv3[:,1],'.r',label='vale')
plt.plot(datas3,swn3[:,1],'.g',label='swan')
plt.legend(ncol=3,loc=0)
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,3)
plt.xticks(visible=False)
plt.ylabel('Hm0 (m)'), plt.grid('on')
plt.subplot(312)
plt.plot(datal3,ddl3[:,4],'.b',label='lioc')
plt.plot(datav3,ddv3[:,7],'.r',label='vale')
plt.plot(datas3,swn3[:,3],'.g',label='swan')
plt.xlabel('Tp (s)'), plt.grid('on')
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,20)
plt.xticks(visible=False)
plt.subplot(313)
plt.plot(datal3,ddl3[:,5],'.b',label='lioc')
plt.plot(datav3,ddv3[:,4],'.r',label='vale')
plt.plot(datas3,swn3[:,2],'.g',label='swan')
plt.xlabel('Dp (graus)'), plt.grid('on')
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,360)
plt.xticks(visible=True)

#ADCP 4
plt.figure()
plt.subplot(311)
plt.title('ADCP 4')
plt.plot(datal4,ddl4[:,3],'.b',label='lioc')
plt.plot(datav4,ddv4[:,1],'.r',label='vale')
plt.plot(datas4,swn4[:,1],'.g',label='swan')
plt.legend()
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,3)
plt.xticks(visible=False)
plt.ylabel('Hm0 (m)'), plt.grid('on')
plt.subplot(312)
plt.plot(datal4,ddl4[:,4],'.b',label='lioc')
plt.plot(datav4,ddv4[:,7],'.r',label='vale')
plt.plot(datas4,swn4[:,3],'.g',label='swan')
plt.ylabel('Tp (s)'), plt.grid('on')
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,20)
plt.xticks(visible=False)
plt.subplot(313)
plt.plot(datal4,ddl4[:,5],'.b',label='lioc')
plt.plot(datav4,ddv4[:,4],'.r',label='vale')
plt.plot(datas4,swn4[:,2],'.g',label='swan')
plt.ylabel('Dp (graus)'), plt.grid('on')
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,360)
plt.xticks(visible=True)






plt.show()
