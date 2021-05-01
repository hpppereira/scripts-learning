# -*- coding: utf-8 -*-
'''
Comparacao dos dados brutos e processados da boia
do SIODOC.

# Laboratorio de Instrumentacao Oceanografica - LIOc-COPPE/UFRJ

Infos:
1) Boia Wavescan (heave, pitch e roll)
2) Tem os dados de bussola
3) Precisa descontar a declinacao magnetica

Duvidas/Pesquisas:
a) Precisa fazer a correcao da bussola nas series
de heave, pitch e roll, segundo NDBC 96, pg13 ?
b) Verificar a combinacao necessaria para a DAAT/PLEDS.
Plotar o vento e comparar com a faixa 4.
  b.1) Verificar a mudança na direcao da faixa um, tem que
  rotacionar no sentido anti-horario.
c) Processar os dados brutos e comparar com os parametros
processados pela boia
d) Na PLEDS, plotar o vento e a direcao das ondas para
tentar
'''

import numpy as np
import pylab as pl
from datetime import datetime 
import os

# pl.close('all')

#caminho dos parametros processado pela boia e pelo lioc
pathname_siodoc = os.environ['HOME'] + '/Dropbox/siodoc/dados/proc/'
pathname_lioc = os.environ['HOME'] + '/Dropbox/siodoc/rot/saida/'

#carrega a planilha de dados
dd = np.loadtxt(pathname_siodoc + 'janis_data.dat') #siodoc
dd_lioc = np.loadtxt(pathname_lioc + 'paramwp_8-arrcabo_siodoc.out',delimiter=',') #lioc

#decinacao mag (-23 graus)
#Obs: os dados de direcao das ondas e do vento
#	  sao corrigidos abaixo
dmag = -23

#data com datetime
#siodoc
datat = [datetime(int(dd[i,2]),int(dd[i,1]),int(dd[i,0]),int(dd[i,3])) for i in range(len(dd))]

#data em string
datat_str = np.array(datat).astype(str)

#lioc
# deixa em string a data em numero (auxiliar para o datat_lioc)
#formata o vetor de datas pra long e depois string
datat_lioc = dd_lioc[:,0].astype(np.long)
datat_lioc = datat_lioc.astype(np.str)
datat_lioc = [datetime( int(datat_lioc[i][0:4]),int(datat_lioc[i][4:6]), int(datat_lioc[i][6:8]), int(datat_lioc[i][8:10]) ) for i in range(len(datat_lioc))]
datat_lioc_str = np.array(datat_lioc).astype(str)

#processa apenas os dados que tem dados brutos
p0 = np.where(datat_str == datat_lioc_str[0])[0]
p1 = np.where(datat_str == datat_lioc_str[-1])[0]

dd = dd[p0:p1+1,:]
datat = datat[p0:p1+1]

bp = dd[:,6] #pressao atm
at = dd[:,7] #temp ar
hm0 = dd[:,27] #hm0
hm0a = dd[:,28] #hm0 swell
hm0b = dd[:,29] #hm0 sea
hmax = dd[:,30] #hmax (onda individual)
dp = dd[:,38] + dmag #dp
dpa = dd[:,39] + dmag #dp swell
dpb = dd[:,40] + dmag #dp sea
spr = dd[:,50] + dmag #espalhamento ang em torno de tp
thhf = dd[:,51] + dmag #direcao media de alta freq
thmax = dd[:,52] #periodo da onda maxima
thtp = dd[:,53] + dmag #direcao da onda no Tp (idem dp?)
tm01 = dd[:,54] #periodo medio (m0/m1)
tm02 = dd[:,55] #periodo medio (sqrt(m0/m1))
tm02a = dd[:,56] #periodo medio (swell)
tp = dd[:,57] #periodo de pico
wt = dd[:,58] #temp agua sup
wd = dd[:,66] + dmag #dir vento
wg = dd[:,67] #int de rajada do vento
ws = dd[:,68] #int do vento

#lioc
#                       0  1   2   3    4     5    6   7   8     9         10     11   12   13    14   15   16
#parametros de onda = data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2

hm0_lioc = dd_lioc[:,6]
tp_lioc = dd_lioc[:,7]
dp_lioc = dd_lioc[:,8] + dmag #correcao lioc #dp1
dp1_lioc = dd_lioc[:,13] + dmag #correcao lioc #dp1
dp2_lioc = dd_lioc[:,16] + dmag #correcao lioc #dp2

#corrige valores que ficaram menor que zero

dp[np.where(dp < 0)] = dp[np.where(dp < 0)] + 360
dpa[np.where(dpa < 0)] = dpa[np.where(dpa < 0)] + 360
thtp[np.where(thtp < 0)] = thtp[np.where(thtp < 0)] + 360
wd[np.where(wd < 0)] = wd[np.where(wd < 0)] + 360

dp_lioc[np.where(dp_lioc < 0)] = dp_lioc[np.where(dp_lioc < 0)] + 360
dp1_lioc[np.where(dp1_lioc < 0)] = dp1_lioc[np.where(dp1_lioc < 0)] + 360
dp2_lioc[np.where(dp2_lioc < 0)] = dp2_lioc[np.where(dp2_lioc < 0)] + 360

#figuras
pl.figure()
pl.title('Altura Significativa - Hm0')
pl.plot(datat,hm0,'bo',datat_lioc,hm0_lioc,'ro')

pl.figure()
pl.title('Periodo de Pico - Tp')
pl.plot(datat,tp,'bo',datat_lioc,tp_lioc,'ro')

pl.figure()
pl.title('Direcao de Pico - Dp e Vento (WD)')
pl.plot(datat,thhf,'bo',datat_lioc,dp_lioc,'ro',datat,wd,'go')
pl.legend(['dp-siodoc','dp-lioc','vento'])


# pl.figure()
# pl.subplot(311)
# pl.title('Parametros de Ondas - SIODOC')
# pl.plot(datat,hm0,'.',label='Hm0'), pl.grid()
# pl.xticks(visible=False), pl.ylabel('metros'), pl.legend()
# pl.subplot(312)
# pl.plot(datat,tp,'.',label='Tp'), pl.grid()
# pl.xticks(visible=False), pl.ylabel('segundos'), pl.legend()
# pl.subplot(313)
# pl.plot(datat,thtp,'.',label='Dp'), pl.grid()
# pl.ylabel('graus'), pl.legend(), pl.axis([datat[0], datat[-1], 0, 360])
# pl.xticks(rotation=15)

# pl.figure()
# pl.subplot(511)
# pl.title('Direcoes de Ondas - Total, Swell e Sea')
# pl.plot(datat,dp,'.',label='dp')
# pl.xticks(visible=False), pl.legend()
# pl.subplot(512)
# pl.plot(datat,dpa,'.',label='dpa-swell')
# pl.xticks(visible=False), pl.legend()
# pl.subplot(513)
# pl.plot(datat,dpb,'.',label='dpb-sea')
# pl.xticks(visible=False), pl.legend()
# pl.subplot(514)
# pl.plot(datat,thhf,'.',label='thtf-alta_freq')
# pl.xticks(visible=False), pl.legend()
# pl.subplot(515)
# pl.plot(datat,thtp,'.',label='thtp-dir_tp?')
# pl.legend()

# pl.figure()
# pl.title('Direcoes de Ondas - Total, Swell e Sea')
# pl.plot(datat,dp,'.',label='dp')
# pl.plot(datat,dpa,'.',label='dpa-swell')
# pl.plot(datat,dpb,'.',label='dpb-sea')
# pl.ylabel('graus'), pl.grid()
# pl.axis([datat[0], datat[-1], 0, 360])
# pl.legend()
# pl.xticks(rotation=15)

# pl.figure()
# pl.title('Direcoes de Ondas - AltaFreq e DirTp (outro?)')
# pl.plot(datat,thhf,'.',label='thtf-alta_freq')
# pl.plot(datat,thtp,'.',label='thtp-dir_tp')
# pl.ylabel('graus'), pl.grid()
# pl.axis([datat[0], datat[-1], 0, 360])
# pl.legend()
# pl.xticks(rotation=15)

# pl.figure()
# pl.subplot(311)
# pl.title('Direcao do vento e Direcao do Sea e de AltaFrq')
# pl.plot(datat,wd,'.',label='DirVento')
# pl.xticks(visible=False), pl.legend()
# pl.axis([datat[0], datat[-1], 0, 360]), pl.grid()
# pl.subplot(312)
# pl.plot(datat,dpb,'.',label='DirSea')
# pl.xticks(visible=False), pl.legend()
# pl.axis([datat[0], datat[-1], 0, 360]), pl.grid()
# pl.subplot(313)
# pl.plot(datat,thhf,'.',label='DirAltaFrq')
# pl.axis([datat[0], datat[-1], 0, 360]), pl.grid()
# pl.legend(), pl.xticks(rotation=15)

pl.show()
