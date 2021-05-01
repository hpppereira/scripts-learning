# Calcula parametros espectrais dos dados d CDIP com o WAFO

import numpy as np
import pandas as pd
import xarray as xr
import wafo.spectrum.models as wsm

ds = xr.open_dataset('/home/hp/Documents/laura_cdip/214p1_historic.nc')

# data em datetime
datet = pd.to_datetime(ds.waveEnergyDensity.waveTime.values)

# valores de frequencia e direcao
f = ds.waveFrequency.values

param = []
for t in range(len(datet)):
    print ('{} de {}'.format(t, len(datet)))

    # espectro de energia
    s = ds.waveEnergyDensity.values[t,:]

    # calculo do espectro
    S = wsm.SpecData1D(s, f, type='freq',
                       freqtype='f', tr=None, h=np.inf)

    # calculo do periodo de pico
    Tp2 = 1/f[s == s.max()][0]

    # largura de banda
    bw = S.bandwidth(['alpha','eps2','eps4', 'Qp'])

    # parametrosd e onda
    [ch, R, txt] = S.characteristic(fact=np.arange(0, 15), T=2048, g=9.81)

    # momentos espectrais
    mom, mom_txt = S.moment(nr=4, even=False, j=0)

    varr = [datet[t]] + list(np.concatenate((bw, ch, mom))) + [Tp2]

    param.append(varr)

cols = ['date', 'alpha','eps2','eps4', 'Qp1'] + txt + mom_txt + ['Tp2']

param = pd.DataFrame(param, columns=cols)
param.set_index('date', inplace=True)

param.to_csv('/home/hp/Documents/laura_cdip/param_214p1_historic.csv', float_format='%.4f')