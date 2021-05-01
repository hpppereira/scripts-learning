# -*- coding: utf-8 -*-
'''

Compara resultados do particionamento do LIOc e WW3

Data da ultima modificacao: 25/08/2015

-----------------------------------------------------------------
#LIOc
#         0   1   2   3    4     5    6   7   8     9       10      
#header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p

#  11    12   13   14    15   16   17    18   19
# hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')

-----------------------------------------------------------------

#WW3
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

import numpy as np
from matplotlib import pylab as pl
import matplotlib as mpl
from matplotlib import pyplot as plt
from datetime import datetime
import os
import netCDF4 as nc

# pl.close('all')

local = 'Rio Grande/RS'
local1 = 'rio_grande'
latlon = '-31.56667 / -49.86667'
idargos = '69153'
idwmo = '31053'
glstr = '32'

pathname = os.environ['HOME'] + '/Dropbox/ww3br/rot/out/'
# pathname = os.environ['HOME'] + '/Dropbox/ww3br/Geral/rot/out/'

#lioc
lioc = np.loadtxt(pathname + 'triaxys_' + glstr + '_' + local1 + '.out',delimiter=',',skiprows = 0)
# lioc = np.loadtxt(pathname + 'triaxys_' + glstr + '_' + local1 + '_picos.out',delimiter=',',skiprows = 0)

# lioc = np.loadtxt(os.environ['HOME'] + '/Dropbox/projetos/ww3br/Geral/doc/compartilhados/Rio Grande/paramwp_8-rio_grande.out',delimiter=',',skiprows = 0)

#recorta a serie para o periodo desejado
lfi = pl.find(lioc[:,0]==200905010000)
lfs = pl.find(lioc[:,0]==200906010000)
lioc = lioc[lfi:lfs,:]

#Carrega ww3
ww3 = np.loadtxt(pathname + 'ww3part_riogrande.out',delimiter=',')
#ww3 = np.loadtxt(pathname + 'ww3partord_riogrande.out',delimiter=',')

#carrega matriz de espec2d do ww3 para maio de 2009
tt = 198 #tempo dentro de fl do dia 200905090600 = 198
fl=nc.Dataset(pathname + 'dspec200905.nc','r')
spc2d=fl.variables['dspectr'][tt,:,:]
# spc1d=np.zeros((spc2d_Lioc.shape[0],spc2d_Lioc.shape[2]),'f')
freq=fl.variables['frequencies']
dire=fl.variables['directions']


# ============================================================================== #
#cria variaveis de datas

#lioc
datat_lioc = []
for i in range(len(lioc)):
	datat_lioc.append(datetime(int(str(lioc[i,0])[0:4]),int(str(lioc[i,0])[4:6]),int(str(lioc[i,0])[6:8]),int(str(lioc[i,0])[8:10])))

#lioc
datat_ww3 = []
for i in range(len(ww3)):
	datat_ww3.append(datetime(int(str(ww3[i,0])[0:4]),int(str(ww3[i,0])[4:6]),int(str(ww3[i,0])[6:8]),int(str(ww3[i,0])[8:10])))

datat_lioc = np.array(datat_lioc)
datat_ww3 = np.array(datat_ww3)

#============= IZABEL ============================
# ordenar e pegar os picos de sea e swell
# ================================================
ww3_tp1 = []
ww3_hs1 = []
ww3_dp1 = []
ww3_tp11 = []
ww3_hs11 = []
ww3_dp11 = []
ww3_tp2 = []
ww3_hs2 = []
ww3_dp2 = []
ww3_W1 = []
ww3_W2 = []
for i in range(len(ww3)):
	aux=[ww3[i,18],ww3[i,24],ww3[i,30],ww3[i,36],ww3[i,42],ww3[i,48]]
	n=pl.find(aux==max(aux))
	nm=pl.find(aux==min(aux))
	ww3_tp2.append(ww3[i,14+(n[0]*6)])
	ww3_hs2.append(ww3[i,13+(n[0]*6)])
	ww3_dp2.append(ww3[i,16+(n[0]*6)])
	ww3_W2.append(ww3[i,18+(n[0]*6)])
	ww3_tp1.append(ww3[i,14+(nm[0]*6)])
	ww3_hs1.append(ww3[i,13+(nm[0]*6)])
	ww3_dp1.append(ww3[i,16+(nm[0]*6)])
	ww3_W1.append(ww3[i,18+(nm[0]*6)])
	#pegar o segundo maior (deve ter uma forma inteligente de fazer)
	aux[n[0]]=0
	nn=pl.find(aux==max(aux))
	if nn != []:
		ww3_tp11.append(ww3[i,14+(nn[0]*6)])
		ww3_hs11.append(ww3[i,13+(nn[0]*6)])
		ww3_dp11.append(ww3[i,16+(nn[0]*6)])
	else:
		ww3_tp11.append(np.nan)
		ww3_hs11.append(np.nan)
		ww3_dp11.append(np.nan)
	




ww3_tp1 = np.array(ww3_tp1)
ww3_hs1 = np.array(ww3_hs1)
ww3_dp1 = np.array(ww3_dp1)
ww3_tp11 = np.array(ww3_tp11)
ww3_hs11 = np.array(ww3_hs11)
ww3_dp11 = np.array(ww3_dp11)
ww3_tp2 = np.array(ww3_tp2)
ww3_hs2 = np.array(ww3_hs2)
ww3_dp2 = np.array(ww3_dp2)
ww3_W1 = np.array(ww3_W1)
ww3_W2 = np.array(ww3_W2)


n1=np.where(ww3[:,3]<=1) #achar unimodais
ww3_tp2 [n1] = np.nan
ww3_hs2 [n1] = np.nan
ww3_dp2 [n1] = np.nan
ww3_W2 [n1] = np.nan

n1=np.where(ww3_W2<=.60) #achar que tem frcao baixa (60% de limite - procurar bibliografia)
ww3_tp2 [n1] = np.nan
ww3_hs2 [n1] = np.nan
ww3_dp2 [n1] = np.nan
ww3_W2 [n1] = np.nan

#######################################################################
#divisao de sea e swell - WAMDI 1988

#calcula o H com base no vento (utilizar somente modelado)
#fazer um grafico de espalhamento (scatter) de de HxU
#plotar a linha de H - o que tiver abaixo da linha eh dominado
#por windsea e o que estiver acima por swell

U = ww3[:,5] #velocidade do vento
H =  []
for i in range(len(U)):

	if U[i] <= 7.5:

		H.append(1.614 * 0.01 * (U[i] ** 2))

	elif U[i] > 7.5:

		H.append(0.01 * (U[i] ** 2) + 8.134 * (0.0001 * U[i] ** 3) )

H = np.array(H)


# #######################################################################
#obtentcao do espec1d do ww3 a partir da integracao do espec 2d

# Espectro 1D
spc1d=np.sum(spc2d,axis=1)


# #######################################################################
# #figuras

# #compara hs, tp e dp
# plt.figure()
# plt.subplot(311)
# plt.plot(datat_lioc,lioc[:,6],'b')
# plt.plot(datat_ww3,ww3[:,7],'r')
# plt.grid()
# plt.ylabel('Hm0 (m)')
# plt.subplot(312)
# plt.plot(datat_lioc,lioc[:,7],'bo')
# plt.plot(datat_ww3,ww3[:,8],'ro')
# plt.grid()
# plt.ylabel('Tp (s)')
# plt.subplot(313)
# plt.plot(datat_lioc,lioc[:,8]-23,'bo') ##corrigir decl mag
# plt.plot(datat_ww3,ww3[:,10],'ro')
# plt.grid()
# plt.ylabel('Dp (graus)')

# #comparacao dp com e sem decl mag
# plt.figure()
# plt.subplot(211)
# plt.plot(datat_lioc,lioc[:,8],'bo') ##corrigir decl mag
# plt.plot(datat_ww3,ww3[:,10],'ro')
# plt.grid()
# plt.ylabel('Dp (graus) - sem dec.mag')
# plt.subplot(212)
# plt.plot(datat_lioc,lioc[:,8]-23,'bo') ##corrigir decl mag
# plt.plot(datat_ww3,ww3[:,10],'ro')
# plt.grid()
# plt.ylabel('Dp (graus) - com dec.mag')


# #######################################################################

# #coparaca particao - hs, tp e dp
# plt.figure()
# plt.title('Hm0 - particionado')
# plt.plot(datat_lioc,lioc[:,14],'o',label='boia_2')
# plt.plot(datat_ww3,ww3[:,13],'-',label='ww3_1')
# plt.plot(datat_ww3,ww3[:,19],'-',label='ww3_2')
# plt.plot(datat_ww3,ww3[:,25],'-',label='ww3_3')
# plt.plot(datat_ww3,ww3[:,31],'-',label='ww3_4')
# plt.plot(datat_ww3,ww3[:,37],'-',label='ww3_5')
# plt.plot(datat_ww3,ww3[:,43],'-',label='ww3_6')

# plt.legend()

# plt.figure()
# plt.title('Tp - particionado')
# plt.plot(datat_lioc,lioc[:,15],'o',label='boia_2')
# plt.plot(datat_ww3,ww3[:,14],'-',label='ww3_1')
# plt.plot(datat_ww3,ww3[:,20],'-',label='ww3_2')
# plt.plot(datat_ww3,ww3[:,26],'-',label='ww3_3')
# plt.plot(datat_ww3,ww3[:,32],'-',label='ww3_4')
# plt.plot(datat_ww3,ww3[:,39],'-',label='ww3_5')
# plt.plot(datat_ww3,ww3[:,44],'-',label='ww3_6')

# plt.legend()

# plt.figure()
# plt.title('Dp - particionado')
# plt.plot(datat_lioc,lioc[:,16]-23,'o',label='boia_2')
# plt.plot(datat_ww3,ww3[:,16],'-',label='ww3_1')
# plt.plot(datat_ww3,ww3[:,22],'-',label='ww3_2')
# plt.plot(datat_ww3,ww3[:,28],'-',label='ww3_3')
# plt.plot(datat_ww3,ww3[:,34],'-',label='ww3_4')
# plt.plot(datat_ww3,ww3[:,40],'-',label='ww3_5')
# plt.plot(datat_ww3,ww3[:,46],'-',label='ww3_6')


# #######################################################################

#hm0 total
plt.figure()
plt.plot(U,H,'k.',label='Limite Sea/Swell')
plt.plot(U,lioc[:,6],'b*',label='Hm0-Boia')
plt.plot(U,ww3[:,7],'ro',label='Hm0-WW3')
plt.xlabel('Velocidade do vento (m/s)')
plt.ylabel('Altura de Onda (m)')
plt.legend(loc=0)
plt.grid()

#hm01
plt.figure()
plt.plot(U,H,'k.',label='Limite Sea/Swell')
plt.plot(U,lioc[:,11],'b*',label='Hm0-Boia-Pico1')
plt.xlabel('Velocidade do vento (m/s)')
plt.ylabel('Altura de Onda (m)')
plt.legend(loc=0)
plt.grid()

#hm02
plt.figure()
plt.plot(U,H,'k.',label='Limite Sea/Swell')
plt.plot(U,lioc[:,14],'b*',label='Hm0-Boia-Pico2')
plt.xlabel('Velocidade do vento (m/s)')
plt.ylabel('Altura de Onda (m)')
plt.legend(loc=0)
plt.grid()

# #######################################################################

#plotagem do espectro 2d do ww3
# plt.figure()
# plt.contourf(freq,dire,spc2d)
# plt.xlabel('Freq. (Hz)'), plt.ylabel('graus')
# plt.colorbar(label=u'm2/Hz')


#plt.show()



# #compara hs, tp e dp
# plt.figure()
# plt.subplot(311)
# plt.plot(datat_lioc,lioc[:,6],'b')
# plt.plot(datat_ww3,ww3[:,7],'r')
# plt.grid()
# plt.ylabel('Hm0 (m)')
# plt.xticks(visible=False)
# pl.legend(['boia','ww3'],loc=0)
# plt.subplot(312)
# plt.plot(datat_lioc,lioc[:,7],'bo')
# plt.plot(datat_ww3,ww3[:,8],'ro')
# plt.grid()
# plt.ylabel('Tp (s)')
# plt.xticks(visible=False)
# plt.subplot(313)
# plt.plot(datat_lioc,lioc[:,8]-23,'bo') ##corrigir decl mag
# plt.plot(datat_ww3,ww3[:,10],'ro')
# plt.grid()
# plt.ylabel('Dp (graus)')


#######################################################################

#coparaca particao - hs, tp e dp
plt.figure()
plt.subplot(411)
# plt.title('Hm0 - particionado')
#plt.plot(datat_ww3,ww3[:,13],'bo',label='ww3_1')
plt.plot(datat_ww3,ww3_hs2,'go',label='windsea_ww3')
# plt.plot(datat_ww3,ww3[:,19],'-',label='ww3_2')
# plt.plot(datat_ww3,ww3[:,25],'b-',label='ww3_3')
# plt.plot(datat_ww3,ww3[:,31],'-',label='ww3_4')
# plt.plot(datat_ww3,ww3[:,37],'-',label='ww3_5')
# plt.plot(datat_ww3,ww3[:,43],'-',label='ww3_6')
plt.plot(datat_lioc,lioc[:,14],'ro',label='windsea_boia')
plt.ylim(0,7), plt.legend(loc=0)
plt.ylabel('Hm0 (m)')
plt.xticks(visible=False)
plt.grid()

plt.subplot(412)
# plt.title('Tp - particionado')
#plt.plot(datat_ww3,ww3[:,14],'bo',label='ww3_1')
plt.plot(datat_ww3,ww3_tp2,'go',label='ww3_ord')
# plt.plot(datat_ww3,ww3[:,20],'-',label='ww3_2')
# plt.plot(datat_ww3,ww3[:,26],'-',label='ww3_3')
# plt.plot(datat_ww3,ww3[:,32],'bo',label='ww3_4')
# plt.plot(datat_ww3,ww3[:,39],'-',label='ww3_5')
# plt.plot(datat_ww3,ww3[:,44],'-',label='ww3_6')
plt.plot(datat_lioc,lioc[:,15],'ro',label='boia_2')
plt.ylim(0,25)
plt.ylabel('Tp (s)')
plt.xticks(visible=False)
plt.grid()

plt.subplot(413)
# plt.title('Dp - particionado')
#plt.plot(datat_ww3,ww3[:,16],'bo',label='ww3_1')
plt.plot(datat_ww3,ww3_dp2,'go',label='ww3_ord')
# plt.plot(datat_ww3,ww3[:,22],'-',label='ww3_2')
# plt.plot(datat_ww3,ww3[:,28],'b-',label='ww3_3')
# plt.plot(datat_ww3,ww3[:,34],'-',label='ww3_4')
# plt.plot(datat_ww3,ww3[:,40],'-',label='ww3_5')
# plt.plot(datat_ww3,ww3[:,46],'-',label='ww3_6')
plt.plot(datat_lioc,lioc[:,16]-23,'ro',label='boia_2')
plt.ylim(0,360)
plt.ylabel('Dp (graus)')
plt.grid()

plt.subplot(414)
plt.plot(datat_ww3,ww3_W2,'yo',label='npart')
plt.ylabel('fracao windsea')
plt.grid()

plt.figure()
plt.subplot(411)
# plt.title('Hm0 - particionado')
#plt.plot(datat_ww3,ww3[:,13],'bo',label='ww3_1')
plt.plot(datat_ww3,ww3_hs1,'go',label='swell_ww3')
plt.plot(datat_ww3,ww3_hs11,'bo',label='swell2_ww3')
# plt.plot(datat_ww3,ww3[:,19],'-',label='ww3_2')
# plt.plot(datat_ww3,ww3[:,25],'b-',label='ww3_3')
# plt.plot(datat_ww3,ww3[:,31],'-',label='ww3_4')
# plt.plot(datat_ww3,ww3[:,37],'-',label='ww3_5')
# plt.plot(datat_ww3,ww3[:,43],'-',label='ww3_6')
plt.plot(datat_lioc,lioc[:,11],'ro',label='swell_boia')
plt.ylim(0,7), plt.legend(loc=9,ncol=3)
plt.ylabel('Hm0 (m)')
plt.xticks(visible=False)
plt.grid()

plt.subplot(412)
# plt.title('Tp - particionado')
#plt.plot(datat_ww3,ww3[:,14],'bo',label='ww3_1')
plt.plot(datat_ww3,ww3_tp1,'go',label='ww3_ord')
plt.plot(datat_ww3,ww3_tp11,'bo',label='ww3_ord')
# plt.plot(datat_ww3,ww3[:,20],'-',label='ww3_2')
# plt.plot(datat_ww3,ww3[:,26],'-',label='ww3_3')
# plt.plot(datat_ww3,ww3[:,32],'bo',label='ww3_4')
# plt.plot(datat_ww3,ww3[:,39],'-',label='ww3_5')
# plt.plot(datat_ww3,ww3[:,44],'-',label='ww3_6')
plt.plot(datat_lioc,lioc[:,12],'ro',label='boia_2')
plt.ylim(0,25)
plt.ylabel('Tp (s)')
plt.xticks(visible=False)
plt.grid()

plt.subplot(413)
# plt.title('Dp - particionado')
#plt.plot(datat_ww3,ww3[:,16],'bo',label='ww3_1')
plt.plot(datat_ww3,ww3_dp1,'go',label='ww3_ord')
plt.plot(datat_ww3,ww3_dp11,'bo',label='ww3_ord')
# plt.plot(datat_ww3,ww3[:,22],'-',label='ww3_2')
# plt.plot(datat_ww3,ww3[:,28],'b-',label='ww3_3')
# plt.plot(datat_ww3,ww3[:,34],'-',label='ww3_4')
# plt.plot(datat_ww3,ww3[:,40],'-',label='ww3_5')
# plt.plot(datat_ww3,ww3[:,46],'-',label='ww3_6')
plt.plot(datat_lioc,lioc[:,13]-23,'ro',label='boia_2')
plt.ylim(0,360)
plt.ylabel('Dp (graus)')
plt.grid()

plt.subplot(414)
plt.plot(datat_ww3,ww3_W1,'yo',label='npart')
plt.ylabel('fracao windsea')
plt.grid()

plt.show()

