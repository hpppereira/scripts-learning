

import numpy as np
import pandas as pd


def qc_range(df, v, lim):
    """
    Teste Range
    df = matriz de dados
    v = variavel
    lim = dicionario com limites
    """

    # teste de range
    df[v].loc[(df[v] < lim[v][0]) | (df[v] > lim[v][1])] = np.nan

    return df[v]

def qc_spike(df, v, lim):
    """
    Teste Spike
    df = matriz de dados
    v = variavel
    lim = dicionario com desvio padrao
    """

    df[v].loc[(np.abs(df[v]) > df[v].mean() + (lim[v] * df[v].std()))] = np.nan

#    print ('Media: {}'.format(np.nanmean(df[v])))
#    print ('Des. Pad: {}'.format(np.nanstd(df[v])*lim[v]))

    return df[v]

def qc_vartemp(df, v, lim):
    """
    # hist(np.diff(df.wvht.iloc[np.where(pd.to_timedelta(a) < '0 days 02:00:00')]), 500)
    Teste Variabilidade Temporal
    df = matriz de dados
    v = variavel
    lim = dicionario com valor limite e lag
    """

    # derivada 
    d = np.diff(df[v])

    df[v].iloc[np.where(np.abs(d) > lim[v][0])[0]] = np.nan

    return df[v]

def qc_sensores_correlatos():
    pass

