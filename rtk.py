
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from scipy import signal
from scipy.interpolate import interp1d

plt.close('all')

mare = pd.read_csv('tide_data.txt', sep='\t', header=0, names=['date','mare'],
                   index_col='date', parse_dates=True)

dateparse = lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S')
mare_tmib = pd.read_csv('TMIB_CELSE_Mare.txt', sep='\t', header=0,
                   index_col='Timestamp', parse_dates=True, date_parser=dateparse)

# mare = mare['2020-08-18':'2020-08-21']

# formato de data do arquivo rtk
dateparse_rtk = lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S.%f')

# lista dos arquivos rtk
lista_rtk = np.sort(glob('RTK/alt_*.txt'))

# arquivo a ser concatenado
df = pd.DataFrame()

# loop dos arquivos diarios

cont = 0
for arquivo_rtk in lista_rtk:
    cont += 1
    print ('{} de {}'.format(cont, len(lista_rtk)))
    print (arquivo_rtk)
    aux = pd.read_csv(arquivo_rtk, sep='\s+', parse_dates=[['UTC', 'date']],
                    date_parser=dateparse_rtk, index_col=['UTC_date'])

    df = pd.concat((df, aux), axis=0)

# coloca dataframe em ordem crescente de data
df.sort_index(inplace=True)

# hora utc para local
df.index = df.index - timedelta(hours=3)

# filtro passa baixa
fc = 0.05  # Cut-off frequency of the filter
fs = 1.0
w = fc / (fs / 2) # Normalize the frequency
b, a = signal.butter(5, w, 'high')
df['onda'] = signal.filtfilt(b, a, df, axis=0)

rbr = pd.DataFrame(index=pd.date_range(mare_tmib.index[0], mare_tmib.index[-1], freq='1S'))

# ondadf = pd.concat((df.onda.iloc[1315000:1340000],df.onda.iloc[125000:156305]),
#                   axis=0, ignore_index=True)

ondadf = df.onda.values[200000:]
lista_onda = list(ondadf) * 6
onda = np.array(lista_onda)[:len(rbr)]
onda1 = onda[np.random.randint(len(onda), size=(len(onda)))]

# correcao de spikes
onda1[np.where(onda1 < -2)[0]] = onda1[np.where(onda1 < -2)[0]] + 1
onda1[np.where(onda1 > +2)[0]] = onda1[np.where(onda1 > +2)[0]] - 1

# interpola mare_tmib para o numero de pontos da serie do rbr
x = np.linspace(0, len(mare_tmib), len(mare_tmib))
y = mare_tmib.Depth.values
fint = interp1d(x, y, kind='cubic')
xnew = np.linspace(0, len(mare_tmib), len(rbr))
mareint = fint(xnew)

rbr['pressao'] = mareint + onda1
rbr['pressao'] = rbr.pressao - 15.32
rbr.index.name = 'data'

rbr.to_csv('dados_rbr.csv', float_format='%.3f')

# aux = np.random.rand(len(mare_tmib)) * 1.5
# aux = aux - aux.mean()
# a = mare_tmib.resample('1S').asfreq()
# b = a.interpolate()
# c = b + aux

# df1 = df['Altitude0'].resample('2Min', loffset='2Min').mean()
# df2 = df['marefilt'].resample('5Min', loffset='2Min').mean()


#correcoes de niveis de mare
# mare_tmib['Depth'] = mare_tmib['Depth'] - float(mare_tmib.Depth.mean() - mare.mean())
# df1cor = df1 - float(np.nanmean(df1) - mare.mean()) 
# df['marefiltcor'] = df['marefilt'] - float(np.nanmean(df.marefilt) - mare.mean())

# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.plot(df.index, df.Altitude0, label='RTK_bruto')
# ax1.plot(df.index, df.marefiltcor, label='RTKfiltcor')
# ax1.plot(df1cor.index, df1cor, label='RTK2mincor')
# ax1.legend()

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(rbr.index, rbr.pressao, label='RBR')
ax1.plot(mare.index, mare.mare, label='Mare')
# ax1.plot(mare_tmib.index, mare_tmib.Depth, label='TMIB')
# ax1.plot(mare_tmib.index, mare_tmib.marerand, label='TMIBW')
# ax1.plot(df.index, df.Altitude0, label='RTK')
# ax1.plot(df1.index, df1.Altitude0, label='RTK2min')
# ax1.plot(df2.index, df2.Altitude0, label='RTK2mincorr')
ax1.legend()

# df1 = df.rolling('2Min').mean()
# # df2 = df.resample('2Min').asfreq()

# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# # ax1.plot(df)
# ax1.plot(df1 + 1.4, label='rolling')
# ax1.plot(df2 + 1.4, label='mean')
# # ax1.plot(df3 + 1.4, label='mean')
# ax1.plot(mare, label='mare')
# ax1.set_xlim(df1.index[0], df1.index[-1])
# ax1.legend()

plt.show()