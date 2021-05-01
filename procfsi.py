'''
Processamento dos dados de FSI-2D ( o FSI que mede
onda eh o 3D
Nao tem os dados de pressao. Vamos tentar obter
o espectro de heave a partir da soma dos espectros
de velocidades horizontais

a serie VX equivale a VN e a VY equivale a VE
Projeto WW3BR

Data da ultima modificacao: 25/08/2015

'''

#bibliotecas
import os
import numpy as np
import espec
from matplotlib import pylab as pl

pl.close('all')
#localizacao dos dados
pathname = os.environ['HOME'] + '/Dropbox/ww3br/dados/fsi/'

#carrega dados .fsi
#data
data = np.loadtxt(pathname + '11204_2012-02-24-12-50.fsi',
	dtype=str,skiprows=25,usecols=([0]),unpack=False)

#dados
vx,vy,hx,hy,hz,tiltx,tilty,vn,ve = np.loadtxt(pathname + '11204_2012-02-24-12-50.fsi',
	dtype=float,skiprows=25,usecols=([1,2,5,6,7,8,9,13,14]),unpack=True)

#espectros
aa_vx = espec.espec1(vx,len(vx)/16,1)
aa_vy = espec.espec1(vy,len(vy)/16,1)
aa_vn = espec.espec1(vn,len(vn)/16,1)
aa_ve = espec.espec1(ve,len(ve)/16,1)

#figuras

#espectro
pl.figure()
pl.plot(aa_vx[:,0],aa_vx[:,1])
pl.plot(aa_vn[:,0],aa_vn[:,1])
pl.plot(aa_vy[:,0],aa_vy[:,1])
pl.plot(aa_ve[:,0],aa_ve[:,1])
pl.legend(['vx','vn','vy','ve'])
pl.show()
