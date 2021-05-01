# Vento GFS NCEP/NOAA. Abertura, concatenacao, gera arquivo para o ww3 e plota as figuras 
#  PLICAVEL AOS VENTO 0.25

# Nome: gfs.t00z.pgrb2.0p25.f000.grib2 
# Programa para processamento dos arquivos de vento mod GFS em grib2 operacional do ncep
# Vento GFS NCEP/NOAA. Abertura, concatenacao, gera arquivo para o ww3 e plota as figuras 
# Gera as figuras em png. Arquivo .txt pro wavewatch (ventoGFS.txt). Arquivo netcdf final concatenado (recorte_ww3_GFS_20110928.nc)
# E possivel checar todos os passos do programa no arquivo log_GFS_pythonOP.txt
#
# Ricardo Martins Campos 03/05/2012
# Izabel Nogueira
# LIOC-PENO-COPPE-UFRJ
# Motor-de-popa

nt=57  # numero de tempos, arquivos de entrada para gerar o arquivo e figuras. nt tempos de previsao

import matplotlib
matplotlib.use('Agg')

import os
import netCDF4 as nc
from numpy import *
from pylab import *
from matplotlib import dates
import datetime
from datetime import timedelta, datetime
import numpy as np

from mpl_toolkits.basemap import Basemap, shiftgrid, interp
import mpl_toolkits.basemap
import matplotlib.pyplot as plt

from time import strptime
from calendar import timegm

# Paleta de cores para a plotagem
from mpl_toolkits.basemap import cm
colormap = cm.GMT_polar
#palette = plt.cm.OrRd
palette = plt.cm.jet
palette.set_bad('aqua', 10.0)
import matplotlib.colors as colors


# comando shell remover os gribs 
os.system("rm *.grib2")
# Criando o arquivo descritor da operacao
fl = open('log_GFS_pythonOP.txt', 'w')
fl.write('=========== Status GFS ===========\n')
datenow=datetime.now()  # data e hora de agora
fl.write('Comecando em (hora local) '+repr(datenow.year)+'-'+repr(datenow.month)+'-'+repr(datenow.day)+'  '+repr(datenow.hour)+'H '+repr(datenow.minute)+'M '+repr(datenow.second)+'S \n')

# lista todos os arquivos de previsao .nc do gfs
# Ajustei para o shell get_gfs_wind10m.sh fazer isso ao converter de grib2 pra netcdf (11/05/2012)
f = open('listaGFS.txt')
fl.write('Montou a listaGFS.txt \n')

# Arquivo com os nomes dos arquivos netcdfs
line = f.readline() 
line=line[0:-1]  # nome do arquivo .nc

jday = []
fu = nc.Dataset(line, 'r')  # abre o .nc
uwnd=fu.variables['UGRD_10maboveground'][0,20:701,:]  # le o vento ja selecionando parte da grade  So para alocar as matrizes
U=zeros((nt,uwnd.shape[0],uwnd.shape[1]))     # U final que ira conter todos os ventos uwnd para o .nc final concatenado
V=zeros((nt,uwnd.shape[0],uwnd.shape[1]))     # V final que ira conter todos os ventos vwnd para o .nc final concatenado

nuwnd=zeros((uwnd.shape[0],uwnd.shape[1]))
nvwnd=zeros((uwnd.shape[0],uwnd.shape[1]))

lat=fu.variables['latitude'][20:701]      # latitudes da grade selecionada
latas=lat[40:381]  # latitude grade Atlantico sul 
if latas[0] < 0 and latas[-1] <= 0:
	lat_0=-(abs(latas[-1])+abs(latas[0]))/2.0
else:
	lat_0=(latas[0]+latas[-1])/2.0
lon_0=-25.0

lon=fu.variables['longitude'][:]     # longitudes da grade selecionada

fl.write('Leu as latitudes e longitudes. Alocou as matrizes U e V \n')

f = open('listaGFS.txt')    # leitura de todos os .nc que estao no diretorio
vf=file('windGFS025.txt','w')  # abertura do arquivo texto final para o ww3

levels=[4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40]
levelsas=[4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34]
sk=7;skas=3;  # skip do vento, na plotagem com Quiver

fd = open('date')
cont=0

fl.write('Abriu as listas e o arquivo ventoGFS.txt para o ww3. Inicio do Loop de plotagem/escrita \n')

for i in range(1, nt+1):

	line = f.readline();fl.write('\n'+line) 
	line=line[0:-1];
	nomefig=line[0:-3]  # arruma o nome da figura
	
        nomed=fd.readline()
	nomed=nomed[0:-1]
        data=nomed[0:-2];hora=nomed[8:10]; # pega a data e hora pelo arquivo data.
        jday.append((timegm( strptime(data+hora, '%Y%m%d%H') ) - timegm( strptime('01/01/1950', '%d/%M/%Y') )) / 3600. / 24.)
	fl.write('Acertou o nome da figura. Pegou a data e hora pelo nome do arquivo aberto \n')
	fu = nc.Dataset(line, 'r')
        uwnd=fu.variables['UGRD_10maboveground'][0,20:701,:]   # le a variavel U ja selecionando a grade desejada
        vwnd=fu.variables['VGRD_10maboveground'][0,20:701,:]   # le a variavel V ja selecionando a grade desejada
 
     
	fl.write('Leu as variaveis UGRD_10maboveground'+repr(uwnd.shape)+' e VGRD_10maboveground'+repr(uwnd.shape)+' \n')
	magn=sqrt((uwnd*uwnd)+(vwnd*vwnd))    # Intensidade do vento, a ser plotada de fundo nas figuras
	fl.write('Concatenou em U e V. Calculou a intensidade. \n')

	lon=fu.variables['longitude'][:]	
	magn,lon = shiftgrid(180.,magn,lon,start=False)
	lon=fu.variables['longitude'][:]
	uwnd,lon = shiftgrid(180.,uwnd,lon,start=False)
	lon=fu.variables['longitude'][:]
	vwnd,lon = shiftgrid(180.,vwnd,lon,start=False)

        U[i-1,:,:]=uwnd[:,:]    # concatenacao de U
        V[i-1,:,:]=vwnd[:,:]    # concatenacao de V

	vf.write(data);vf.write('  ');vf.write(hora);vf.write('0000');  # escreve a data no formato do ww3
	vf.write('\n')
	np.savetxt(vf,uwnd,fmt="%10.5f",delimiter='')   # escreve U no formato do ww3
	np.savetxt(vf,vwnd,fmt="%10.5f",delimiter='')   # escreve V no formato do ww3
	fl.write('Escreveu a data, U e V no formato do ww3. \n')


# #	Gerando as figuras Global com basemap
# #	magn, lon = shiftgrid(180, magn, lon, start=False)
#         fig=plt.figure(figsize=(8,5))	
# 	map = Basemap(projection='eck4',lon_0 = 0, resolution = 'l')
# 	[mnlon,mnlat]=np.meshgrid(lon[:],lat[:])
# 	xx, yy = map(mnlon,mnlat)
# #	plt.text(0.05, 0.05, "Ricardo Campos  Lioc-COPPE/UFRJ", ha="center",fontsize=6)
# #	if magn.max()<30.0 :
# #		levels=[2,4,6,8,10,12,14,16,18,20,25,30]
# #		map.contourf(xx,yy,magn,levels,cmap=palette,norm=colors.normalize(vmin=5.0,vmax=30,clip=False))
# #	else:
# #		levels=linspace(2,magn.max(), num=13, endpoint=True, retstep=False)
# #		map.contourf(xx,yy,magn,levels.round(),cmap=palette,norm=colors.normalize(vmin=5.0,vmax=magn.max(),clip=False))
# #		#map.contourf(xx,yy,m[k,:,:],levels.round(1),cmap=palette,norm=colors.normalize(vmin=0,vmax=m[k,:,:].max(),clip=False))
# #
# 	map.contourf(xx,yy,magn,levels,cmap=palette,extend="max")
# 	map.drawmeridians(np.arange(round(lon.min()),round(lon.max()),40),labels=[0,0,0,1],linewidth=0.3,fontsize=6)
# 	map.drawparallels(np.arange(round(lat.min()),round(lat.max()),20),labels=[1,0,0,0],linewidth=0.3,fontsize=6)
# 	map.drawcoastlines(linewidth=0.8)
# 	map.drawcountries(linewidth=0.5)
# 	map.drawstates(linewidth=0.1)
# 	map.fillcontinents(color='gray')
# 	ax = plt.gca()
# 	pos = ax.get_position()
# 	l, b, w, h = pos.bounds
# 	cax = plt.axes([l+0.07, b+0.01, w-0.15, 0.025]) # setup colorbar axes.
# 	plt.colorbar(cax=cax, orientation='horizontal') # draw colorbar
# 	plt.axes(ax)  # make the original axes current again
# 	# plotagem dos vetores em cima do campo de intensidade do vento
# 	[mnlon,mnlat]=np.meshgrid(lon[::sk],lat[::sk])
# 	xx, yy = map(mnlon,mnlat)
# 	Q = map.quiver(xx,yy,uwnd[::sk,::sk],vwnd[::sk,::sk],width=0.001,scale=1000)
# 	title('GFS.NCEP Vento em Superficie / Surface Wind (m/s)  '+data[6:8]+'/'+data[4:6]+'/'+data[0:4]+' '+hora+'Z', fontsize=11)
#         savefig('GlobalGFS_'+str(((i-1)*3)).zfill(3)+'.jpg', dpi=None, facecolor='w', edgecolor='w',
#         orientation='portrait', papertype=None, format='jpg',
#         transparent=False, bbox_inches=None, pad_inches=0.1)
#         plt.close()
 	fl.write('Gerou a figura Global \n')


# 	# Gerando figura pro Altantico Sul 
#         fig=plt.figure(figsize=(7,6))
# 	lonas=lon[220:401] 
# 	map = Basemap(llcrnrlat=latas[0],urcrnrlat=latas[-1],\
# 	llcrnrlon=lonas[0],urcrnrlon=lonas[-1],\
# 	rsphere=(6378137.00,6356752.3142),\
# 	resolution='l',area_thresh=1000.,projection='cyl',\
# 	lat_1=latas[0],lon_1=lonas[0],lat_0=lat_0,lon_0=lon_0)
# 	[mnlonas,mnlatas]=np.meshgrid(lonas[:],latas[:])
# 	xxas, yyas = map(mnlonas,mnlatas)
# 	map.drawcoastlines(linewidth=0.8)
# 	map.drawcountries()
# 	map.drawstates()
# 	map.fillcontinents(color='gray')
# 	map.drawmeridians(np.arange(round(lonas.min()),round(lonas.max()),20),labels=[0,0,0,1])
# 	map.drawparallels(np.arange(round(latas.min()),round(latas.max()),10),labels=[1,0,0,0])

# #	latc=[-23.94,-22.9,-21.75]
# #	lonc=[-46.34 ,-43.233,-41.2]
# #	xc,yc = map(lonc,latc)
# #	map.plot(xc,yc,'r.')

# 	map.contourf(xxas,yyas,magn[20:191,220:401],levelsas,cmap=palette,extend="max")
# 	ax = plt.gca()
# 	pos = ax.get_position()
# 	l, b, w, h = pos.bounds
# 	cax = plt.axes([l+0.07, b-0.06, w-0.15, 0.025]) # setup colorbar axes.
# 	plt.colorbar(cax=cax, orientation='horizontal') # draw colorbar
# 	plt.axes(ax)  # make the original axes current again
# 	[mnlonas,mnlatas]=np.meshgrid(lonas[::skas],latas[::skas])
# 	xxas, yyas = map(mnlonas,mnlatas)
# 	Q = map.quiver(xxas,yyas,uwnd[20:191:skas,220:401:skas],vwnd[20:191:skas,220:401:skas],width=0.0015,scale=800)
# 	title('GFS.NCEP MOD Vento em Superficie / Surface Wind (m/s)  '+data[6:8]+'/'+data[4:6]+'/'+data[0:4]+' '+hora+'Z', fontsize=11)
#         savefig('AtlSulGFS_'+str(((i-1)*3)).zfill(3)+'.jpg', dpi=None, facecolor='w', edgecolor='w',
#         orientation='portrait', papertype=None, format='jpg',
#         transparent=False, bbox_inches=None, pad_inches=0.1)
#         plt.close()

	fl.write('Gerou a figura Atlantico Sul \n')


	cont=cont+3

vf.close
fu.close
fd.close
f.close

fl.write('\nTerminou o loop principal \n')
 # Escrever arquivo log com o status de cada etapa de rodada do programa

# from pupynere import netcdf_file
# from numpy import array


# #from Scientific.IO.NetCDF import NetCDFFile as Dataset
# from numpy import arange, dtype 

# fd = open('date')
# datainic=fd.readline()
# datainic=datainic[0:-3]
# fd.close


# # open a new netCDF file for writing.
# ncfile = netcdf_file('WindWW3_GFS_'+datainic+'.nc','w')

# # create the lat and lon dimensions.
# ncfile.createDimension( 'time' , U.shape[0] )
# ncfile.createDimension( 'latitude' , U.shape[1] )
# ncfile.createDimension( 'longitude' , U.shape[2] )
# # Define the coordinate variables. They will hold the coordinate
# # information, that is, the latitudes and longitudes.
# ti = ncfile.createVariable('time',dtype('float32').char,('time',))
# lats = ncfile.createVariable('latitude',dtype('float32').char,('latitude',))
# lons = ncfile.createVariable('longitude',dtype('float32').char,('longitude',))
# # Assign units attributes to coordinate var data. This attaches a
# # text attribute to each of the coordinate variables, containing the
# # units.
# ti.units     = 'days since 1950-01-01 00:00:00' 
# lats.units = 'degrees_north'
# lons.units = 'degrees_east'
# # write data to coordinate vars.
# ti [:] = jday
# lats[:] = lat
# lons[:] = lon
# # create  variable
# u10m = ncfile.createVariable('u10',dtype('float32').char,('time','latitude','longitude'))
# v10m = ncfile.createVariable('v10',dtype('float32').char,('time','latitude','longitude'))
# # set the units attribute.
# u10m.units = 'm/s'
# v10m.units = 'm/s'
# # write data to variables.
# u10m[:,:,:] = U[:,:,:]
# v10m[:,:,:] = V[:,:,:]
# # close the file
# ncfile.close()

# fl.write('Escreveu U e V concatenados em recorte_ww3_GFS \n')

# # Checa se escreveu todas as linhas do arquivo do ww3 corretamente
# os.system("wc -l windGFS.txt > checa.txt")
# fc=file('checa.txt','r')
# line = fc.readline()
# fc.close()
# nl=int(line[0:-14])+1;
# fl.write('Numero de linhas do arquivo escrito final: '+repr(nl)+' \n')
# fl.write('Numero de linhas total do arquivo concatenado U: '+repr(U.shape[0]*U.shape[1])+' \n')
# fl.write('Numero de linhas total do arquivo concatenado V: '+repr(V.shape[0]*V.shape[1])+' \n')

# if U.shape[0]*(1+U.shape[1]*2)==nl and V.shape[0]*(1+V.shape[1]*2)==nl:
# 	fl.write('Escreveu todas as linhas do arquivo ww3 corretamente! \n')
# else:
# 	fl.write('PROBLEMAS NA ESCRITA DO ARQUIVO WW3! \n')



datenow=datetime.now()  # data e hora de agora
fl.write('Termino em (hora local) '+repr(datenow.year)+'-'+repr(datenow.month)+'-'+repr(datenow.day)+'  '+repr(datenow.hour)+'H '+repr(datenow.minute)+'M '+repr(datenow.second)+'S \n')

fl.close()
#os.system("rm -f gfs*.nc")
os.system("rm -f gfs*.grib2")
# os.system("rm -f checa.txt")
os.system("rm -f listaGFS.txt")
os.system("rm -f date")


