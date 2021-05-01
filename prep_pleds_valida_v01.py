"""
Processamento dos dados da boia do MERENDA do ES
e do espectro do modelo do WW3 para fazer a PLEDS
da diferenca

VMTA Momento Espectral de Ordem 0
VTPK Periodo de Pico Espectral
VPED Direcao Espectral
Para obter Hs usar 4.01*sqrt(VMTA) ou 4.01*sqrt(VMTA1)


Indice da Faixa Valores de Periodos para a Faixa Sistema de ondas
1 23,9 a 12,3 s SWELL
2 12,3 a 7,63 s SWELL/QUASI-SEA
3 7,63 a 4,31 s QUASI-SEA/SEA
4 4,31 a 2,43 s SEA

"""

from scipy import signal
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import waveproc_v03
reload(waveproc_v03)
from waveproc_v03 import WaveProc

plt.close('all')

# ---------------------------------------------------------------------------- #
# Dados de entrada

# Processa dados brutos de onda e cria arquivo csv com parametros (True) ou 
# le os dados do arquivo csv gerado (False). arquivo apenas cm hs, tp e dp
proc_raw = True
# proc_raw = False

# pathname
pathname = '../data/boia_merenda/'

# data inicial e final para processar com base no nome do arquivo (YYMMDDHHMM.dat)
dat_ii = 'Onda_06110100.dat'
dat_ff = 'Onda_06113023.dat'

dt = 1.0 
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

out = pd.read_table(pathname + 'saida.out', sep='\t', parse_dates=[[0,1]],
                    date_parser=dateparse, index_col=0)

out.index.name = 'date'
out['hm0'] = 4.01 * np.sqrt(out['  VMTA'])
out['tp'] = out['           VTPK']
out['dp'] = out['  VPED']

# ---------------------------------------------------------------------------- #
# Leitura dos dados processados por essa rotina

if proc_raw == False:

    df = pd.read_csv('../out/proc_lioc.csv', parse_dates=True,
                     index_col='date')

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
    espe = [] # variaveis para a pleds
    dire = []

    # indice do arquivo inidical e final para processar
    ii = np.where(list_dat == dat_ii)[0][0]
    ff = np.where(list_dat == dat_ff)[0][0]

    # for filename in list_dat:
    for filename in list_dat[ii:ff]:

        print filename

        # read the data
        raw = pd.read_table(pathname + 'brutos/' + filename, skiprows=13, sep='\s+',
                           names=['heave','roll','pitch','compass'])

        raw = raw.iloc[:1023]

        # date in timestamp
        dates.append(str(pd.to_datetime(filename[-12:-4], format='%y%m%d%H')))

        # stop

        # correcao
        raw['roll'] = raw.roll * -1
        # raw.heave = -raw.heave
        # raw.roll = np.cos(np.pi*raw.compass/180) * raw.roll + np.sin(np.pi*raw.compass/180) * raw.heave  
        # raw.pitch = -np.sin(np.pi*raw.compass/180) * raw.roll + np.cos(np.pi*raw.compass/180) * raw.heave 

        raw['roll'] = np.cos(np.pi*raw.compass/180) * raw.roll + np.sin(np.pi*raw.compass/180) * raw.pitch  #roll
        raw['pitch'] = -np.sin(np.pi*raw.compass/180) * raw.roll + np.cos(np.pi*raw.compass/180) *raw.pitch;  # pitch

        raw['heave'] = raw.heave * -1

        # eixo de frequencia 32 graus
        # x = dt * 64
        # f1 = np.arange(1/x,33/x,1/x) #vetor de frequencias
        # stop

        # calculo do espectro 1d
        f, s1 = signal.welch(raw.heave, fs=1/dt, window='hann',
                     nperseg=100, noverlap=50, nfft=None,
                     detrend='constant', return_onesided=True,
                     scaling='density', axis=-1)


        # calculo do espectro cruzado
        f, Pxy1 = signal.csd(raw.heave, raw.roll, fs=1/dt, window='hann',
                             nperseg=100, noverlap=50, nfft=None,
                             detrend='constant', return_onesided=True,
                             scaling='density', axis=-1)

        f, Pxy2 = signal.csd(raw.heave, raw.pitch, fs=1/dt, window='hann',
                     nperseg=100, noverlap=50, nfft=None,
                     detrend='constant', return_onesided=True,
                     scaling='density', axis=-1)

        ir1 = np.imag(Pxy1)
        ir2 = np.imag(Pxy2)

        c0 = np.angle(ir1+1j*ir2); # angulo

        c0 = c0 * 180 / np.pi
        c0 = 270 - c0

        c0[np.where(c0<0)[0]] = c0[np.where(c0<0)[0]] + 360
        c0[np.where(c0>360)[0]] = c0[np.where(c0>360)[0]] - 360

        # df.dp.loc[df.dp<0] = df.dp.loc[df.dp<0] + 360
        # df.dp.loc[df.dp>360] = df.dp.loc[df.dp>360] - 360


        # indice da frequencia de pico
        ipk = np.where(s1==s1.max())[0][0]

        # altura significativa
        df = f[2]-f[1]
        m0 = np.sum(s1) * df
        hm0 = 4.01 * np.sqrt(m0)

        # periodo de pico
        tp = 1./f[ipk]

        # direcao de pico
        dp = c0[ipk]

        # plotagem do espectro e direcao principal
        # fig = plt.figure(figsize=(8,6), facecolor='w')
        # ax1 = fig.add_subplot(2,1,1)
        # ax1.plot(f, s1)
        # ax2 = fig.add_subplot(2,1,2)
        # ax2.plot(f, c0)
        # ax2.set_ylim(0,360)

        # fig.savefig('/home/hp/Documents/teste1/dirspec_%s.png' %filename)

        # plt.close('all')

        sp_fx1 = s1[5:9].mean()    # 20.0 - 12.5
        sp_fx2 = s1[8:14].mean()   # 12.5 - 7.7
        sp_fx3 = s1[13:24].mean()  # 7.7 - 4.3
        sp_fx4 = s1[23:42].mean()  # 4.3 - 2.4

        dir_fx1 = c0[5:9].mean()    # 20.0 - 12.5
        dir_fx2 = c0[8:14].mean()   # 12.5 - 7.7
        dir_fx3 = c0[13:24].mean()  # 7.7 - 4.3
        dir_fx4 = c0[23:42].mean()  # 4.3 - 2.4


        espe.append([sp_fx1,0,sp_fx2,0,sp_fx3,0,sp_fx4,0])
        dire.append([dir_fx1,0,dir_fx2,0,dir_fx3,0,dir_fx4,0])

        # stop



        # print raw.heave[0]
        # print raw.heave[0]

    #     w = WaveProc(n1 = raw.heave.values,
    #                  n3 = raw.roll.values,
    #                  n2 = raw.pitch.values,
    #                  fs = 1,
    #                  nfft = len(raw)/2,
    #                  h = 5000,
    #                  dmag=-23)

    #     w.timedomain()
    #     w.freqdomain()

        # param.append([w.hs, w.tp, w.dp])
        param.append([hm0,tp,dp])

    # df = pd.DataFrame(np.array(param), columns=['hm0','tp','dp'], index = pd.to_datetime(dates))
    df = pd.DataFrame(np.array(param), columns=['hm0','tp','dp'], index = pd.to_datetime(dates))
    df.index.name = 'date'

    df.to_csv('../out/proc_lioc.csv')


# ---------------------------------------------------------------------------- #
# cria arquivos para saida da daat

espe = np.array(espe).T
dire = np.array(dire).T

np.savetxt('../out/espe_buoy.txt', espe)
np.savetxt('../out/dire_buoy.txt', dire)


if __name__ == '__main__':

    import pleds
    reload(pleds)
    pleds.pleds(espe, dire, title=filename, figname='pleds_ww3.png')


# ---------------------------------------------------------------------------- #
# calculo de direcao (testes)

# converte para graus

# df.dp2.loc[df.dp2<0] = df.dp2.loc[df.dp2<0] + 360
# df.dp2.loc[df.dp2>360] = df.dp2.loc[df.dp2>360] - 360

# df.dp3.loc[df.dp3<0] = df.dp3.loc[df.dp3<0] + 360
# df.dp3.loc[df.dp3>360] = df.dp3.loc[df.dp3>360] - 360

# ---------------------------------------------------------------------------- #
# Plotagem

# comparacao hs, tp e dp 

# fig = plt.figure(figsize=(12,11), facecolor='w')

# ax1 = fig.add_subplot(3,1,1)
# ax1.plot(out.index, out.hm0, '-')
# ax1.plot(df.index, df.hm0, '-')
# # ax1.plot(mod.index, mod.hm0, '-')
# # ax1.set_ylabel('Battery (V)', color='b')
# ax1.tick_params('y', colors='b')
# ax1.set_xlim(df.index[0], df.index[-1])
# ax1.legend(['buoy','lioc'], ncol=2)
# plt.xticks(rotation=10)

# ax2 = fig.add_subplot(3,1,2)
# ax2.plot(out.index, out.tp, '.')
# ax2.plot(df.index, df.tp, '.')
# # ax2.plot(mod.index, mod.tp, '.')
# # ax1.set_ylabel('Battery (V)', color='b')
# ax1.tick_params('y', colors='b')
# ax2.set_xlim(df.index[0], df.index[-1])
# plt.xticks(rotation=10)

# ax3 = fig.add_subplot(3,1,3)
# ax3.plot(out.index, out.dp, '.')
# ax3.plot(df.index, df.dp, '.')
# # ax3.plot(df.index, df.dp2, '.')
# # ax3.plot(mod.index, mod.dp, '.')
# # ax1.set_ylabel('Battery (V)', color='b')
# ax1.tick_params('y', colors='b')
# plt.xticks(rotation=10)
# ax3.set_xlim(df.index[0], df.index[-1])
# # ax3.legend(['buoy','lioc'], ncol=2)


# ---------------------------------------------------------------------------- #
# Plotagem da direcao de pico

# comparacao hs, tp e dp 


# ax1.tick_params('y', colors='b')
# ax1.set_xlim(df.index[0], df.index[-1])
# ax1.legend(['buoy','dp1','dp2','dp3'], ncol=4)
# plt.xticks(rotation=10)



plt.show()
