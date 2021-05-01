'''
Processanmento dos dados
validados pelo pnboia
das boias de rig, fln e sanntos
entre 2012/02/01 a 2012/06/30

- Utilizado para o artigo
Wave Observarion ...
Ocean Dynamics


- compara com a modelagem do ww3

- periodo em que teve dados
simultaneos

'''

import pandas as pd
import numpy as np
import os
from datetime import datetime
import matplotlib.pylab as pl
import matplotlib.dates as mdates
import concat
from scipy.stats import norm,rayleigh

reload(concat)


pl.close('all')


#pathname = os.environ['HOME'] + '/Dropbox/pnboia/rot/out/'
#rig = pd.read_csv(pathname + 'wavewind_rig_2012.csv', index_col=['date'], parse_dates=['date'])
#fln = pd.read_csv(pathname + 'wavewind_fln_2012.csv', index_col=['date'], parse_dates=['date'])
#san = pd.read_csv(pathname + 'wavewind_san_2012.csv', index_col=['date'], parse_dates=['date'])


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
rig['dpu'] = np.cos(np.deg2rad(90-rig.dp)) * 1
rig['dpv'] = np.sin(np.deg2rad(90-rig.dp)) * 1

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


#concatena resultados da modelagem

#direm = np.sort(os.listdir(os.environ['HOME'] + '/Dropbox/pnboia/modelagem/resultados/'))

rigm = concat.ww3(pathname=pathnamem, filename='RioGrande.txt')
flnm = concat.ww3(pathname=pathnamem, filename='Floripa.txt')
sanm = concat.ww3(pathname=pathnamem, filename='Santos.txt')



###############################################################################################################
###############################################################################################################
###############################################################################################################


#retira valores nulos e pega as datas do modelo (o modelo nao contabilizou o dia 29/02. em que tem dados na boia)

#modelo - colocou nan no dia 29/02
indmod = [pl.find(rigm.index[i] == rig.index)[0] for i in range(1,len(rigm))]

rigm = rigm[1:]
flnm = flnm[1:]
sanm = sanm[1:]
rig = rig.ix[indmod]
fln = fln.ix[indmod]
san = san.ix[indmod]

indtp = pl.find(rig.tp.isnull()==False)
inddp = pl.find(rig.dp.isnull()==False)
indhm0 = pl.find(rig.hm0.isnull()==False)
rig_hm0 = rig.hm0[indhm0]
rig_tp = rig.tp[indtp]
rig_dp = rig.dp[inddp]
rig_hs = rig.hs[indhm0]
rig_hmax = rig.hmax[indhm0]
rigm_hm0 = rigm.hm0[indhm0]
rigm_tp = rigm.tp[indtp]
rigm_dp = rigm.dp[inddp]

indhm0 = pl.find(fln.hm0.isnull()==False)
indtp = pl.find(fln.tp.isnull()==False)
inddp = pl.find(fln.dp.isnull()==False)
fln_hm0 = fln.hm0[indhm0]
fln_tp = fln.tp[indtp]
fln_dp = fln.dp[inddp]
flnm_hm0 = flnm.hm0[indhm0]
flnm_tp = flnm.tp[indtp]
flnm_dp = flnm.dp[inddp]

indhm0 = pl.find(san.hm0.isnull()==False)
indtp = pl.find(san.tp.isnull()==False)
inddp = pl.find(san.dp.isnull()==False)
san_hm0 = san.hm0[indhm0]
san_tp = san.tp[indtp]
san_dp = san.dp[inddp]
sanm_hm0 = sanm.hm0[indhm0]
sanm_tp = sanm.tp[indtp]
sanm_dp = sanm.dp[inddp]



################################################################
################################################################

#histograma hs, tp e dp, rig, fln e san
fig = pl.figure(figsize=(12,9))

fsz = 15

ax1 = fig.add_subplot(321)
ax1.set_title(r'$Hm0$',fontsize=fsz)
param = rayleigh.fit(rig.hs.loc[rig.hs.notnull()])
x = np.linspace(0,6,100)
pdf_fitted = rayleigh.pdf(x,loc=param[0],scale=param[1])
ax1.hist(rig.hs, bins=20, normed=1, alpha=.4, color='lightgrey')
ax1.plot(x,pdf_fitted,'k--',linewidth=1.5)
ax1.set_xticks([0,1,2,3,4,5,6],['0','1','2','3','4','5','6'])
ax1.set_ylabel(r'$RIG\ (PDF)$')
ax1.set_ylim(0,0.9)
ax1.text(4,0.4,r'$\mathrm{}\ \mu=%.2f\ m$' %(rig.hs.mean()) + '\n' + 
              r'$\mathrm{}\ \sigma=%.2f\ m$' %(rig.hs.std()) + '\n' +
              r'$max=%.2f\ m$' %(rig.hm0.max()) + '\n' + 
              r'$Hmax=%.2f\ m$' %(rig.hmax.max()), fontsize=13)

pl.show()
stop
pl.subplot(322)
pl.title(r'$Tp$',fontsize=15)
param = norm.fit(rig.tp.loc[rig.tp.notnull()])
x = np.linspace(0,20,100)
pdf_fitted = norm.pdf(x,loc=param[0],scale=param[1])
rig.tp.hist(bins=20, normed=1,alpha=.4,color='lightgrey')
pl.plot(x,pdf_fitted,'k--',linewidth=1.5)
pl.xticks([0,2,4,6,8,10,12,14,16,18,20],['0','2','4','6','8','10','12','14','16','18','20'])
pl.ylim(0,0.2)
pl.text(13.5,0.1,r'$\mathrm{}\ \mu=%.1f\ s$' %(rig.tp.mean()) + '\n' + 
              r'$\mathrm{}\ \sigma=%.1f\ s$' %(rig.tp.std()) + '\n' +
              r'$max=%.1f\ s$' %(rig.tp.max()) + '\n' + 
              r'$THmax=%.1f\ s$' %(rig.tp.loc[rig.hmax==rig.hmax.max()][0]), fontsize=13)


pl.subplot(323)
param = rayleigh.fit(fln.hs.loc[fln.hs.notnull()])
x = np.linspace(0,6,100)
pdf_fitted = rayleigh.pdf(x,loc=param[0],scale=param[1])
fln.hs.hist(bins=20, normed=1,alpha=.4,color='lightgrey')
pl.plot(x,pdf_fitted,'k--',linewidth=1.5)
pl.xticks([0,1,2,3,4,5,6],['0','1','2','3','4','5','6'])
pl.ylabel(r'$flnN\ (PDF)$')
pl.ylim(0,0.9)
pl.text(4,0.4,r'$\mathrm{}\ \mu=%.2f\ m$' %(fln.hs.mean()) + '\n' + 
              r'$\mathrm{}\ \sigma=%.2f\ m$' %(fln.hs.std()) + '\n' +
              r'$max=%.2f\ m$' %(fln.hm0.max()) + '\n' + 
              r'$Hmax=%.2f\ m$' %(fln.hmax.max()), fontsize=13)


pl.subplot(324)
param = norm.fit(fln.tp.loc[fln.tp.notnull()])
x = np.linspace(0,20,100)
pdf_fitted = norm.pdf(x,loc=param[0],scale=param[1])
fln.tp.hist(bins=20, normed=1,alpha=.4,color='lightgrey')
pl.plot(x,pdf_fitted,'k--',linewidth=1.5)
pl.xticks([0,2,4,6,8,10,12,14,16,18,20],['0','2','4','6','8','10','12','14','16','18','20'])
pl.ylim(0,0.2)
pl.text(13.5,0.1,r'$\mathrm{}\ \mu=%.1f\ s$' %(fln.tp.mean()) + '\n' + 
                 r'$\mathrm{}\ \sigma=%.1f\ s$' %(fln.tp.std()) + '\n' +
                 r'$max=%.1f\ s$' %(fln.tp.max()) + '\n' + 
                 r'$THmax=%.1f\ s$' %(fln.tp.loc[fln.hmax==fln.hmax.max()][0]), fontsize=13)


pl.subplot(325)
param = rayleigh.fit(san.hs.loc[san.hs.notnull()])
x = np.linspace(0,6,100)
pdf_fitted = rayleigh.pdf(x,loc=param[0],scale=param[1])
san.hs.hist(bins=20, normed=1,alpha=.4,color='lightgrey')
pl.plot(x,pdf_fitted,'k--',linewidth=1.5)
pl.xticks([0,1,2,3,4,5,6],['0','1','2','3','4','5','6'])
pl.ylabel(r'$sanN\ (PDF)$')
pl.xlabel(r'$Meters$')
pl.ylim(0,0.9)
pl.text(4,0.4,r'$\mathrm{}\ \mu=%.2f\ m$' %(san.hs.mean()) + '\n' + 
              r'$\mathrm{}\ \sigma=%.2f\ m$' %(san.hs.std()) + '\n' +
              r'$max=%.2f\ m$' %(san.hm0.max()) + '\n' + 
              r'$Hmax=%.2f\ m$' %(san.hmax.max()), fontsize=13)


pl.subplot(326)
param = norm.fit(san.tp.loc[san.tp.notnull()])
x = np.linspace(0,20,100)
pdf_fitted = norm.pdf(x,loc=param[0],scale=param[1])
san.tp.hist(bins=20, normed=1,alpha=.4,color='lightgrey')
pl.plot(x,pdf_fitted,'k--',linewidth=1.5)
pl.xticks([0,2,4,6,8,10,12,14,16,18,20],['0','2','4','6','8','10','12','14','16','18','20'])
pl.xlabel(r'$Seconds$')
pl.ylim(0,0.2)
pl.text(13.5,0.1,r'$\mathrm{}\ \mu=%.1f\ s$' %(san.tp.mean()) + '\n' + 
              r'$\mathrm{}\ \sigma=%.1f\ s$' %(san.tp.std()) + '\n' +
              r'$max=%.1f\ s$' %(san.tp.max()) + '\n' + 
              r'$THmax=%.1f\ s$' %(san.tp.loc[san.hmax==san.hmax.max()][0]), fontsize=13)



#pl.sanvefig('fig_OD/hist_hstp.eps', format='eps', dpi=1200, bbox_inches='tight')
#pl.sanvefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/histhstp.eps', format='eps', dpi=1200, bbox_inches='tight')
pl.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/histhstp.pdf', format='pdf', dpi=1200, bbox_inches='tight')



###############################################################################################################
###############################################################################################################
###############################################################################################################
#scatter plot

# pl.figure() #figsize=(12,4))

# ms = 1
# al = 0.3

# pl.subplot(331)
# m, b = np.polyfit(rig_hm0,rigm_hm0,1)
# pl.plot(rig_hm0,rigm_hm0,'o', color='lightgrey', markersize=ms, alpha=al)
# pl.plot(np.arange(7), m*np.arange(7) + b, 'k-')
# pl.plot(np.arange(7),np.arange(7),'k--')
# pl.axis([0,6,0,6])
# pl.ylabel(r'$RIG$',fontsize=15)
# pl.title(r'$Hm0\ (m)$',fontsize=15)

# pl.subplot(332)
# m, b = np.polyfit(rig_tp,rigm_tp,1)
# pl.plot(rig_tp,rigm_tp,'o', color='lightgrey', markersize=ms, alpha=al)
# pl.plot(np.arange(21), m*np.arange(21) + b, 'k-')
# pl.plot(np.arange(21),np.arange(21),'k--')
# pl.axis([2,20,2,20])
# pl.title(r'$Tp\ (s)$',fontsize=15)

# pl.subplot(333)
# m, b = np.polyfit(rig_dp,rigm_dp,1)
# pl.plot(rig_dp,rigm_dp,'o', color='lightgrey', markersize=ms, alpha=al)
# pl.plot(np.arange(361), m*np.arange(361) + b, 'k-')
# pl.plot(np.arange(361),np.arange(361),'k--')
# pl.axis([0,360,0,360])
# pl.xticks([0,90,180,270,360])
# pl.yticks([0,90,180,270,360])
# pl.title(r'$Dp\ ($' + u'\u00b0' + r'$)$',fontsize=15)


# pl.subplot(334)
# m, b = np.polyfit(fln_hm0,flnm_hm0,1)
# pl.plot(fln_hm0,flnm_hm0,'o', color='lightgrey', markersize=ms, alpha=al)
# pl.plot(np.arange(7), m*np.arange(7) + b, 'k-')
# pl.plot(np.arange(7),np.arange(7),'k--')
# pl.axis([0,6,0,6])
# pl.ylabel(r'$FLN$',fontsize=15)


# pl.subplot(335)
# m, b = np.polyfit(fln_tp,flnm_tp,1)
# pl.plot(fln_tp,flnm_tp,'o', color='lightgrey', markersize=ms, alpha=al)
# pl.plot(np.arange(21), m*np.arange(21) + b, 'k-')
# pl.plot(np.arange(21),np.arange(21),'k--')
# pl.axis([2,20,2,20])

# pl.subplot(336)
# m, b = np.polyfit(fln_dp,flnm_dp,1)
# pl.plot(fln_dp,flnm_dp,'o', color='lightgrey', markersize=ms, alpha=al)
# pl.plot(np.arange(361), m*np.arange(361) + b, 'k-')
# pl.plot(np.arange(361),np.arange(361),'k--')
# pl.axis([0,360,0,360])
# pl.xticks([0,90,180,270,360])
# pl.yticks([0,90,180,270,360])
# pl.twinx()
# pl.yticks([0,90,180,270,360],visible=False)
# pl.ylabel(r'$WaveWatch\ III$',fontsize=15)

# pl.subplot(337)
# m, b = np.polyfit(san_hm0,sanm_hm0,1)
# pl.plot(san_hm0,sanm_hm0,'o', color='lightgrey', markersize=ms, alpha=al)
# pl.plot(np.arange(7), m*np.arange(7) + b, 'k-')
# pl.plot(np.arange(7),np.arange(7),'k--')
# pl.axis([0,6,0,6])
# pl.ylabel(r'$SAN$',fontsize=15)

# pl.subplot(338)
# m, b = np.polyfit(san_tp,sanm_tp,1)
# pl.plot(san_tp,sanm_tp,'o', color='lightgrey', markersize=ms, alpha=al)
# pl.plot(np.arange(21), m*np.arange(21) + b, 'k-')
# pl.plot(np.arange(21),np.arange(21),'k--')
# pl.axis([2,20,2,20])
# pl.xlabel(r'$AXYS-3M$',fontsize=15)

# pl.subplot(339)
# m, b = np.polyfit(san_dp,sanm_dp,1)
# pl.plot(san_dp,sanm_dp,'o', color='lightgrey', markersize=ms, alpha=al)
# pl.plot(np.arange(361), m*np.arange(361) + b, 'k-')
# pl.plot(np.arange(361),np.arange(361),'k--')
# pl.axis([0,360,0,360])
# pl.xticks([0,90,180,270,360])
# pl.yticks([0,90,180,270,360])


# pl.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/scatter.pdf', format='pdf', dpi=1200, bbox_inches='tight')


###############################################################################################################
###############################################################################################################
###############################################################################################################
# #grafico de series temporais

# fs = 26
# tl = 35

# fw1 = '2012-03-28 14:00:00' #maior hs para hmax/hs>2
# fw2 = '2012-05-25 06:00:00' #maior hmax/hs

# fig = pl.figure(figsize=(19,13))
# ax1 = fig.add_subplot(311)
# ax1.set_title(r'$RIG$',fontsize=tl)

# #ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))

# ax1.plot([pd.to_datetime(fw1),pd.to_datetime(fw1)],[0,6],'k--', linewidth=2)
# ax1.plot([pd.to_datetime(fw2),pd.to_datetime(fw2)],[0,6],'k--', linewidth=2)
# p1 = ax1.plot(rig.index,rig.hm0,'b',rigm.index,rigm.hm0,'r')
# ax1.legend(p1,[r'$AXYS$',r'$WW3$'],ncol=2,loc=0)
# ax1.grid()
# ax1.set_ylim(0,6)
# ax1.set_ylabel(r'$Hm0\ (m)$',fontsize=tl)
# ax1.set_xticklabels(ax1.get_xticklabels(), visible=False)
# ax1.set_yticklabels(ax1.get_yticks(), fontsize=fs)

# ax2 = fig.add_subplot(312)
# #xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
# ax2.plot([pd.to_datetime(fw1),pd.to_datetime(fw1)],[2,20],'k--', linewidth=2)
# ax2.plot([pd.to_datetime(fw2),pd.to_datetime(fw2)],[2,20],'k--', linewidth=2)
# ax2.plot(rig.index,rig.tp,'.b',rigm.index,rigm.tp,'.r')
# ax2.grid()
# ax2.set_ylim(2,20)
# #pl.xticks(visible=False)
# ax2.set_ylabel(r'$Tp\ (s)$',fontsize=tl)
# ax2.set_xticklabels(ax2.get_xticklabels(), visible=False)
# ax2.set_yticklabels(ax2.get_yticks(), fontsize=fs)

# ax3 = fig.add_subplot(313)
# ax3.plot([pd.to_datetime(fw1),pd.to_datetime(fw1)],[0,360],'k--', linewidth=2)
# ax3.plot([pd.to_datetime(fw2),pd.to_datetime(fw2)],[0,360],'k--', linewidth=2)
# ax3.plot(rig.index,rig.dp,'.b',rigm.index,rigm.dp,'.r')
# ax3.grid()
# ax3.set_ylim(0,360)
# ax3.set_yticks(np.arange(0,360+45,45))
# ax3.set_ylabel(r'$Dp\ ($' + u'\u00b0' + r'$)$',fontsize=tl)
# ax3.set_yticklabels(np.arange(0,360+45,45), fontsize=fs)
# ax3.set_xticklabels(ax3.get_xticks(), fontsize=fs, rotation=10)
# ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))

# fig.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/ww3buoy.pdf', format='pdf', dpi=1200, bbox_inches='tight')


# #Floripa

# pl.figure(figsize=(12,8))
# pl.subplot(311)
# pl.title(r'$flnorian\'opolis/SC$',fontsize=fs)
# pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
# pl.plot(fln.index,fln.hm0,'b',flnm.index,flnm.hm0,'r')
# pl.legend([r'$AXYS$',r'$WW3$'],ncol=2,loc=0)
# pl.grid()
# pl.ylim(0,6)
# pl.xticks(visible=False)
# pl.ylabel(r'$Hm0\ (m)$',fontsize=fs)
# pl.subplot(312)
# pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
# pl.plot(fln.index,fln.tp,'.b',flnm.index,flnm.tp,'.r')
# pl.grid()
# pl.ylim(2,20)
# pl.xticks(visible=False)
# pl.ylabel(r'$Tp\ (s)$',fontsize=fs)
# pl.subplot(313)
# pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
# pl.plot(fln.index,fln.dp,'.b',flnm.index,flnm.dp,'.r')
# pl.grid()
# pl.ylim(0,360)
# pl.yticks(np.arange(0,360+45,45))
# pl.ylabel(r'$Dp\ ($' + u'\u00b0' + r'$)$',fontsize=fs)

# #Santos

# pl.figure(figsize=(12,8))
# pl.subplot(311)
# pl.title(r'$sanntos/SP$',fontsize=fs)
# pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
# pl.plot(san.index,san.hm0,'b',sanm.index,sanm.hm0,'r')
# pl.legend([r'$AXYS$',r'$WW3$'],ncol=2,loc=0)
# pl.grid()
# pl.ylim(0,6)
# pl.xticks(visible=False)
# pl.ylabel(r'$Hm0\ (m)$',fontsize=fs)
# pl.subplot(312)
# pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
# pl.plot(san.index,san.tp,'.b',sanm.index,sanm.tp,'.r')
# pl.grid()
# pl.ylim(2,20)
# pl.xticks(visible=False)
# pl.ylabel(r'$Tp\ (s)$',fontsize=fs)
# pl.subplot(313)
# pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
# pl.plot(san.index,san.dp,'.b',sanm.index,sanm.dp,'.r')
# pl.grid()
# pl.ylim(0,360)
# pl.yticks(np.arange(0,360+45,45))
# pl.ylabel(r'$Dp\ ($' + u'\u00b0' + r'$)$',fontsize=18)


###############################################################################################################
###############################################################################################################
###############################################################################################################
#estatisticas


# bias = pd.DataFrame()
# rmse = pd.DataFrame()
# si = pd.DataFrame()
# corr = pd.DataFrame()

# #data frame de estatisticas
# bias = pd.DataFrame({'rig_hm0' : [(rigm.hm0 - rig.hm0).mean()],
# 					 'rig_tp'  : [(rigm.tp - rig.tp).mean()],
# 					 'rig_dp'  : [(rigm.dp - rig.dp).mean()],
# 					 'fln_hm0' : [(flnm.hm0 - fln.hm0).mean()],
# 					 'fln_tp'  : [(flnm.tp - fln.tp).mean()],
# 					 'fln_dp'  : [(flnm.dp - fln.dp).mean()],
# 					 'san_hm0' : [(sanm.hm0 - san.hm0).mean()],
# 					 'san_tp'  : [(sanm.tp - san.tp).mean()],
# 					 'san_dp'  : [(sanm.dp - san.dp).mean()]})


# rmse = pd.DataFrame({'rig_hm0' : [np.sqrt( np.sum( (rigm.hm0 - rig.hm0) ** 2 ) / len(rig) )],
# 					 'rig_tp'  : [np.sqrt( np.sum( (rigm.tp - rig.tp) ** 2 ) / len(rig) )],
# 					 'rig_dp'  : [np.sqrt( np.sum( (rigm.dp - rig.dp) ** 2 ) / len(rig) )],
# 					 'fln_hm0' : [np.sqrt( np.sum( (flnm.hm0 - fln.hm0) ** 2 ) / len(fln) )],
# 					 'fln_tp'  : [np.sqrt( np.sum( (flnm.tp - fln.tp) ** 2 ) / len(fln) )],
# 					 'fln_dp'  : [np.sqrt( np.sum( (flnm.dp - fln.dp) ** 2 ) / len(fln) )],
# 					 'san_hm0' : [np.sqrt( np.sum( (sanm.hm0 - san.hm0) ** 2 ) / len(san) )],
# 					 'san_tp'  : [np.sqrt( np.sum( (sanm.tp - san.tp) ** 2 ) / len(san) )],
# 					 'san_dp'  : [np.sqrt( np.sum( (sanm.dp - san.dp) ** 2 ) / len(san) )]})


# si = pd.DataFrame({'rig_hm0' : [rmse['rig_hm0'][0] / rig.hm0.mean()],
# 				   'rig_tp'  : [rmse['rig_tp'][0] / rig.tp.mean()],
# 				   'rig_dp'  : [rmse['rig_dp'][0] / rig.dp.mean()],
# 				   'fln_hm0' : [rmse['fln_hm0'][0] / fln.hm0.mean()],
# 				   'fln_tp'  : [rmse['fln_tp'][0] / fln.tp.mean()],
# 				   'fln_dp'  : [rmse['fln_dp'][0] / fln.dp.mean()],
# 				   'san_hm0' : [rmse['san_hm0'][0] / san.hm0.mean()],
# 				   'san_tp'  : [rmse['san_tp'][0] / san.tp.mean()],
# 				   'san_dp'  : [rmse['san_dp'][0] / san.dp.mean()]})


# corr = pd.DataFrame({'rig_hm0' : [np.corrcoef(rigm_hm0,rig_hm0)[0,1]],
# 				     'rig_tp'  : [np.corrcoef(rigm_tp,rig_tp)[0,1]],
# 				     'rig_dp'  : [np.corrcoef(rigm_dp,rig_dp)[0,1]],
# 				     'fln_hm0' : [np.corrcoef(flnm_hm0,fln_hm0)[0,1]],
# 				     'fln_tp'  : [np.corrcoef(flnm_tp,fln_tp)[0,1]],
# 				     'fln_dp'  : [np.corrcoef(flnm_dp,fln_dp)[0,1]],
# 				     'san_hm0' : [np.corrcoef(sanm_hm0,san_hm0)[0,1]],
# 				     'san_tp'  : [np.corrcoef(sanm_tp,san_tp)[0,1]],
# 				     'san_dp'  : [np.corrcoef(sanm_dp,san_dp)[0,1]]})







#pl.close('all')




pl.show()