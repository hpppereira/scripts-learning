# Organiza dados historicos do PNBOIA do site do CHM
#
# Separar dados por campanhas
#
# Procedimentos:
# 1. Verificar Lat/Lon
# 2. Aplicar CQ
# 3. Salvar CSV padronizado
# 4. Gerar plot com Bokeeh

import os
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from importlib import reload
import controle_qualidade_pnboia
reload(controle_qualidade_pnboia)
from controle_qualidade_pnboia import qc_vartemp

plt.close('all')

def read_historic_data_chm(pathname, filename):
    """
    """
    dateparse = lambda x: pd.datetime.strptime(x, '%Y %m %d %H')

    df = pd.read_excel(pathname + filename, parse_dates=[['ano', 'mes', 'dia', 'hora']],
                                          header=0,
                                          date_parser=dateparse, index_col='ano_mes_dia_hora')
    df.index.name = 'date'

    return df

if __name__ == '__main__':

    # [limite de variacao, lag de tempo]
    lim_vartemp = {
                   'lon': [0.1, 1],
                   'lat': [0.1, 1]
                  }

    # periodo de medicao das campanhas
    campanhas = {'itajai_c1': ['2009-04-22', '2009-12-10'],
                 'itajai_c2': ['2011-02-17', '2012-10-27'],
                 'itajai_c3': ['2013-02-01', '2013-10-07'],
                 'itajai_c4': ['2014-11-06', '2015-12-09'],
                 'itajai_c5': ['2016-04-10', '2016-07-15'],
                 'itajai_c6': ['2017-02-04', '2018-11-16']
                }

    pathname = os.environ['HOME'] + '/gdrive/pnboia/dados/historico_all/'
    pathname_out = os.environ['HOME'] + '/gdrive/pnboia/dados/historico_campanhas/'
    filename = 'itajai.xlsx'

    df = read_historic_data_chm(pathname, filename)

    # coloca nan nos valor -9990
    df[df < -9000] = np.nan

    # qualifica lon, lat
    df = qc_vartemp(df.copy(), 'lon', lim_vartemp)
    df = qc_vartemp(df.copy(), 'lat', lim_vartemp)

    # coloca nan nas lon onde a lon é nan e vice-versa
    df.lat[np.where(df.lon.isna())[0]] = np.nan
    df.lon[np.where(df.lat.isna())[0]] = np.nan

    df['id_campanha'] = np.nan

    # separa dados por campanhas
    for c in campanhas.keys():
       df['id_campanha'][campanhas[c][0]:campanhas[c][1]] = int(c[-1])

    # retira os valores que nao estao em nenhuma campanha
    df = df.loc[~df.id_campanha.isna()]

    df.to_csv(pathname_out + c.split('_')[0] + '_raw.csv', float_format='%g', na_rep='NaN')