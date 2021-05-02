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
from matplotlib.patches import Rectangle
from matplotlib import reload
from scipy import signal
import pandas as pd
import xarray as xr

plt.close('all')

def read_ww3_result_merenda(pahname, filename='BRMerenda_ww3.txt'):

    """
    Leitura dos resultados da WW3 da BRMerenda
    """

    dateparse = lambda x: pd.datetime.strptime(x, '%Y %m %d %H %M')

    mod = pd.read_table(pathname + filename, sep='\s+',
                        parse_dates=[[0,1,2,3,4]],
                        date_parser=dateparse,
                        header=None)

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

def read_and_process_buoy_raw_data(pathname, dat_ii, dat_ff, dt, dmag, faixas):

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
    param = []
    dates = []
    espe = []
    dire = []

    # indice do arquivo inidical e final para processar
    ii = np.where(list_dat == dat_ii)[0][0]
    ff = np.where(list_dat == dat_ff)[0][0]

    # for filename in list_dat:
    for filename in list_dat[ii:ff+1]:

        print (filename)

        # read the data
        raw = pd.read_table(pathname + filename, skiprows=13, sep='\s+',
                           names=['heave','roll','pitch','compass'])

        raw = raw.iloc[:1023]

        # date in timestamp
        dates.append(str(pd.to_datetime(filename[-12:-4], format='%y%m%d%H')))

        # correcao
        raw['roll'] = raw.roll * -1
        raw['roll'] = np.cos(np.pi*raw.compass/180) * raw.roll + np.sin(np.pi*raw.compass/180) * raw.pitch  #roll
        raw['pitch'] = -np.sin(np.pi*raw.compass/180) * raw.roll + np.cos(np.pi*raw.compass/180) *raw.pitch;  # pitch
        raw['heave'] = raw.heave * -1

        nfft = len(raw)/12
        # calculo do espectro 1d
        f, s1 = signal.welch(raw.heave, fs=1/dt, window='hann',
                     nperseg=nfft, noverlap=nfft/2, nfft=None,
                     detrend='constant', return_onesided=True,
                     scaling='density', axis=-1)

        # calculo do espectro cruzado
        f, Pxy1 = signal.csd(raw.heave, raw.roll, fs=1/dt, window='hann',
                             nperseg=nfft, noverlap=nfft/2, nfft=None,
                             detrend='constant', return_onesided=True,
                             scaling='density', axis=-1)

        f, Pxy2 = signal.csd(raw.heave, raw.pitch, fs=1/dt, window='hann',
                     nperseg=nfft, noverlap=nfft/2, nfft=None,
                     detrend='constant', return_onesided=True,
                     scaling='density', axis=-1)

        ir1 = np.imag(Pxy1)
        ir2 = np.imag(Pxy2)

        # angulo
        c0 = np.angle(ir1+1j*ir2)
        c0 = c0 * 180 / np.pi
        c0 = 270 - c0 + dmag
        c0[np.where(c0<0)[0]] = c0[np.where(c0<0)[0]] + 360
        c0[np.where(c0>360)[0]] = c0[np.where(c0>360)[0]] - 360

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

        # indice mais proximo do vetor de frequencia
        fx1_a = (np.abs(f-1/faixas['faixa_1'][0])).argmin()
        fx1_b = (np.abs(f-1/faixas['faixa_1'][1])).argmin()

        fx2_a = (np.abs(f-1/faixas['faixa_2'][0])).argmin()
        fx2_b = (np.abs(f-1/faixas['faixa_2'][1])).argmin()

        fx3_a = (np.abs(f-1/faixas['faixa_3'][0])).argmin()
        fx3_b = (np.abs(f-1/faixas['faixa_3'][1])).argmin()

        fx4_a = (np.abs(f-1/faixas['faixa_4'][0])).argmin()
        fx4_b = (np.abs(f-1/faixas['faixa_4'][1])).argmin()


        # faixas para a pleds
        sp_fx1 = s1[fx1_a:fx1_b].mean()    # 20.0 - 12.5
        sp_fx2 = s1[fx2_a:fx2_b].mean()   # 12.5 - 7.7
        sp_fx3 = s1[fx3_a:fx3_b].mean()  # 7.7 - 4.3
        sp_fx4 = s1[fx4_a:fx4_b].mean()  # 4.3 - 2.4

        # direcao media das faixas
        dir_fx1 = c0[fx1_a:fx1_b].mean()
        dir_fx2 = c0[fx2_a:fx2_b].mean()
        dir_fx3 = c0[fx3_a:fx3_b].mean()
        dir_fx4 = c0[fx4_a:fx4_b].mean()

        # matrizes para a pleds
        espe.append([sp_fx1,0,sp_fx2,0,sp_fx3,0,sp_fx4,0])
        dire.append([dir_fx1,0,dir_fx2,0,dir_fx3,0,dir_fx4,0])

        param.append([hm0,tp,dp])

    espe = np.array(espe).T
    dire = np.array(dire).T

    buoy_raw = pd.DataFrame(np.array(param), columns=['hm0','tp','dp'], index = pd.to_datetime(dates))
    buoy_raw.index.name = 'date'

    return buoy_raw, espe, dire, f, s1

def read_and_process_buoy_wind(pathname):

    list_arqs = np.sort(os.listdir(pathname))
    list_wind = []
    mean_wind = []
    for l in list_arqs:
        if l.startswith('Vento'):
            df = pd.read_table(pathname + l, comment='%', delimiter='\s+', header=None, names=['ws1','wd1','ws2','wd2'])
            dtime = pd.to_datetime(l[6:-4], format='%y%m%d%H')
            mean_wind.append([dtime]+list(df.mean()))

    dfw = pd.DataFrame(mean_wind, columns=['date','ws1','wd1','ws2','wd2'])
    dfw = dfw.set_index('date')
    return dfw

def read_ww3_nc_spcpoint(pathname, filename):
    ds = xr.open_dataset(pathname + filename)
    freq = ds.frequencies.values
    direcao = ds.directions.values
    return ds, freq, direcao

def get_ww3_spec(dataset, time):
    spec2d = dataset['dspectr'].data[time,:,:]
    spec1d = spec2d.mean(axis=0)
    return spec1d, spec2d

def plot_spec2d(spec2d, freq, direcao, pathfig):
    plt.figure()
    plt.contour(freq, direcao, spec2d)
    plt.colorbar()
    plt.grid()
    plt.savefig(pathfig + str(ds.time[t].values) + '.png')
    plt.close('all')
    return 

def read_ww3_wind(pathname, filename):
    ws, wd = np.loadtxt(pathname + filename, skiprows=4, usecols=[5,6], unpack=True)
    return ws, wd

def prep_pleds_ww3(freq, direcao, spec2d, faixas):

    """
    Entrada: Vetor de frequencia e direcao, espectros 1d e 2d e tuplas com as
    4 faixas
    Saida: matrizes 'espe' e 'dire'
    """

    # indice mais proximo do vetor de frequencia
    fx1_a = (np.abs(freq-1/faixas['faixa_1'][0])).argmin()
    fx1_b = (np.abs(freq-1/faixas['faixa_1'][1])).argmin()

    fx2_a = (np.abs(freq-1/faixas['faixa_2'][0])).argmin()
    fx2_b = (np.abs(freq-1/faixas['faixa_2'][1])).argmin()

    fx3_a = (np.abs(freq-1/faixas['faixa_3'][0])).argmin()
    fx3_b = (np.abs(freq-1/faixas['faixa_3'][1])).argmin()

    fx4_a = (np.abs(freq-1/faixas['faixa_4'][0])).argmin()
    fx4_b = (np.abs(freq-1/faixas['faixa_4'][1])).argmin()

    # matriz 2d de cada faixa
    spec2d_fx1 = spec2d[:,fx1_a:fx1_b]
    spec2d_fx2 = spec2d[:,fx2_a:fx2_b]
    spec2d_fx3 = spec2d[:,fx3_a:fx3_b]
    spec2d_fx4 = spec2d[:,fx4_a:fx4_b]

    # energia em cada faixa
    m0_fx1 = spec2d_fx1.sum()
    m0_fx2 = spec2d_fx2.sum()
    m0_fx3 = spec2d_fx3.sum()
    m0_fx4 = spec2d_fx4.sum()

    # lista com m0 das faixas
    m0_fx = [m0_fx1, m0_fx2, m0_fx3, m0_fx4]

    # indice da direcao e frequencia de pico de cada faixa
    # ind_dp_fx1, ind_fp_fx1 = np.where(spec2d_fx1 == spec2d_fx1.max())
    # ind_dp_fx2, ind_fp_fx2 = np.where(spec2d_fx2 == spec2d_fx2.max())
    # ind_dp_fx3, ind_fp_fx3 = np.where(spec2d_fx3 == spec2d_fx3.max())
    # ind_dp_fx4, ind_fp_fx4 = np.where(spec2d_fx4 == spec2d_fx4.max())

    ind_dp_fx1 = int(spec2d[:,fx1_a:fx1_b].argmax() / spec2d[:,fx1_a:fx1_b].shape[1])
    ind_dp_fx2 = int(spec2d[:,fx2_a:fx2_b].argmax() / spec2d[:,fx2_a:fx2_b].shape[1])
    ind_dp_fx3 = int(spec2d[:,fx3_a:fx3_b].argmax() / spec2d[:,fx3_a:fx3_b].shape[1])
    ind_dp_fx4 = int(spec2d[:,fx4_a:fx4_b].argmax() / spec2d[:,fx4_a:fx4_b].shape[1])


    # print ind_dp_fx1[0]
    # print (ind_dp_fx4, ind_fp_fx4)

    # print (direcao[np.where(spec2d_fx1 == spec2d_fx1.max())[0]])
    # stop

    # lista com direcao media das faixas
    # dp_fx = [direcao[np.where(spec2d_fx1 > 0.01)[0]].mean(),
    #          direcao[np.where(spec2d_fx2 > 0.01)[0]].mean(),
    #          direcao[np.where(spec2d_fx3 > 0.01)[0]].mean(),
    #          direcao[np.where(spec2d_fx4 > 0.01)[0]].mean()]

    # print dp_fx
    # stop


    # lista com direcao associaada a fp de cada faixa
    # dp_fx = [direcao[ind_dp_fx1][0],
    #          direcao[ind_dp_fx2][0],
    #          direcao[ind_dp_fx3][0],
    #          direcao[ind_dp_fx4][0]]

    dp_fx = [direcao[ind_dp_fx1],
             direcao[ind_dp_fx2],
             direcao[ind_dp_fx3],
             direcao[ind_dp_fx4]]

    print (ind_fp_fx1, ind_dp_fx2, ind_dp_fx3, ind_dp_fx4)
    print (ind_dp_fx1, ind_dp_fx2, ind_dp_fx3, ind_dp_fx4)

    return m0_fx, dp_fx

def read_preppleds_spcpoint(pathname, filename):

    df = pd.read_table(pathname + filename, delimiter='\s+', skiprows=5, header=None,
         names=['yr','mo','day','hour',
                'en1','hs1','dp1',
                'en2','hs2','dp2',
                'en3','hs3','dp3',
                'en4','hs4','dp4'])

    # monta matriz no formato para a pleds
    espe = np.zeros((8, df.shape[0]))
    dire = np.copy(espe)

    # cria matriz espe e dire no formato da pleds
    espe[[0,2,4,6],:] = df[['en1','en2','en3','en4']].values.T
    dire[[0,2,4,6],:] = df[['dp1','dp2','dp3','dp4']].values.T

    return espe, dire

def pleds(faixas, espe, dire, ws, wd, title, namefig, typep='spec'):

    # cria figura
    fig = plt.figure(figsize=(8,9))
    ax = fig.add_subplot(111)
    plt.plot(0,'w')

    # edge colocar das ploatagens
    edc = 'black'
    # limites dos eixos - desloca o eixo x para melhor visualizar os dados
    shit_xaxis = -45 
    if typep == 'diff':
        shit_xaxis = -180 # centraliza o zero
        # edc = None
    
    # dire = dire + shit_xaxis
    # wd = wd + shit_xaxis
    xmin, xmax, ymin, ymax = 0+shit_xaxis, 360+shit_xaxis, 0-9, 248+24
    plt.axis([xmin, xmax, ymin, ymax])
    plt.xticks([])
    plt.yticks([])

    # triangulos para plotagem
    ha = np.hanning(11)

    # titulo
    plt.text(22+shit_xaxis,248+30,'DIRECTIONAL WAVE SPECTRUM EVOLUTION (PLEDS) - %s' \
                      %(title))

    # cria retangulos
    ee = 5 #espacamento para comecar a escrever
    cr = 65 #comprimento dos retangulos
    at = 7 #altura dos triangulos

    ax.add_patch(Rectangle((0*cr+shit_xaxis, -8), cr, at, alpha=0.8, facecolor='r'))
    ax.text(ee+0*cr+shit_xaxis, -7, "%.1f - %.1f s" %faixas['faixa_1'])

    ax.add_patch(Rectangle((1*cr+shit_xaxis, -8), cr, at, alpha=0.8, facecolor='y'))
    ax.text(ee+1*cr+shit_xaxis, -7, "%.1f - %.1f s" %faixas['faixa_2'])

    ax.add_patch(Rectangle((2*cr+shit_xaxis, -8), cr, at, alpha=0.8, facecolor='g'))
    ax.text(ee+2*cr+shit_xaxis, -7, "%.1f - %.1f s" %faixas['faixa_3'])

    ax.add_patch(Rectangle((3*cr+shit_xaxis, -8), cr, at,alpha=0.8, facecolor='b'))
    ax.text(ee+3*cr+shit_xaxis, -7, "%.1f - %.1f s" %faixas['faixa_4'])

    plt.draw()

    # textos da legenda
    ax.text(ee+4*cr+shit_xaxis, -7, "5 div = 10 m/s & 0.1 m2", fontsize=9)

    # tamanho do eixo y dependendo para 30 ou 31 dias
    if espe.shape[1] <= 240:
        y = [10,248]
    else:
        y = [10,248+8]

    #linhas verticais - divisoes a cada 20 graus - 18 setores
    # 1    2     3    4    5    6    7    8
    # N / NNE / NE / ENE / E / ESE / SE / SSE / S
    for i in np.arange(0,360,22.5):
        x = [i+shit_xaxis,i+shit_xaxis]
        plt.plot(x,[y[0],y[1]+2],'k',alpha=0.2)

    #linhas horizontais (3 horas)
    xx = [0+shit_xaxis, 360+shit_xaxis]
    dia = 0
    for i in np.arange(y[0],y[1]+4,2):
        yy = [i,i]
        plt.plot(xx,yy,'k',alpha=0.1)
        if i in np.arange(y[0],y[1],8):
            dia += 1
            plt.plot(xx,yy,'k',alpha=0.2)
            plt.text(-13+shit_xaxis,yy[0]-2,str(dia).zfill(2))
            plt.text(363+shit_xaxis,yy[0]-2,str(dia).zfill(2))

    # coloca valores de direcao rosa dos ventos (mudar aqui para mudar os eixos)

    if typep == 'spec':
        cardinais = {'NW': -45, 'N': 0, 'NE': 45, 'E': 90, 'SE': 135, 'S': 180, 'SW': 225, 'W': 270}
        # if typep == 'diff':
            # cardinais = {'NW': -45, 'N': 0, 'NE': 45, ' E': 90, 'SE': 135, 'S': 180, 'SW': 225, 'W': 270}
            # print ('aaaaaaaaaaa')
            # cardinais = {'W': -90, 'NW': -45, 'N': 0, 'NE': 45, ' E': 90, 'SE': 135, 'S': 180, 'SW': 225}
        for cardinal in cardinais.keys():
            if cardinais[cardinal] >= 0:
                plt.text(cardinais[cardinal], 10, cardinal, color='k', weight='bold')
                plt.text(cardinais[cardinal], 2, str(cardinais[cardinal]), color='red', fontsize=10)
            if cardinais[cardinal] < 0:
                plt.text(cardinais[cardinal], 2, str(cardinais[cardinal]+360), color='red', fontsize=10)
    if typep == 'diff':
        for d in np.arange(-160,161,20):
            plt.text(d, 2, str(d), color='red', fontsize=10)




    # legenda dos dias
    plt.text(1.15+shit_xaxis,80,'days in a month',rotation=90)

    # contador para a plotagem na data correta
    cont = dire.shape[1]
    for t in range(dire.shape[1]-1,-2,-1):
        cont -= 1

        #indice das cores
        icor = -1

        #varia as 4 faixas
        for f in [0,2,4,6]:
            icor += 1
            arq5 = ['r','y','g','b']

            # eixo x (direcao) com largura fixa
            x = np.linspace(dire[f,t]-10, dire[f,t]+10, len(ha))

            # eixo y - hanning
            y = ha * espe[f, t] + cont

            # plotagem do triangulo
            plt.fill(x, y+10, arq5[icor], edgecolor=edc, alpha=0.8)

        # plogem do vento
        if ws[t] != None:

            wsn = ws / ws.max()

            x = np.array([wd[t]-1,wd[t]+1,wd[t]+1,wd[t]-1])
            y = np.array([t, t, wsn[t]*10+cont, wsn[t]*10+cont])

            plt.fill(x, y+10, 'w', edgecolor=edc, alpha=0.8)

    fig.savefig(namefig)
    return

if __name__ == '__main__':

    proc_raw_buoy = False
    proc_nc_ww3 = False
    make_pleds_buoy = True
    make_pleds_ww3 = False
    make_plot_spec2d_ww3 = False
    make_pleds_preppleds = True
    make_pleds_diff = True

    # janela para media movel na pleds
    win = 12

    # faixas de periodo (segundos) para a pleds
    faixas = {'faixa_1': (23.9, 12.3),
              'faixa_2': (12.3, 7.63),
              'faixa_3': (7.63, 4.31),
              'faixa_4': (4.31, 2.43)}

    # ------------------------------------------------------------------------ #
    if proc_raw_buoy == True:
        pathname_raw = '../data/boia_merenda/brutos/'
        filename_out = 'buoy_merenda_200611'
        dat_ii = 'Onda_06110100.dat'
        dat_ff = 'Onda_06113023.dat'
        dt = 1.0
        dmag = -23
        buoy_raw, espe, dire, freq_buoy, s1 = read_and_process_buoy_raw_data(pathname_raw, dat_ii, dat_ff, dt, dmag, faixas)
        np.savetxt('../out/espe_%s.txt' %filename_out, espe)
        np.savetxt('../out/dire_%s.txt' %filename_out, dire)
        buoy_raw.to_csv('../out/param_%s.csv' %filename_out)

    # ------------------------------------------------------------------------ #
    if proc_nc_ww3 == True:
        pathname_nc = '../data/ww3_merenda/'
        filename = 'dspec200611.nc'
        filename_out = 'ww3_merenda_200611'
        pathfig = os.environ['HOME'] + '/Documents/teste4/'

        # leitura dos arquivos netcdf da saida da spcpoint
        ds, freq_ww3, direcao = read_ww3_nc_spcpoint(pathname_nc, filename)

        # cria as matrizes auxiliares de energia e direcao para cada faixa
        m0_fx, dp_fx = [], []
        for t in range(ds.time.shape[0]):
            spec1d, spec2d = get_ww3_spec(ds, time=t)
            m0_fx_aux, dp_fx_aux = prep_pleds_ww3(freq_ww3, direcao, spec2d, faixas)
            m0_fx.append(m0_fx_aux)
            dp_fx.append(dp_fx_aux)
            if make_plot_spec2d_ww3 == True:
                plot_spec2d(spec2d, freq_ww3, direcao, pathfig)

        # pega dados de 3 em 3 horas
        m0_fx = np.array(m0_fx).T
        dp_fx = np.array(dp_fx).T

        # monta matriz no formato para a pleds
        espe = np.zeros((8, m0_fx.shape[1]))
        dire = np.copy(espe)

        # cria matriz espe e dire no formato da pleds
        espe[[0,2,4,6],:] = m0_fx
        dire[[0,2,4,6],:] = dp_fx

        # salva arquivos de saida da pleds
        np.savetxt('../out/espe_%s.txt' %filename_out, espe)
        np.savetxt('../out/dire_%s.txt' %filename_out, dire)

    # ------------------------------------------------------------------------ #
    if make_pleds_preppleds == True:
        title = 'PREPPLEDS WW3'
        pathname = '../data/ww3_merenda/'
        filename = 'prepPLEDS_200611_izabel.txt'
        pathname_wind = '../data/ww3_merenda/'
        filename_wind = 'wind_200611.txt'
        espe, dire = read_preppleds_spcpoint(pathname, filename)
        dire = dire + np.random.rand(dire.shape[0],dire.shape[1]) * 20 - 20/2  #cria randomico
        dire = pd.rolling_window(dire, window=win, mean=True, axis=1, how=None)
        dire[np.where(dire == 0)] = 0.01
        espe, dire = espe[:,::3] * 100, dire[:,::3]
        ws, wd = read_ww3_wind(pathname_wind, filename_wind)
        wd = pd.rolling_window(wd, window=win, mean=True, axis=0, how=None)
        ws, wd = ws[::3], wd[::3]
        espe_prep, dire_prep = espe, dire
        pleds(faixas, espe, dire, ws, wd, title=title, namefig='../fig/pleds_ww3.png', typep='spec')

    # ------------------------------------------------------------------------ #
    if make_pleds_buoy == True:
        title = 'ES - Buoy - Nov/2006'
        pathname_wind = '../data/boia_merenda/Vento/'
        filename_wind = 'wind_200611.txt'
        espe = np.loadtxt('../out/espe_buoy_merenda_200611.txt')
        dire = np.loadtxt('../out/dire_buoy_merenda_200611.txt')
        espe = espe * 4
        dire = pd.rolling_window(dire, window=win, win_type=None, min_periods=None, freq=None, center=False, mean=True, axis=1, how=None)
        dire[np.where(dire == 0)] = 0.01
        espe, dire = espe[:,::3], dire[:,::3]
        dfw = read_and_process_buoy_wind(pathname_wind)
        dfw = dfw['2006-11']
        dfw['wd1'] = dfw.wd1.rolling(window=win).mean()
        ws, wd = dfw[['ws1','wd1']].values.T
        ws, wd = ws[::3], wd[::3]
        pleds(faixas, espe, dire, ws, wd, title=title, namefig='../fig/pleds_buoy.png', typep='spec')

    # ------------------------------------------------------------------------ #
    if make_pleds_ww3 == True:
        title = 'ES - WW3 - Nov/2006'
        pathname_wind = '../data/ww3_merenda/'
        filename_wind = 'wind_200611.txt'
        espe = np.loadtxt('../out/espe_ww3_merenda_200611.txt')
        dire = np.loadtxt('../out/dire_ww3_merenda_200611.txt')
        espe = espe * 0.6
        dire = dire + np.random.rand(dire.shape[0],dire.shape[1]) * 20 - 20/2  #cria randomico
        dire = pd.rolling_window(dire, window=win, mean=True, axis=1, how=None)
        dire[np.where(dire == 0)] = 0.01
        espe, dire = espe[:,::3], dire[:,::3]
        ws, wd = read_ww3_wind(pathname_wind, filename_wind)
        wd = pd.rolling_window(wd, window=win, mean=True, axis=0, how=None)
        ws, wd = ws[::3], wd[::3]
        pleds(faixas, espe, dire, ws, wd, title=title, namefig='../fig/pleds_ww3_py.png', typep='spec')

        # ------------------------------------------------------------------------ #
    if make_pleds_diff == True:

        title = 'ES - Diff - Nov/2006'

        # modelo
        pathname_wind_ww3 = '../data/ww3_merenda/'
        filename_wind_ww3 = 'wind_200611.txt'
        espe_ww3 = np.loadtxt('../out/espe_ww3_merenda_200611.txt')
        dire_ww3 = np.loadtxt('../out/dire_ww3_merenda_200611.txt')
        espe_ww3 = espe_ww3 * 0.6
        dire_ww3 = dire_ww3 + np.random.rand(dire_ww3.shape[0],dire_ww3.shape[1]) * 20 - 20/2  #cria randomico
        dire_ww3 = pd.rolling_window(dire_ww3, window=win, center=True, mean=True, axis=1, how=None)
        dire_ww3[np.where(dire_ww3 == 0)] = 0.01
        espe_ww3, dire_ww3 = espe_ww3[:,::3], dire_ww3[:,::3]
        ws_ww3, wd_ww3 = read_ww3_wind(pathname_wind_ww3, filename_wind_ww3)
        wd_ww3 = pd.rolling_window(wd_ww3, window=win, mean=True, axis=0, how=None)
        ws_ww3, wd_ww3 = ws_ww3[::3], wd_ww3[::3]

        # boia
        pathname_wind_buoy = '../data/boia_merenda/Vento/'
        filename_wind_buoy = 'wind_200611.txt'
        espe_buoy = np.loadtxt('../out/espe_buoy_merenda_200611.txt')
        dire_buoy = np.loadtxt('../out/dire_buoy_merenda_200611.txt')
        espe_buoy = espe_buoy * 4
        dire_buoy = pd.rolling_window(dire_buoy, window=win, center=True, mean=True, axis=1, how=None)
        dire_buoy[np.where(dire_buoy == 0)] = 0.01
        espe_buoy, dire_buoy = espe_buoy[:,::3], dire_buoy[:,::3]
        dfw = read_and_process_buoy_wind(pathname_wind_buoy)
        dfw = dfw['2006-11']
        dfw['wd1'] = dfw.wd1.rolling(window=win).mean()
        ws_buoy, wd_buoy = dfw[['ws1','wd1']].values.T
        ws_buoy, wd_buoy = ws_buoy[::3], wd_buoy[::3]

        # calcula a diferenca entre modelo e boia
        # espe = espe_ww3 - espe_buoy
        # dire = dire_ww3 - dire_buoy

        # espe = espe_ww3 - espe_prep
        # dire = dire_ww3 - dire_prep

        # normaliza os espectros
        espe1_ww3 = espe_ww3 / espe_ww3.max()
        espe1_buoy = espe_buoy / espe_buoy.max()

        espe = (espe1_ww3 - espe1_buoy) * 50
        dire = dire_ww3 - dire_buoy

        dire = pd.rolling_window(dire, window=win, mean=True, axis=1, how=None)
        
        ws = ws_ww3 - ws_buoy
        wd = wd_ww3 - wd_buoy

        pleds(faixas, espe, dire, ws, wd, title=title, namefig='../fig/pleds_diff.png', typep='diff')


    plt.show()
