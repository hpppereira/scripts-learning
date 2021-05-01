'''
Compara os dados brutos processados pelo lioc,
os dados processados pela vale e os resultados do SWAN
e do WW3

- Atualmente esta comparando os meses de fev e jul modelados
pelo SWAN e WW3
- Desconta a declinacao magnetica nos dados brutos do ADCP
- Os dados processados pela Vale ja tem a declinacao descontada

Autores:
Izabel C. M. Nogueira
Henrique P. P. Pereira

Data da ultima modificacao: 03/06/2015
'''

import numpy as np
from datetime import datetime
import pylab as pl
import os

pl.close('all')

############################################################################
#carrega dados processados pelo lioc a partir dos dados brutos

pathname = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/rot/out/bruto/parametros/'

#  0    1    2    3     4   5  
# data, hs, hmax, hm0, tp, dp
ddl1 = np.loadtxt(pathname + 'lioc_adcp1.out',delimiter=',')
ddl2 = np.loadtxt(pathname + 'lioc_adcp2.out',delimiter=',')
ddl3 = np.loadtxt(pathname + 'lioc_adcp3.out',delimiter=',')
ddl4 = np.loadtxt(pathname + 'lioc_adcp4.out',delimiter=',')

# data com datetime
datat1lioc = [datetime(int(str(ddl1[i,0])[0:4]),int(str(ddl1[i,0])[4:6]),int(str(ddl1[i,0])[6:8]),
    int(str(ddl1[i,0])[8:10]),int(str(ddl1[i,0])[10:12])) for i in range(len(ddl1))]
datat2lioc = [datetime(int(str(ddl2[i,0])[0:4]),int(str(ddl2[i,0])[4:6]),int(str(ddl2[i,0])[6:8]),
    int(str(ddl2[i,0])[8:10]),int(str(ddl2[i,0])[10:12])) for i in range(len(ddl2))]
datat3lioc = [datetime(int(str(ddl3[i,0])[0:4]),int(str(ddl3[i,0])[4:6]),int(str(ddl3[i,0])[6:8]),
    int(str(ddl3[i,0])[8:10]),int(str(ddl3[i,0])[10:12])) for i in range(len(ddl3))]
datat4lioc = [datetime(int(str(ddl4[i,0])[0:4]),int(str(ddl4[i,0])[4:6]),int(str(ddl4[i,0])[6:8]),
    int(str(ddl4[i,0])[8:10]),int(str(ddl4[i,0])[10:12])) for i in range(len(ddl4))]

#correcao da declinacao magnetica
dmag = -23.5
ddl1[:,5] = ddl1[:,5] + 90 + dmag
ddl2[:,5] = ddl2[:,5] + 90 + dmag
ddl3[:,5] = ddl3[:,5] + 90 + dmag
ddl4[:,5] = ddl4[:,5] + 90 + dmag

#corrige valores
ddl1[pl.find(ddl1[:,5]>360),5] = ddl1[pl.find(ddl1[:,5]>360),5] - 360
ddl1[pl.find(ddl1[:,5]<0),5] = ddl1[pl.find(ddl1[:,5]<0),5] + 360

ddl2[pl.find(ddl2[:,5]>360),5] = ddl2[pl.find(ddl2[:,5]>360),5] - 360
ddl2[pl.find(ddl2[:,5]<0),5] = ddl2[pl.find(ddl2[:,5]<0),5] + 360

ddl3[pl.find(ddl3[:,5]>360),5] = ddl3[pl.find(ddl3[:,5]>360),5] - 360
ddl3[pl.find(ddl3[:,5]<0),5] = ddl3[pl.find(ddl3[:,5]<0),5] + 360

ddl4[pl.find(ddl4[:,5]>360),5] = ddl4[pl.find(ddl4[:,5]>360),5] - 360
ddl4[pl.find(ddl4[:,5]<0),5] = ddl4[pl.find(ddl4[:,5]<0),5] + 360


############################################################################
#carrega dados processados pelo lioc a partir das planilhas processadas da vale

#diretorio de onde estao os dados processados
pathname  = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/rot/out/proc/parametros/'

#   0    1    2     3     4      5       6      7   8
# data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02'
ddv1 = np.loadtxt(pathname + 'vale_adcp1.out',delimiter=',')
ddv2 = np.loadtxt(pathname + 'vale_adcp2.out',delimiter=',')
ddv3 = np.loadtxt(pathname + 'vale_adcp3.out',delimiter=',')
ddv4 = np.loadtxt(pathname + 'vale_adcp4.out',delimiter=',')

#data com datetime
datat1vale = [datetime(int(str(ddv1[i,0])[0:4]),int(str(ddv1[i,0])[4:6]),int(str(ddv1[i,0])[6:8]),
    int(str(ddv1[i,0])[8:10]),int(str(ddv1[i,0])[10:12])) for i in range(len(ddv1))]
datat2vale = [datetime(int(str(ddv2[i,0])[0:4]),int(str(ddv2[i,0])[4:6]),int(str(ddv2[i,0])[6:8]),
    int(str(ddv2[i,0])[8:10]),int(str(ddv2[i,0])[10:12])) for i in range(len(ddv2))]
datat3vale = [datetime(int(str(ddv3[i,0])[0:4]),int(str(ddv3[i,0])[4:6]),int(str(ddv3[i,0])[6:8]),
    int(str(ddv3[i,0])[8:10]),int(str(ddv3[i,0])[10:12])) for i in range(len(ddv3))]
datat4vale = [datetime(int(str(ddv4[i,0])[0:4]),int(str(ddv4[i,0])[4:6]),int(str(ddv4[i,0])[6:8]),
    int(str(ddv4[i,0])[8:10]),int(str(ddv4[i,0])[10:12])) for i in range(len(ddv4))]

############################################################################
#carrega dados do ww3

#Saida WW3
# 0   1   2    3   4   5  6  7   8
#ano,mes,dia,hora,min,hs,tp,dp,spread

wadcp01_fev = np.loadtxt(os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/hindcast/resultados/201302/tab51.ww3',skiprows=3,usecols=(0,1,4,9,10))
wadcp01_jul = np.loadtxt(os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/hindcast/resultados/201307/tab51.ww3',skiprows=3,usecols=(0,1,4,9,10))

#modelo
data_wadcp01_fev = wadcp01_fev[:,0].astype(str) #ano mes
data_wadcp01_day = wadcp01_fev[:,1].astype(int)
datam_wadcp01_fev = np.array([datetime(int(data_wadcp01_fev[i][0:4]),int(data_wadcp01_fev[i][4:6]),int(data_wadcp01_fev[i][6:8]),int(data_wadcp01_day[i])) for i in range(len(data_wadcp01_day))])

data_wadcp01_jul = wadcp01_jul[:,0].astype(str) #ano mes
data_wadcp01_day = wadcp01_jul[:,1].astype(int)
datam_wadcp01_jul = np.array([datetime(int(data_wadcp01_jul[i][0:4]),int(data_wadcp01_jul[i][4:6]),int(data_wadcp01_jul[i][6:8]),int(data_wadcp01_day[i])) for i in range(len(data_wadcp01_day))])


############################################################################
#carrega dados do swan 

#  0    1     2       3       4        5        6       7       
#Time, Hsig, PkDir, RTpeak, X-Windv, Y-Windv, Hswell, Dspr
# [ ]   [m]  [degr]  [sec]     [m/s], [m/s],    [m],  [degr]

# sadcp03_fev = np.loadtxt(os.environ['HOME'] + '/Dropbox/ww3vale/Trocas/TestesSWAN/Configuracao7/201302/table_point_ADCP03.out',comments='%')
# sadcp03_jul = np.loadtxt(os.environ['HOME'] + '/Dropbox/ww3vale/Trocas/TestesSWAN/Configuracao7/201307/table_point_ADCP03.out',comments='%')

# datam_sadcp03_fev = []
# for i in range(len(sadcp03_fev)):
# 	datam_sadcp03_fev.append(datetime(int(str(sadcp03_fev[i,0])[0:4]), int(str(sadcp03_fev[i,0])[4:6]), \
# 		int(str(sadcp03_fev[i,0])[6:8]),int(str(sadcp03_fev[i,0])[9:11]) ))

# datam_sadcp03_jul = []
# for i in range(len(sadcp03_jul)):
# 	datam_sadcp03_jul.append(datetime(int(str(sadcp03_jul[i,0])[0:4]), int(str(sadcp03_jul[i,0])[4:6]), \
# 		int(str(sadcp03_jul[i,0])[6:8]),int(str(sadcp03_jul[i,0])[9:11]) ))


############################################################################
# plotagem adcp 01

pl.figure()
pl.subplot(321)
pl.title('ADCP-1 - Fev/2013')
pl.plot(datat1lioc,ddl1[:,3],'b.',label='lioc')
pl.plot(datat1vale,ddv1[:,1],'r.',label='vale')
pl.plot(datam_wadcp01_fev,wadcp01_fev[:,2],'g.',label='ww3')
pl.plot(datam_wadcp01_jul,wadcp01_jul[:,2],'g.')
pl.legend(loc=0,fontsize=10)
pl.ylabel('Hs (m)'), pl.grid()
pl.xlim(datam_wadcp01_fev[0],datam_wadcp01_fev[-1]), pl.ylim(0,3)
pl.xticks(rotation=10,visible=False)
pl.subplot(323)
pl.plot(datat1lioc,ddl1[:,4],'b.')
pl.plot(datat1vale,ddv1[:,7],'r.')
pl.plot(datam_wadcp01_fev,1./wadcp01_fev[:,3],'g.')
pl.plot(datam_wadcp01_jul,1./wadcp01_jul[:,3],'g.')
pl.ylabel('Tp (s)'), pl.grid()
pl.xlim(datam_wadcp01_fev[0],datam_wadcp01_fev[-1]), pl.ylim(2,18)
pl.xticks(rotation=10,visible=False)
pl.subplot(325)
pl.plot(datat1lioc,ddl1[:,5],'b.')
pl.plot(datat1vale,ddv1[:,4],'r.')
pl.plot(datam_wadcp01_fev,wadcp01_fev[:,4],'g.',)
pl.plot(datam_wadcp01_jul,wadcp01_jul[:,4],'g.')
pl.ylabel('Dp (graus)'), pl.grid()
pl.xlim(datam_wadcp01_fev[0],datam_wadcp01_fev[-1]), pl.ylim(0,250)
pl.xticks(rotation=15)


pl.subplot(322)
pl.title('ADCP-1 - Jul/2013')
pl.plot(datat1lioc,ddl1[:,3],'b.',label='lioc')
pl.plot(datat1vale,ddv1[:,1],'r.',label='vale')
pl.plot(datam_wadcp01_fev,wadcp01_fev[:,2],'g.',label='ww3')
pl.plot(datam_wadcp01_jul,wadcp01_jul[:,2],'g.')
pl.grid()
pl.xlim(datam_wadcp01_jul[0],datam_wadcp01_jul[-1]), pl.ylim(0,3)
pl.xticks(rotation=10,visible=False)
pl.subplot(324)
pl.plot(datat1lioc,ddl1[:,4],'b.')
pl.plot(datat1vale,ddv1[:,7],'r.')
pl.plot(datam_wadcp01_fev,1./wadcp01_fev[:,3],'g.')
pl.plot(datam_wadcp01_jul,1./wadcp01_jul[:,3],'g.')
pl.grid()
pl.xlim(datam_wadcp01_jul[0],datam_wadcp01_jul[-1]), pl.ylim(2,18)
pl.xticks(rotation=10,visible=False)
pl.subplot(326)
pl.plot(datat1lioc,ddl1[:,5],'b.')
pl.plot(datat1vale,ddv1[:,4],'r.')
pl.plot(datam_wadcp01_fev,wadcp01_fev[:,4],'g.')
pl.plot(datam_wadcp01_jul,wadcp01_jul[:,4],'g.')
pl.grid()
pl.xlim(datam_wadcp01_jul[0],datam_wadcp01_jul[-1]), pl.ylim(0,250)
pl.xticks(rotation=15)



############################################################################
# plotagem adcp 03 - swan

pl.figure()
pl.subplot(321)
pl.title('ADCP-3 - Fev/2013')
pl.plot(datat3lioc,ddl3[:,3],'b.',label='lioc')
pl.plot(datat3vale,ddv3[:,1],'r.',label='vale')
#pl.plot(datam_sadcp03_fev,sadcp03_fev[:,1],'g.',label='swan')
pl.legend(loc=0,fontsize=10)
pl.ylabel('Hs (m)'), pl.grid()
pl.xlim(datam_wadcp01_fev[0],datam_wadcp01_fev[-1]), pl.ylim(0,3)
pl.xticks(rotation=10,visible=False)
pl.subplot(323)
pl.plot(datat3lioc,ddl3[:,4],'b.')
pl.plot(datat3vale,ddv3[:,7],'r.')
#pl.plot(datam_sadcp03_fev,sadcp03_fev[:,3],'g.')
pl.ylabel('Tp (s)'), pl.grid()
pl.xlim(datam_wadcp01_fev[0],datam_wadcp01_fev[-1]), pl.ylim(2,18)
pl.xticks(rotation=10,visible=False)
pl.subplot(325)
pl.plot(datat3lioc,ddl3[:,5],'b.')
pl.plot(datat3vale,ddv3[:,4],'r.')
#pl.plot(datam_sadcp03_fev,sadcp03_fev[:,2],'g.')
pl.ylabel('Dp (graus)'), pl.grid()
pl.xlim(datam_wadcp01_fev[0],datam_wadcp01_fev[-1]), pl.ylim(0,250)
pl.xticks(rotation=15)


pl.subplot(322)
pl.title('ADCP-3 - Jul/2013')
pl.plot(datat3lioc,ddl3[:,3],'b.',label='lioc')
pl.plot(datat3vale,ddv3[:,1],'r.',label='vale')
#pl.plot(datam_sadcp03_jul,sadcp03_jul[:,1],'g.',label='swan')
pl.grid()
pl.xlim(datam_wadcp01_jul[0],datam_wadcp01_jul[-1]), pl.ylim(0,3)
pl.xticks(rotation=10,visible=False)
pl.subplot(324)
pl.plot(datat3lioc,ddl3[:,4],'b.')
pl.plot(datat3vale,ddv3[:,7],'r.')
#pl.plot(datam_sadcp03_jul,sadcp03_jul[:,3],'g.')
pl.grid()
pl.xlim(datam_wadcp01_jul[0],datam_wadcp01_jul[-1]), pl.ylim(2,18)
pl.xticks(rotation=10,visible=False)
pl.subplot(326)
pl.plot(datat3lioc,ddl3[:,5],'b.')
pl.plot(datat3vale,ddv3[:,4],'r.')
#pl.plot(datam_sadcp03_jul,sadcp03_jul[:,2],'g.')
pl.grid()
pl.xlim(datam_wadcp01_jul[0],datam_wadcp01_jul[-1]), pl.ylim(0,250)
pl.xticks(rotation=15)


pl.show()