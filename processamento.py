#processamento dos dados de ondas
#dados do Bruno Movido

import numpy as np
import os
import datetime

pathname = os.environ['HOME'] + '/Desktop/movido_onda/'

ws,wd,rh,at,bp = np.loadtxt(pathname + 'Meteoro_P-40_03-09-2004_10-09-2010.txt',usecols=(2,3,4,5,6),unpack=True)
data,hora = np.loadtxt(pathname + 'Meteoro_P-40_03-09-2004_10-09-2010.txt',usecols=(0,1),dtype=str,unpack=True)

aux = np.array([[int(data[i][0:4]),int(data[i][5:7]),int(data[i][8:10])] for i in range(len(data))])

ano,mes,dia = aux[:,0],aux[:,1],aux[:,2]

#passa dia para numero de dias a partir do 01/01/0001
datenum = np.array([datetime.datetime.toordinal(datetime.date(ano[i],mes[i],dia[i])) for i in range(len(ano))])

