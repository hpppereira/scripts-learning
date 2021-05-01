'''
Compara ww3 para o adcp e swan
Escolhe o ponto para comparar

LIOc - Laboratorio de Instrumentacao Oceanografica
Izabel C M Nogueira
Ricardo M Campos
Henrique P P Pereira
Isabel Cabral
Talitha Lourenco
Tamiris Alfama

Data da ultima modificacao: 14/08/2015
'''

import numpy as np
from datetime import datetime
import pylab as pl
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import os
import matplotlib.dates as mdates
import pandas as pd

pl.close('all')

############################################################################
#carrega dados processados pelo lioc a partir das planilhas processadas da vale

#diretorio de onde estao os dados processados
pathnamea  = os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/proc/parametros/'

#   0    1    2     3     4      5       6      7   8
# data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02'
ddv1 = np.loadtxt(pathnamea + 'adcp01_vale.out',delimiter=',')
ddv2 = np.loadtxt(pathnamea + 'adcp02_vale.out',delimiter=',')
ddv3 = np.loadtxt(pathnamea + 'adcp03_vale.out',delimiter=',')
ddv4 = np.loadtxt(pathnamea + 'adcp04_vale.out',delimiter=',')

#filtro com media movel (hs, tp e dp)
w = 3
ddv1[:,1] = pd.rolling_mean(ddv1[:,1],w)
ddv1[:,2] = pd.rolling_mean(ddv1[:,2],w)
ddv1[:,3] = pd.rolling_mean(ddv1[:,3],w)
ddv2[:,1] = pd.rolling_mean(ddv2[:,1],w)
ddv2[:,2] = pd.rolling_mean(ddv2[:,2],w)
ddv2[:,3] = pd.rolling_mean(ddv2[:,3],w)
ddv3[:,1] = pd.rolling_mean(ddv3[:,1],w)
ddv3[:,2] = pd.rolling_mean(ddv3[:,2],w)
ddv3[:,3] = pd.rolling_mean(ddv3[:,3],w)
ddv4[:,1] = pd.rolling_mean(ddv4[:,1],w)
ddv4[:,2] = pd.rolling_mean(ddv4[:,2],w)
ddv4[:,3] = pd.rolling_mean(ddv4[:,3],w)


#data com datetime
dtv1 = [datetime.strptime(str(int(ddv1[i,0])),'%Y%m%d%H%M') for i in range(len(ddv1))]
dtv2 = [datetime.strptime(str(int(ddv2[i,0])),'%Y%m%d%H%M') for i in range(len(ddv2))]
dtv3 = [datetime.strptime(str(int(ddv3[i,0])),'%Y%m%d%H%M') for i in range(len(ddv3))]
dtv4 = [datetime.strptime(str(int(ddv4[i,0])),'%Y%m%d%H%M') for i in range(len(ddv4))]

##############################################################################
# carrega resultado do SWAN
pathnamebes = os.environ['HOME'] + '/Dropbox/ww3vale_info/TU/hindcast/output/BES/'
pathnamevix = os.environ['HOME'] + '/Dropbox/ww3vale_info/TU/hindcast/output/VIX/'

#dirbes = np.sort(os.listdir(pathnamebes))
dirbes = []
for f in np.sort(os.listdir(pathnamebes)):
	if f.startswith('2013'):
		dirbes.append(f)

#dirvix = np.sort(os.listdir(pathnamevix))
dirvix = []
for f in np.sort(os.listdir(pathnamevix)):
	if f.startswith('2013'):
		dirvix.append(f)


#         0   1    2  3 
# ddm = Data, Hs, Tp, Dp 
dds1 = np.array([[0,0,0,0]])
dds2 = np.array([[0,0,0,0]])
dds3 = np.array([[0,0,0,0]])
dds4 = np.array([[0,0,0,0]])

#loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
for dto in dirbes:

	dds11 = np.loadtxt(pathnamevix + dto + '/table_point_ADCP01.out',skiprows=7,usecols=(0,1,3,2))
	dds1 = np.concatenate((dds1,dds11),axis=0)

	dds22 = np.loadtxt(pathnamebes + dto + '/table_point_ADCP02.out',skiprows=7,usecols=(0,1,3,2))
	dds2 = np.concatenate((dds2,dds22),axis=0)

	dds33 = np.loadtxt(pathnamebes + dto + '/table_point_ADCP03.out',skiprows=7,usecols=(0,1,3,2))
	dds3 = np.concatenate((dds3,dds33),axis=0)

	dds44 = np.loadtxt(pathnamebes + dto + '/table_point_ADCP04.out',skiprows=7,usecols=(0,1,3,2))
	dds4 = np.concatenate((dds4,dds44),axis=0)

#pula a primeira linha pois ja eh a mesma do ultima arquivo
dds1 = dds1[1:,:]
dds2 = dds2[1:,:]
dds3 = dds3[1:,:]
dds4 = dds4[1:,:]

#data
dts1 = np.array([ datetime.strptime(str(dds1[i,0]*100),'%Y%m%d%H.0') for i in range(len(dds1)) ])
dts2 = np.array([ datetime.strptime(str(dds2[i,0]*100),'%Y%m%d%H.0') for i in range(len(dds2)) ])
dts3 = np.array([ datetime.strptime(str(dds3[i,0]*100),'%Y%m%d%H.0') for i in range(len(dds3)) ])
dts4 = np.array([ datetime.strptime(str(dds4[i,0]*100),'%Y%m%d%H.0') for i in range(len(dds4)) ])


#################################################################################
#figuras

pl.figure(figsize=(12,8))
pl.subplot(311)
pl.title('ADCP-01')
pl.plot(dtv1,ddv1[:,1],'b')
pl.plot(dts1,dds1[:,1],'r')
pl.xlim(dts1[0],dts1[-1]), pl.grid()
pl.ylabel('Hs (m)')
pl.subplot(312)
pl.plot(dtv1,ddv1[:,7],'.b')
pl.plot(dts1,dds1[:,2],'.r')
pl.xlim(dts1[0],dts1[-1]), pl.grid()
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(dtv1,ddv1[:,4],'.b')
pl.plot(dts1,dds1[:,3],'.r')
pl.xlim(dts1[0],dts1[-1]), pl.grid()
pl.ylabel('Dp (graus)')
pl.yticks([0,45,90,135,180,225,270,315,360])
pl.legend(['ADCP','SWAN'],loc='upper center',ncol=2,bbox_to_anchor=(0.5, -0.105))

pl.figure(figsize=(12,8))
pl.subplot(311)
pl.title('ADCP-02')
pl.plot(dtv2,ddv2[:,1],'b')
pl.plot(dts2,dds2[:,1],'r')
pl.xlim(dts2[0],dts2[-1]), pl.grid()
pl.ylabel('Hs (m)')
pl.subplot(312)
pl.plot(dtv2,ddv2[:,7],'.b')
pl.plot(dts2,dds2[:,2],'.r')
pl.xlim(dts2[0],dts2[-1]), pl.grid()
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(dtv2,ddv2[:,4],'.b')
pl.plot(dts2,dds2[:,3],'.r')
pl.xlim(dts2[0],dts2[-1]), pl.grid()
pl.ylabel('Dp (graus)')
pl.yticks([0,45,90,135,180,225,270,315,360])
pl.legend(['ADCP','SWAN'],loc='upper center',ncol=2,bbox_to_anchor=(0.5, -0.105))


pl.figure(figsize=(12,8))
pl.subplot(311)
pl.title('ADCP-03')
pl.plot(dtv3,ddv3[:,1],'b')
pl.plot(dts3,dds3[:,1],'r')
pl.xlim(dts3[0],dts3[-1]), pl.grid()
pl.ylabel('Hs (m)')
pl.subplot(312)
pl.plot(dtv3,ddv3[:,7],'.b')
pl.plot(dts3,dds3[:,2],'.r')
pl.xlim(dts3[0],dts3[-1]), pl.grid()
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(dtv3,ddv3[:,4],'.b')
pl.plot(dts3,dds3[:,3],'.r')
pl.xlim(dts3[0],dts3[-1]), pl.grid()
pl.ylabel('Dp (graus)')
pl.yticks([0,45,90,135,180,225,270,315,360])
pl.legend(['ADCP','SWAN'],loc='upper center',ncol=2,bbox_to_anchor=(0.5, -0.105))


pl.figure(figsize=(12,8))
pl.subplot(311)
pl.title('ADCP-04')
pl.plot(dtv4,ddv4[:,1],'b')
pl.plot(dts4,dds4[:,1],'r')
pl.xlim(dts4[0],dts4[-1]), pl.grid()
pl.ylabel('Hs (m)')
pl.subplot(312)
pl.plot(dtv4,ddv4[:,7],'.b')
pl.plot(dts4,dds4[:,2],'.r')
pl.xlim(dts4[0],dts4[-1]), pl.grid()
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(dtv4,ddv4[:,4],'.b')
pl.plot(dts4,dds4[:,3],'.r')
pl.xlim(dts4[0],dts4[-1]), pl.grid()
pl.ylabel('Dp (graus)')
pl.yticks([0,45,90,135,180,225,270,315,360])
pl.legend(['ADCP','SWAN'],loc='upper center',ncol=2,bbox_to_anchor=(0.5, -0.105))


######################################################################
#escolhe o adcp que vai calcular as estatisticas
ddv = ddv3
dds = dds3
datav = dtv3
datam = dts3

#cria matriz de dados com as datas escolhidas
#adcp01
dini = pl.find(np.array(datav).astype(str)=='2013-01-20 00:05:00') #data inicial - 2013-02-20 00:05:00
dfim = pl.find(np.array(datav).astype(str)=='2013-12-31 23:05:00') #data final - 2014-02-11 00:05:00
ddv11 = ddv[dini:dfim+1,:]

#modelo
dini = pl.find(np.array(datam).astype(str)=='2013-01-01 00:00:00')[0] #data inicial
dfim = pl.find(np.array(datam).astype(str)=='2013-12-31 00:00:00')[0] #data final
ddm11 = dds[dini:dfim+1,:]  ###modificar para cada grade do swan

#retira os dados com nan de cada variavel
indhs = np.where(np.isnan(ddv11[:,1]) == False)[0]
indtp = np.where(np.isnan(ddv11[:,7]) == False)[0]
inddp = np.where(np.isnan(ddv11[:,4]) == False)[0]

#define variaveis (sem nan e com o mesmo tamanho - utilizar para as estatisticas)
hs = ddv11[indhs,1]
hs_mod = ddm11[indhs,1]
tp = ddv11[indtp,7] 
# tp_mod = 1./ddm11[indtp,3] #transforma fp para tp (no caso do ww3)
tp_mod = ddm11[indtp,2] #swan
dp = ddv11[inddp,4]
dp_mod = ddm11[inddp,3]


#calculo das estatisticas entre modelo e cacimbas

### BIAS ###
#hs
bias_hs = np.mean(hs_mod - hs)
#tp
bias_tp = np.mean(tp_mod - tp)
#dp
bias_dp = np.mean(dp_mod - dp)

### ERMS ###
#hs
rmse_hs = np.sqrt( pl.sum( (hs_mod - hs) ** 2 ) / len(hs) )
#tp
rmse_tp = np.sqrt( pl.sum( (tp_mod - tp) ** 2 ) / len(tp) )
#hs
rmse_dp = np.sqrt( pl.sum( (dp_mod - dp) ** 2 ) / len(dp) )

### SI ###
#hs
si_hs = rmse_hs / np.mean(hs)
#tp
si_tp = rmse_tp / np.mean(tp)
#dp
si_dp = rmse_dp / np.mean(dp)


### Correlacao ###
#hs
corr_hs = np.corrcoef(hs_mod,hs)[0,1]
#tp
corr_tp = np.corrcoef(tp_mod,tp)[0,1]
#dp
corr_dp = np.corrcoef(dp_mod,dp)[0,1]

### media boia ###
mean_adcp_hs = np.mean(hs)
mean_adcp_tp = np.mean(tp)
mean_adcp_dp = np.mean(dp)
### media modelo ###
mean_mod_hs = np.mean(hs_mod)
mean_mod_tp = np.mean(tp_mod)
mean_mod_dp = np.mean(dp_mod)

### maximo boia ###
max_adcp_hs = np.max(hs)
max_adcp_tp = np.max(tp)
max_adcp_dp = np.max(dp)
### maximo modelo ###
max_mod_hs = np.max(hs_mod)
max_mod_tp = np.max(tp_mod)
max_mod_dp = np.max(dp_mod)

# estatistica (matriz est)
# ---------------------------------------------
# Hs | BIAS   | RMSE    | SI      | CORR
# Tp | BIAS   | RMSE    | SI      | CORR
# Dp | BIAS   | RMSE    | SI      | CORR
# Hs | Med Obs| Med Mod | Max Obs | Max Mod
# Tp | Med Obs| Med Mod | Max Obs | Max Mod
# Dp | Med Obs| Med Mod | Max Obs | Max Mod

#estatistica 1 (hs, tp, dp) estat_dados.csv
# Hs  | Med | DesPad | Min | P90 | Max
# Tp  | Med | DesPad | Min | P90 | Max
# Dp  | Med | DesPad | Min | P90 | Max

estat1 = np.zeros((3,5))
estat1[0,0] = np.mean(hs)
estat1[1,0] = np.mean(tp)
estat1[2,0] = np.mean(dp)
estat1[0,1] = np.std(hs)
estat1[1,1] = np.std(tp)
estat1[2,1] = np.std(dp)
estat1[0,2] = np.min(hs)
estat1[1,2] = np.min(tp)
estat1[2,2] = np.min(dp)
estat1[0,3] = np.percentile(hs,90)
estat1[1,3] = np.percentile(tp,90)
estat1[2,3] = np.percentile(dp,90)
estat1[0,4] = np.max(hs)
estat1[1,4] = np.max(tp)
estat1[2,4] = np.max(dp)

#estatistica 2 (hs, tp, dp) estat_modelo.csv
# Hs  | Med | DesPad | Min | P90 | Max
# Tp  | Med | DesPad | Min | P90 | Max
# Dp  | Med | DesPad | Min | P90 | Max

estat2 = np.zeros((3,5))
estat2[0,0] = np.mean(hs_mod)
estat2[1,0] = np.mean(tp_mod)
estat2[2,0] = np.mean(dp_mod)
estat2[0,1] = np.std(hs_mod)
estat2[1,1] = np.std(tp_mod)
estat2[2,1] = np.std(dp_mod)
estat2[0,2] = np.min(hs_mod)
estat2[1,2] = np.min(tp_mod)
estat2[2,2] = np.min(dp_mod)
estat2[0,3] = np.percentile(hs_mod,90)
estat2[1,3] = np.percentile(tp_mod,90)
estat2[2,3] = np.percentile(dp_mod,90)
estat2[0,4] = np.max(hs_mod)
estat2[1,4] = np.max(tp_mod)
estat2[2,4] = np.max(dp_mod)
# perc90[0,1] = np.percentile(hs_mod,90)
# perc90[1,1] = np.percentile(tp_mod,90)
# perc90[2,1] = np.percentile(dp_mod,90)

est=np.zeros((6,4))
est[0,0]=bias_hs
est[1,0]=bias_tp
est[2,0]=bias_dp
est[3,0]=mean_adcp_hs
est[4,0]=mean_adcp_tp
est[5,0]=mean_adcp_dp
est[0,1]=rmse_hs
est[1,1]=rmse_tp
est[2,1]=rmse_dp
est[3,1]=mean_mod_hs
est[4,1]=mean_mod_tp
est[5,1]=mean_mod_dp
est[0,2]=si_hs
est[1,2]=si_tp
est[2,2]=si_dp
est[3,2]=max_adcp_hs
est[4,2]=max_adcp_tp
est[5,2]=max_adcp_dp
est[0,3]=corr_hs
est[1,3]=corr_tp
est[2,3]=corr_dp
est[3,3]=max_mod_hs
est[4,3]=max_mod_tp
est[5,3]=max_mod_dp

# np.savetxt('estat_validacao.csv',est,delimiter=",",fmt='%2.2f')
# np.savetxt('estat_dados.csv',estat1,delimiter=",",fmt='%2.2f')
# np.savetxt('estat_modelo.csv',estat2,delimiter=",",fmt='%2.2f')



pl.show()

