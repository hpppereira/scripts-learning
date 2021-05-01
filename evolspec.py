'''
Plotagem da evolucao do espectro
'''

import os
import numpy as np
import espec
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import proconda

plt.close('all')


pathname = os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/bruto/series_ast/'
pathnamep = os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/proc/parametros/'

adcp = pd.read_table(pathnamep + '/adcp01_vale.out', sep=',')

adcp.index = pd.to_datetime(adcp['# data'],format='%Y%m%d%H%M')

filename = 'evolspec_201304.png'

#adcp = adcp.loc['2013-02'][1:-1] #usar para fev
adcp = adcp.loc['2013-04'][1:] #usar para abril

listaadcpmes = ['adcp1_201304']

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

# fig.savefig('fig/evolspec_201302_a.png', bbox_inches='tight')

# plt.show()
