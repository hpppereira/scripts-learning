'''
Calcula estatisticas entre os dados e o resultado do modelo
'''

import numpy as np
import os
from datetime import datetime
import pylab as pl

# escolha o dado: cacimbas ou bc10 ou Merenda
name='cacimbas'

pathname_cac= os.environ['HOME'] + '/Dropbox/ww3es/Geral/rot/saida/' + name
pathname_ww3= os.environ['HOME'] + '/Dropbox/ww3es/Geral/rot/saida/ww3' + name

#data, hs, tp, dp
cac = np.loadtxt(pathname_cac + '/param_8_'+name+'.out',delimiter=',')
ww3 = np.loadtxt(pathname_ww3 + '/param_8_ww3'+name+'.out',delimiter=',')

#data em datetime
datac = np.array([datetime.strptime(str(int(cac[i,0])), '%Y%m%d%H%M%S') for i in range(len(cac))])
dataw = np.array([datetime.strptime(str(int(ww3[i,0])), '%Y%m%d%H%M%S') for i in range(len(ww3))])


#acha no modelo apenas as datas que tem dados (deixa o vetor do modelo do mesmo comprimento do dado)
nest = np.zeros(len(cac)) #vetor de zeros do tamanho dos dados 
datas_cac = datac.astype(str)
datas_ww3 = dataw.astype(str)

for idata in range(len(datas_cac)):
	nest[idata] = np.where(datas_ww3 == datas_cac[idata])[0]

nest = nest.astype(int)

ww3 = ww3[nest]
dataw = dataw[nest]


#retira os dados com nan de cada variavel
indhs = np.where(np.isnan(cac[:,1]) == False)[0]
indtp = np.where(np.isnan(cac[:,2]) == False)[0]
inddp = np.where(np.isnan(cac[:,3]) == False)[0]

#define variaveis (sem nan e com o mesmo tamanho - utilizar para as estatisticas)
hs = cac[indhs,1]
hs_mod = ww3[indhs,1]
tp = cac[indtp,2]
tp_mod = ww3[indtp,2]
dp = cac[inddp,3]
dp_mod = ww3[inddp,3]

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
np.savetxt(name + 'estat_validacao.csv',est,delimiter=",",fmt='%2.2f')
np.savetxt(name + 'estat_dados.csv',estat1,delimiter=",",fmt='%2.2f')
np.savetxt(name + 'estat_modelo.csv',estat2,delimiter=",",fmt='%2.2f')

# scatter plot 
xi=hs
y=hs_mod
coefficients = np.polyfit(xi, y, 1)
polynomial = np.poly1d(coefficients) 
ys = polynomial(xi) 
pl.figure()
pl.subplot(3,1,1)
pl.plot(xi, y, '.')
pl.plot(xi, ys, 'r--')
pl.plot(range(0,7),range(0,7),'k')
pl.grid()
pl.xlabel('Hs (m) medido')
pl.ylabel('Hs (m) modelado')

xi=tp
y=tp_mod
coefficients = np.polyfit(xi, y, 1)
polynomial = np.poly1d(coefficients) 
ys = polynomial(xi) 
pl.subplot(3,1,2)
pl.plot(xi, y, '.')
pl.plot(xi, ys, 'r--')
pl.plot(range(0,21),range(0,21),'k')
pl.grid()
pl.xlabel('Tp (s) medido')
pl.ylabel('Tp (s) modelado')

xi=dp
y=dp_mod
coefficients = np.polyfit(xi, y, 1)
polynomial = np.poly1d(coefficients) 
ys = polynomial(xi) 
pl.subplot(3,1,3)
pl.plot(xi, y, '.')
pl.plot(xi, ys, 'r--')
pl.plot(range(0,250),range(0,250),'k')
pl.xlim(0,250)
pl.ylim(0,250)
#pl.axis('equal')
pl.grid()
pl.xlabel('Dp (graus) medido')
pl.ylabel('Dp (graus) modelado')
pl.show()