import pandas as pd
from pylab import show
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:admin@127.0.0.1/DADOS_MET')
df = pd.read_sql_table('dadosMeteorologicos', engine, parse_dates=['dataHora'], index_col='dataHora')

df.temperatura.plot()
show()
