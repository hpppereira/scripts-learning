"""Funcoes uteis p PNBOIA"""


def read_historic_data_chm(pathname):
    """
    """

    dateparse = lambda x: pd.datetime.strptime(x, ' %d %b %Y %H:%M:%S')


    df = pd.read_excel(pathname + filename)

    df['date'] = [datetime.strptime(str(int(df.Ano[i])) +  str(int(df.Mes[i])).zfill(2) + str(int(df.Dia[i])).zfill(2) + str(int(df.Hora[i])).zfill(2),'%Y%m%d%H') for i in range(len(df))] 
    df = df.set_index('date')

    df.rename(columns={
            '%Longitude': 'lon',
            'Latitude': 'lat',
            'Nivel de bateria da boia (V)': 'battery',
            'Alinhamento da Boia (graus)': 'bhead',
            'Velocidade do Vento a 10 metros (m/s)': 'wspd',
            'Direcao do Vento a 4.7 metros':  'wdir',
            'Rajada do Vento a 10 metros (m/s)': 'gust',
            'Temperatura do Ar (C)': 'atmp',
            'Pressao Atmosferica (mb)': 'pres',
            'Ponto de Orvalho (C)': 'dewp',
            'Umidade Relativa': 'humi',
            'Temperatura da Superficie do Mar (C)': 'wtmp',
            'Velocidade da Corrente na profundidade de 6 a 8.5m (mm/s)': 'cvel01',
            'Direcao da Corrente na profundidade de 6 a 8.5m (graus)': 'cdir01',
            'Velocidade da Corrente na profundidade de 8.5 a 11m (mm/s)': 'cvel02',
            'Direcao da Corrente na profundidade de 8.5 a 11m (graus)': 'cdir02',
            'Velocidade da Corrente na profundidade de 11 a 13.5m (mm/s)': 'cvel03',
            'Direcao da Corrente na profundidade de 11 a 13.5m (graus)': 'cdir03',
            'Altura Significativa de Ondas (m)': 'wvht',
            'Altura Maxima de Ondas (m)': 'wmax',
            'Periodo de Pico (s)': 'dpd',
            'Direcao de Ondas media (graus)': 'mwd',
            'Espalhamento (graus)': 'spr'}, inplace=True)

    df = df[['lon', 'lat', 'bat', 'bhead', 'wspd', 'wdir', 'gust', 'atmp',
            'pres', 'dewp', 'humi', 'wtmp', 'cvel01', 'cdir01', 'cvel02',
            'cdir02', 'cvel03', 'cdir03', 'wvht', 'wmax', 'dpd', 'mwd', 'spr']]


    return df
