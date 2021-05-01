# -*- coding: utf-8 -*-
'''
Analise dos dados processandos do PNBOIA
pelo LIOc

#sanida do Python
#         0   1   2   3    4     5    6   7   8     9       10       11   12   13   14    15   16   17    18   19
#header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')
'''

import numpy as np
from matplotlib import pylab as pl
import matplotlib as mpl
from matplotlib import pyplot as plt
from datetime import datetime
import os
from scipy.stats import norm
import matplotlib.mlab as mlab
import windrose
from windrose import WindroseAxes
import pandas as pd
from matplotlib.ticker import FuncFormatter
import matplotlib
import windrose
from windrose import WindroseAxes
from scipy.stats import norm,rayleigh
import espec
import matplotlib.dates as mdates
import proconda
from matplotlib.ticker import FixedFormatter

reload(windrose)
reload(windrose)
reload(proconda)
reload(proconda)

pl.close('all')

# ============================================================================== #
#Carrega os dados

pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/proc/triaxys/'
pathname1 = os.environ['HOME'] + '/Dropbox/pnboia/dados/bruto/triaxys/pre_proc/'
pathname2 = os.environ['HOME'] + '/Dropbox/pnboia/dados/bruto/triaxys/pre_proc/'


###############################################################################################################
###############################################################################################################
###############################################################################################################

#caminho dos dados da boia e resultados do modelo
pathname = os.environ['HOME'] + '/Dropbox/pnboia/rot/out/' #boia
pathnamem = os.environ['HOME'] + '/Dropbox/pnboia/modelagem/resultados/' #modelo

#carrega dados do modelo
rig = pd.read_csv(pathname + 'RIG_Wave.csv', parse_dates=['date'], index_col='date')
fln = pd.read_csv(pathname + 'FLN_Wave.csv', parse_dates=['date'], index_col='date')
san = pd.read_csv(pathname + 'SAN_Wave.csv', parse_dates=['date'], index_col='date')

#seleciona datas de periodos simultaneos
aux1 = '2012-02-01 01:00:00'
aux2 = '2012-06-30 23:00:00'

rig = rig.loc[aux1:aux2]
fln = fln.loc[aux1:aux2]
san = san.loc[aux1:aux2]


#calcula direcao em u e v
#rig['dpu'] = np.cos(np.deg2rad(90-rig.dp)) * 1
#rig['dpv'] = np.sin(np.deg2rad(90-rig.dp)) * 1

#calcula direcao media de u e v
#dpmean = np.rad2deg(np.arctan(rig.dpv.mean() / rig.dpu.mean()))

#dp1 = np.rad2deg(np.arctan(rig.dpu / rig.dpv)) + 180
#dp1[pl.find(dp1 < 0)] = dp1[pl.find(dp1 < 0)] + 180
#dp1[pl.find(dp1 > 360)] = dp1[pl.find(dp1 > 360)] - 180
#dp1[pl.find(dp1 > 180)] = dp1[pl.find(dp1 > 180)] - 180

#pl.plot(rig.dp,'-o')
#pl.plot(dp1,'-*')
#pl.show()
#stop


###############################################################################################################
###############################################################################################################
###############################################################################################################

# #inicio e fim para plotagem da evolserie
# ini = 1300
# fim = 1470

# #tamanho da fonte
# fonts = 22

# #evolucao serie
# fig = pl.figure(figsize=(13,9))
# ax1 = fig.add_subplot(311)
# ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d \n %H:%M'))
# ax1.plot(rig.index,rig.hm0,'-b',fln.index,fln.hm0,'-g',san.index,san.hm0,'-r', linewidth=2)
# ax1.plot([rig.loc['2012-03-28 18:00:00'].name,rig.loc['2012-03-28 18:00:00'].name],[0,6],'k--',linewidth=1.4)
# ax1.legend([r'$RIG$',r'$FLN$',r'$SAN$'], labelspacing=None, columnspacing=1, fontsize=fonts-4, ncol=3)
# ax1.plot([rig.loc['2012-03-29 18:00:00'].name,rig.loc['2012-03-29 18:00:00'].name],[0,6],'k--',linewidth=1.4)
# ax1.set_xlim(rig.index[ini],rig.index[fim])
# ax1.set_xticklabels(ax1.get_xticklabels(), visible=False)
# ax1.grid()

# ax1.set_yticklabels(ax1.get_yticks(), fontsize=fonts-3)

# ax1.set_ylabel(r'$Hm0\ (m)$',fontsize=fonts)
# ax2 = fig.add_subplot(312)
# ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d \n %H:%M'))
# ax2.plot(rig.index,rig.tp,'ob',fln.index,fln.tp,'og',san.index,san.tp,'or')
# ax2.plot([rig.loc['2012-03-28 18:00:00'].name,rig.loc['2012-03-28 18:00:00'].name],[0,20],'k--',linewidth=1.4)
# ax2.plot([rig.loc['2012-03-29 18:00:00'].name,rig.loc['2012-03-29 18:00:00'].name],[0,20],'k--',linewidth=1.4)
# ax2.grid()

# ax2.set_yticklabels(ax2.get_yticks(), fontsize=fonts-3)

# ax2.set_xticklabels(ax2.get_xticklabels(), visible=False)
# ax2.set_xlim(rig.index[ini],rig.index[fim])
# ax2.set_ylabel(r'$Tp\ (s)$',fontsize=fonts)

# ax3 = fig.add_subplot(313)
# ax3.plot(rig.index,rig.dp,'ob',fln.index,fln.dp,'og',san.index,san.dp,'or')
# ax3.plot([rig.loc['2012-03-28 18:00:00'].name,rig.loc['2012-03-28 18:00:00'].name],[0,360],'k--',linewidth=1.4)
# ax3.plot([rig.loc['2012-03-29 18:00:00'].name,rig.loc['2012-03-29 18:00:00'].name],[0,360],'k--',linewidth=1.4)
# ax3.grid()
# ax3.set_yticklabels(np.arange(0,360+45,45), fontsize=fonts-3)

# ax3.set_xlim(rig.index[ini],rig.index[fim])
# ax3.set_yticks(np.arange(0,360+45,45))
# ax3.set_ylim(0,360)
# ax3.set_ylabel(r'$Dp\ $' + u'(\u00b0)',fontsize=fonts)
# ax3.set_xticklabels(ax3.get_xticks(), fontsize=fonts-3, rotation=10)
# ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))

# fig.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/evolserie.pdf', format='pdf', dpi=1200, bbox_inches='tight')


###################################################################################################
###################################################################################################
###################################################################################################
# #evolucao espectral

# nfft = 328
# fs = 1.28
# h = 200

# data1 = '201203281800.HNE' #hs chegou no maximo em rio grande
# data2 = '201203291800.HNE' #24 horas depois

# rig1 = pd.read_table(pathname1 + 'rio_grande/hne/' + data1,sep='\s*',skiprows=11,names=['time','eta','etay','etax'])
# fln1 = pd.read_table(pathname1 + 'florianopolis/hne/' + data1,sep='\s*',skiprows=11,names=['time','eta','etay','etax'])
# san1 = pd.read_table(pathname1 + 'santos/hne/' + data1,sep='\s*',skiprows=11,names=['time','eta','etay','etax'])

# rig2 = pd.read_table(pathname1 + 'rio_grande/hne/' + data2,sep='\s*',skiprows=11,names=['time','eta','etay','etax'])
# fln2 = pd.read_table(pathname1 + 'florianopolis/hne/' + data2,sep='\s*',skiprows=11,names=['time','eta','etay','etax'])
# san2 = pd.read_table(pathname1 + 'santos/hne/' + data2,sep='\s*',skiprows=11,names=['time','eta','etay','etax'])

# #calcula parametros de ondas

# #rio grande 1
# hm0_rig1, tp_rig1, dp_rig1, sigma1, sigma2, sigma1p, sigma2p, freq, df, k, sn_rig1, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1_rig1, dire2 = proconda.ondaf(
# rig1.eta,rig1.etax,rig1.etay,h,nfft,fs)
# dmag_rig = -17

# #corrige a declinacao magnetica
# dp_rig1 = dp_rig1 + dmag_rig
# if dp_rig1 < 0:
#     dp_rig1 = dp_rig1 + 360
# dire1_rig1 = dire1_rig1 + dmag_rig
# dire1_rig1[pl.find(dire1_rig1<0)] = dire1_rig1[pl.find(dire1_rig1<0)] + 360

# #rio grande 2
# hm0_rig2, tp_rig2, dp_rig2, sigma1, sigma2, sigma1p, sigma2p, freq, df, k, sn_rig2, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1_rig2, dire2 = proconda.ondaf(
# rig2.eta,rig2.etax,rig2.etay,h,nfft,fs)

# #corrige a declinacao magnetica
# dp_rig2 = dp_rig2 + dmag_rig
# if dp_rig2 < 0:
#     dp_rig2 = dp_rig2 + 360
# dire1_rig2 = dire1_rig2 + dmag_rig
# dire1_rig2[pl.find(dire1_rig2<0)] = dire1_rig2[pl.find(dire1_rig2<0)] + 360

# #florianopolis 1
# hm0_fln1, tp_fln1, dp_fln1, sigma1, sigma2, sigma1p, sigma2p, freq, df, k, sn_fln1, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1_fln1, dire2 = proconda.ondaf(
# fln1.eta,fln1.etax,fln1.etay,h,nfft,fs)
# dmag_fln = -20

# #corrige a declinacao magnetica
# dp_fln1 = dp_fln1 + dmag_fln
# if dp_fln1 < 0:
#     dp_fln1 = dp_fln1 + 360
# dire1_fln1 = dire1_fln1 + dmag_fln
# dire1_fln1[pl.find(dire1_fln1<0)] = dire1_fln1[pl.find(dire1_fln1<0)] + 360

# #florianopolis 2
# hm0_fln2, tp_fln2, dp_fln2, sigma1, sigma2, sigma1p, sigma2p, freq, df, k, sn_fln2, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1_fln2, dire2 = proconda.ondaf(
# fln2.eta,fln2.etax,fln2.etay,h,nfft,fs)

# #corrige a declinacao magnetica
# dp_fln2 = dp_fln2 + dmag_fln
# if dp_fln2 < 0:
#     dp_fln2 = dp_fln2 + 360
# dire1_fln2 = dire1_fln2 + dmag_fln
# dire1_fln2[pl.find(dire1_fln2<0)] = dire1_fln2[pl.find(dire1_fln2<0)] + 360

# #santos 1
# hm0_san1, tp_san1, dp_san1, sigma1, sigma2, sigma1p, sigma2p, freq, df, k, sn_san1, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1_san1, dire2 = proconda.ondaf(
# san1.eta,san1.etax,san1.etay,h,nfft,fs)
# dmag_san = -22

# #corrige a declinacao magnetica
# dp_san1 = dp_san1 + dmag_san
# if dp_san1 < 0:
#     dp_san1 = dp_san1 + 360
# dire1_san1 = dire1_san1 + dmag_san
# dire1_san1[pl.find(dire1_san1<0)] = dire1_san1[pl.find(dire1_san1<0)] + 360

# #santos 2
# hm0_san2, tp_san2, dp_san2, sigma1, sigma2, sigma1p, sigma2p, freq, df, k, sn_san2, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1_san2, dire2 = proconda.ondaf(
# san2.eta,san2.etax,san2.etay,h,nfft,fs)

# #corrige a declinacao magnetica
# dp_san2 = dp_san2 + dmag_san
# if dp_san2 < 0:
#     dp_san2 = dp_san2 + 360
# dire1_san2 = dire1_san2 + dmag_san
# dire1_san2[pl.find(dire1_san2<0)] = dire1_san2[pl.find(dire1_san2<0)] + 360



##################################################################################################
# ##################################################################################################

# fs = 17
# fs1 = 15

# fig = pl.figure(figsize=(10,8))
# ax1 = fig.add_subplot(321)
# ax1.plot(sn_rig1[:,0],sn_rig1[:,1],'b',sn_fln1[:,0],sn_fln1[:,1],'g',sn_san1[:,0],sn_san1[:,1],'r',linewidth=1.4)
# ax1.set_title(r'$2012-03-28\ 18h$',fontsize=fs)
# ax1.legend([r'$Hm0=%.1f\ m;\ Tp=%.1f\ s;\ Dp=%.i\ $' %(round(hm0_rig1,1),round(tp_rig1,1),round(dp_rig1,0)) + u'\u00b0',
#             r'$Hm0=%.1f\ m;\ Tp=%.1f\ s;\ Dp=%.i\ $' %(round(hm0_fln1,1),round(tp_fln1,1),round(dp_fln1,0)) + u'\u00b0',
#             r'$Hm0=%.1f\ m;\ Tp=%.1f\ s;\ Dp=%.i\ $' %(round(hm0_san1,1),round(tp_san1,1),round(dp_san1,0)) + u'\u00b0'], fontsize=fs1-1, bbox_to_anchor=(1.08,-1.6))
# ax1.grid()
# ax1.set_xlim(0.05,0.25)
# ax1.set_ylim(0,50)
# ax1.set_ylabel(r'$m^{2}/Hz$',fontsize=fs)
# ax1.set_yticklabels(ax1.get_yticks(), fontsize=fs1, visible=True)
# ax1.set_xticklabels(ax1.get_xticks(), fontsize=fs1, visible=True)

# ax2 = fig.add_subplot(322)
# ax2.plot(sn_rig2[:,0],sn_rig2[:,1],'b',sn_fln2[:,0],sn_fln2[:,1],'g',sn_san2[:,0],sn_san2[:,1],'r',linewidth=1.4)
# ax2.set_title(r'$2012-03-29\ 18h$',fontsize=fs)
# ax2.legend([r'$Hm0=%.1f\ m;\ Tp=%.1f\ s;\ Dp=%.i\ $' %(round(hm0_rig2,1),round(tp_rig2,1),round(dp_rig2,0)) + u'\u00b0',
#             r'$Hm0=%.1f\ m;\ Tp=%.1f\ s;\ Dp=%.i\ $' %(round(hm0_fln2,1),round(tp_fln2,1),round(dp_fln2,0)) + u'\u00b0',
#             r'$Hm0=%.1f\ m;\ Tp=%.1f\ s;\ Dp=%.i\ $' %(round(hm0_san2,1),round(tp_san2,1),round(dp_san2,0)) + u'\u00b0'], fontsize=fs1-1, bbox_to_anchor=(1.08,-1.6))
# ax2.set_xlim(0.05,0.25)
# ax2.set_ylim(0,50)
# ax2.grid()
# ax2.set_yticklabels(ax2.get_yticks(), fontsize=fs1, visible=True)
# ax2.set_xticklabels(ax2.get_xticks(), fontsize=fs1, visible=True)

# ax3 = fig.add_subplot(323)
# ax3.plot(sn_rig1[:,0],dire1_rig1,'b',sn_fln1[:,0],dire1_fln1,'g',sn_san1[:,0],dire1_san1,'r',linewidth=1.4)
# ax3.set_xlim(0.05,0.25)
# ax3.set_yticks(np.arange(0,360+45,45))
# ax3.set_ylim(0,360)
# ax3.grid()
# ax3.set_xlabel(r'$Frequency\ (Hz)$',fontsize=fs)
# ax3.set_ylabel(r'$Mean\ Direction\ $' + u'(\u00b0)',fontsize=fs)
# ax3.set_xticklabels(ax3.get_xticks(), fontsize=fs1)
# ax3.set_yticklabels(ax3.get_yticks(), fontsize=fs1)

# ax4 = fig.add_subplot(324)
# ax4.plot(sn_rig2[:,0],dire1_rig2,'b',sn_fln2[:,0],dire1_fln2,'g',sn_san2[:,0],dire1_san2,'r',linewidth=1.4)
# ax4.set_xlim(0.05,0.25)
# ax4.set_yticks(np.arange(0,360+45,45))
# ax4.set_ylim(0,360)
# ax4.grid()
# ax4.set_xlabel(r'$Frequency\ (Hz)$',fontsize=fs)
# ax4.set_xticklabels(ax4.get_xticks(), fontsize=fs1)
# ax4.set_yticklabels(ax4.get_yticks(), fontsize=fs1)

# fig.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/evolspec.pdf', format='pdf', dpi=1200, bbox_inches='tight')




################################################################
################################################################

#histograma hs, tp e dp, rig, fln e san


# def histogram(fig, ax, serie, tit, ylab, ylim, x, fsz, xt1, xt2, texp1, texp2):

#   '''
#   ax1 = axes for subplot
#   serie = temporal serie
#   tit = title
#   x = xticks spaced limits
#   fsz = fontsize
#   xt = xticks
#   ylab = ylabel
#   '''
#   ax.set_title(tit, fontsize=fsz)
#   param = rayleigh.fit(serie.loc[serie.notnull()])
#   pdf_fitted = rayleigh.pdf(x,loc=param[0],scale=param[1])
#   ax.hist(serie[~np.isnan(serie)], bins=20, normed=1, alpha=.4, color='lightgrey')
#   ax.plot(x,pdf_fitted,'k--',linewidth=1.5)
#   ax.grid()
#   ax.set_xticks(xt1, xt2)
#   ax.set_ylabel(ylab)
#   ax.set_ylim(ylim)
#   ax.text(texp1, texp2,r'$\mathrm{}\ \mu=%.1f\ m$' %(serie.mean()) + '\n' + 
#                  r'$\mathrm{}\ \sigma=%.1f\ m$' %(serie.std()) + '\n' +
#                  r'$P90=%.1f\ m$' %(np.percentile(serie[~np.isnan(serie)], 90)) + '\n' + 
#                  r'$max=%.1f\ m$' %(serie.max()), fontsize=13)



# fig1 = pl.figure(figsize=(12,9))

# #Hm0 - RIG
# histogram(
#           fig=fig1,
#           ax=fig1.add_subplot(321),
#           serie=rig.hm0,
#           tit=r'$Hm0$',
#           ylab=r'$RIG\ (PDF)$',
#           ylim=(0,1),
#           x=np.linspace(0,6,100),
#           fsz=15,
#           xt1 = list(np.arange(7)),
#           xt2 = list(np.arange(7).astype(str)),
#           texp1 = 4, 
#           texp2 = 0.44 
#           )

# #Tp - RIG
# histogram(
#           fig=fig1,
#           ax=fig1.add_subplot(322),
#           serie=rig.tp,
#           tit=r'$Tp$',
#           ylab='',
#           ylim=(0,0.2),
#           x=np.linspace(0,20,100),
#           fsz=15,
#           xt1 = list(np.arange(0,22,2)),
#           xt2 = list(np.arange(0,22,2).astype(str)),
#           texp1 = 13.5,
#           texp2 = 0.09
#           )


# #Hm0 - FLN
# histogram(
#           fig=fig1,
#           ax=fig1.add_subplot(323),
#           serie=fln.hm0,
#           tit='',
#           ylab=r'$FLN\ (PDF)$',
#           ylim=(0,1),
#           x=np.linspace(0,6,100),
#           fsz=15,
#           xt1 = list(np.arange(7)),
#           xt2 = list(np.arange(7).astype(str)),
#           texp1 = 4, 
#           texp2 = 0.44 
#           )

# #Tp - FLN
# histogram(
#           fig=fig1,
#           ax=fig1.add_subplot(324),
#           serie=fln.tp,
#           tit='',
#           ylab='',
#           ylim=(0,0.2),
#           x=np.linspace(0,20,100),
#           fsz=15,
#           xt1 = list(np.arange(0,22,2)),
#           xt2 = list(np.arange(0,22,2).astype(str)),
#           texp1 = 13.5,
#           texp2 = 0.09
#           )


# #Hm0 - SAN
# histogram(
#           fig=fig1,
#           ax=fig1.add_subplot(325),
#           serie=san.hm0,
#           tit='',
#           ylab=r'$SAN\ (PDF)$',
#           ylim=(0,1),
#           x=np.linspace(0,6,100),
#           fsz=15,
#           xt1 = list(np.arange(7)),
#           xt2 = list(np.arange(7).astype(str)),
#           texp1 = 4, 
#           texp2 = 0.44 
#           )

# #Tp - SAN
# histogram(
#           fig=fig1,
#           ax=fig1.add_subplot(326),
#           serie=san.tp,
#           tit='',
#           ylab='',
#           ylim=(0,0.2),
#           x=np.linspace(0,20,100),
#           fsz=15,
#           xt1 = list(np.arange(0,22,2)),
#           xt2 = list(np.arange(0,22,2).astype(str)),
#           texp1 = 13.5,
#           texp2 = 0.09
#           )

# fig1.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/histhstp.pdf', format='pdf', dpi=1200, bbox_inches='tight')


#################################################################################
#wave rose


#define funcao para criar windrose




def waverose(inte, dire, figsz, nsector, radsize, xsize, leg, bbx):

  def new_axes():
    fig = plt.figure(figsize=figsz, dpi=80, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax, fig

  ax, fig = new_axes()

  def set_legend(ax, bbx):
    l = ax.legend(loc="center right",borderaxespad=bbx)
    # l.get_frame().set_fill(False) #transparent legend
    plt.setp(l.get_texts(), fontsize=20,weight='normal')

  ax.bar(dire,inte, normed=True, bins=5, opening=0.8, edgecolor='white',nsector=nsector)
  ax.grid(True,linewidth=1.5,linestyle='dotted')

  ax.set_radii_angle(fontsize=radsize)
  ax.set_xticklabels(ax.theta_labels,fontsize=xsize)
  ax.set_radii_angle(fontsize=radsize)
  ax.set_xticklabels(ax.theta_labels,fontsize=xsize)

  if leg=='on':
    set_legend(ax, bbx)
    
  return ax, fig


ax1, fig1 = waverose(inte=rig.hm0, dire=rig.dp, figsz=(8.5,6), nsector=16, radsize=20, xsize='x-large', leg='off', bbx=-10.8)
ax2, fig2 = waverose(inte=rig.tp, dire=rig.dp,  figsz=(8.5,6), nsector=16, radsize=20, xsize='x-large', leg='off', bbx=-10.8)
ax3, fig3 = waverose(inte=fln.hm0, dire=fln.dp, figsz=(8.5,6), nsector=16, radsize=20, xsize='x-large', leg='off', bbx=-10.8)
ax4, fig4 = waverose(inte=fln.tp, dire=fln.dp,  figsz=(8.5,6), nsector=16, radsize=20, xsize='x-large', leg='off', bbx=-10.8)
ax5, fig5 = waverose(inte=san.hm0, dire=san.dp, figsz=(8.5,6), nsector=16, radsize=20, xsize='x-large', leg='on', bbx=-14)
ax6, fig6 = waverose(inte=san.tp, dire=san.dp,  figsz=(8.5,6), nsector=16, radsize=20, xsize='x-large', leg='on', bbx=-14)

# fig1.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/RIG_WR_HsDp.eps', dpi=1200, facecolor='w', edgecolor='w', orientation='portrait', format='eps', transparent=True, pad_inches=0.1, bbox_inches='tight')
# fig2.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/RIG_WR_TpDp.eps', dpi=1200, facecolor='w', edgecolor='w', orientation='portrait', format='eps', transparent=True, pad_inches=0.1, bbox_inches='tight')
# fig3.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/FLN_WR_HsDp.eps', dpi=1200, facecolor='w', edgecolor='w', orientation='portrait', format='eps', transparent=True, pad_inches=0.1, bbox_inches='tight')
# fig4.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/FLN_WR_TpDp.eps', dpi=1200, facecolor='w', edgecolor='w', orientation='portrait', format='eps', transparent=True, pad_inches=0.1, bbox_inches='tight')
# fig5.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/SAN_WR_HsDp.eps', dpi=1200, facecolor='w', edgecolor='w', orientation='portrait', format='eps', transparent=True, pad_inches=0.1, bbox_inches='tight')
# fig6.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/SAN_WR_TpDp.eps', dpi=1200, facecolor='w', edgecolor='w', orientation='portrait', format='eps', transparent=True, pad_inches=0.1, bbox_inches='tight')








# ##################################################################################
# ##################################################################################
# ##################################################################################

# #freakwave


# ##############################################################################################################
# ##############################################################################################################
# ##############################################################################################################
# #freak-waves

# #indices dos valores se nan
# indrig = pl.find(np.isnan(rig.hs)==False)
# indfln = pl.find(np.isnan(fln.hs)==False)
# indsan = pl.find(np.isnan(san.hs)==False)


# #valores da relacao de freakwaves
# rig['rfw'] = rig.hmax/rig.hs
# fln['rfw'] = fln.hmax/fln.hs
# san['rfw'] = san.hmax/san.hs

# #indices das relacoes maiores que 2.0
# irfw_rig = pl.find(rig.rfw > 2.0)
# irfw_fln = pl.find(fln.rfw > 2.0)
# irfw_san = pl.find(san.rfw > 2.0)


# #indice do maior valor da relacao de freakwaves
# #2012-03-22 04:00:00
# imax_rfw_rig = pl.find(rig.rfw == max(rig.rfw[irfw_rig]))
# imax_hs_rig = pl.find(rig.hs == max(rig.hs[irfw_rig]))

# imax_rfw_fln = pl.find(fln.rfw == max(fln.rfw[irfw_fln]))
# imax_hs_fln = pl.find(fln.hs == max(fln.hs[irfw_fln]))

# imax_rfw_san = pl.find(san.rfw == max(san.rfw[irfw_san]))
# imax_hs_san = pl.find(san.hs == max(san.hs[irfw_san]))

# fs = 25

# colors = ['k','red','red']
# bins = np.linspace(rig.rfw.min(),rig.rfw.max(),5)
# bins = np.arange(rig.rfw.min(),rig.rfw.max(),0.1)
# fig, ax = pl.subplots(figsize=(10,8))
# #ax.hist(rig.rfw[indrig], len(rig.rfw[indrig])/100, facecolor='#b0b0ac', alpha=0.3)
# #ax.hist(fln.rfw[indfln], len(fln.rfw[indfln])/100, facecolor='#b9bd9f', alpha=0.3)
# #ax.hist(san.rfw[indsan], len(san.rfw[indsan])/100, facecolor='#c2c993', alpha=0.3)
# ax.hist([rig.rfw[indrig], fln.rfw[indfln], san.rfw[indsan]], bins=bins, color=['black','grey','lightgrey'], alpha=0.8, align=u'left', label=['RIG','FLN','SAN'])
# #ax.hist(rig.rfw[indrig], bottom=None, color='lightgrey', alpha=0.8, align='left', label='RIG')
# ax.set_xticks(bins[:-1][::2])

# #ajusta o axis
# xx = ax.get_xticks()
# ll = ['%.1f' % a for a in xx]
# #ax.set_xticklabels(xx, ll)

# #ax.xaxis.set_major_formatter(FixedFormatter())

# ax.legend(prop={'size': 20})

# #ax.axis('tight')
# ax.plot([2,2],[0,1000], '-.k', linewidth=2.5)
# ax.grid()
# ax.set_ylabel(r'$Number\ of\ occurence$',fontsize=fs)
# ax.set_xlabel(r'$Hmax/Hs$',fontsize=20)
# ax.set_yticks(ax.get_yticks(),[0,100,200,300,400,500])
# ax.set_xticklabels(ll, fontsize=fs, rotation=None)
# ax.set_yticklabels(ax.get_yticks(), fontsize=fs, rotation=None)

# #fig.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/hmaxhs.pdf', format='pdf', dpi=1200, bbox_inches='tight')



# fs = 1.28
# h = 200
# nfft = 328

# data1 = '201203220400.HNE' #Hs=1.29 ; Hm0=1.31 ; Tp=08.01 ; Dp=175.9 ; Hmax=3.1 ; Hmax/Hs=2.4 
# data2 = '201203281400.HNE' #Hs=4.42 ; Hm0=4.83 ; Tp=11.65 ; Dp=199.8 ; Hmax=9.62 ; Hmax/Hs=2.17 

# fw1 = pd.read_table(pathname1 + 'rio_grande/hne/' + data1,sep='\s*',skiprows=11,names=['time','eta','etay','etax'])
# fw2 = pd.read_table(pathname1 + 'rio_grande/hne/' + data2,sep='\s*',skiprows=11,names=['time','eta','etay','etax'])

# #calcula parametros de ondas
# hm0_1, tp_1, dp_1, sigma1, sigma2, sigma1p_1, sigma2p, freq, df, k, sn_1, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1_1, dire2_1 = proconda.ondaf(
# fw1.eta,fw1.etax,fw1.etay,h,nfft,fs)

# Hs,H10,Hmax,Tmed,THmax_1 = proconda.ondat(fw1.time,fw1.eta,200)

# hm0_2, tp_2, dp_2, sigma1, sigma2, sigma1p_2, sigma2p, freq, df, k, sn_2, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1_2, dire2_2 = proconda.ondaf(
# fw2.eta,fw2.etax,fw2.etay,h,nfft,fs)

# Hs,H10,Hmax,Tmed,THmax_2 = proconda.ondat(fw2.time,fw2.eta,200)


# fig = pl.figure()
# ax1 = fig.add_subplot(211)
# ax1.plot(fw1.time,fw1.eta,'-ob')
# ax1.plot(fw1.time,fw1.etax,'-or')
# ax1.plot(fw1.time,fw1.etay,'-og')
# pl.title(data1)
# pl.grid()
# #ax1.plot(fw1.eta,'.b')
# ax2 = fig.add_subplot(212)
# ax2.plot(fw2.time,fw2.eta,'-ob')
# ax2.plot(fw2.time,fw2.etax,'-or')
# ax2.plot(fw2.time,fw2.etay,'-og')
# pl.grid()
# pl.title(data2)
# #ax2.plot(fw2.eta,'.b')



pl.show()
