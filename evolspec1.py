'''
Plotagem da evolucao do espectro
'''

import os
import numpy as np
import espec
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime

plt.close('all')


pathname  = os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/bruto/series_ast/'
pathnamep = os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/proc/parametros/'
pathnamem = os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/mod/'

adcp = pd.read_table(pathnamep + '/adcp01_vale.out', sep=',')

adcp.index = pd.to_datetime(adcp['# data'],format='%Y%m%d%H%M')

#################################

esp_mod  = np.loadtxt(pathnamem + 'espe1d_mod_201302.txt')
freq_mod = np.loadtxt(pathnamem + 'freq_mod_201302.txt')

#carrega parametros do modelo
date_swn, hm0_swn, tp_swn, dp_swn = np.loadtxt(os.environ['HOME'] + '/Dropbox/ww3vale/trocas/msc_isa/Espectros/201302/SWAN/table_point_adcp01.out',
 skiprows=7, usecols=(0,1,3,2), unpack=True)


#create date vector for model
mod_date = pd.date_range('2013-02-01','2013-03-01', freq='H')

# filename = 'evolspec_201302.png'

adcp = adcp.loc['2013-02'][1:-1] #usar para fev
#adcp = adcp.loc['2013-04'][1:] #usar para abril

listaadcpmes = ['adcp1_201302']

#################################


datestradcp = np.array([datetime.strftime(adcp.index[i], '%Y-%m-%d %H') for i in range(len(adcp.index))])
datestrmod  = np.array([datetime.strftime(mod_date[i],   '%Y-%m-%d %H') for i in range(len(mod_date))])

#acha no modelo onde tem dados do adcp
ind = []
for i in range(len(datestrmod)):
	aux = pl.find(datestrmod[i] == datestradcp)
	if len(aux):
		ind.append(int(aux))


#pega no modelo onde tem dados do adcp
esp_mod = esp_mod[:,ind]


for adcpmes in listaadcpmes:

    #lista arquivos do diretorio atual do periodo escolhido
    listap = []

    for f in os.listdir(pathname):
        if f.startswith(adcpmes):
            listap.append(f)

    listap=np.sort(listap)


e = []
for i in range(len(listap)):

	co, dd, dc = np.loadtxt(pathname + listap[i],unpack=True)

	if len(co) == 1024:
		print str(i) + ' - ' + str(len(co))
		fs = 1
		nfft = 64
	elif len(co) > 1024:
		print str(i) + ' - ' + str(len(co))
		fs = 2
		nfft = 128


	#espectro
	aa = espec.espec1(co,nfft,fs)

	e.append(aa[:,1])

	esp = np.array(e).T


############################################################################

# fig = plt.figure(figsize=(15,9))
# ax1 = fig.add_subplot(411)
# ax1.contour(adcp.index,aa[:,0],esp, 20) #[0.05,0.08,0.10, 0.15, 0.20])
# ax1.set_xticklabels(ax1.get_xticklabels(), visible=False)
# ax1.grid()
# #ax1.set_axes('tight')
# ax1.set_ylim(0.05,0.4)
# ax1.set_ylabel('Freq. (Hz)')

# #ax1.set_xticklabels(ax.get_xticks(), adcp.index.astype(str),  fontsize=10, rotation=5)

# ax2 = fig.add_subplot(412)
# ax2.plot(adcp.index,adcp[' hm0'])
# ax2.set_xticklabels(ax2.get_xticklabels(), visible=False)
# ax2.grid()
# ax2.set_ylabel('Hs (m)')

# ax3 = fig.add_subplot(413)
# ax3.plot(adcp.index,adcp[' tp'],'.')
# ax3.set_xticklabels(ax3.get_xticklabels(), visible=False)
# ax3.grid()
# ax3.set_ylabel('Tp (s)')

# ax4 = fig.add_subplot(414)
# ax4.plot(adcp.index,adcp[' dirtp'],'b.')
# #ax4.plot(adcp.index,adcp[' meandir'],'r.')
# ax4.grid()
# ax4.set_ylabel('Dp (graus)')
# ax4.set_yticks(range(0,405,45))
# ax4.set_ylim(0,360)
# #ax4.set_xticklabels(ax4.get_xticks(), visible=True, rotation=5)
# #ax4.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))

# fig.savefig('fig/evolspec_201302_adcp.png', bbox_inches='tight')

# ############################################################################


# fig = plt.figure(figsize=(15,9))
# ax1 = fig.add_subplot(411)
# ax1.contour(adcp.index,freq_mod,esp_mod, 20) #[0.05,0.08,0.10, 0.15, 0.20])
# ax1.set_xticklabels(ax1.get_xticklabels(), visible=False)
# ax1.grid()
# #ax1.set_axes('tight')
# ax1.set_ylim(0.05,0.4)
# ax1.set_ylabel('Freq. (Hz)')

# #ax1.set_xticklabels(ax.get_xticks(), adcp.index.astype(str),  fontsize=10, rotation=5)

# ax2 = fig.add_subplot(412)
# ax2.plot(mod_date, hm0_swn)
# ax2.set_xticklabels(ax2.get_xticklabels(), visible=False)
# ax2.grid()
# ax2.set_ylabel('Hs (m)')

# ax3 = fig.add_subplot(413)
# ax3.plot(mod_date, tp_swn,'.')
# ax3.set_xticklabels(ax3.get_xticklabels(), visible=False)
# ax3.grid()
# ax3.set_ylabel('Tp (s)')

# ax4 = fig.add_subplot(414)
# ax4.plot(mod_date, dp_swn,'b.')
# #ax4.plot(adcp.index,adcp[' meandir'],'r.')
# ax4.grid()
# ax4.set_ylabel('Dp (graus)')
# ax4.set_yticks(range(0,405,45))
# ax4.set_ylim(0,360)
# #ax4.set_xticklabels(ax4.get_xticks(), visible=True, rotation=5)
# #ax4.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))

# fig.savefig('fig/evolspec_201302_swan.png', bbox_inches='tight')






###########################################################
#evolucao espetrao - dado e modelo
#stop

#normaliza o espectro do dado e modelo
#esp = esp / esp.max()
#esp = esp / esp.max()
#esp_mod = esp_mod / esp_mod.max()

fig = plt.figure(figsize=(15,9))
ax1 = fig.add_subplot(211)
ax1.contourf(adcp.index,aa[:,0],esp)#, np.arange(0.0,1.1,0.05), shading='flat')
ax1.set_xticklabels(ax1.get_xticklabels(), visible=False)
ax1.grid()
#ax1.set_axes('tight')
ax1.set_ylim(0.05,0.4)
ax1.set_ylabel('Freq. (Hz)')

ax2 = fig.add_subplot(212)
ax2.contourf(adcp.index,freq_mod,esp_mod)#, np.arange(0.0,1.1,0.05))
#ax2.set_xticklabels(ax2.get_xticklabels(), visible=True)
ax2.grid()
#ax1.set_axes('tight')
ax2.set_ylim(0.05,0.4)
ax2.set_ylabel('Freq. (Hz)')




plt.show()
