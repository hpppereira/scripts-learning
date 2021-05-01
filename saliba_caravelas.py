# processamento dos dados de caravelas


import os
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.close('all')

def leitura_css(pathfile, sheet_name):
    """
    """
    # if pathfile == 'dados/Outono/20.03.27 sem onda e corrente/33° ESTAGIO OPERACIONAL_20.03.27.xlsx':
    #     dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%Y %H:%M:%S')
    # else:

    dateparse = lambda x: pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S')

    df = pd.read_excel(
                  pathfile,
                  sheet_name=sheet_name,
                  header=0,
                  names=None,
                  # index_col=[0],
                  usecols=[0,1,2],
                  squeeze=False,
                  dtype=None,
                  engine=None,
                  converters=None,
                  true_values=None,
                  false_values=None,
                  skiprows=0,
                  nrows=None,
                  na_values=None,
                  keep_default_na=True,
                  verbose=False,
                  parse_dates=None,
                  date_parser=dateparse,
                  thousands=None,
                  comment=None,
                  skipfooter=0,
                  convert_float=True,
                  mangle_dupe_cols=True)

    # pega tamanho certo da tabela
    df = df.loc[~df.Data.isna()]

    # df.index.name = 'date'
    df.columns = ['date', 'obs', 'css']
    df.set_index('date', inplace=True)
    return df


if __name__ == "__main__":

    pathname = '/home/hp/Documents/saliba_caravelas/'
    # leitura dos dados da estacao 
    # lista = glob('dados/**/Dados*auditoria*.xlsx', recursive=True)
    # lista = glob('dados/**/*ESTAGIO OPERACIONAL*.xlsx', recursive=True)
    lista = glob(pathname + 'dados/**/*ESTAGIO OPERACIONAL*.xlsx', recursive=True)

    css106 = pd.DataFrame()
    css506 = pd.DataFrame()
    for l in lista:
        print (l)

        # leitura dos dados da estacao #106
        css106_aux = leitura_css(pathfile=l, sheet_name='106')
        css106 = pd.concat((css106, css106_aux))


        # # leitura dos dados da estacao #106
        # css106_aux = leitura_css(pathfile=l, sheet_name='#106')
        # print (css106_aux.iloc[0])

        css506_aux = leitura_css(pathfile=l, sheet_name='506')
        css506 = pd.concat((css506, css506_aux))

        # css506 = leitura_css(pathfile=l, sheet_name='#506')


    fig = plt.figure(figsize=(7,5))
    ax1 = fig.add_subplot(111)
    css106.plot(ax=ax1, title='#106')
    ax1.set_ylabel('OBS (FTU) / CSS (mg/L)')
    ax1.grid()
    fig.savefig(pathname + 'css_obs_106_completo.png')

    fig = plt.figure(figsize=(7,5))
    ax1 = fig.add_subplot(111)
    css106.plot(ax=ax1, title='#106')
    ax1.set_xlim('2020-03-03','2020-03-17')
    ax1.set_ylabel('OBS (FTU) / CSS (mg/L)')
    ax1.grid()
    fig.savefig(pathname + 'css_obs_106_202003.png')

    fig = plt.figure(figsize=(7,5))
    ax1 = fig.add_subplot(111)
    css506.plot(ax=ax1, title='#506')
    ax1.set_ylabel('OBS (FTU) / CSS (mg/L)')
    ax1.grid()
    fig.savefig(pathname + 'css_obs_506_completo.png')

    fig = plt.figure(figsize=(7,5))
    ax1 = fig.add_subplot(111)
    css506.plot(ax=ax1, title='#506')
    ax1.set_xlim('2020-03-03','2020-03-17')
    ax1.set_ylabel('OBS (FTU) / CSS (mg/L)')
    ax1.grid()
    fig.savefig(pathname + 'css_obs_506_202003.png')



    plt.show()
