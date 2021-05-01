'''
Reports mensais dos dados do PNBOIA

Henrique P P Pereira
'''

import os
import pandas as pd
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

plt.close('all')

#caminho dos dados da boia e resultados do modelo
pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/proc/' #boia

#carrega dados do modelo
rig  = pd.read_csv(pathname + 'RIG_8_Triaxys.csv', parse_dates=['date'], index_col='date')
riga = pd.read_csv(pathname + 'RIG_Argos.csv', parse_dates=['date'], index_col='date')
fln  = pd.read_csv(pathname + 'FLN_8_Triaxys.csv', parse_dates=['date'], index_col='date')
flna = pd.read_csv(pathname + 'FLN_Argos.csv', parse_dates=['date'], index_col='date')
san  = pd.read_csv(pathname + 'SAN_8_Triaxys.csv', parse_dates=['date'], index_col='date')
sana = pd.read_csv(pathname + 'SAN_Argos.csv', parse_dates=['date'], index_col='date')

rig.dp = rig.dp - 17
fln.dp = fln.dp - 22
san.dp = san.dp - 23

rig.loc[rig.dp < 0].dp = rig.loc[rig.dp < 0].dp + 360
fln.loc[fln.dp < 0].dp = fln.loc[fln.dp < 0].dp + 360
san.loc[san.dp < 0].dp = san.loc[san.dp < 0].dp + 360

#plot reports monthly
for m in range(2,7):

	rig1 = rig.loc['2012-'+str(m)]
	fln1 = fln.loc['2012-'+str(m)]
	san1 = san.loc['2012-'+str(m)]

	riga1 = riga.loc['2012-'+str(m)]
	flna1 = flna.loc['2012-'+str(m)]
	sana1 = sana.loc['2012-'+str(m)]
	
	fig = plt.figure(figsize=(24,12))
	ax1 = fig.add_subplot(331)
	ax1.set_title('PNBOIA - B69153 \n Rio Grande/RS')
	ax1.plot(rig1.index, rig1.hm0, 'b', rig1.index, rig1.hmax, 'r--')
	ax1.set_xticklabels(ax1.get_xticklabels(), visible=False)
	ax1.set_ylim(0,10)
	ax1.grid()
	ax1.set_ylabel('Hs, Hmax (m)')

	ax2 = fig.add_subplot(332)
	ax2.set_title('PNBOIA - B69152 \n Florianopolis/SC')
	ax2.plot(fln1.index, fln1.hm0, 'b', fln1.index, fln1.hmax, 'r--')
	ax2.set_xticklabels(ax2.get_xticklabels(), visible=False)
	ax2.set_ylim(0,10)
	ax2.grid()
	
	ax3 = fig.add_subplot(333)
	ax3.set_title('PNBOIA - B69150 \n Santos/SP')
	ax3.plot(san1.index, san1.hm0, 'b', san1.index, san1.hmax, 'r--')
	ax3.set_xticklabels(ax3.get_xticklabels(), visible=False)
	ax3.set_ylim(0,10)
	ax3.grid()

	ax4 = fig.add_subplot(334)
	ax4.plot(rig1.index, rig1.tp, 'bo')
	ax4.set_xticklabels(ax4.get_xticklabels(), visible=False)
	ax4.set_ylim(0,20)
	ax4.grid()
	ax4.set_ylabel('Tp (s)')

	ax5 = fig.add_subplot(335)
	ax5.plot(fln1.index, fln1.tp, 'bo')
	ax5.set_xticklabels(ax5.get_xticklabels(), visible=False)
	ax5.set_ylim(0,20)
	ax5.grid()

	ax6 = fig.add_subplot(336)
	ax6.plot(san1.index, san1.tp, 'bo')
	ax6.set_xticklabels(ax6.get_xticklabels(), visible=False)
	ax6.set_ylim(0,20)
	ax6.grid()

	ax7 = fig.add_subplot(337)
	ax7.plot(rig1.index, rig1.dp, 'bo')
#	ax7.set_xticklabels(ax7.get_xticklabels(), visible=True)
	ax7.set_xticklabels(ax7.get_xticklabels(), visible=True, rotation=25)
	ax7.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
	ax7.set_yticks(np.arange(0,360+45,45))
	ax7.set_ylim(0,360)
	ax7.grid()
	ax7.set_ylabel('Dp (deg)')

	ax8 = fig.add_subplot(338)
	ax8.plot(fln1.index, fln1.dp, 'bo')
	ax8.set_xticklabels(ax8.get_xticklabels(), visible=True, rotation=25)
	ax8.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#	ax8.set_xticklabels(ax8.get_xticklabels(), visible=True)
	ax8.set_yticks(np.arange(0,360+45,45))
	ax8.set_ylim(0,360)
	ax8.grid()

	ax9 = fig.add_subplot(339)
	ax9.plot(san1.index, san1.dp, 'bo')
	ax9.set_xticklabels(ax9.get_xticklabels(), visible=True, rotation=25)
	ax9.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
	ax9.set_yticks(np.arange(0,360+45,45))
	ax9.set_ylim(0,360)
	ax9.grid()

	fig.savefig('fig/report_ 20120' + str(m) + '.png')

pl.show()


