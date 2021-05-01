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


#plt.close('all')

pathname_lioc = os.environ['HOME'] + '/Dropbox/ww3vale_hp/TU/rot/out/bruto/parametros/'
pathname_vale  = os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/proc/parametros/'
pathname_swan = os.environ['HOME'] + '/Dropbox/ww3vale/TU/hindcast/ADCP/201304/'

#carrega dados processados pelo lioc (escolher vel, vel1 (inverte vx e vy) ou ast (ast eh sem _))
#  0    1     2    3   4   5 
# data, hs, hmax, hm0, tp, dp
ddl1 = np.loadtxt(pathname_lioc + 'adcp01_lioc.out',delimiter=',')
ddl2 = np.loadtxt(pathname_lioc + 'adcp02_lioc.out',delimiter=',')
ddl3 = np.loadtxt(pathname_lioc + 'adcp03_lioc.out',delimiter=',')
ddl4 = np.loadtxt(pathname_lioc + 'adcp04_lioc.out',delimiter=',')

ddl1 = np.loadtxt(pathname_lioc + 'adcp01_lioc_vel.out',delimiter=',')
ddl2 = np.loadtxt(pathname_lioc + 'adcp02_lioc_vel.out',delimiter=',')
ddl3 = np.loadtxt(pathname_lioc + 'adcp03_lioc_vel.out',delimiter=',')
ddl4 = np.loadtxt(pathname_lioc + 'adcp04_lioc_vel.out',delimiter=',')

# ddl1 = np.loadtxt(pathname_lioc + 'adcp01_lioc_vel1.out',delimiter=',')
# ddl2 = np.loadtxt(pathname_lioc + 'adcp02_lioc_vel1.out',delimiter=',')
# ddl3 = np.loadtxt(pathname_lioc + 'adcp03_lioc_vel1.out',delimiter=',')
# ddl4 = np.loadtxt(pathname_lioc + 'adcp04_lioc_vel1.out',delimiter=',')


# datas com datetime
datal1 = np.array([ datetime.strptime(str(int(ddl1[i,0])), '%Y%m%d%H%M') for i in range(len(ddl1)) ])
datal2 = np.array([ datetime.strptime(str(int(ddl2[i,0])), '%Y%m%d%H%M') for i in range(len(ddl2)) ])
datal3 = np.array([ datetime.strptime(str(int(ddl3[i,0])), '%Y%m%d%H%M') for i in range(len(ddl3)) ])
datal4 = np.array([ datetime.strptime(str(int(ddl4[i,0])), '%Y%m%d%H%M') for i in range(len(ddl4)) ])

#carrega parametros de ondas dos dados processados pela vale
#   0    1    2     3     4      5       6      7   8
# data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02'
ddv1 = np.loadtxt(pathname_vale + 'adcp01_vale.out',delimiter=',')
ddv2 = np.loadtxt(pathname_vale + 'adcp02_vale.out',delimiter=',')
ddv3 = np.loadtxt(pathname_vale + 'adcp03_vale.out',delimiter=',')
ddv4 = np.loadtxt(pathname_vale + 'adcp04_vale.out',delimiter=',')

#data com datetime
datav1 = np.array([ datetime.strptime(str(int(ddv1[i,0])), '%Y%m%d%H%M') for i in range(len(ddv1)) ])
datav2 = np.array([ datetime.strptime(str(int(ddv2[i,0])), '%Y%m%d%H%M') for i in range(len(ddv2)) ])
datav3 = np.array([ datetime.strptime(str(int(ddv3[i,0])), '%Y%m%d%H%M') for i in range(len(ddv3)) ])
datav4 = np.array([ datetime.strptime(str(int(ddv4[i,0])), '%Y%m%d%H%M') for i in range(len(ddv4)) ])

#correcao da direcao - convencao (+90) e declinacao magnetica (-23.5)
corr = -23

ddl1[:,5] = ddl1[:,5] + corr - 180 #ambiguidade de 180 em parte do registro
ddl2[:,5] = ddl2[:,5] + corr - 23 #parece que a declinacao foi descontada no equipamento e no pos proc (2 vezes)
ddl3[:,5] = ddl3[:,5] + corr + 90 + 23 #ambiguidade de 180 em parte do registro e sem correcao mag
ddl4[:,5] = ddl4[:,5] + corr - 180 + 23

ddl1[pl.find(ddl1[:,5] > 360)] = ddl1[pl.find(ddl1[:,5] > 360)] - 360
ddl2[pl.find(ddl2[:,5] > 360)] = ddl2[pl.find(ddl2[:,5] > 360)] - 360
ddl3[pl.find(ddl3[:,5] > 360)] = ddl3[pl.find(ddl3[:,5] > 360)] - 360
ddl4[pl.find(ddl4[:,5] > 360)] = ddl4[pl.find(ddl4[:,5] > 360)] - 360

ddl1[pl.find(ddl1[:,5] < 0)] = ddl1[pl.find(ddl1[:,5] < 0)] + 360
ddl2[pl.find(ddl2[:,5] < 0)] = ddl2[pl.find(ddl2[:,5] < 0)] + 360
ddl3[pl.find(ddl3[:,5] < 0)] = ddl3[pl.find(ddl3[:,5] < 0)] + 360
ddl4[pl.find(ddl4[:,5] < 0)] = ddl4[pl.find(ddl4[:,5] < 0)] + 360


###correcoes de ambiguidade
ddl1[pl.find(ddl1[:,5] > 250)] = ddl1[pl.find(ddl1[:,5] > 250)] - 180
# ddl2[pl.find(ddl2[:,5] < 0)] = ddl2[pl.find(ddl2[:,5] < 0)] + 360
ddl3[pl.find(ddl3[:,5] > 200)] = ddl3[pl.find(ddl3[:,5] > 200)] - 90 - 23
ddl4[pl.find(ddl4[:,5] > 150)] = ddl4[pl.find(ddl4[:,5] > 150)] - 90 - 45


#carrega parametros de ondas dos so swan
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

# ini = pl.find(datal1.astype(str) == '2013-01-19 19:00:00')[0]
# fim = pl.find(datal1.astype(str) == '2014-02-12 13:00:00')[0]

# ini = 0
# fim = 2421

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
pl.yticks([0,45,90,135,180,225,270,315,360])
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
pl.yticks([0,45,90,135,180,225,270,315,360])


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
pl.yticks([0,45,90,135,180,225,270,315,360])

#ADCP 4
plt.figure()
plt.subplot(311)
plt.title('ADCP 4')
plt.plot(datal4,ddl4[:,3],'.b',label='lioc')
plt.plot(datav4,ddv4[:,1],'.r',label='vale')
plt.plot(datas4,swn4[:,1],'.g',label='swan')
plt.legend(ncol=3,loc=0)
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
pl.yticks([0,45,90,135,180,225,270,315,360])

#direcoes
pl.figure()
pl.subplot(411)
pl.title('Direcao de Pico')
plt.plot(datal1,ddl1[:,5],'.b',label='lioc')
plt.plot(datav1,ddv1[:,4],'.r',label='vale')
plt.plot(datas1,swn1[:,2],'.g',label='swan')
plt.ylabel('ADCP 01'), plt.grid('on')
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,360)
plt.xticks(visible=False)
pl.yticks([0,45,90,135,180,225,270,315,360])
pl.legend(['lioc','planilha','swan'],ncol=3,loc=0)
pl.subplot(412)
plt.plot(datal2,ddl2[:,5],'.b',label='lioc')
plt.plot(datav2,ddv2[:,4],'.r',label='vale')
plt.plot(datas2,swn2[:,2],'.g',label='swan')
plt.ylabel('ADCP 02'), plt.grid('on')
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,360)
plt.xticks(visible=False)
pl.yticks([0,45,90,135,180,225,270,315,360])
pl.subplot(413)
plt.plot(datal3,ddl3[:,5],'.b',label='lioc')
plt.plot(datav3,ddv3[:,4],'.r',label='vale')
plt.plot(datas3,swn3[:,2],'.g',label='swan')
plt.ylabel('ADCP 03'), plt.grid('on')
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,360)
plt.xticks(visible=False)
pl.yticks([0,45,90,135,180,225,270,315,360])
pl.subplot(414)
plt.plot(datal4,ddl4[:,5],'.b',label='lioc')
plt.plot(datav4,ddv4[:,4],'.r',label='vale')
plt.plot(datas4,swn4[:,2],'.g',label='swan')
plt.ylabel('ADCP 04'), plt.grid('on')
plt.xlim(datal1[ini],datal1[fim]), plt.ylim(0,360)
plt.xticks(visible=True)
pl.yticks([0,45,90,135,180,225,270,315,360])

#direcoes
pl.figure()
pl.subplot(411)
pl.title('Direcao de Pico')
plt.plot(datav1,ddv1[:,4],'.r',label='planilha')
plt.ylabel('ADCP 01'), plt.grid('on')
plt.xticks(visible=False), plt.ylim(0,360)
pl.yticks([0,45,90,135,180,225,270,315,360])
pl.legend()
pl.subplot(412)
plt.plot(datav2,ddv2[:,4],'.r',label='vale')
plt.ylabel('ADCP 02'), plt.grid('on')
plt.xticks(visible=False), plt.ylim(0,360)
pl.yticks([0,45,90,135,180,225,270,315,360])
pl.subplot(413)
plt.plot(datav3,ddv3[:,4],'.r',label='vale')
plt.ylabel('ADCP 03'), plt.grid('on')
plt.xticks(visible=False), plt.ylim(0,360)
pl.yticks([0,45,90,135,180,225,270,315,360])
pl.subplot(414)
plt.plot(datav4,ddv4[:,4],'.r',label='vale')
plt.ylabel('ADCP 04'), plt.grid('on')
plt.xticks(visible=True), plt.ylim(0,360)
pl.yticks([0,45,90,135,180,225,270,315,360])

plt.show()
