"""
Processamento dos dados WW3 do arquivo netCDF gerado
pela rotina spcpoint.py
henrique
"""

from matplotlib import reload
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

plt.close('all')

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

    filename = 'dspec200704.nc'

    # faixas de periodo (segundos) para a pleds
    faixa_1 = (23.9, 12.3)
    faixa_2 = (11.2, 7.6)
    faixa_3 = (7.6, 4.3)
    faixa_4 = (4.3, 2.4)

    ds, freq, direcao = read_nc(filename)

    m0_fx, dp_fx = [], []
    for t in range(ds.time.shape[0]):
        spec1d, spec2d = get_spec(ds, time=t)
        m0_fx_aux, dp_fx_aux = preppleds(freq, direcao, spec2d, faixa_1, faixa_2, faixa_3, faixa_4)
        m0_fx.append(m0_fx_aux)
        dp_fx.append(dp_fx_aux)

    # pega dados de 3 em 3 horas
    m0_fx = np.array(m0_fx).T
    dp_fx = np.array(dp_fx).T

    # monta matriz no formato para a pleds
    espe = np.zeros((8, m0_fx.shape[1]))
    dire = np.copy(espe)

    espe[[0,2,4,6],:] = m0_fx
    dire[[0,2,4,6],:] = dp_fx

    np.savetxt('../out/espe_ww3.txt', espe)
    np.savetxt('../out/dire_ww3.txt', dire)

    import pleds
    reload(pleds)
    pleds.pleds(espe, dire, title=filename, figname='pleds_ww3.png')

    # espe[,]




