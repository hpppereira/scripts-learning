'''
Leitura do resultado do WW3
para a saida particionada
com todos os pontos

colunas = tempo
linhas = valores
#cria matriz para colocar os valores das particoes

#   0    1     2    3      4    5   6   
# data, lat, lon, npart, prof, ws, wd

#  7    8   9   10   11    12
# hs0, tp0, L0, dp0, spr0, W0

# 13    14  15  16    17   18
# hs1, tp1, L1, dp1, spr1, W1

# 19   20   21  22    23   24
# hs2, tp2, L2, dp2, spr2, W2

#  25  26   27  28   29    30
# hs3, tp3, L3, dp3, spr3, W3

# 31   32   33   34   35   36
# hs4, tp4, L4, dp4, spr4, W4

# 37   38   39   40   41   42
# hs5, tp5, L5, dp5, spr5, W5

# 43   44   45   46   47   48
# hs6, tp6, L6, dp6, spr6, W6
'''
from matplotlib import pylab as pl
import numpy as np
import os

pathname = os.environ['HOME'] + '/Dropbox/ww3br/dados/ww3/'

f = open(pathname + 'RioGrande_200905_part.ww3')

# data = []
# lat = []
# lon = []
# local = [] #local - string
# npart = [] #numero das particoes
# prof = []
# ws = []
# wd = []

mat = np.zeros((745,49))
mat[:,:] = np.nan
npa = mat.shape[1] - 1 #numero de parametros analisados

# c = 0
t = -1
lines = f.readlines()

for l in range(len(lines)):

	if "PNBOIARGra" in lines[l]:

		t += 1

		cabec = lines[l].split()
		mat[t,0] = float(cabec[0] + cabec[1][0:4]) #data
		mat[t,1] = float(cabec[2]) #lat
		mat[t,2] = float(cabec[3]) #lon
		mat[t,3] = float(cabec[5]) #numero de particoes
		mat[t,4] = float(cabec[6]) #prof
		mat[t,5] = float(cabec[7]) #vel vento
		mat[t,6] = float(cabec[8]) #dir vento

		#numero de particoes
		npart = int(mat[t,3])

		#varia as linhas das particoes
		aux = 7 #valor auxiliar para colocacao dos valores em mat
		for p in range(1,npart+2): #+ 2 pq eh numpart + 1 e inicia do 1

			#parametros de cada particao (linha)
			pp = np.array(lines[l+p].split()).astype(float)
			pp = pp[1:] #retira a primeira linha (n da particao)
			mat[t,aux:aux+6] = pp
			aux += 6

mat = mat[:t,:]

mato = np.copy(mat) #mat ordenada por frequencias


#ordenar matriz em ordem descrescente de periodo
for i in range(0,len(mat),6):
	a = mat[i,7:]
	b = a.reshape((len(a)/6,6))
	c = np.argsort(b[:,1]) #acha os indices ordenados pelo periodo
	d = b[c,:] #deixa o maiores periodos nas primeiras linhas
	d[pl.find(np.isnan(d[:,1])==False)] = np.flipud(d[pl.find(np.isnan(d[:,1])==False)])
	e = d.reshape((d.shape[0] * d.shape[1])) #cria vetor 1d
	# print '---- \n',d

	mato[i,7:] = e #matriz de dados ordenada por periodo

np.savetxt('out/ww3part_riogrande.out',mat,delimiter=',',fmt=['%i']+npa*['%.2f'],
	header='data,lat,lon,npart,prof,ws,wd,hs0,tp0,L0,dp0,spr0,W0,hs1,tp1,L1,dp1,spr1,W1,hs2,tp2,L2,dp2,spr2,W2,hs3,tp3,L3,dp3,spr3,W3,hs4,tp4,L4,dp4,spr4,W4,hs5,tp5,L5,dp5,spr5,W5,hs6,tp6,L6,dp6,spr6,W6')

np.savetxt('out/ww3partord_riogrande.out',mato,delimiter=',',fmt=['%i']+npa*['%.2f'],
	header='data,lat,lon,npart,prof,ws,wd,hs0,tp0,L0,dp0,spr0,W0,hs1,tp1,L1,dp1,spr1,W1,hs2,tp2,L2,dp2,spr2,W2,hs3,tp3,L3,dp3,spr3,W3,hs4,tp4,L4,dp4,spr4,W4,hs5,tp5,L5,dp5,spr5,W5,hs6,tp6,L6,dp6,spr6,W6')

