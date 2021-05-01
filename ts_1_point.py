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
npo=1
# Number of times 
#nt=744
nt=744
# Name of tab output file
name='grade2.tab'





# Pay attention to the pre-requisites and libraries
import os
from datetime import datetime
from pylab import *
import pylab as plt
from matplotlib.ticker import FixedLocator
from matplotlib.dates import DateFormatter
import numpy as np
from datetime import datetime

lon=-44
lat=-25


ano=zeros(nt,'i2');mes=zeros(nt,'i2');dia=zeros(nt,'i2');hora=zeros(nt,'i2');minu=zeros(nt,'i2')
hs=zeros((nt),'f');tp=zeros((nt),'f');dp=zeros((nt),'f');psprd=zeros((nt),'f')
# Write the name of your .tab file
fp = open(name);cabc=fp.readline();cabc=fp.readline();cabc=fp.readline()



for i in range(0,nt):

	cabc=fp.readline()

	ano[i]=(cabc[2:6])
	mes[i]=int(cabc[6:8])
	dia[i]=int(cabc[8:10])
	hora[i]=int(cabc[11:13])
	minu[i]=int(cabc[13:15])

	line=cabc.strip().split()


	hs[i]=float(line[4])
	if float(line[9])==0:
		tp[i]=0
	else:
		tp[i]=1/float(line[9])

	dp[i]=float(line[10])
	psprd[i]=float(line[11])

fp.close



dates = np.array([plt.date2num(datetime(aa,mm,dd,hh,mi)) for aa,mm,dd,hh,mi in zip(ano,mes,dia,hora,minu)])



fig = plt.figure(figsize=(7,8))

ax = fig.add_subplot(411)
ax.plot_date(dates,hs[:],'ro')
title(' Wavewatch III. Point: Lat'+repr(lat)[0:8]+' Lon'+repr(lon)[0:8])
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
ax.plot_date(dates,tp[:])
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
ax.plot_date(dates,dp[:])
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
ax.plot_date(dates,psprd[:])
ax.set_xlim( dates[0], dates[-1] )
ax.xaxis.set_major_locator( HourLocator(arange(0,nt,48)) )
ax.xaxis.set_minor_locator( HourLocator(arange(0,nt,48)) )
ax.xaxis.set_major_formatter( DateFormatter('%d') )
ax.fmt_xdata = DateFormatter('%d')
ylabel("Peak Spreading (degrees)", fontsize=8)
for label in ax.get_xticklabels() + ax.get_yticklabels():
	label.set_fontsize(8)
grid()


savefig('sww3.png', dpi=None, facecolor='w', edgecolor='w',
	orientation='portrait', papertype=None, format='png',
	transparent=False, bbox_inches=None, pad_inches=0.1)

plt.close()



vf=file('pointparameters.txt','w')
vf.write('% WAVEWATCH III Point: Lat'+repr(lat)[0:8]+' Lon'+repr(lon)[0:8])
vf.write('\n')	
vf.write('%     Date           Hs      Tp       Dp     PSprd')
  
vf.write('\n')

np.savetxt(vf,zip(ano,mes,dia,hora,minu,hs[:],tp[:],dp[:],psprd[:]),fmt="%4i %2i %2i %2i %2i %7.3f %7.3f %8.1f %8.2f",delimiter='/t')   # escreve V no formato do ww3
vf.close




