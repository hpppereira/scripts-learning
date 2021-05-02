import netCDF4 as nc
import datetime
# Python Libraries 
import matplotlib
matplotlib.use('Agg')

# Pay attention to the pre-requisites and libraries
from pylab import *
import pylab as plt
import numpy as np

fu=nc.Dataset('ww310d_2014110112_avg_ATLASUL_spec.nc','r')
var=fu.variables.keys()
time=fu.variables['time']

start = datetime.datetime(2014,11,01,12)
data=np.array([start + datetime.timedelta(hours=i) for i in xrange(len(time))])


for i in range (4,len(var)): #lon,lat,levels,time,loc...
	name=var[i]
	loc=fu.variables[name]
	spc1d=np.zeros((loc.shape[0],loc.shape[2]),'f')
	# dimensao das variaveis
	#float32 loc223(time, levels, latitude, longitude)
	#(265, 6, 25, 36)
	for t in range(0,loc.shape[0]):

		levels=[0.1,0.5,1,2,3,4,5,6,8,10,12,15]
		# espectro 2D
		fig=plt.figure(figsize=(8,6))
		contourf(loc[t,0,:,:],levels)
		grid()
		xlabel('Frequency (Hz)')
		ylabel('Direction (degrees)')
		title('WAVEWATCH III - Espectro Direcional / Directional Spectrum  '+repr(data[t].strftime("%d-%m-%Y-%H"))+'Z', fontsize=11)
		ax = plt.gca()
		pos = ax.get_position()
		l, b, w, h = pos.bounds
		cax = plt.axes([l+w+0.01, b+0.01, 0.03, h-0.01]) # setup colorbar axes.
		plt.colorbar(cax=cax) # draw colorbar
		plt.axes(ax)  # make the original axes current again
		savefig('spec_2D'+repr(data[t].strftime("%d%m%Y%H"))+repr(var[i])+'.jpg', dpi=None, facecolor='w', edgecolor='w',
		orientation='portrait', papertype=None, format='jpg',
		transparent=False, bbox_inches=None, pad_inches=0.1)
		plt.close()

		# espectro 1D
		for il in range(0,loc.shape[2]):
			spc1d[t,il]=sum(loc[t,0,:,il])

		fig=plt.figure(figsize=(8,6))
		plot(spc1d[t,:])
		grid()
		xlabel('Frequency (Hz)')
		ylabel('Power Spectrum (m^2/Hz)')         
		title('WAVEWATCH III - Espectro de Energia / Power Spectrum  '+repr(data[t].strftime("%d-%m-%Y-%H"))+'Z', fontsize=11)		
		savefig('spec_1D'+repr(data[t].strftime("%d%m%Y%H"))+repr(var[i])+'.jpg', dpi=None, facecolor='w', edgecolor='w',
		orientation='portrait', papertype=None, format='jpg',
		ransparent=False, bbox_inches=None, pad_inches=0.1)
		plt.close()









# from pupynere import NetCDFFile as nc
# fu=nc('ww310d_2014110112_avg_ATLASUL_spec.nc','r')