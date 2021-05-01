'''
Calcula estatisticas entre os dados da axys
e o ww3 para o projeto SEAL

Os dados para ser carregados estao em dataframe
com 'date, hs, tp e dp'
'''

import pandas as pd
import numpy as np
import os

pathname = os.environ['HOME'] + '/Dropbox/ww3seal/rot/out/'

#carrega os dados do ponto da triaxys - dado e modelo

#date, hs, tp , dp
dfax = pd.read_csv(pathname + 'axys.csv', parse_dates=['date'])
dfaxm = pd.read_csv(pathname + 'axys_mod.csv', parse_dates=['date'])

med = {}
p90 = {}
maxi = {}
bias = {}
rmse = {}
si = {}
corr = {}

bias['hs'] = np.mean((dfaxm.hs - dfax.hs))
bias['tp'] = np.mean((dfaxm.tp - dfax.tp))
bias['dp'] = np.mean((dfaxm.dp - dfax.dp))

rmse['hs'] = np.sqrt( np.sum( (dfaxm.hs - dfax.hs) ** 2 ) / len(dfax) )
rmse['tp'] = np.sqrt( np.sum( (dfaxm.tp - dfax.tp) ** 2 ) / len(dfax) )
rmse['dp'] = np.sqrt( np.sum( (dfaxm.dp - dfax.dp) ** 2 ) / len(dfax) )

si['hs'] = rmse['hs'] / np.mean(dfax.hs)
si['tp'] = rmse['tp'] / np.mean(dfax.tp)
si['dp'] = rmse['dp'] / np.mean(dfax.dp)

corr['hs'] = np.corrcoef(dfaxm.hs,dfax.hs)[0,1]
corr['tp'] = np.corrcoef(dfaxm.tp,dfax.tp)[0,1]
corr['dp'] = np.corrcoef(dfaxm.dp,dfax.dp)[0,1]

med['hs'] = np.mean(dfax.hs)
med['tp'] = np.mean(dfax.tp)
med['dp'] = np.mean(dfax.dp)

p90['hs'] = np.percentile(dfax.hs,90)
p90['tp'] = np.percentile(dfax.tp,90)
p90['dp'] = np.percentile(dfax.dp,90)

maxi['hs'] = np.max(dfax.hs)
maxi['tp'] = np.max(dfax.tp)
maxi['dp'] = np.max(dfax.dp)