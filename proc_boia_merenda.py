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

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal

plt.close('all')

# ---------------------------------------------------------------------------- #
# Dados de entrada

# Processa dados brutos de onda e cria arquivo csv com parametros (True) ou
# le os dados do arquivo csv gerado (False). arquivo apenas cm hs, tp e dp
# proc_raw = True
# proc_raw = False

# pathname

# data inicial e final para processar com base no nome do arquivo (YYMMDDHHMM.dat)


def read_ww3_result_merenda(pahname, filename='BRMerenda_ww3.txt'):

    """
    Leitura dos resultados da WW3 da BRMerenda
    """

    dateparse = lambda x: pd.datetime.strptime(x, '%Y %m %d %H %M')

    mod = pd.read_table(pathname + filename, sep='\s+',
                        parse_dates=[[0,1,2,3,4]],
                        date_parser=dateparse,
                        header=None,
                        # names=[['date','hs','tp','dp','spr']],
                        # index_col=0,
                        )

    mod.columns = ['date','hm0','tp','dp','spr']
    mod.set_index('date', inplace=True)

    ww3_result = np.copy(mod)

    return ww3_result

def read_buoy_processed_data_merenda(pathname, filename='saida.out'):

    """
    Leitura dos dados processados da boia
    """

    dateparse = lambda x: pd.datetime.strptime(x, '%d %m %Y %H %M')

    out = pd.read_table(pathname + filename, sep='\t', parse_dates=[[0,1]],
                        date_parser=dateparse, index_col=0)

    out.index.name = 'date'
    out['hm0'] = 4.01 * np.sqrt(out['  VMTA'])
    out['tp'] = out['           VTPK']
    out['dp'] = out['  VPED']

    buoy_data = np.copy(out)

    return buoy_data

def read_buoy_lioc_processed_data_merenda(pathname, filename='proc_lioc.csv'):

    """
    Leitura dos dados processados por essa rotina
    """

    buoy_lioc = pd.read_csv(pathname + filename, parse_dates=True,
                     index_col='date')

    return buoy_lioc

def read_and_process_buoy_raw_data(pathname, dat_ii, dat_ff, dt):

    """
    Leitura dos dados brutos da boia
    Processamento dos dados brutos com longuet-higgins
    comparar os parametros calculados com a serie de dados processados
    """

    list_dat = []
    list_files = np.sort(os.listdir(pathname))
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
        raw = pd.read_table(pathname + filename, skiprows=13, sep='\s+',
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

        # faixas para a pleds
        sp_fx1 = s1[5:9].mean()    # 20.0 - 12.5
        sp_fx2 = s1[8:14].mean()   # 12.5 - 7.7
        sp_fx3 = s1[13:24].mean()  # 7.7 - 4.3
        sp_fx4 = s1[23:42].mean()  # 4.3 - 2.4

        # direcao media das faixas
        dir_fx1 = c0[5:9].mean()    # 20.0 - 12.5
        dir_fx2 = c0[8:14].mean()   # 12.5 - 7.7
        dir_fx3 = c0[13:24].mean()  # 7.7 - 4.3
        dir_fx4 = c0[23:42].mean()  # 4.3 - 2.4

        # matrizes para a pleds
        espe.append([sp_fx1,0,sp_fx2,0,sp_fx3,0,sp_fx4,0])
        dire.append([dir_fx1,0,dir_fx2,0,dir_fx3,0,dir_fx4,0])



        param.append([hm0,tp,dp])

    espe = np.array(espe).T
    dire = np.array(dire).T

    buoy_raw = pd.DataFrame(np.array(param), columns=['hm0','tp','dp'], index = pd.to_datetime(dates))
    buoy_raw.index.name = 'date'

    return buoy_raw, espe, dire


def read_nc(filename):
    ds = xr.open_dataset(filename)
    freq = ds.frequencies.values
    direcao = ds.directions.values
    return ds, freq, direcao

def get_spec(dataset, time):
    spec2d = dataset['dspectr'].data[time,:,:]
    spec1d = spec2d.mean(axis=0)
    return spec1d, spec2d

def preppleds(freq, direcao, spec2d, faixa_1, faixa_2, faixa_3, faixa_4):

    # indice mais proximo do vetor de frequencia
    fx1_a = (np.abs(freq-1/faixa_1[0])).argmin()
    fx1_b = (np.abs(freq-1/faixa_1[1])).argmin()

    fx2_a = (np.abs(freq-1/faixa_2[0])).argmin()
    fx2_b = (np.abs(freq-1/faixa_2[1])).argmin()

    fx3_a = (np.abs(freq-1/faixa_3[0])).argmin()
    fx3_b = (np.abs(freq-1/faixa_3[1])).argmin()

    fx4_a = (np.abs(freq-1/faixa_4[0])).argmin()
    fx4_b = (np.abs(freq-1/faixa_4[1])).argmin()

    # matriz 2d de cad faixa
    spec2d_fx1 = spec2d[:,fx1_a:fx1_b]
    spec2d_fx2 = spec2d[:,fx2_a:fx2_b]
    spec2d_fx3 = spec2d[:,fx3_a:fx3_b]
    spec2d_fx4 = spec2d[:,fx4_a:fx4_b]

    # energia em cada faixa
    m0_fx1 = spec2d_fx1.sum()
    m0_fx2 = spec2d_fx2.sum()
    m0_fx3 = spec2d_fx3.sum()
    m0_fx4 = spec2d_fx4.sum()

    # indice da direcao e frequencia de pico de cada faixa
    ind_dp_fx1, ind_fp_fx1 = np.where(spec2d_fx1 == spec2d_fx1.max())
    ind_dp_fx2, ind_fp_fx2 = np.where(spec2d_fx2 == spec2d_fx2.max())
    ind_dp_fx3, ind_fp_fx3 = np.where(spec2d_fx3 == spec2d_fx3.max())
    ind_dp_fx4, ind_fp_fx4 = np.where(spec2d_fx4 == spec2d_fx4.max())

    m0_fx = [m0_fx1, m0_fx2, m0_fx3, m0_fx4]

    # teste 1
    # dp_fx = [direcao[ind_dp_fx1][0], direcao[ind_dp_fx2][0], direcao[ind_dp_fx3][0], direcao[ind_dp_fx4][0]]

    # teste 2
    dp_fx = [direcao[np.where(spec2d_fx1 > 0.01)[0]].mean(),
             direcao[np.where(spec2d_fx2 > 0.01)[0]].mean(),
             direcao[np.where(spec2d_fx3 > 0.01)[0]].mean(),
             direcao[np.where(spec2d_fx4 > 0.01)[0]].mean()]


    return m0_fx, dp_fx






if __name__ == '__main__':

    pathname = '../data/boia_merenda/'
    filename = 'buoy_merenda_200611'
    dat_ii = 'Onda_06110100.dat'
    dat_ff = 'Onda_06113023.dat'
    dt = 1.0 # intervalo de amostragem dos dados brutos

    ww3_result = read_ww3_result_merenda(pathname, filename='BRMerenda_ww3.txt')
    buoy_data = read_buoy_processed_data_merenda(pathname, filename='saida.out')
    buoy_lioc = read_buoy_lioc_processed_data_merenda(pathname, filename='proc_lioc.csv')
    buoy_raw, espe, dire = read_and_process_buoy_raw_data(pathname+'/brutos/', dat_ii, dat_ff, dt)

    np.savetxt('../out/espe_buoy.txt', espe)
    np.savetxt('../out/dire_buoy.txt', dire)
    buoy_raw.to_csv('../out/proc_lioc.csv')

    import pleds
    reload(pleds)
    pleds.pleds(espe, dire, title=filename, figname='pleds_teste.png')


    # filename = 'dspec200704.nc'

    # # faixas de periodo (segundos) para a pleds
    # faixa_1 = (23.9, 12.3)
    # faixa_2 = (11.2, 7.6)
    # faixa_3 = (7.6, 4.3)
    # faixa_4 = (4.3, 2.4)

    # ds, freq, direcao = read_nc(filename)

    # m0_fx, dp_fx = [], []
    # for t in range(ds.time.shape[0]):
    #     spec1d, spec2d = get_spec(ds, time=t)
    #     m0_fx_aux, dp_fx_aux = preppleds(freq, direcao, spec2d, faixa_1, faixa_2, faixa_3, faixa_4)
    #     m0_fx.append(m0_fx_aux)
    #     dp_fx.append(dp_fx_aux)

    # # pega dados de 3 em 3 horas
    # m0_fx = np.array(m0_fx).T
    # dp_fx = np.array(dp_fx).T

    # # monta matriz no formato para a pleds
    # espe = np.zeros((8, m0_fx.shape[1]))
    # dire = np.copy(espe)

    # espe[[0,2,4,6],:] = m0_fx
    # dire[[0,2,4,6],:] = dp_fx

    # np.savetxt('../out/espe_ww3.txt', espe)
    # np.savetxt('../out/dire_ww3.txt', dire)

    # import pleds
    # reload(pleds)
    # pleds.pleds(espe, dire, title=filename, figname='pleds_ww3.png')

    # espe[,]
