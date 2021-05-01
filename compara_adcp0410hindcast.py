'''
compara o hindcast de 2015 com os dados
do ADCP 04 e 10 operacional
'''

import os
import numpy as np
import pylab as pl
from datetime import datetime


#pl.close('all')

#############################################################################
#carrega dados dos ADCPs baixados operacionalmente (site)

pathname_site = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/ADCP/operacional/' 

#adcp - boia 4 e 10
adcp04 = 'TU_boia04.out' #dentro do porto
adcp10 = 'TU_boia10.out' #dentro do porto


# 0      1      2     3         4        5    6   7   8 9
#data,bateria,rumo,pressao,temperatura,pitch,roll,hs,tp,dp
dd04 = np.loadtxt(pathname_site + adcp04,delimiter=',')
dd10 = np.loadtxt(pathname_site + adcp10,delimiter=',')

dt04 = [ datetime.strptime(str(int(dd04[i,0])), '%Y%m%d%H%M') for i in range(len(dd04)) ]
dt10 = [ datetime.strptime(str(int(dd10[i,0])), '%Y%m%d%H%M') for i in range(len(dd10)) ]


#############################################################################
#carrega e concatena dados do hindcast

#diretorio de onde estao os resultados do ADCP01 (ADCP 04)
pathname1  = os.environ['HOME'] + '/Dropbox/ww3vale_hp/TU/hindcast/output/BES/'

#lista apenas os diretorios de 2015 (que tem o adcp 10)
direm1 = []
for f in np.sort(os.listdir(pathname1)):
	if f.startswith('2015'):
		direm1.append(f)


#diretorio de onde estao os resultados do ADCP10
pathname2  = os.environ['HOME'] + '/Dropbox/ww3vale_hp/TU/hindcast/output/VIX/'

#lista apenas os diretorios de 2015 (que tem o adcp 10)
direm2 = []
for f in np.sort(os.listdir(pathname2)):
	if f.startswith('2015'):
		direm2.append(f)


mm10=np.array([[0,0,0,0]])
mm04=np.array([[0,0,0,0]])  #vai ser pego do ADCP01

#loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
## ADCP 01 (ADCP 04)
for dto in direm1:

	madcp10 = np.loadtxt(pathname1 + dto + '/table_point_ADCP10.out',skiprows=7,usecols=(0,1,3,2))
	mm10 = np.concatenate((mm10,madcp10[:,:]),axis=0)

## ADCP 10
for dto in direm2:

	madcp04 = np.loadtxt(pathname2 + dto + '/table_point.out',skiprows=7,usecols=(0,1,3,2))
	mm04 = np.concatenate((mm04,madcp04[:,:]),axis=0)


#retira a primeira linha que eh zeros
mm10 = mm10[1:,:]
mm04 = mm04[1:,:]

#data do swan
dts10 = np.array([ datetime.strptime(str(mm10[i,0]*100),'%Y%m%d%H.0') for i in range(len(mm10)) ])
dts04 = np.array([ datetime.strptime(str(mm04[i,0]*100),'%Y%m%d%H.0') for i in range(len(mm04)) ])


#####################################################################
#realizar uma consistencia manual rapida dos dados para calcular
#as estatisticasdd04[aux,1:] = np.nan

#boia 04
aux = pl.find(dd04[:,9] > 300) #retira direcoes maiores que 300
dd04[aux,1:] = np.nan
aux = pl.find(dd04[:,7] < 0.5) #retira hs menor que 0.5
dd04[aux,1:] = np.nan
aux = pl.find(dd04[:,7] > 3.5) #retira hs maior que 0.5
dd04[aux,1:] = np.nan
dd04[range(1724,1840),1:] = np.nan #valores consecutivos iguais
dd04[range(2220,2710),1:] = np.nan #valores consecutivos iguais

#boia 10
aux = pl.find(dd10[:,9] > 300) #retira direcoes maiores que 300
dd10[aux,1:] = np.nan
aux = pl.find(dd10[:,7] > 2.2) #retira hs maior que 2.2
dd10[aux,1:] = np.nan
dd10[range(0,240),1:] = np.nan #valores consecutivos iguais
dd10[range(478,573),1:] = np.nan #valores consecutivos iguais
dd10[range(982,1073),1:] = np.nan #valores consecutivos iguais
dd10[range(1720,1842),1:] = np.nan #valores consecutivos iguais
dd10[range(2219,2710),1:] = np.nan #valores consecutivos iguais


#####################################################################


#figuras

pl.figure()
pl.subplot(311)
pl.title('ADCP 04 - Operacional')
pl.plot(dt04,dd04[:,7],'b.',dts04,mm04[:,1],'r')
pl.ylim(0,4), pl.grid()
pl.ylabel('Hs (m)')
pl.subplot(312)
pl.plot(dt04,dd04[:,8],'b.',dts04,mm04[:,2],'.r')
pl.ylim(0,20), pl.grid()
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(dt04,dd04[:,9],'b.',dts04,mm04[:,3],'.r')
pl.ylim(0,360), pl.grid()
pl.ylabel('Dp (graus)')
pl.yticks([0,45,90,135,180,225,270,315,360])


pl.figure()
pl.subplot(311)
pl.title('ADCP 10 - Operacional')
pl.plot(dt10,dd10[:,7],'b.',dts10,mm10[:,1],'r')
pl.ylim(0,4), pl.grid()
pl.ylabel('Hs (m)')
pl.subplot(312)
pl.plot(dt10,dd10[:,8],'b.',dts10,mm10[:,2],'.r')
pl.ylim(0,20), pl.grid()
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(dt10,dd10[:,9],'b.',dts10,mm10[:,3],'.r')
pl.ylim(0,360), pl.grid()
pl.ylabel('Dp (graus)')
pl.yticks([0,45,90,135,180,225,270,315,360])




######################################################################
#escolhe o adcp que vai calcular as estatisticas
ddv = dd10
dds = mm10
datav = dt10
datam = dts10

#cria matriz de dados com as datas escolhidas
#adcp01
dini = pl.find(np.array(datav).astype(str)=='2015-02-23 14:40:00') #colocar minuto 40 no adcp10 e 50 no adcp04
dfim = pl.find(np.array(datav).astype(str)=='2015-08-18 22:00:00') #data final - 2014-02-11 00:05:00
ddv11 = ddv[dini:dfim+1,:]

#modelo
dini = pl.find(np.array(datam).astype(str)=='2015-01-01 00:00:00')[0] #data inicial
dfim = pl.find(np.array(datam).astype(str)=='2015-08-01 00:00:00')[0] #data final
ddm11 = dds[dini:dfim+1,:]  ###modificar para cada grade do swan

#retira os dados com nan de cada variavel
indhs = np.where(np.isnan(ddv11[:,7]) == False)[0]
indtp = np.where(np.isnan(ddv11[:,8]) == False)[0]
inddp = np.where(np.isnan(ddv11[:,9]) == False)[0]

#define variaveis (sem nan e com o mesmo tamanho - utilizar para as estatisticas)
hs = ddv11[indhs,7]
hs_mod = ddm11[indhs,1]
tp = ddv11[indtp,8] 
# tp_mod = 1./ddm11[indtp,3] #transforma fp para tp (no caso do ww3)
tp_mod = ddm11[indtp,2] #swan
dp = ddv11[inddp,9]
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

# np.savetxt('estat_ADCP10OP_validacao.csv',est,delimiter=",",fmt='%2.2f')
# np.savetxt('estat_ADCP10OP_dados.csv',estat1,delimiter=",",fmt='%2.2f')
# np.savetxt('estat_ADCP10OP_modelo.csv',estat2,delimiter=",",fmt='%2.2f')








pl.show()
