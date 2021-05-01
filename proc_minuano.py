

import pandas as pd
import matplotlib.pyplot as plt
plt.close('all')

dateparse = lambda x: pd.datetime.strptime(x, '%Y %m %d %H')

df = pd.read_csv('minuano.csv',
                 parse_dates=[['year', 'month', 'day', 'hour']],
                 date_parser=dateparse,
                 index_col='year_month_day_hour')

df.index.name = 'date'


fig = plt.figure(figsize=(10,15),facecolor='w')

ax1 = fig.add_subplot(311)
ax1.plot(df.bp)
ax1.set_ylabel('Pressão Atm. (hPa)')
ax1.set_title('PNBOIA - MINUANO')
ax1.grid()

ax2 = fig.add_subplot(312, sharex=ax1)
ax2.plot(df.ws1)
ax22 = ax2.twinx()
ax22.plot(df.wd1, 'r.')
ax2.set_ylabel('Wind Spd. (m/s)')
ax2.grid()

ax3 = fig.add_subplot(313, sharex=ax1)
ax3.plot(df.sigw)
ax3.plot(df.maxw, 'r')
ax3.set_ylabel('Hs (m)')
ax3.grid()

plt.show()