# The program reads the point output files .tab of wavewatch III v 3.14. 
# It just organize the .tab and make the figures. At the end, the program writes a pointparameter text files for each point 
# Do not forget to set the correct values of npo and nt, as well as the name of .tab file.
#
# Ricardo Martins Campos (PhD student) 
# riwave@gmail.com
# +55 21 38654845    +55 21 84660434
# ----------------------------------------------------------------------------------------
# Laboratorio de Instrumentacao Oceanografica (LIOC) AECO/PENO/COPPE/UFRJ  
# MotorDePopa Wave Research Group
# ASA - CENPES/PETROBRAS 
# Rio de Janeiro - Brazil
# ----------------------------------------------------------------------------------------
# Contributions: Luiz Alexandre Guerra (CENPES/PETROBRAS).
# ----------------------------------------------------------------------------------------
# Number of points .tab
# npo=25  # ate 28/09/2014
npo=26  # a partir de 28/09/2014
# Number of times 
nt=169
# Name of tab output file
name='southatl.tab'


import matplotlib
matplotlib.use('Agg')


# ----------------------
# Pay attention to the pre-requisites and libraries
import os
from pylab import *
import pylab as plt
import numpy as np

from time import strptime
from calendar import timegm

# Palette and colors for plotting the figures
from mpl_toolkits.basemap import cm
colormap = cm.GMT_polar
palette = plt.cm.jet
# palette.set_bad('aqua', 10.0)
import matplotlib.colors as colors





# Pay attention to the pre-requisites and libraries
import os
from datetime import datetime
from pylab import *
import pylab as plt
from matplotlib.ticker import FixedLocator
from matplotlib.dates import DateFormatter
import numpy as np
from datetime import datetime






ano=zeros(nt,'i2');mes=zeros(nt,'i2');dia=zeros(nt,'i2');hora=zeros(nt,'i2');minu=zeros(nt,'i2')
hs=zeros((nt,npo),'f');tp=zeros((nt,npo),'f');dp=zeros((nt,npo),'f');psprd=zeros((nt,npo),'f')
lon=zeros(npo,'f');lat=zeros(npo,'f')
wndinf=zeros((npo,2,nt),'f')
# Write the name of your .tab file
fp = open(name)
nomefig=fp.readline();nomefig=nomefig[8:12]+nomefig[13:15]+nomefig[16:18]
fp.close
fp = open(name)



for j in range(0,npo):

	fw = open('wind_deph_pos_'+str(j+1).zfill(3)+'.txt')
	lixo=fw.readline();lixo=fw.readline();lixo=fw.readline();lixo=fw.readline();

	for i in range(0,nt):
		line=fw.readline()
		line=line.strip().split()
		wndinf[j,0,i]=line[5] # Wind speed
		wndinf[j,1,i]=line[6] # Wind direction

	fw.close


for i in range(0,nt):

	cabc=fp.readline()

	ano[i]=int(cabc[8:12])
	mes[i]=int(cabc[13:15])
	dia[i]=int(cabc[16:18])
	hora[i]=int(cabc[19:21])
	minu[i]=int(cabc[22:24])

	lixo=fp.readline()
	lixo=fp.readline()
	lixo=fp.readline()
	lixo=fp.readline()

	for j in range(0,npo):

		line=fp.readline()
		line=line.strip().split()

		lon[j]=line[0]
		lat[j]=line[1]

		hs[i,j]=float(line[2])
		if float(line[7])==0:
			tp[i,j]=0
		else:
			tp[i,j]=1/float(line[7])
		dp[i,j]=float(line[8])
		psprd[i,j]=float(line[9])



	lixo=fp.readline()
	lixo=fp.readline()

fp.close



dates = np.array([plt.date2num(datetime(aa,mm,dd,hh,mi)) for aa,mm,dd,hh,mi in zip(ano,mes,dia,hora,minu)])


for j in range(0,npo):

	fig = plt.figure(figsize=(9,7))
#	title(' Wavewatch III. Point: Lat'+repr(lat[j].round(2))+' Lon'+repr(lon[j].round(2)))
#	plt.figtext(3,8.5,' Wavewatch III. Point:  Lat '+repr(lat[j].round(2))[0:6]+' Lon '+repr(lon[j].round(2))[0:6],fontsize=9)

	ax = fig.add_subplot(321)
	ax.plot_date(dates,wndinf[j,0,:],'ko')
	ax.set_xlim( dates[0], dates[-1] )
	ax.xaxis.set_major_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_minor_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_major_formatter( DateFormatter('%d') )
	ax.fmt_xdata = DateFormatter('%d')
	ylabel("Velocidade do Vento (m/s)", fontsize=8)
	for label in ax.get_xticklabels() + ax.get_yticklabels():
		label.set_fontsize(8)
	grid()

	ax = fig.add_subplot(322)
	ax.plot_date(dates,wndinf[j,1,:],'ko')
	ax.set_xlim( dates[0], dates[-1] )
	ax.set_ylim(0,360)
	ax.xaxis.set_major_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_minor_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_major_formatter( DateFormatter('%d') )
	ax.fmt_xdata = DateFormatter('%d')
	ylabel("Direcao do Vento (graus)", fontsize=8)
	for label in ax.get_xticklabels() + ax.get_yticklabels():
		label.set_fontsize(8)
	grid()


	ax = fig.add_subplot(323)
	ax.plot_date(dates,hs[:,j],'ro')
	ax.set_xlim( dates[0], dates[-1] )
	ax.xaxis.set_major_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_minor_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_major_formatter( DateFormatter('%d') )
	ax.fmt_xdata = DateFormatter('%d')
	ylabel("Altura Significativa de onda (m)", fontsize=8)
	for label in ax.get_xticklabels() + ax.get_yticklabels():
		label.set_fontsize(8)
	grid()



	ax = fig.add_subplot(324)
	ax.plot_date(dates,dp[:,j])
	ax.set_xlim( dates[0], dates[-1] )
	ax.set_ylim(0,360)
	ax.xaxis.set_major_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_minor_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_major_formatter( DateFormatter('%d') )
	ax.fmt_xdata = DateFormatter('%d')
	ylabel("Direcao de Pico (graus)", fontsize=8)
	for label in ax.get_xticklabels() + ax.get_yticklabels():
		label.set_fontsize(8)
	grid()



	ax = fig.add_subplot(325)
	ax.plot_date(dates,tp[:,j])
	ax.set_xlim( dates[0], dates[-1] )
	ax.xaxis.set_major_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_minor_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_major_formatter( DateFormatter('%d') )
	ax.fmt_xdata = DateFormatter('%d')
	ylabel("Periodo de Pico (s)", fontsize=8)
	xlabel("Dia do mes", fontsize=10)
	for label in ax.get_xticklabels() + ax.get_yticklabels():
		label.set_fontsize(8)
	grid()



	ax = fig.add_subplot(326)
	ax.plot_date(dates,psprd[:,j])
	ax.set_xlim( dates[0], dates[-1] )
	ax.xaxis.set_major_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_minor_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_major_formatter( DateFormatter('%d') )
	ax.fmt_xdata = DateFormatter('%d')
	ylabel("Espalhamento direcional [spreading] (graus) ", fontsize=6)
	xlabel("Dia do mes", fontsize=10)
	for label in ax.get_xticklabels() + ax.get_yticklabels():
		label.set_fontsize(8)
	grid()

	plt.figtext(0.3,0.95,'GFS + WavewatchIII.   Ponto:  Lat '+repr(lat[j].round(2))[0:6]+' Lon '+repr(lon[j].round(2))[0:6],fontsize=12)

	savefig('sww3_p'+str(j+1).zfill(3)+'.jpg', dpi=None, facecolor='w', edgecolor='w',
	orientation='portrait', papertype=None, format='jpg',
	transparent=False, bbox_inches=None, pad_inches=0.1)

	plt.close()

for i in range(0,npo):

	vf=file('pointparameters_'+str(i+1).zfill(3)+'.txt','w')
	vf.write('% WAVEWATCH III Point:  Lat '+repr(lat[j].round(2))[0:6]+' Lon '+repr(lon[j].round(2))[0:6])
	vf.write('\n')	
	vf.write('%     Date           Hs      Tp       Dp     PSprd')
  
	vf.write('\n')

	np.savetxt(vf,zip(ano,mes,dia,hora,minu,hs[:,i],tp[:,i],dp[:,i],psprd[:,i]),fmt="%4i %2i %2i %2i %2i %7.3f %7.3f %8.1f %8.2f",delimiter='/t')   # escreve V no formato do ww3
	vf.close


os.system("rm /home/rmc/ww3/ww3v314/output/wait_pontos.txt")

