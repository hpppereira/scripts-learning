"""
calcula media das profundidades do ctd
"""

import pandas as pd
import numpy as np

# leitura dos arquivos

d = {'perfil1': [],
     'perfil2': [],
     'perfil3': []}

prof_max = 13.5

df1 = pd.DataFrame()
for f in list(d.keys()):

    print (f)

    df2 = pd.read_csv(f+'.csv', header=0, names=['depth','temp','sal'], index_col='depth')

    df1 = pd.concat([df1, df2], axis=1)


df = pd.DataFrame(index=df2.index)
df['temp'] = df1['temp'].mean(axis=1)
df['sal'] = df1['sal'].mean(axis=1)

df = df[:13.5]

df.to_csv('ctd_mean.csv', float_format='%.2f')


# se ate a coluna q tem dados

#     # calculo do valor medio por profundidade
#     profs_max.append(int(df.index.max().round()))
#
#     #cria arqivs medios
#     # arq_med = []
#     for p in range(profs_max[-1]):
#         # print (d)
#         med = df.loc[(df.index > p) & (df.index < p+1)].mean()
#         d[f].append([int(p+1), med.temp, med.sal])
#
#
#
#
# # salva arquivos .csv com prof max idem a menor profundidade dos 3 arquivos
# for f in list(d.keys()):
#
#     a = pd.DataFrame(np.array(d[f])[:np.min(profs_max)], columns=['depth','temp','sal'])
#     a = a.set_index('depth')
#     a.to_csv(f+'_mean.csv', float_format='%.2f')
#
#     # np.savetxt(f+'.txt', a, header='depth temp sal', fmt=['%i', '%.2f', '%.2f'])
#
#
#     # acha valor maximo de profundidade
#         # print (med)
