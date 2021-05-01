# Izabel Nogueira 
# Projeto OAKMONT - Baia de Todos os Santos
# plota campos de saida o SWAN no formato tab com cabecario (TABLEout 'grid' HEADer)

from pylab import *
from mpl_toolkits.basemap import Basemap, shiftgrid, interp 
import mpl_toolkits.basemap
import matplotlib.pyplot as plt
import numpy as npy
from utmToLatLng import *

# potar batimetria: sim(1)
isbat=1

# rodada com vento: sim(1)
iswin=0


# Grade Maior
ny=250#numero de pontos em x
nx=200#numero de pontos em y
nmp=0.2#escala entre os meridianos e paralelos
name='table_coarsegrid.out'
dl=0
box=1 # plotar dominio da grade menor
latfine=[-13.120004,-13.0273,-12.6451,-12.7377,-13.1200]
lonfine=[-38.7500,-38.3993,-38.5045,-38.8548,-38.7500]

# Grade Menor
ny=250#numero de pontos em x
nx=200#numero de pontos em y
nmp=0.1#escala entre os meridianos e paralelos
name='table_finegrid.out'
dl=0.1 # descolamento da grade - para grades inclinadas
box=0

# ----------------- Plotar saida do SWAN ------------------- 
 
file=open(name,'r')
tfile=file.readlines()
np=len(tfile)-7
hs=zeros(np,'f');dm=zeros(np,'f');bat=zeros(np,'f');X=zeros(np,'f');Y=zeros(np,'f')
Xwin=zeros(np,'f');Ywin=zeros(np,'f')
file.close()
file=open(name,'r')
lixo=file.readline()
lixo=file.readline()
lixo=file.readline()
lixo=file.readline()
lixo=file.readline()
lixo=file.readline()
lixo=file.readline()
for i in range(0,np):
    line=file.readline()
    X[i]=float(line[5:14])
    Y[i]=float(line[18:28])
    hs[i]=float(line[47:53])
    dm[i]=float(line[61:70])
    bat[i]=float(line[30:43])
    Xwin[i]=float(line[116:126])
    Ywin[i]=float(line[130:140])

file.close()

adm=[i for i,x in enumerate(dm) if x <0]
dm[adm]=NaN
hs1=reshape(hs,(ny,nx))
bat1=reshape(bat,(ny,nx))
dm1=reshape(dm,(ny,nx))
dm1=(-90-dm1)%360;
xwind=reshape(Xwin,(ny,nx))
ywind=reshape(Ywin,(ny,nx))

# wave direction
dx=cos(dm1*pi/180);
dy=sin(dm1*pi/180);
dxn=20;
dyn=20;
[m,n]=shape(dx)
dir_x=zeros([m,n]);dir_y=zeros([m,n])
for i in range(1,m,dxn):
    for j in range(1,n,dyn):
        dir_x[i,j]=dx[i,j]
        dir_y[i,j]=dy[i,j]
        
      
# Latitudes e Longitudes
lat=zeros(np,'f');lon=zeros(np,'f')
for li in range(0,np):
    [lati,loni]=utmToLatLng(23,X[li],Y[li], northernHemisphere=False)
    lat[li]=lati;lon[li]=loni

if lon[0] < 0 and lon[np-1] <= 0:
	lon_0=-(abs(lon[np-1])+abs(lon[0]))/2.0
else:
	lon_0=(lon[0]+lon[np-1])/2.0


if lat[0] < 0 and lat[np-1] <= 0:
	lat_0=-(abs(lat[np-1])+abs(lat[0]))/2.0
else:
	lat_0=(lat[0]+lat[np-1])/2.0
 
fig=plt.figure(figsize=(12,12))

map = Basemap(llcrnrlat=lat[0],urcrnrlat=lat[np-1],\
	llcrnrlon=lon[0]-dl,urcrnrlon=lon[np-1]+dl,\
	resolution='h',area_thresh=0.01,projection='merc',\
	lat_0=lat_0,lon_0=lon_0)

mnlon=reshape(lon,(ny,nx))
mnlat=reshape(lat,(ny,nx))
xx, yy = map(mnlon,mnlat)

# levels
levels=[0,0.25,0.5,0.75,1,1.5,2,2.5,3,3.5,4]

# esperar uma regiao com contorno melhor
map.drawcoastlines(linewidth=1.2)
map.drawcountries()
map.drawstates()
map.drawmapboundary()
map.contourf(xx,yy,hs1[:,:],levels)
map.quiver(xx[1:ny:20,1:nx:20],yy[1:ny:20,1:nx:20],dir_x[1:ny:20,1:nx:20],dir_y[1:ny:20,1:nx:20],scale=15)
map.drawmeridians(arange(lon.min(),lon.max(),nmp),labels=[0,0,0,1],fmt="%2.2f")
map.drawparallels(arange(lat.min(),lat.max(),nmp),labels=[1,0,0,0],fmt="%2.2f")
map.fillcontinents(color='grey')
plt.grid(True)
if box==1:
    xr,yr = map(lonfine,latfine)
    map.plot(xr,yr,'ro-',mec='r',mfc='w',lw=4,mew=3,ms=10)
    title('SWAN Wave Simulation - Coarse Grid',size=18)
else:
    title('SWAN Wave Simulation',size=18)
    
# ponto ww3
lonww3=-44.42;latww3=-23.28;
xw,yw = map(lonww3,latww3)
map.plot(xw,yw,'rs',mec='r',mfc='w',mew=4,ms=10)  
text(xw-3000,yw-2500,'WW3',fontsize=16,weight='bold',color='r')

# ponto DadoAngra
lonww3=-44.46;latww3=-23.02;
xw,yw = map(lonww3,latww3)
map.plot(xw,yw,'rs',mec='r',mfc='w',mew=4,ms=10)  
text(xw-3000,yw-2000,'Dado',fontsize=16,weight='bold',color='r')

cb=plt.colorbar(orientation='vertical',shrink=0.7)
cb.set_label('Significant Wave Height (m)',size=18)
plt.show()


if isbat==1:
    fig2=plt.figure(figsize=(12,12))
    if box==1:
        levels=[0,25,50,75,100,125,200,500,1000,2000,3000]
    else:
        levels=[0,10,20,30,40,50,60,70,80,90,100]
    map.drawcoastlines(linewidth=1.2)
    map.drawcountries()
    map.drawstates()
    map.drawmapboundary()
    map.contourf(xx,yy,bat1[:,:],levels)
    map.drawmeridians(arange(lon.min(),lon.max(),nmp),labels=[0,0,0,1],fmt="%2.2f")
    map.drawparallels(arange(lat.min(),lat.max(),nmp),labels=[1,0,0,0],fmt="%2.2f")
    map.fillcontinents(color='grey')
    plt.grid(True)
    if box==1:
        xr,yr = map(lonfine,latfine)
        map.plot(xr,yr,'ro-',mec='r',mfc='w',lw=4,mew=3,ms=10)
        title('SWAN Wave Simulation - Coarse Grid',size=18)
    else:
        title('SWAN Wave Simulation',size=18)
        
    # ponto ww3
    lonww3=-44.42;latww3=-23.28;
    xw,yw = map(lonww3,latww3)
    map.plot(xw,yw,'rs',mec='r',mfc='w',mew=4,ms=10)  
    text(xw-3000,yw-2500,'WW3',fontsize=16,weight='bold',color='r')
    # ponto DadoAngra
    lonww3=-44.46;latww3=-23.02;
    xw,yw = map(lonww3,latww3)
    map.plot(xw,yw,'rs',mec='r',mfc='w',mew=4,ms=10)  
    text(xw-3000,yw-2000,'Dado',fontsize=16,weight='bold',color='r')
    
    cb=plt.colorbar(orientation='vertical',shrink=0.7)
    cb.set_label('Depth (m)',size=18)
    plt.show()
    
if iswin==1:
    fig3=plt.figure(figsize=(12,12))
    levels=[0,0.25,0.5,0.75,1,1.5,2,2.5,3,3.5,4]
    map.drawcoastlines(linewidth=1.2)
    map.drawcountries()
    map.drawstates()
    map.drawmapboundary()
    map.contourf(xx,yy,hs1[:,:],levels)
    map.quiver(xx[1:ny:20,1:nx:20],yy[1:ny:20,1:nx:20],dir_x[1:ny:20,1:nx:20],dir_y[1:ny:20,1:nx:20],scale=15)
    map.quiver(xx[1:ny:10,1:nx:10],yy[1:ny:10,1:nx:10],xwind[1:ny:10,1:nx:10],ywind[1:ny:10,1:nx:10],scale=100,color='w')
    map.drawmeridians(arange(lon.min(),lon.max(),nmp),labels=[0,0,0,1],fmt="%2.2f")
    map.drawparallels(arange(lat.min(),lat.max(),nmp),labels=[1,0,0,0],fmt="%2.2f")
    map.fillcontinents(color='grey')
    plt.grid(True)
    if box==1:
        xr,yr = map(lonfine,latfine)
        map.plot(xr,yr,'ro-',mec='r',mfc='w',lw=4,mew=3,ms=10)
        title('SWAN Wave Simulation - Coarse Grid',size=18)
    else:
        title('SWAN Wave Simulation',size=18)
        
    # ponto ww3
    lonww3=-44.42;latww3=-23.28;
    xw,yw = map(lonww3,latww3)
    map.plot(xw,yw,'rs',mec='r',mfc='w',mew=4,ms=10)  
    text(xw-4000,yw-3500,'WW3',fontsize=16,weight='bold',color='r')
    
    cb=plt.colorbar(orientation='vertical',shrink=0.7)
    cb.set_label('Significant Wave Height (m)',size=18)
    plt.show()
