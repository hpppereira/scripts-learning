# This program reads the spectral output files .spc from wavewatch III v 3.14.  LIOC
# It organizes the .spc files, creates the figures and builds the netcdf file containing the directinal wave spectra of each point output. 
# Do not forget to set the correct values of nt (number of time outputs) as well as the name of .spc file.
# You'll have problems with point-out names with less than 10 characters. Set the wavewatch with output names equal to or larger than 'LIOC_BCam1', for example.
# Ricardo Martins Campos (PhD student)  27/09/2012
# riwave@gmail.com
# +1 202 5531739 
# ----------------------------------------------------------------------------------------
# Laboratorio de Instrumentacao Oceanografica (LIOC) AECO/PENO/COPPE/UFRJ  - Rio de Janeiro - Brazil 
# MotorDePopa Wave Research Group
# NCEP / NOAA - National Weather Service 
# ----------------------------------------------------------------------------------------
# Edited by: 
# ----------------------------------------------------------------------------------------
# Contributions: Izabel Nogueira (LIOC/PENO/COPPE/UFRJ), Luiz Alexandre Guerra (CENPES/PETROBRAS), Carlos Eduardo Parente (LIOC/PENO/COPPE/UFRJ), Nelson Violante (LIOC/PENO/COPPE/UFRJ), Fred Ostritz (LIOC/PENO/COPPE/UFRJ), Mariana Ximenes (LIOC/PENO/COPPE/UFRJ)
# ----------------------------------------------------------------------------------------
# number of time-outputs 
nt=169
# Name of spectra output file
name='southatl.spc'
# Decision of ploting output figures and(or) writing output files. If equal to 0 the output will not be created. If equal to 1 the output will be created
# Power Spectra (1D) Plot 
pspdecp=1
# Power Spectra (1D) text file 
pspdecw=1
# Directional Wave spectra (2D) Plot
dspdecp=1
# Directional Wave spectra (2D) NetCDF file
dspdecw=1
# PREP PLEDS output file
ppoutf=1
# Prep PLEDS ---------------------------------------------------
# Index limits for each frequency band. Take a look at the file directions_frequencies.txt and choose the frequency interval ans its indexes.
# 1) initialFreq-la, 2) la-lb, 3) lb-lc, 4) lc-ld, 5) ld-finalFreq  : Total of 5 bands 
la=5
lb=9
lc=12
ld=17
# --------------------------------------------------------------------------





# Python Libraries 
import matplotlib
matplotlib.use('Agg')

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


os.system("echo 'esperando fig pontos' > /home/lioc/ww3/ww3v314/output/wait_pontos.txt")


ano=zeros(nt,'i2');mes=zeros(nt,'i2');dia=zeros(nt,'i2');hora=zeros(nt,'i2');minu=zeros(nt,'i2')


# Open the spectra output file
fp = open(name)

# Header --------------------------------------
cabc=fp.readline()
modelr=cabc[1:22];gridl=cabc[44:-2]
cabc=cabc.strip().split()
nf=int(cabc[3]);nd=int(cabc[4]);npo=int(cabc[5])

freq=zeros(nf,'f');dire=zeros(nd,'f')
dspec=zeros((npo,nt,nd,nf),'f')
adire=zeros(dire.shape)
adspec=zeros(dspec.shape)

# Frequencies --------------------
ncf=nf/8; rncf=int(nf-(int(nf/8)*8));
k=0
for i in range(0,int(ncf)):
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
ncd=nd/7; rncd=int(nd-(int(nd/7)*7));
k=0
for i in range(0,int(ncd)):
	line=fp.readline()
	line=line.strip().split()
	for j in range(0,7):
		dire[k]=float(line[j])*180/pi
		k=k+1

if rncd>0:
	line=fp.readline()
	line=line.strip().split()
	for i in range(0,rncd):
		dire[k]=float(line[i])*180/pi
		k=k+1

inddire=int(find(dire==min(dire)))
adire[0:nd-(inddire+1)]=dire[(inddire+1):nd]
adire[nd-(inddire+1):nd]=dire[0:(inddire+1)]
for i in range(0,nd):
	dire[i]=adire[nd-i-1]
# ----------------------------------
     
# DF in frequency (dfim) . Nelson Violante and Fred Ostritz       
fretab=zeros((nf),'f')
dfim=zeros((nf),'f')	

fre1 = freq[0] 
fretab[0] = fre1
co = freq[(nf-1)]/freq[(nf-2)] 
dfim[0] = (co-1) * pi / nd * fretab[0] 

for ifre in range(1,nf-1):
	fretab[ifre] = fretab[ifre-1] * co 
	dfim[ifre] = (co-1) * pi / nd * (fretab[ifre]+fretab[ifre-1]) 

fretab[nf-1] = fretab[nf-2]*co
dfim[nf-1] = (co-1) * pi / nd * fretab[(nf-2)]       
# ------------------ 


# intialization of variables that will be used to calculate the energy, Hs and Dp of each band(PLEDS).
ef=zeros((npo,nt,5),'f') 
dpf=zeros((npo,nt,5),'f')     
pws=zeros((npo,nt,nf),'f')
pwst=zeros((npo,nt,nf),'f') 
hs=zeros((npo,nt,5),'f') 
hstot=zeros((npo,nt),'f') 
indd=zeros((npo,nt,5),'i') 
# -----
lon=zeros(npo,'f');lat=zeros(npo,'f');deph=zeros(npo,'f');namep=zeros((npo,10),'c')
wnds=zeros((npo,nt),'f');wndd=zeros((npo,nt),'f')

nl=int((nf*nd)/7); rnl=int((nf*nd)-(int((nf*nd)/7)*7));

auxs=zeros((nf*nd),'f')
sdata=zeros(nt,'i')

jday=zeros((nt),'d')

# Main loop in time
for t in range(0,nt):
	
	cabc=fp.readline()

	if t==0:
		datainic=cabc[0:8]+cabc[9:11]


	jday[t] = ((timegm( strptime(cabc[0:8]+cabc[9:11], '%Y%m%d%H') ) - timegm( strptime('01/01/1970', '%d/%M/%Y') )))

	sdata[t]=cabc[0:8]+cabc[9:11]

	cabc=cabc.strip().split()
	ano[t]=int(cabc[0][0:4])
	mes[t]=int(cabc[0][4:6])	
	dia[t]=int(cabc[0][6:8])
	hora[t]=int(cabc[1][0:2])
	minu[t]=int(cabc[1][2:4])

	
	# second loop: point outputs 
	for p in range(0,npo):

		cabc=fp.readline()
		cabc=cabc.strip().split()
		namep[p,:]=cabc[0][1:-1]
		lat[p]=cabc[1];lon[p]=cabc[2]
		deph[p]=cabc[3]
		wnds[p,t]=float(cabc[4]);wndd[p,t]=float(cabc[5])


		k=0
		for i in range(0,nl):
			line=fp.readline()
			line=line.strip().split()
			for j in range(0,7):
				auxs[k]=float(line[j])
				k=k+1

		if rnl>0:
			line=fp.readline()
			line=line.strip().split()
			for i in range(0,rnl):
				auxs[k]=float(line[i])
				k=k+1

		for ic in range(0,nf):
			for il in range(0,nd):
		                    dspec[p,t,il,ic]=auxs[il*nf+ic]


		adspec[p,t,0:nd-(inddire+1),:]=dspec[p,t,(inddire+1):nd,:]
		adspec[p,t,nd-(inddire+1):nd,:]=dspec[p,t,0:(inddire+1),:]
		for i in range(0,nd):
			dspec[p,t,i,:]=adspec[p,t,nd-i-1,:]

		adspec[p,t,0:int(nd/2),:]=dspec[p,t,int(nd/2):nd,:]
		adspec[p,t,int(nd/2):nd,:]=dspec[p,t,0:int(nd/2),:]
		dspec[p,t,:,:]=adspec[p,t,:,:]


		# PREP PLEDS (Campos&Parente 2009) -------------------------------------------------
		for il in range(0,nf):		
			pwst[p,t,il]=sum(dspec[p,t,:,il])

		pwst[p,t,:]=pwst[p,t,:]*dfim[:]	
		
		# Total energy at each frequency band
		ef[p,t,0]=sum(pwst[p,t,0:la])
		ef[p,t,1]=sum(pwst[p,t,la:lb])
		ef[p,t,2]=sum(pwst[p,t,lb:lc])
		ef[p,t,3]=sum(pwst[p,t,lc:ld])
		ef[p,t,4]=sum(pwst[p,t,ld:])
		# Significant wave height at each frequency band
		hs[p,t,0]=4.01*sqrt(ef[p,t,0])
		hs[p,t,1]=4.01*sqrt(ef[p,t,1])
		hs[p,t,2]=4.01*sqrt(ef[p,t,2])
		hs[p,t,3]=4.01*sqrt(ef[p,t,3])
		hs[p,t,4]=4.01*sqrt(ef[p,t,4])
		
		# Just for checking the total significant wave height. Must be equal to 4.01*sqrt(sum(pwst[p,t,:]))
		hstot[p,t]=sqrt(hs[p,t,0]**2 + hs[p,t,1]**2 + hs[p,t,2]**2 + hs[p,t,3]**2 + hs[p,t,4]**2)
				
		# Directional index of the maximum energy at each band				
		indd[p,t,0] = int(dspec[p,t,:,0:la].argmax()/dspec[p,t,:,0:la].shape[1])
		indd[p,t,1] = int(dspec[p,t,:,la:lb].argmax()/dspec[p,t,:,la:lb].shape[1]) 			
		indd[p,t,2] = int(dspec[p,t,:,lb:lc].argmax()/dspec[p,t,:,lb:lc].shape[1]) 
		indd[p,t,3] = int(dspec[p,t,:,lc:ld].argmax()/dspec[p,t,:,lc:ld].shape[1]) 
		indd[p,t,4] = int(dspec[p,t,:,ld:nf].argmax()/dspec[p,t,:,ld:nf].shape[1]) 	
				
		dpf[p,t,0] = dire[indd[p,t,0]]
		dpf[p,t,1] = dire[indd[p,t,1]]
		dpf[p,t,2] = dire[indd[p,t,2]]
		dpf[p,t,3] = dire[indd[p,t,3]]
		dpf[p,t,4] = dire[indd[p,t,4]]	



		# SPECTRA PLOTS 

		# Power Spectra Plot -------------------------------------------------
		if pspdecp==1: 
			fig=plt.figure(figsize=(8,6))
			plot(freq,pwst[p,t,:])
			grid()
			xlabel('Frequency (Hz)')
			ylabel('Power Spectrum (m^2/Hz)')         
			title('WAVEWATCH III - Espectro de Energia / Power Spectrum      '+repr(sdata[t])[6:8]+'/'+repr(sdata[t])[4:6]+'/'+repr(sdata[t])[0:4]+' '+repr(sdata[t])[8:10]+'Z', fontsize=11)		
			plt.figtext(0.66,0.88,"Profundidade: "+repr(deph[p])[0:6]+" m",fontsize=9)
			plt.figtext(0.66,0.85,"Veloc Vento: "+repr(wnds[p,t])[0:4]+" m/s",fontsize=9)
			plt.figtext(0.66,0.82,"Direc Vento: "+repr(wndd[p,t])[0:4]+" degrees",fontsize=9)
			plt.figtext(0.66,0.79,"Altura Sign de onda: "+repr(4.01*sqrt(sum(pwst[p,t,:])))[0:4]+" m",fontsize=9)
			savefig('pspec_p'+str(p+1).zfill(3)+'_'+str(t).zfill(3)+'.jpg', dpi=None, facecolor='w', edgecolor='w',
			orientation='portrait', papertype=None, format='jpg',
			transparent=False, bbox_inches=None, pad_inches=0.1)
			plt.close()
		# -------------------------------------------------------------------



		# Directional Spectra 2D Plot ---------------------------------
		if dspdecp==1:
			fig=plt.figure(figsize=(8,6))

			if dspec[p,t,:,:].max()<15.0 :
				levels=[0.1,0.5,1,2,3,4,5,6,8,10,12,15]
#				contour(freq, dire, dspec[p,t,:,:],levels, colors='0.2')
				contourf(freq, dire, dspec[p,t,:,:],levels,cmap=palette,norm=colors.normalize(vmin=0.1,vmax=15.0,clip=False), extent=[-3,3,-3,3])
			else:
				levels=linspace(0.1,dspec[p,t,:,:].max(), num=12, endpoint=True, retstep=False)
#				contour(freq, dire, dspec[p,t,:,:],levels.round(1), colors='0.2')
				contourf(freq, dire, dspec[p,t,:,:],levels.round(1),cmap=palette,norm=colors.normalize(vmin=0.1,vmax=dspec[p,t,:,:].max(),clip=False), extent=[-3,3,-3,3])

			grid()
			xlabel('Frequency (Hz)')
			ylabel('Direction (degrees)')
			title('WAVEWATCH III - Espectro Direcional / Directional Spectrum     '+repr(sdata[t])[6:8]+'/'+repr(sdata[t])[4:6]+'/'+repr(sdata[t])[0:4]+' '+repr(sdata[t])[8:10]+'Z', fontsize=11)
			ax = plt.gca()
			pos = ax.get_position()
			l, b, w, h = pos.bounds
			cax = plt.axes([l+w+0.01, b+0.01, 0.03, h-0.01]) # setup colorbar axes.
			plt.colorbar(cax=cax) # draw colorbar
			plt.axes(ax)  # make the original axes current again
			plt.figtext(0.66,0.88,"Profundidade: "+repr(deph[p])[0:6]+" m",fontsize=9)
			plt.figtext(0.66,0.85,"Veloc Vento: "+repr(wnds[p,t])[0:4]+" m/s",fontsize=9)
			plt.figtext(0.66,0.82,"Direc Vento: "+repr(wndd[p,t])[0:4]+" degrees",fontsize=9)
			plt.figtext(0.66,0.79,"Altura Sign de onda: "+repr(4.01*sqrt(sum(pwst[p,t,:])))[0:4]+" m",fontsize=9)
			savefig('dspec_p'+str(p+1).zfill(3)+'_'+str(t).zfill(3)+'.jpg', dpi=None, facecolor='w', edgecolor='w',
			orientation='portrait', papertype=None, format='jpg',
			transparent=False, bbox_inches=None, pad_inches=0.1)
			plt.close()
		# -----------------------------------------


fp.close




# Writing output text files 

# Simple text output file with directions and frequencies. 
vf=file('directions_frequencies.txt','w')
vf.write('% WAVEWATCH III results - directions (degrees) and frequencies (Hz)')
vf.write('\n')
np.savetxt(vf,dire.reshape(1,-1),fmt="%8.2f",delimiter=' ') 
np.savetxt(vf,freq.reshape(1,-1),fmt="%8.4f",delimiter=' ') 
vf.close()


# Simple text output file with deph, wind speed and wind direction for each point output 
for p in range(0,npo):

	vf=file('wind_deph_pos_'+str(p+1).zfill(3)+'.txt','w')
	vf.write('% WAVEWATCH III results - header informations .spc file')
	vf.write('\n')
	vf.write('% Position: Lat'+repr(lat[p])+' Lon'+repr(lon[p]))
	vf.write('\n')
	vf.write('% Deph: '+repr(deph[p])+' m')
	vf.write('\n')
	vf.write('%     Date     WindSpeed(m/s) WindDir(degrees)')
	vf.write('\n')
	np.savetxt(vf,zip(ano,mes,dia,hora,minu,wnds[p,:],wndd[p,:]),fmt="%4i %2i %2i %2i %2i %8.3f %8.2f",delimiter='/t') 
	vf.close()


# Power Spectra 1D output file ---------------------------------------------
if pspdecw==1:
	for p in range(0,npo):

		vf=file('pspec_p'+str(p+1).zfill(3)+'.txt','w')
		vf.write('% WAVEWATCH III - Power Spectrum')
		vf.write('\n')
		vf.write('% Position:  Lat '+repr(lat[p])[0:6]+'   Lon '+repr(lon[p])[0:6])
		vf.write('\n')
		vf.write('% Deph:  '+repr(deph[p])+' m')
		vf.write('\n')
		vf.write('% Frequencies:  ')
		vf.write('\n')
		np.savetxt(vf,freq.reshape(1,-1),fmt="%8.4f")
		vf.write('% Power Spectra (m^2/Hz) 1D with '+repr(nf)+' frequencies . Each line is one power spectrum (a vector,1D) related to its time. Take the dates at the other output files.')
		vf.write('\n')
		np.savetxt(vf,pwst[p,:,:],fmt="%8.5f") 
		vf.close()

# -------------------------------------------------------------------


# PREP PLEDS output file ---------------------------------------------
if ppoutf==1:
	for p in range(0,npo):

		vf=file('prepPLEDS_'+str(p+1).zfill(3)+'.txt','w')
		vf.write('% WAVEWATCH III PREP_PLEDS - Input for Matlab plots PLEDS-WW3 (Campos&Parente 2009)')
		vf.write('\n')
		vf.write('% Position:  Lat '+repr(lat[p])[0:6]+'   Lon '+repr(lon[p])[0:6])
		vf.write('\n')
		vf.write('% Deph:  '+repr(deph[p])+' m')
		vf.write('\n')
		vf.write('% Freq Band (s):    1) '+repr(1/freq[0])[0:5]+'-'+repr(1/freq[la])[0:5]+'        2) '+repr(1/freq[la])[0:5]+'-'+repr(1/freq[lb])[0:5]+'        3) '+repr(1/freq[lb])[0:5]+'-'+repr(1/freq[lc])[0:5]+'        4) '+repr(1/freq[lc])[0:5]+'-'+repr(1/freq[ld])[0:5]+'        5) '+repr(1/freq[ld])[0:5]+'-'+repr(1/freq[nf-1])[0:5])         
		vf.write('\n')
		vf.write('% Date(Y M D H)     En(1) Hs(1) Dp(1)    En(2) Hs(2) Dp (2)     En(3) Hs(3) Dp(3)     En(4) Hs(4) Dp(4)     En(5) Hs(5) Dp(5)')
		vf.write('\n')
		np.savetxt(vf,zip(ano,mes,dia,hora,ef[p,:,0],hs[p,:,0],dpf[p,:,0],ef[p,:,1],hs[p,:,1],dpf[p,:,1],ef[p,:,2],hs[p,:,2],dpf[p,:,2],ef[p,:,3],hs[p,:,3],dpf[p,:,3],ef[p,:,4],hs[p,:,4],dpf[p,:,4]),fmt="%4i %2i %2i %2i %12.5f %4.2f %5.1f %10.5f %4.2f %5.1f %10.5f %4.2f %5.1f %10.5f %4.2f %5.1f %10.5f %4.2f %5.1f",delimiter='/t') 
		vf.close()

# -------------------------------------------------------------------

os.system("ls prepPLEDS*txt > listaPleds.txt")
os.system("ls wind_deph_pos*.txt > listaWind.txt")

# # NetCDF output File --------------------------------
# if dspdecw==1:

# 	from pupynere import netcdf_file

# 	for i in range(0,npo):
# 		# open a new netCDF file for writing. 
# 		ncfile = netcdf_file('dspec'+str(i+1).zfill(3)+'_'+datainic+'.nc','w')
# 		# create  dimensions.
# 		# ncfile.createDimension( 'point' , dspec.shape[0] )
# 		ncfile.createDimension( 'time' , dspec.shape[1] )
# 		ncfile.createDimension( 'directions' , dspec.shape[2] )
# 		ncfile.createDimension( 'frequencies' , dspec.shape[3] )
# 		# po = ncfile.createVariable('point',dtype('float32').char,('point',))
# 		ti = ncfile.createVariable('time',dtype('float32').char,('time',))
# 		dirs = ncfile.createVariable('directions',dtype('float32').char,('directions',))
# 		fres = ncfile.createVariable('frequencies',dtype('float32').char,('frequencies',))

# 		ti.units     = 'seconds since 1970-01-01 00:00:00' 
# 		dirs.units = 'degrees'
# 		fres.units = 'hertz'
# 		# write data to coordinate vars.
# 		#po=array([1, 2])
# 		ti [:] = jday
# 		dirs[:] = dire
# 		fres[:] = freq
# 		# create  variable
# 		spec = ncfile.createVariable('dspectr',dtype('float32').char,('time','directions','frequencies'))
# 		# set the units attribute.
# 		spec.units = 'Hz.m^2.degree'
# 		# write data to variables.
# 		spec[:,:,:] = dspec[i,:,:,:]
# 		# close the file
# 		ncfile.close()

