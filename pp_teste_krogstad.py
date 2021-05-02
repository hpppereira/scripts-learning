'''
metodologia de particionamento
espectral por krogstad
'''

import numpy as np

fp = np.array([0.07,0.10,0.2,0.4]) #hz - frequencia de pico
dp = np.array([200,90,30,0]) # - direcao de pico
NP = len(fp) # numero de pontos
EP = np.ones(NP) # energia da particao - limite??
EP[2] = 0.5 ##teste
a = 1 # ??
b = 1 # ??

#Checking if partition energy is below a minimum threshold.
eth = a / (fp**4 + b);

for i in range (NP):

	if EP[i] < eth[i]:
		print('Energia da Particao menor que o limite : \n'
			'eth = ' + str(eth[i]) + '  /  EP = ' + str(EP[i]))

		EP[i] = 0 #limite recebe zero
# <
# eth(i)
# EP(i)=0;