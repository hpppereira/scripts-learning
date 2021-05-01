import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus as urlquote


engine = create_engine("postgres://atmos:%s@localhost:5432/postgres" % urlquote('QnDB2wNu') )

# Media movel no PANDAS
query = ("SELECT * FROM dados_omega where stid = 'ma_dt301_iv' ORDER BY timesec ASC")
df = pd.read_sql(query, engine)
df.index =  pd.to_datetime(df.time)
df = df['2021-03-10 00:00':'2021-03-15 00:00']
df = df['velvenmedsup'].rolling('3H').mean()
df_pandas = df['2021-03-13 00:00':'2021-03-15 00:00']


# Media Movel no QUERY do PostgreSQL
query = ("SELECT AD.time,avg(AD.velvenmedsup) OVER (ORDER BY AD.time ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS media_movel3h FROM (SELECT * FROM dados_omega WHERE stid = 'ma_dt301_iv') AD")
df2 = pd.read_sql(query, engine)
df2.index =  pd.to_datetime(df2.time)
df2 = df2.drop(columns = 'time')
df_sql = df2['2021-03-13 00:00':'2021-03-15 00:00']

compara = pd.concat([df_pandas,df_sql],axis=1)