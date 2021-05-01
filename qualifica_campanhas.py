# Qualificar dados das campanhas de medições do PNBOIA
# e adicionar no Banco de Dados
#
# Procedimentos:
# 2. Aplicar CQ
# 3. Salvar CSV padronizado
# 4. Gerar plot com Bokeeh

import os
import pandas as pd
from importlib import reload
import controle_qualidade_pnboia
reload(controle_qualidade_pnboia)
from controle_qualidade_pnboia import *

def carrega_dados_brutos(pathname, filename):
    """
    """
    df = pd.read_csv(pathname + filename, index_col='date', parse_dates=True)

    return df

def qualifica_dados(df):

    # define limites
    lim_range, lim_spike, lim_vartemp = limites_qc()    

    for v in lim_range.keys():
        df_qc[v] = qc_range(df_qc, v, lim_range)

    for v in lim_spike.keys():
        df_qc[v] = qc_spike(df_qc, v, lim_spike)

    for v in lim_vartemp.keys():
        df_qc[v] = qc_vartemp(df_qc, v, lim_vartemp)

    return df_qc

def atualiza_bd():
    pass

def limites_qc():
    """
    """
    lim_range = {
                 'wspd1': [0, 59],
                 'gust1': [0, 59],
                 'wdir1': [0, 360],
                 'wspd2': [0, 59],
                 'gust2': [0, 59],
                 'wdir2': [0, 360],
                 'atmp': [-39, 59],
                 'humi': [25, 102],
                 'dewp': [-29, 39],
                 'pres': [501, 1099],
                 'wtmp': [-3, 29],
                 'bhead': [0, 360],
#                 'arad': [0, np.inf],
                 'cvel01': [-4990, 4990],
                 'cdir01': [0, 360],
                 'cvel02': [-4990, 4990],
                 'cdir02': [0, 360],
                 'cvel03': [-4990, 4990],
                 'cdir03': [0, 360],
                 'wvht': [0, 19.9],
                 'wmax': [0, 19.9],
                 'dpd': [1.7, 25],
                 'mwd': [0, 360],
                 'spr': [0, 360],
                 }

    lim_spike = {
                 'wspd1': 6.0,
                 'gust1': 6,
                 'wdir1': 6,
                 'wspd2': 6,
                 'gust2': 6,
                 'wdir2': 6,
                 'atmp': 6,
                 'humi': 6,
                 'dewp': 6,
                 'pres': 6,
                 'wtmp': 6,
                 'bhead': 6,
                 'arad': 6,
                 'cvel01': 6,
                 'cdir01': 6,
                 'cvel02': 6,
                 'cdir02': 6,
                 'cvel03': 6,
                 'cdir03': 6,
                 'wvht': 6,
                 'wmax': 6,
                 'dpd': 6,
                 'mwd': 6,
                 'spr': 6,
                 }


    lim_vartemp = {
                   'wspd1': [5, 1],
                   'atmp': [3, 1],
                   #'humi': [np.inf, 1],
                   #'dewp': [1, ],
                   'pres': [6, 1],
                   'wtmp': [3, 1],
                   #'bhead': [1, ],
                   #'arad': [1, ],
                   'cvel01': [132, 1],
                   #'cdir01': [1, ],
                   'cvel02': [132, 1],
                   #'cdir02': [1, ],
                   'cvel03': [132, 1],
                   #'cdir03': [1, ],
                   'wvht': [2, 1],
                   #'wmax': [1, ],
                   #'dpd': [1, ],
                   #'mwd': [1, ],
                   #'spr': [1, ], 
                  }
                   
    return lim_range, lim_spike, lim_vartemp

if __name__ == "__main__":

    pathname = os.environ['HOME'] + '/gdrive/pnboia/dados/historico_campanhas/'
    filename = 'itajai_raw.csv'
    filename_out = 'itajai'

    df_raw = carrega_dados_brutos(pathname, filename)
    df_qc = df_raw.copy()

    df_qc = qualifica_dados(df_qc)

    # salva 
    df_qc.to_csv(pathname + filename_out + '_qc.csv', float_format='%g', na_rep='NaN')

    # loop para salvar dados por campanha
    for c in df_qc.id_campanha.unique():
        df_qc.loc[df_qc.id_campanha == c].to_csv(pathname + filename_out + '_qc_c{}.csv'.format(c))




#
