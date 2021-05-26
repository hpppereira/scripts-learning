'''
Programa para carregar e plotar
o espectro 1d e 2d da saida do ww3

Realiza testes de procedimento
de particionamento espectral
'''

#carrega bibliotecas necessarias
import netCDF4 as nc
import pylab as pl
import os
#apaga as figuras
pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/ww3vale_old/Geral/partespec/dados/'

#abre o arquivo nc
dados = nc.Dataset(pathname + 'dspec032_2014110400.nc','r')

#mostra variaveis
print dados

#define variaveis
spec2 = dados.variables['dspectr'][:] #espectro 2D
freq = dados.variables['frequencies'][:] #frequencia
dire = dados.variables['directions'][:] #direcao

#plota espectro 2D (tempo 0)
pl.contourf(freq,dire,spec2[0,:,:])
pl.colorbar()
pl.xlabel('Frequencia (Hz)')
pl.ylabel('Direcao (graus)')

#integra o espectro 2D em direcao para obter o espectro 1D

spec1 = []
for i in range(len(freq)):

    spec1.append(sum(spec2[0,:,i]))

#plota o espectro 1D (tempo 0)
pl.figure()
pl.plot(freq,spec1)
pl.xlabel('Frequencia (Hz)')
pl.ylabel('Energia (m2/Hz)')

pl.show()