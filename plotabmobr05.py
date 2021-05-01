'''
Plota os dados da BMOBR05 que sao baixados no site
da ambidados 'getbmobr05.py'
'''

import os
import pandas as pd

pathname = os.environ['HOME'] + '/Dropbox/Sistemas-BMOP/Dados/op/'

dd = pd.read_csv(pathname + 'Dados_BMOBR05.csv')

