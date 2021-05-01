'''
Compara ww3 para o adcp01

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

pl.close('all')

############################################################################
#carrega dados processados pelo lioc a partir das planilhas processadas da vale

#diretorio de onde estao os dados processados
pathname  = os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/proc/parametros/'

#   0    1    2     3     4      5       6      7   8
# data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02'
ddv1 = np.loadtxt(pathname + 'adcp01_vale.out',delimiter=',')
ddv2 = np.loadtxt(pathname + 'adcp02_vale.out',delimiter=',')
ddv3 = np.loadtxt(pathname + 'adcp03_vale.out',delimiter=',')
ddv4 = np.loadtxt(pathname + 'adcp04_vale.out',delimiter=',')

#data com datetime
datat1vale = [datetime(int(str(ddv1[i,0])[0:4]),int(str(ddv1[i,0])[4:6]),int(str(ddv1[i,0])[6:8]),
    int(str(ddv1[i,0])[8:10]),int(str(ddv1[i,0])[10:12])) for i in range(len(ddv1))]
datat2vale = [datetime(int(str(ddv2[i,0])[0:4]),int(str(ddv2[i,0])[4:6]),int(str(ddv2[i,0])[6:8]),
    int(str(ddv2[i,0])[8:10]),int(str(ddv2[i,0])[10:12])) for i in range(len(ddv2))]
datat3vale = [datetime(int(str(ddv3[i,0])[0:4]),int(str(ddv3[i,0])[4:6]),int(str(ddv3[i,0])[6:8]),
    int(str(ddv3[i,0])[8:10]),int(str(ddv3[i,0])[10:12])) for i in range(len(ddv3))]
datat4vale = [datetime(int(str(ddv4[i,0])[0:4]),int(str(ddv4[i,0])[4:6]),int(str(ddv4[i,0])[6:8]),
    int(str(ddv4[i,0])[8:10]),int(str(ddv4[i,0])[10:12])) for i in range(len(ddv4))]

##############################################################################
# carrega resultado do WW3
pathname_mod = os.environ['HOME'] + '/Dropbox/ww3vale/TU/hindcast/resultados/'
direm = np.sort(os.listdir(pathname_mod))

#         0     1   2   3   4
# ddm = Data, hora, Hs, Fp, Dp -- calcula o Tp mais abaixo
ddm = np.array([[0,0,0,0,0]])
ddm1 = np.array([[0,0,0,0]]) #tp
ddm2 = np.array([[0,0,0,0]]) #tp

#loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
for dto in direm:

    #pula a primeira linha pois ja eh a mesma do ultima arquivo
	dadosm = np.loadtxt(pathname_mod + dto + '/tab51.ww3',skiprows=3,usecols=(0,1,4,9,10))
	ddm = np.concatenate((ddm,dadosm),axis=0)
	dadosm1 = np.loadtxt(pathname_mod + dto + '/swan1.out',skiprows=7,usecols=(0,1,3,2))
	ddm1 = np.concatenate((ddm1,dadosm1),axis=0)
	dadosm2 = np.loadtxt(pathname_mod + dto + '/swan2.out',skiprows=7,usecols=(0,1,3,2))
	ddm2 = np.concatenate((ddm2,dadosm2),axis=0)


ddm = ddm[1:,:]
ddm1 = ddm1[1:,:]
ddm2 = ddm2[1:,:]

#modelo
data_mod = ddm[:,0].astype(str) #ano mes
data_mod_day = ddm[:,1].astype(int)
datam = np.array([datetime(int(data_mod[i][0:4]),int(data_mod[i][4:6]),int(data_mod[i][6:8]),int(data_mod_day[i])) for i in range(len(data_mod))])

#modelo - data em AAAAMMDDHHMMSS
datami = np.array([str(int(ddm[i,0]))+str(int(data_mod_day[i])).zfill(2)+'00' for i in range(len(data_mod))])
datami = datami.astype(int)


###
#calculos dis indices estatisticos

local1 = 'adcp01swn2'
per = 'jul2013' #periodo para salvar o arquivo

#cria matriz de dados com as datas escolhidas
#adcp01
dini = pl.find(np.array(datat1vale).astype(str)=='2013-02-01 00:05:00') #data inicial - 2013-02-01 00:05:00
dfim = pl.find(np.array(datat1vale).astype(str)=='2014-02-11 00:05:00') #data final - 2014-02-11 00:05:00
ddv11 = ddv1[dini:dfim+1,:]

#modelo
dini = pl.find(np.array(datam).astype(str)=='2013-02-01 00:00:00')[0] #data inicial
dfim = pl.find(np.array(datam).astype(str)=='2014-02-11 00:00:00')[0] #data final
ddm11 = ddm2[dini:dfim+1,:]  ###modificar para cada grade do swan

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

# np.savetxt(local1 + '_' + per + '_estat_validacao.csv',est,delimiter=",",fmt='%2.2f')
# np.savetxt(local1 + '_' + per + '_estat_dados.csv',estat1,delimiter=",",fmt='%2.2f')
# np.savetxt(local1 + '_' + per + '_estat_modelo.csv',estat2,delimiter=",",fmt='%2.2f')


###


#figuras
fig = pl.figure()
ax = fig.add_subplot(311)
ax.plot(datat1vale[:],ddv1[:,1],'.b',datam[:],ddm[:,2],'.r',datam[:],ddm1[:,1],'.g',datam,ddm2[:,1],'.y')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
ax.set_ylabel('Hs (m)',fontsize=12), ax.grid()
ax.legend(['ADCP01','WW3','SWAN60X45','SWAN120X90'],loc='upper center',ncol=4)
ax.set_ylim(0,4)
ax.set_xlim(datam[dini],datam[dfim])


ax2 = fig.add_subplot(312)
ax2.plot(datat1vale[:],ddv1[:,7],'.b',datam[:],1./ddm[:,3],'.r',datam[:],ddm1[:,2],'.g',datam,ddm2[:,2],'.y')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
ax2.set_ylabel('Tp (s)',fontsize=12), pl.grid()
ax2.set_ylim(0,20)
ax2.set_xlim(datam[dini],datam[dfim])

ax3 = fig.add_subplot(313)
ax3.plot(datat1vale[:],ddv1[:,4],'.b',datam[:],ddm[:,4],'.r',datam[:],ddm1[:,3],'.g',datam,ddm2[:,3],'.y')
ax3.set_ylabel('Dp (graus)',fontsize=12), pl.grid()
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
ax3.set_ylim(0,360)
ax3.set_xlim(datam[dini],datam[dfim])


# fig = pl.figure()
# ax = fig.add_subplot(311)
# ax.plot(datat1vale,ddv1[:,1],datat3vale,ddv3[:,1])
# ax.set_ylabel('Hs (m)',fontsize=12), ax.grid()
# ax.legend(['ADCP01','ADCP03'])
# ax.set_ylim(0,4)
# ax.set_xlim(datam[dini],datam[dfim])
# ax2 = fig.add_subplot(312)
# ax2.plot(datat1vale,ddv1[:,7],'.',datat3vale,ddv3[:,7],'.')
# ax2.set_ylabel('Tp (s)',fontsize=12), pl.grid()
# ax2.set_ylim(0,20)
# ax2.set_xlim(datam[dini],datam[dfim])
# ax3 = fig.add_subplot(313)
# ax3.plot(datat1vale,ddv1[:,4],'.',datat3vale,ddv3[:,4],'.')
# ax3.set_ylabel('Dp (graus)',fontsize=12), pl.grid()
# ax3.set_ylim(0,360)
# ax3.set_xlim(datam[dini],datam[dfim])



pl.show()

