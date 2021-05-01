'''
Extrai pontos do grid do SWAN - Porto de Tubarao'''


from pylab import *
import matplotlib.pyplot as plt
import numpy as npy
import os


# --------------------------------------------------------------------
#                        informacoes das grades
# --------------------------------------------------------------------
plt.close('all')

#diretorio dos resultados  
pathname = os.environ['HOME'] + '/Dropbox/SWAN//old/grid_point/'

# Grade Menor
ny=95#numero de pontos em x
nx=115#numero de pontos em y

name='table_grid.out'

start=datetime.datetime(2013,02,01,00,00) ######### mudar data
# escolher o ponto de interesse (ADCP02)
lonint=-40.24200058
latint=-20.29789925

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
hsp=zeros((nt,1))
tpp=zeros((nt,1))
dmp=zeros((nt,1))

for t in range(0,nt):
    ti=1
    np1=0
    for i in range(np1,np*ti):
        line=file.readline()
        X[i]=float(line[5:14])-360
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
    xwind=reshape(Xwin,(ny,nx))
    ywind=reshape(Ywin,(ny,nx))
    Hsswell1=reshape(Hsswell,(ny,nx))

    # wave direction
    dx=cos(dm1*pi/180);
    dy=sin(dm1*pi/180);

    [m,n]=shape(dx)
    dir_x=zeros([m,n]);dir_y=zeros([m,n])
    for i in range(1,m,1):
        for j in range(1,n,1):
            dir_x[i,j]=dx[i,j]
            dir_y[i,j]=dy[i,j]
            
          
    xx=reshape(X,(ny,nx))
    yy=reshape(Y,(ny,nx))
    
    print str(t)

    n=where((xx==lonint) & (yy==latint))
    hsp[t]=hs1[n][0]
    tpp[t]=tp1[n][0]
    dmp[t]=dm1[n][0]
    


datas=npy.array([datat[i].strftime('%Y%m%d%H') for i in range(len(datat))])
datai=npy.array([datas.astype(int)])
dat=npy.concatenate((datai.T,hsp,tpp,dmp),axis=1)


npy.savetxt('ADCP02.txt',dat,fmt='%i %.2f %.2f %.2f',delimiter='/t',header='Valores de Tempo Hs(m) Tp(s) Dp(graus)')





