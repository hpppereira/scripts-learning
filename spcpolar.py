# The program reads the spectral output files .spc from wavewatch III v 3.14. 
# It organizes the .spc files, creates the figures and builds the netcdf file containing the directinal wave spectra of each point output. 
# Do not forget to set the correct values of nt (number of time outputs as well as the name of .spc file.
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
# number of time-outputs 
nt=288
# Name of spectra output file
name='ww3.92050200.spc'







# Pay attention to the pre-requisites and libraries
import os
from datetime import datetime
from pylab import *
import pylab as plt
import matplotlib.pyplot as ppt
from matplotlib.ticker import FixedLocator
from matplotlib.dates import DateFormatter
import numpy as np
from pupynere import NetCDFFile as nc

from time import strptime
from calendar import timegm

# Palette and colors for plotting the figures
from mpl_toolkits.basemap import cm
colormap = cm.GMT_polar
palette = plt.cm.jet
# palette.set_bad('aqua', 10.0)
import matplotlib.colors as colors



levels=[0.1,0.5,1,2,3,4,5,6,7,8,9,10,15]

jday = []
ano=zeros(nt,'i2');mes=zeros(nt,'i2');dia=zeros(nt,'i2');hora=zeros(nt,'i2');minu=zeros(nt,'i2')

# Open the spectra output file
fp = open(name)

# Header --------------------------------------
cabc=fp.readline()
modelr=cabc[0:22];gridl=cabc[44:-2]
cabc=cabc.strip().split()
nf=int(cabc[3]);nd=int(cabc[4]);npo=int(cabc[5])

freq=zeros(nf,'f');dire=zeros(nd,'f')
dspec=zeros((npo,nt,nd,nf),'f')
adire=zeros(dire.shape)
adspec=zeros(dspec.shape)
# pdspec=zeros((npo,nt,nd+1,nf),'f')

# Frequencies --------------------
ncf=nf/8;rncf=int(round(8*((float(nf)/8)-ncf)))

k=0
for i in range(0,ncf):
	line=fp.readline()
	line=line.strip().split()
	for j in range(0,8):
		freq[k]=float(line[j])
		k=k+1

if rncf>0:
	line=fp.readline()
	line=line.strip().split()
	for i in range(0,rncf):
		freq[k]=float(line[i])
		k=k+1	

# Directions ---------------------

ncd=nd/7;rncd=int(round(7*((float(nd)/7)-ncd)))

k=0
for i in range(0,ncd):
	line=fp.readline()
	line=line.strip().split()
	for j in range(0,7):
		dire[k]=float(line[j])#*180/pi
		k=k+1

if rncd>0:
	line=fp.readline()
	line=line.strip().split()
	for i in range(0,rncd):
		dire[k]=float(line[i])#*180/pi
		k=k+1

adire[0:17]=dire[7:24]
adire[17:24]=dire[0:7]
for i in range(0,nd):
	dire[i]=adire[nd-i-1]
# ----------------------------------

# Criando as grades para figura polar
frequencia,direcao = np.meshgrid(freq,dire)



lon=zeros(npo,'f');lat=zeros(npo,'f');deph=zeros(npo,'f');namep=zeros(npo,'c')
wnds=zeros((npo,nt),'f');wndd=zeros((npo,nt),'f')

nl=(nf*nd)/7;rnl=int(round(7*((float(nf*nd)/7)-nl)))
auxs=zeros((nf*nd),'f')





for t in range(0,nt):
	
	cabc=fp.readline()

	if t==0:
		datainic=cabc[0:8]+cabc[9:11]


	jday.append((timegm( strptime(cabc[0:8]+cabc[9:11], '%Y%m%d%H') ) - timegm( strptime('01/01/1950', '%d/%M/%Y') )) / 3600. / 24.)

	sdata=cabc[0:8]+cabc[9:11]
	cabc=cabc.strip().split()
	ano[t]=int(cabc[0][0:4])
	mes[t]=int(cabc[0][4:6])	
	dia[t]=int(cabc[0][6:8])
	hora[t]=int(cabc[1][0:2])
	minu[t]=int(cabc[1][2:4])

	for p in range(0,npo):

		cabc=fp.readline()
                namep[p]=cabc[1:11]
		cabc=cabc[12:-1].strip().split()
#		namep[p]=cabc[0][1:-1]
		lat[p]=cabc[0];lon[p]=cabc[1]
		deph[p]=cabc[2]
		wnds[p,t]=float(cabc[3]);wndd[p,t]=float(cabc[4])


		k=0
		for i in range(0,nl):
			line=fp.readline()
			line=line.strip().split()
			for j in range(0,7):
				auxs[k]=float(line[j])
				k=k+1

		if rncd>0:
			line=fp.readline()
			line=line.strip().split()
			for i in range(0,rnl):
				auxs[k]=float(line[i])
				k=k+1

		for ic in range(0,nf):
			for il in range(0,nd):
		                    dspec[p,t,il,ic]=auxs[il*nf+ic]
                 

		adspec[p,t,0:17,:]=dspec[p,t,7:24,:]
		adspec[p,t,17:24,:]=dspec[p,t,0:7,:]
		for i in range(0,nd):
			dspec[p,t,i,:]=adspec[p,t,nd-i-1,:]

#		adspec[p,t,0:12,:]=dspec[p,t,12:24,:]
#		adspec[p,t,12:24,:]=dspec[p,t,0:12,:]
#		dspec[p,t,:,:]=adspec[p,t,:,:]

#		pdspec[p,t,:,:]=dspec[p,t,:,:]    #((npo,nt,nd+1,nf),'f')
# Fazendo a figura do espectro polar--------------------------
                
                fig, ax = ppt.subplots(subplot_kw=dict(projection='polar'))
                ax.set_theta_zero_location("N")
                ax.set_theta_direction(-1)
                autumn()
                cax = ax.contourf(direcao,frequencia,dspec[p,t,:,:],levels,cmap=palette,norm=colors.normalize(vmin=0.1,vmax=15,clip=True), extent=[-3,3,-3,3])
                autumn()
                cb = fig.colorbar(cax)
                cb.set_label("Energia Espectral")
#		fig=plt.figure(figsize=(8,6))
#		contour(freq, dire, dspec[p,t,:,:],levels, colors='0.2')
#		axis([freq.min(), freq.max(), 0, 360])
#		contourf(freq, dire, dspec[p,t,:,:],levels,cmap=palette,norm=colors.normalize(vmin=0.1,vmax=15,clip=True), extent=[-3,3,-3,3]) 
#		axis([freq.min(), freq.max(), 0, 360]) 
#		grid()
#		xlabel('Frequency (Hz)')
#		ylabel('Direction (degrees)')
                
		title('WAVEWATCH III - Espectro Direcional. Ponto '+repr(p+1)+': Lat'+repr(lat[p])[0:8]+' Lon'+repr(lon[p])[0:8]+' - '+repr(dia[t])+'/'+repr(mes[t])+'/'+repr(ano[t])+' '+repr(hora[t])+'Z', fontsize=11)
#		ax = plt.gca()
#		pos = ax.get_position()
#		l, b, w, h = pos.bounds
#		cax = plt.axes([l+w+0.01, b+0.01, 0.03, h-0.01]) # setup colorbar axes.
#		plt.colorbar(cax=cax) # draw colorbar
#		plt.axes(ax)  # make the original axes current again
#		ax.text(0.58,25.,"Profundidade:"+repr(deph[p])[0:6]+" m",fontsize=8)
#		ax.text(0.58,15.,"Vel. do Vento:"+repr(wnds[p,t])[0:4]+" m/s",fontsize=7)
#		ax.text(0.58,5.,"Dir. do Vento:"+repr(wndd[p,t])[0:4]+" degrees",fontsize=7)
		savefig('dspec_p'+repr(p+1)+'_'+sdata+'.png', dpi=None, facecolor='w', edgecolor='w',
		orientation='portrait', papertype=None, format='png',
		transparent=False, bbox_inches=None, pad_inches=0.1)

                ppt.close()





fp.close


vf=file('directions_frequencies.txt','w')
vf.write('% WAVEWATCH III results - directions (degrees) and frequencies (Hz)')
vf.write('\n')
np.savetxt(vf,dire.reshape(1,-1),fmt="%8.2f",delimiter=' ') 
np.savetxt(vf,freq.reshape(1,-1),fmt="%8.4f",delimiter=' ') 
vf.close




for i in range(0,npo):

	vf=file('wind_deph_pos_'+repr(i+1)+'.txt','w')
	vf.write('% WAVEWATCH III results - header informations .spc file')
	vf.write('\n')
	vf.write('% Position: Lat'+repr(lat[i])+' Lon'+repr(lon[i]))
	vf.write('\n')
	vf.write('% Deph: '+repr(deph[i])[:-4]+' m')
	vf.write('\n')
	vf.write('%     Date     WindSpeed(m/s) WindDir(degrees)')
	vf.write('\n')
	np.savetxt(vf,zip(ano,mes,dia,hora,minu,wnds[i,:],wndd[i,:]),fmt="%4i %2i %2i %2i %2i %8.3f %8.2f",delimiter='/t') 
	vf.close



from pupynere import netcdf_file
from numpy import array
from numpy import arange, dtype 

for i in range(0,npo):
	# open a new netCDF file for writing.
	ncfile = netcdf_file('dspec'+datainic+'_'+repr(i+1)+'.nc','w')

	# create  dimensions.
	# ncfile.createDimension( 'point' , dspec.shape[0] )
	ncfile.createDimension( 'time' , dspec.shape[1] )
	ncfile.createDimension( 'directions' , dspec.shape[2] )
	ncfile.createDimension( 'frequencies' , dspec.shape[3] )

	# po = ncfile.createVariable('point',dtype('float32').char,('point',))
	ti = ncfile.createVariable('time',dtype('float32').char,('time',))
	dirs = ncfile.createVariable('directions',dtype('float32').char,('directions',))
	fres = ncfile.createVariable('frequencies',dtype('float32').char,('frequencies',))

 
	ti.units     = 'days since 1950-01-01 00:00:00' 
	dirs.units = 'degrees'
	fres.units = 'hertz'
	# write data to coordinate vars.
	#po=array([1, 2])
	ti [:] = jday
	dirs[:] = dire
	fres[:] = freq
	# create  variable
	spec = ncfile.createVariable('dspectr',dtype('float32').char,('time','directions','frequencies'))

	# set the units attribute.
	spec.units = 'Hz.m^2.degree'

	# write data to variables.
	spec[:,:,:] = dspec[i,:,:,:]
	# close the file
	ncfile.close()


