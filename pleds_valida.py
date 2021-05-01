"""
Processamento dos dados da boia do MERENDA do ES
e do espectro do modelo do WW3 para fazer a PLEDS
da diferenca

VMTA Momento Espectral de Ordem 0
VTPK Periodo de Pico Espectral
VPED Direcao Espectral
Para obter Hs usar 4.01*sqrt(VMTA) ou 4.01*sqrt(VMTA1)

"""

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from waveproc import WaveProc

# ---------------------------------------------------------------------------- #
# Dados de entrada

# Processa dados brutos de onda e cria arquivo csv com parametros (True) ou 
# le os dados do arquivo csv gerado (False). arquivo apenas cm hs, tp e dp
proc_raw = True

pathname = os.environ['HOME'] + '/GoogleDrive/AGES/data/boia_merenda/brutos/'


# ---------------------------------------------------------------------------- #
# Leitura dos dados processados da boia

dateparse = lambda x: pd.datetime.strptime(x, '%d %m %Y %H %M')

out = pd.read_table(pathname + 'saida.out', sep='\t', parse_dates=[[0,1]],
                    date_parser=dateparse, index_col=0)


out.index.name = 'date'
out['hm0'] = 4.01 * np.sqrt(out['  VMTA'])
out['tp'] = out['           VTPK']
out['dp'] = out['  VPED']


# ---------------------------------------------------------------------------- #
# Leitura dos dados processados por essa rotina

if proc_raw == False:

    df = pd.read_csv(pathname + 'proc_lioc.csv', parse_dates=True,
                     index_col='date')

# ---------------------------------------------------------------------------- #
# Leitura dos dados brutos da boia
# Processamento dos dados brutos com longuet-higgins
# comparar os parametros calculados com a serie de dados processados

# cria com nome dos dados brutos

if proc_raw == True:

    list_dat = []
    list_files = np.sort(os.listdir(pathname))
    for l in list_files:
        if l.endswith('.dat'):
            list_dat.append(l)

    # calcula parametros de onda

    param = [] # lista de parametros
    dates = []
    for filename in list_dat:

        print filename

        # read the data
        raw = pd.read_table(pathname + filename, skiprows=13, sep='\s+',
                           names=['heave','roll','pitch','head'])

        # date in timestamp
        dates.append(str(pd.to_datetime(filename[-12:-4], format='%y%m%d%H')))

        w = WaveProc(n1 = raw.heave.values,
                     n2 = raw.roll.values,
                     n3 = raw.pitch.values,
                     fs = 1,
                     nfft = len(raw)/2,
                     h = 1000)

        w.timedomain()
        w.freqdomain()

        param.append([w.hs, w.tp, w.dp])

    df = pd.DataFrame(np.array(param), columns=['hm0','tp','dp'], index = dates)
    df.index.name = 'date'

    df.to_csv(pathname + 'proc_lioc.csv')

# ---------------------------------------------------------------------------- #
# Plotagem

# comparacao hs, tp e dp 

fig = plt.figure(figsize=(12,11), facecolor='w')

ax1 = fig.add_subplot(3,1,1)
ax1.plot(out.index, out.hm0, '-o', df.index, df.hm0, '-o')
# ax1.set_ylabel('Battery (V)', color='b')
# ax1.tick_params('y', colors='b')
plt.xticks(rotation=15)

ax2 = fig.add_subplot(3,1,2)
ax2.plot(out.index, out.tp, '-bo', df.index, df.tp, '-ro')
# ax1.set_ylabel('Battery (V)', color='b')
# ax1.tick_params('y', colors='b')
plt.xticks(rotation=15)

ax3 = fig.add_subplot(3,1,3)
ax3.plot(out.index, out.dp, '-o', df.index, df.dp, '-o')
# ax1.set_ylabel('Battery (V)', color='b')
# ax1.tick_params('y', colors='b')
plt.xticks(rotation=15)


plt.show()
