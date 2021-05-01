'''
baixa os dados do site da vale
de forma operacional

roda pelo crontab o shell: 'vale_op.sh'
'''



import numpy as np
import urllib
from bs4 import BeautifulSoup
import subprocess

##### =============================================================== #####

site_boia4 = 'http://www.ambidados.net/vale/boia4.html'
site_boia10 = 'http://www.ambidados.net/vale/boia10.html'
saida = '/home/lioc/Dropbox/ww3vale/Geral/TU/dados/ADCP/operacional/'

##### =============================================================== #####
##### BOIA 4

#baixa o dado e cria uma variavel string
response = urllib.urlopen(site_boia4)
html = response.read()
soup = BeautifulSoup(html)
table = soup.find('table')
rows = table.findAll('tr')

#acha a primeira linha de dados
dd = rows[3].findAll('td')

data = str(dd[0].text)
bate = float(str(dd[1].text).replace(',','.'))
rumo = float(str(dd[2].text).replace(',','.'))
pres = float(str(dd[3].text).replace(',','.'))
temp = float(str(dd[4].text).replace(',','.'))
pitch = float(str(dd[5].text).replace(',','.'))
roll = float(str(dd[6].text).replace(',','.'))
hs = float(str(dd[7].text).replace(',','.'))
dp = float(str(dd[8].text).replace(',','.'))
tp = float(str(dd[9].text).replace(',','.'))

#cria data com numero inteiro (AAAAMMDDHHMM)
datai = int(data[6:10]+data[3:5]+data[0:2]+data[11:13]+data[14:16])

#cria matriz com variaveis
boia4 = np.array([[datai,bate,rumo,pres,temp,pitch,roll,hs,tp,dp]])

# 'data, bate, rumo, pres, temp, pitch, roll, hs, tp, dp')
np.savetxt(saida + 'aux_TU_boia04.out',boia4,delimiter=',',fmt=['%i']+9*['%.2f'])
    

# ##### =============================================================== #####
# ##### BOIA 10

#baixa o dado e cria uma variavel string
response = urllib.urlopen(site_boia10)
html = response.read()
soup = BeautifulSoup(html)
table = soup.find('table')
rows = table.findAll('tr')

#acha a primeira linha de dados
dd = rows[3].findAll('td')

data = str(dd[0].text)
bate = float(str(dd[1].text).replace(',','.'))
rumo = float(str(dd[2].text).replace(',','.'))
pres = float(str(dd[3].text).replace(',','.'))
temp = float(str(dd[4].text).replace(',','.'))
pitch = float(str(dd[5].text).replace(',','.'))
roll = float(str(dd[6].text).replace(',','.'))
hs = float(str(dd[7].text).replace(',','.'))
dp = float(str(dd[8].text).replace(',','.'))
tp = float(str(dd[9].text).replace(',','.'))

#cria data com numero inteiro (AAAAMMDDHHMM)
datai = int(data[6:10]+data[3:5]+data[0:2]+data[11:13]+data[14:16])

#cria matriz com variaveis
boia10 = np.array([[datai,bate,rumo,pres,temp,pitch,roll,hs,tp,dp]])

# data, bate, rumo, pres, temp, pitch, roll, hs, tp, dp
np.savetxt(saida + 'aux_TU_boia10.out',boia10,delimiter=',',fmt=['%i']+9*['%.2f'])

#concatena com a matriz 'boia10_TU_op.out'
# #abre o arquivo no formato de append
# file = open('saida/op_vale/boia10_TU_op.out','a')
# aux = str(boia10)
# file.write(str(boia10[0].astype(str)))
# file.close()

# #caso precise salvar a primeira linha, com cabecalho
# np.savetxt('saida/op_vale/'+'boia10_TU_op.out',boia10,delimiter=',',fmt=['%i']+9*['%.2f'],
#     header='data, bate, rumo, pres, temp, pitch, roll, hs, tp, dp')
