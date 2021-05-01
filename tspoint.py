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
npo=14
# Number of times 
nt=745
# Name of tab output file
name='grid2.tab'





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
# Write the name of your .tab file
fp = open(name)
nomefig=fp.readline();nomefig=nomefig[8:12]+nomefig[13:15]+nomefig[16:18]
fp.close
fp = open(name)



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

	fig = plt.figure(figsize=(7,8))

	ax = fig.add_subplot(411)
	ax.plot_date(dates,hs[:,j],'ro')
	title(' Wavewatch III. Point: Lat'+repr(lat[j])[0:8]+' Lon'+repr(lon[j])[0:8])
	ax.set_xlim( dates[0], dates[-1] )
	ax.xaxis.set_major_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_minor_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_major_formatter( DateFormatter('%d') )
	ax.fmt_xdata = DateFormatter('%d')
	ylabel("Significant Wave Height (m)", fontsize=8)
	for label in ax.get_xticklabels() + ax.get_yticklabels():
		label.set_fontsize(8)
	grid()

	ax = fig.add_subplot(412)
	ax.plot_date(dates,tp[:,j])
	ax.set_xlim( dates[0], dates[-1] )
	ax.xaxis.set_major_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_minor_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_major_formatter( DateFormatter('%d') )
	ax.fmt_xdata = DateFormatter('%d')
	ylabel("Peak Period (s)", fontsize=8)
	for label in ax.get_xticklabels() + ax.get_yticklabels():
		label.set_fontsize(8)
	grid()

	ax = fig.add_subplot(413)
	ax.plot_date(dates,dp[:,j])
	ax.set_xlim( dates[0], dates[-1] )
	ax.xaxis.set_major_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_minor_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_major_formatter( DateFormatter('%d') )
	ax.fmt_xdata = DateFormatter('%d')
	ylabel("Peak Direction (degrees)", fontsize=8)
	for label in ax.get_xticklabels() + ax.get_yticklabels():
		label.set_fontsize(8)
	grid()


	ax = fig.add_subplot(414)
	ax.plot_date(dates,psprd[:,j])
	ax.set_xlim( dates[0], dates[-1] )
	ax.xaxis.set_major_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_minor_locator( HourLocator(arange(0,nt,48)) )
	ax.xaxis.set_major_formatter( DateFormatter('%d') )
	ax.fmt_xdata = DateFormatter('%d')
	ylabel("Peak Spreading (degrees)", fontsize=8)
	for label in ax.get_xticklabels() + ax.get_yticklabels():
		label.set_fontsize(8)
	grid()


	savefig('sww3_p'+repr(j+1)+'_'+nomefig+'.png', dpi=None, facecolor='w', edgecolor='w',
	orientation='portrait', papertype=None, format='png',
	transparent=False, bbox_inches=None, pad_inches=0.1)

	plt.close()

for i in range(0,npo):

	vf=file('pointparameters_'+repr(i+1)+'_'+nomefig+'.txt','w')
	vf.write('% WAVEWATCH III Point: Lat'+repr(lat[i])[0:8]+' Lon'+repr(lon[i])[0:8])
	vf.write('\n')	
	vf.write('%     Date           Hs      Tp       Dp     PSprd')
  
	vf.write('\n')

	np.savetxt(vf,zip(ano,mes,dia,hora,minu,hs[:,i],tp[:,i],dp[:,i],psprd[:,i]),fmt="%4i %2i %2i %2i %2i %7.3f %7.3f %8.1f %8.2f",delimiter='/t')   # escreve V no formato do ww3
	vf.close




