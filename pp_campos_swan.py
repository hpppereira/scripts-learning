'''
Plotagem dos campos de onda
das simulacoes do SWAN - Porto de Tubarao'''


from pylab import *
from mpl_toolkits.basemap import Basemap, shiftgrid, interp 
import mpl_toolkits.basemap
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import numpy as np
import os

# --------------------------------------------------------------------
#                        informacoes das grades
# --------------------------------------------------------------------
plt.close('all')

#diretorio dos resultados
pathname = os.environ['HOME'] + '/Dropbox/SWAN/NEST_VIX/'
#pathname = os.environ['HOME'] + '/Dropbox/SWAN/NEST_BES/'

#data da simulacao
start=datetime.datetime(2015,02,18,00,00)



# Grade Menor
ny=95#numero de pontos em x
nx=115#numero de pontos em y

#grade Maior
ny=45#numero de pontos em x
nx=60#numero de pontos em y

name='table_grid20150218.out'
dl=0
box=1 # plotar dominio da grade menor

# potar batimetria: sim(1)
isbat=1

#grade menor: sim (1)
grdmenor=0

# ----------------------- linha de costa -----------------------

pathnamel = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/dados/linhadecosta/polig/'

pols = os.listdir(pathnamel)

#??
numpoly, numverts = 100, 6

verts = []
for p in pols:

    #carrega cada latlon
    dd = np.loadtxt(pathnamel + p)

    verts.append(zip(dd[:,0],dd[:,1]))


z = np.random.random(numpoly) * 500
z = np.ones(100) *3

# ----------------- Plotar saida do SWAN ------------------- 
 
file=open(pathname + name,'r')
tfile=file.readlines()
npp=len(tfile)-7
nt=npp/(nx*ny)#numero de tempos
np=nx*ny
file.close()

hs=zeros(np,'f');dm=zeros(np,'f');tp=zeros(np,'f');bat=zeros(np,'f');X=zeros(np,'f');Y=zeros(np,'f')
Xwin=zeros(np,'f');Ywin=zeros(np,'f');Hsswell=zeros(np,'f')
file=open(pathname + name,'r')
lixo=file.readline()
lixo=file.readline()
lixo=file.readline()
lixo=file.readline()
lixo=file.readline()
lixo=file.readline()
lixo=file.readline()

# ---------------- cria data com datetime -----------------------
#datas
datat = [start + datetime.timedelta(hours=i) for i in xrange(0,nt)]

for t in range(0,nt):
    ti=1
    np1=0
    for i in range(np1,np*ti):
        line=file.readline()
        X[i]=float(line[5:14])
        Y[i]=float(line[18:28])
        hs[i]=float(line[47:53]) # Hs
        dm[i]=float(line[61:70])  # direcao de pico
        tp[i]=float(line[70:80]) #periodo de pico
        bat[i]=float(line[30:43])
        Xwin[i]=float(line[116:126])
        Ywin[i]=float(line[130:140])
        Hsswell[i]=float(line[117:128])
    
    np1=np*ti
    ti=ti+1
    adm=[i for i,x in enumerate(dm) if x <0]
    dm[adm]=NaN
    hs1=reshape(hs,(ny,nx))
    tp1=reshape(tp,(ny,nx))
    bat1=reshape(bat,(ny,nx))
    dm1=reshape(dm,(ny,nx))
    dm1=(-90-dm1)%360;
    xwind=reshape(Xwin,(ny,nx))
    ywind=reshape(Ywin,(ny,nx))
    Hsswell1=reshape(Hsswell,(ny,nx))

    # wave direction
    dx=cos(dm1*pi/180);
    dy=sin(dm1*pi/180);
    if grdmenor==1:
        dxn=10;
        dyn=10;
        quiversca=25
        quirverwi=0.003
        lonini=-40.35
        lonfi=-40.2
        latini=-20.36
        latfi=-20.25
    else:
        dxn=5;
        dyn=5;
        quiversca=25
        quirverwi=0.003
        lonini=-40.6
        lonfi=-39.8
        latini=-20.75
        latfi=-20


    [m,n]=shape(dx)
    dir_x=zeros([m,n]);dir_y=zeros([m,n])
    for i in range(1,m,dxn):
        for j in range(1,n,dyn):
            dir_x[i,j]=dx[i,j]
            dir_y[i,j]=dy[i,j]
            
          
    xx=reshape(X,(ny,nx))
    yy=reshape(Y,(ny,nx))
    

    # levels
    levels=[0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2]
    levelsswell=[0,.05,.1,.15,.2,.25,.3,.35,.4,.45,.5]
    levelstp=[0,2,4,6,8,10,12,14,16,18,20]
    # levels das grades do WW3
    #levels=[0,0.5,1,1.5,2,3,4,5,6,7,8,9,10,11,12]

    fig, ax = plt.subplots()
    cs=plt.contourf(xx[:,:],yy[:,:],hs1[:,:],levels)
    plt.quiver(xx[1:ny:dyn,1:nx:dxn],yy[1:ny:dyn,1:nx:dxn],dir_x[1:ny:dyn,1:nx:dxn],dir_y[1:ny:dyn,1:nx:dxn],scale=quiversca,width=quirverwi)

    cb=plt.colorbar(cs)
    cb.set_label('Significant Wave Height (m)',size=13)
    # Make the collection and add it to the plot.
    coll = PolyCollection(verts, edgecolors='black',facecolor='gray',closed=False)
    ax.add_collection(coll)
    ax.autoscale_view()
    axis([lonini, lonfi, latini, latfi])
    title(' SWAN Altura Significativa (m) e Direcao / Significant Wave Height and Direction  '+datetime.datetime.strftime(datat[t],"%d/%m/%Y %H")+'Z', fontsize=7)

    savefig(pathname + 'hs_dp'+datetime.datetime.strftime(datat[t],"%d%m%Y%H")+'.jpg', dpi=None, facecolor='w', edgecolor='w',
    orientation='portrait', papertype=None, format='jpg',
    transparent=False, bbox_inches=None, pad_inches=0.1)
    plt.close()
 #   TP
    fig, ax = plt.subplots()
    cs=plt.contourf(xx[:,:],yy[:,:],tp1[:,:],levelstp)
    plt.quiver(xx[1:ny:dyn,1:nx:dxn],yy[1:ny:dyn,1:nx:dxn],dir_x[1:ny:dyn,1:nx:dxn],dir_y[1:ny:dyn,1:nx:dxn],scale=quiversca,width=quirverwi)

    cb=plt.colorbar(cs)
    cb.set_label('Peak Period (s)',size=13)
    # Make the collection and add it to the plot.
    coll = PolyCollection(verts, edgecolors='black',facecolor='gray',closed=False)
    ax.add_collection(coll)
    ax.autoscale_view()
    axis([lonini, lonfi, latini, latfi])
    title(' SWAN Periodo de Pico (s) e Direcao / Peak Period and Direction  '+datetime.datetime.strftime(datat[t],"%d/%m/%Y %H")+'Z', fontsize=7)

    savefig(pathname + 'tp_dp'+datetime.datetime.strftime(datat[t],"%d%m%Y%H")+'.jpg', dpi=None, facecolor='w', edgecolor='w',
    orientation='portrait', papertype=None, format='jpg',
    transparent=False, bbox_inches=None, pad_inches=0.1)
    plt.close()

    # Hs Swell

    fig, ax = plt.subplots()
    cs=plt.contourf(xx[:,:],yy[:,:],Hsswell1[:,:],levelsswell)
    plt.quiver(xx[1:ny:dyn,1:nx:dxn],yy[1:ny:dyn,1:nx:dxn],dir_x[1:ny:dyn,1:nx:dxn],dir_y[1:ny:dyn,1:nx:dxn],scale=quiversca,width=quirverwi)

    cb=plt.colorbar(cs)
    cb.set_label('Hs Swell (m)',size=13)
    # Make the collection and add it to the plot.
    coll = PolyCollection(verts, edgecolors='black',facecolor='gray',closed=False)
    ax.add_collection(coll)
    ax.autoscale_view()
    axis([lonini, lonfi, latini, latfi])
    title(' SWAN Hs Swell (m) e Direcao de pico / Hs Swell and Peak Direction  '+datetime.datetime.strftime(datat[t],"%d/%m/%Y %H")+'Z', fontsize=7)

    savefig(pathname + 'hsswell_dp'+datetime.datetime.strftime(datat[t],"%d%m%Y%H")+'.jpg', dpi=None, facecolor='w', edgecolor='w',
    orientation='portrait', papertype=None, format='jpg',
    transparent=False, bbox_inches=None, pad_inches=0.1)
    plt.close()

    if isbat==1:
        fig, ax = plt.subplots()
        levels=[0,10,20,30,40,50,60,70,80,90,100]

        cs=contourf(xx,yy,bat1[:,:],levels)
        # Make the collection and add it to the plot.
        coll = PolyCollection(verts, edgecolors='black',facecolor='gray',closed=False)
        ax.add_collection(coll)
        ax.autoscale_view()
        cb=plt.colorbar(cs)
        cb.set_label('Depth (m)',size=18)
        axis([lonini, lonfi, latini, latfi])
        savefig(pathname + 'bat.jpg', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format='jpg',
        transparent=False, bbox_inches=None, pad_inches=0.1)
        plt.close()

