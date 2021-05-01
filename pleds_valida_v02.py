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
import waveproc_v02
reload(waveproc_v02)
from waveproc_v02 import WaveProc

plt.close('all')

# ---------------------------------------------------------------------------- #
# Dados de entrada

# Processa dados brutos de onda e cria arquivo csv com parametros (True) ou 
# le os dados do arquivo csv gerado (False). arquivo apenas cm hs, tp e dp
proc_raw = True
# proc_raw = False

# pathname
pathname = os.environ['HOME'] + '/GoogleDrive/AGES/data/boia_merenda/'

# data inicial e final para processar com base no nome do arquivo (YYMMDDHHMM.dat)
dat_ii = 'Onda_06110110.dat'
dat_ff = 'Onda_06113010.dat'

# ---------------------------------------------------------------------------- #
# Leitura dos resultados da WW3 da BRMerenda

dateparse = lambda x: pd.datetime.strptime(x, '%Y %m %d %H %M')

mod = pd.read_table(pathname + 'BRMerenda_ww3.txt', sep='\s+',
                    parse_dates=[[0,1,2,3,4]],
                    date_parser=dateparse,
                    header=None,
                    # names=[['date','hs','tp','dp','spr']],
                    # index_col=0,
                    )

mod.columns = ['date','hm0','tp','dp','spr']
mod.set_index('date', inplace=True)

# ---------------------------------------------------------------------------- #
# Leitura dos dados processados da boia

dateparse = lambda x: pd.datetime.strptime(x, '%d %m %Y %H %M')

out = pd.read_table(pathname + 'brutos/saida.out', sep='\t', parse_dates=[[0,1]],
                    date_parser=dateparse, index_col=0)

out.index.name = 'date'
out['hm0'] = 4.01 * np.sqrt(out['  VMTA'])
out['tp'] = out['           VTPK']
out['dp'] = out['  VPED']

# ---------------------------------------------------------------------------- #
# Leitura dos dados processados por essa rotina

# if proc_raw == False:

#     df = pd.read_csv(pathname + 'proc_lioc.csv', parse_dates=True,
#                      index_col='date')

# ---------------------------------------------------------------------------- #
# Leitura dos dados brutos da boia
# Processamento dos dados brutos com longuet-higgins
# comparar os parametros calculados com a serie de dados processados

# cria com nome dos dados brutos

if proc_raw == True:

    list_dat = []
    list_files = np.sort(os.listdir(pathname + 'brutos/'))
    for l in list_files:
        if l.endswith('.dat'):
            list_dat.append(l)
    list_dat = np.array(list_dat)

    # calcula parametros de onda

    param = [] # lista de parametros
    dates = []

    # indice do arquivo inidical e final para processar
    ii = np.where(list_dat == dat_ii)[0][0]
    ff = np.where(list_dat == dat_ff)[0][0]

    for filename in list_dat:
    # for filename in list_dat[ii:ff]:

        print filename

        # read the data
        raw = pd.read_table(pathname + 'brutos/' + filename, skiprows=13, sep='\s+',
                           names=['heave','roll','pitch','compass'])

        # date in timestamp
        dates.append(str(pd.to_datetime(filename[-12:-4], format='%y%m%d%H')))

        # correcao
        raw.roll = -raw.roll
        raw.roll = np.cos(np.pi*raw.compass/180) * raw.roll + np.sin(np.pi*raw.compass/180) * raw.heave  
        raw.pitch = -np.sin(np.pi*raw.compass/180) * raw.roll + np.cos(np.pi*raw.compass/180) * raw.heave 

        # print raw.heave[0]
        raw.heave = -raw.heave
        # print raw.heave[0]

        # stop

        w = WaveProc(n1 = raw.heave.values,
                     n3 = raw.roll.values,
                     n2 = raw.pitch.values,
                     fs = 1,
                     nfft = len(raw)/2,
                     h = 5000,
                     dmag=-23)

        w.timedomain()
        w.freqdomain()

        param.append([w.hs, w.tp, w.dp])

    df = pd.DataFrame(np.array(param), columns=['hm0','tp','dp'], index = pd.to_datetime(dates))
    df.index.name = 'date'

    df.to_csv(pathname + 'proc_lioc.csv')

# ---------------------------------------------------------------------------- #
# Plotagem

# comparacao hs, tp e dp 

fig = plt.figure(figsize=(12,11), facecolor='w')

# ax1 = fig.add_subplot(3,1,1)
# ax1.plot(out.index, out.hm0, '-')
# ax1.plot(df.index, df.hm0, '-')
# ax1.plot(mod.index, mod.hm0, '-')
# ax1.set_ylabel('Battery (V)', color='b')
# ax1.tick_params('y', colors='b')
# ax1.set_xlim(df.index[0], df.index[-1])
# ax1.legend(['buoy','lioc','ww3'], ncol=3)
# plt.xticks(rotation=10)

# ax2 = fig.add_subplot(3,1,2)
# ax2.plot(out.index, out.tp, '.')
# ax2.plot(df.index, df.tp, '.')
# ax2.plot(mod.index, mod.tp, '.')
# ax1.set_ylabel('Battery (V)', color='b')
# ax1.tick_params('y', colors='b')
# ax2.set_xlim(df.index[0], df.index[-1])
# plt.xticks(rotation=10)

ax3 = fig.add_subplot(1,1,1)
ax3.plot(out.index, out.dp, '.')
ax3.plot(df.index, df.dp, '.')
# ax3.plot(mod.index, mod.dp, '.')
# ax1.set_ylabel('Battery (V)', color='b')
# ax1.tick_params('y', colors='b')
plt.xticks(rotation=10)
ax3.set_xlim(df.index[0], df.index[-1])
ax3.legend(['buoy','lioc'], ncol=2)


plt.show()
