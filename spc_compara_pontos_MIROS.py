import netCDF4 as nc
import datetime
import os
# Python Libraries 
import matplotlib
matplotlib.use('Agg')

# Pay attention to the pre-requisites and libraries
from pylab import *
import pylab as plt
import numpy as np
from subprocess import call

# Para fazer as comparacoes: Rodo esse programa ano diretorio da data e depois rodo o programa dos dados do argos no diretotio:
# /home/lioc/Dropbox/lioc/ww3br/Geral/rot
# run pp_argos1_izabel2.py


# ---------------------------------------------------
#               abrir arquivo WW3LIOc 
# -------------------------------------------------
pathnamem = os.environ['HOME'] + '/Projetos/WW3BR/CLIMATEMPO/COMPARACOES/20141104/P40/'  #====================================
pathnamed=os.environ['HOME'] + '/Projetos/Dropbox/lioc/ww3br/Geral/rot/saida/ww3/'

fl=nc.Dataset(pathnamem + 'dspec032_2014110400.nc','r') #(169, 24, 25) Time, dir, freq #================================
spc2d_Lioc=fl.variables['dspectr']
spc1d_Lioc=np.zeros((spc2d_Lioc.shape[0],spc2d_Lioc.shape[2]),'f')
freq=fl.variables['frequencies']
dire=fl.variables['directions']

# definir eixo de tempo com base na previsao do lioc 7 dias
start = datetime.datetime(2014,11,04,00)                                                   #==============================
data=np.array([start + datetime.timedelta(hours=i) for i in xrange(spc2d_Lioc.shape[0])])
datastr=np.array([datetime.datetime.strftime(data[i],'%Y%m%d%H') for i in xrange(spc2d_Lioc.shape[0])])
datastr=datastr.astype(int)
# # ---------------------------------------------------
# #               abrir arquivo ClimaTempo - loc028  6  t,z,y,x  P-40
# # -------------------------------------------------
fu=nc.Dataset('ww310d_2014110400_avg_ATLASUL_spec.nc','r')                                # ======================================
spc2d_Cli=fu.variables['loc028']
spc1d_Cli=np.zeros((spc2d_Lioc.shape[0],spc2d_Cli.shape[2]),'f') # o tempo e 7 dias
direc1=fu.variables['longitude']
direc=np.zeros([direc1.shape[0]],'f')
direc[0:28]=direc1[0:28]
direc[28::]=(direc1[28::]-360)

# # ---------------------------------------------------
# #               abrir arquivo MIROS P40
# # -------------------------------------------------
MIROS=np.loadtxt('MIROS_20141104.txt',dtype=float)
HsM=MIROS[:,0]
TpM=MIROS[:,1]
DpM=MIROS[:,2]
dataM=np.array([start + datetime.timedelta(hours=i) for i in xrange(HsM.shape[0])])
spc1d_M=np.loadtxt('MIROS_20141104_spc.txt',dtype=float)
freqM=np.loadtxt('MIROS_freq.txt',dtype=float)

## MIROSS - PARAMETROS
HsMP,TpMP,DpMP=np.loadtxt('/home/izabel/Projetos/WW3BR/MIROS/201411_Parametros/MIR_WM1_201411_MON.txt',dtype=float,usecols=(4,7,18),unpack=True)
dataMP1=np.loadtxt('/home/izabel/Projetos/WW3BR/MIROS/201411_Parametros/MIR_WM1_201411_MON.txt',dtype=str,usecols=(0,1),unpack=True)

dataMP=[]
for datat in range(0,dataMP1.shape[1]):
	dataMP.append('%s %s' %(dataMP1[0,datat],dataMP1[1,datat]))

dataMP = np.array(dataMP)
dataMP=[datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in dataMP[:]]


#abrir parametos de ondas
HsLioc=np.zeros([spc2d_Lioc.shape[0]],'f')
HsCli=np.zeros([spc2d_Lioc.shape[0]],'f')
TpLioc=np.zeros([spc2d_Lioc.shape[0]],'f')
TpCli=np.zeros([spc2d_Lioc.shape[0]],'f')
DpLioc=np.zeros([spc2d_Lioc.shape[0]],'f')
DpCli=np.zeros([spc2d_Lioc.shape[0]],'f')

# lioc - tirado do espectro utilizando o metodo de Nelson e Ostriz
dfim=[0.00067954,  0.00144347,  0.00162274,  0.00182427,  0.00205084,
        0.00230554,  0.00259187,  0.00291377,  0.00327564,  0.00368245,
        0.00413979,  0.00465392,  0.00523191,  0.00588168,  0.00661214,
        0.00743333,  0.0083565 ,  0.00939432,  0.01056104,  0.01187265,
        0.01334715,  0.01500478,  0.01686828,  0.01896322,  0.01003596]

# climatempo - retirado do arquivo .spc
freqc=array([ 0.0418    ,  0.0459    ,  0.0505    ,  0.0556    ,  0.0612    ,
        0.0673    ,  0.074     ,  0.0814    ,  0.0895    ,  0.0985    ,
        0.108     ,  0.119     ,  0.131     ,  0.14399999,  0.15899999,
        0.17399999,  0.192     ,  0.211     ,  0.23199999,  0.255     ,
        0.28099999,  0.30899999,  0.34      ,  0.37400001,  0.41100001])

dfimc=array([ 0.00036087,  0.00075745,  0.00083238,  0.00091473,  0.00100522,
        0.00110467,  0.00121396,  0.00133405,  0.00146603,  0.00161107,
        0.00177045,  0.0019456 ,  0.00213808,  0.0023496 ,  0.00258205,
        0.00283749,  0.00311821,  0.00342669,  0.0037657 ,  0.00413824,
        0.00454764,  0.00499754,  0.00549195,  0.00603527,  0.00315987])


for t in range(0,HsLioc.shape[0]):
	# Espectro 1D
	for il in range(0,spc2d_Lioc.shape[2]):
		spc1d_Lioc[t,il]=sum(spc2d_Lioc[t,:,il])

	for il in range(0,spc2d_Cli.shape[2]):
		spc1d_Cli[t,il]=sum(spc2d_Cli[t,0,il,:])


	spc1d_Cli[t,:]=flipud(spc1d_Cli[t,:])
	# fig=plt.figure(figsize=(8,6))
	# plot(freq,spc1d_Lioc[t,:],'-k')
	# plot(freqc,spc1d_Cli[t,:],'-b')
	# plot(freqM,spc1d_M[t,:],'-r')
	# grid()
	# xlabel('Frequency (Hz)')
	# ylabel('Power Spectrum (m^2/Hz)')      
	# legend(['WW3Lioc','WW3ClimaTempo','MIROS'])   
	# title('WAVEWATCH III - Espectro de Energia / Power Spectrum  '+repr(data[t].strftime("%d-%m-%Y-%H"))+'Z', fontsize=11)		
	# savefig(pathnamem + 'spec_1D'+repr(data[t].strftime("%d%m%Y%H"))+'.jpg', dpi=None, facecolor='w', edgecolor='w',
	# orientation='portrait', papertype=None, format='jpg',
	# ransparent=False, bbox_inches=None, pad_inches=0.1)
	# plt.close()

	HsLioc[t]=4*sqrt(sum(spc1d_Lioc[t,:]*dfim))
	HsCli[t]=4*sqrt(sum(spc1d_Cli[t,:]*dfimc))

	nfl=np.where(spc1d_Lioc[t,:]==max(spc1d_Lioc[t,:]))
	nfc=np.where(spc1d_Cli[t,:]==max(spc1d_Cli[t,:]))
	freqLioc=freq[nfl[0]]
	freqCli=freqc[nfc[0]]
	TpLioc[t]=1./freqLioc
	TpCli[t]=1./freqCli
	
	sdc=spc2d_Cli[t,0,nfc[0],:]
	ndl=np.where(spc2d_Lioc[t,:,nfl[0]]==max(spc2d_Lioc[t,:,nfl[0]]))[0]
	ndc=np.where(sdc[0,:]==max(sdc[0,:]))[0]

	DpLioc[t]=dire[ndl[0]]
	DpCli[t]=direc[ndc[0]]
		

# os.chdir('/home/izabel/Projetos/Dropbox/lioc/ww3br/Geral/rot/')
# execfile('pp_argos1_izabel2.py')

data1str=np.array([datetime.datetime.strftime(dataMP[i],'%Y%m%d%H') for i in xrange(len(dataMP))])
data1str=data1str.astype(int)
data1str,indices = np.unique(data1str, return_index=True)
hs1=HsMP[indices]
tp1=TpMP[indices]
dp1=DpMP[indices]

t0=np.where(data1str==datastr[0])[0]
tf=np.where(data1str==datastr[-1])[0]+1

datan=[np.where(datastr[i]==data1str) for i in xrange(len(datastr))]
datan,zero,zero=np.where(datan)
# dados com o eixo de tempo corrigido
HsLiocp=HsLioc[datan]
HsClip=HsCli[datan]
TpLiocp=TpLioc[datan]
TpClip=TpCli[datan]
DpLiocp=DpLioc[datan]
DpClip=DpCli[datan]
Hsboia=hs1[t0:tf]
Tpboia=tp1[t0:tf]
Dpboia=dp1[t0:tf]
datap=datastr[datan]


# #desconsiderando os valores com NaN da boia
Hsboia=Hsboia.astype(float)
aux=np.where(Hsboia > 10)
Hsboia[aux]=np.nan
Tpboia[aux]=np.nan
Dpboia[aux]=np.nan
aux=np.where(Tpboia > 20)
Hsboia[aux]=np.nan
Tpboia[aux]=np.nan
Dpboia[aux]=np.nan


nHs1=np.where(isnan(Hsboia)==False)
HsLiocp=HsLiocp[nHs1]
HsClip=HsClip[nHs1]
TpLiocp=TpLiocp[nHs1]
TpClip=TpClip[nHs1]
DpLiocp=DpLiocp[nHs1]
DpClip=DpClip[nHs1]
Hsboia=Hsboia[nHs1]
Tpboia=Tpboia[nHs1]
Dpboia=Dpboia[nHs1]
datap=datap[nHs1]



dataD=np.array([datap,HsLiocp,HsClip,TpLiocp,TpClip,DpLiocp,DpClip,Hsboia,Tpboia,Dpboia]).T

np.savetxt(pathnamed + 'saidaMIROS'+str(datastr[0])+'.out',dataD,delimiter=',',fmt=['%i']+9*['%.2f'],
	header='data,HsLioc,HsCli,TpLioc,TpCli,DpLioc,DpCli,HsBoia,TpBoia,DpBoia')

fig=plt.figure(figsize=(12,6))
plot(data[datan],hs1[t0:tf],'ro')
plot(data[datan],HsLioc[datan],'-k')
plot(data[datan],HsCli[datan],'-b')
grid()
ylim((0,6))
xlabel('Ocorrencias')
ylabel('Altura Significativa (m)')      
legend(['MIROS','WW3Lioc','WW3ClimaTempo'])   
savefig(pathnamem + 'MIROScomparaHs.png', dpi=None, facecolor='w', edgecolor='w',
orientation='portrait', papertype=None, format='png',
ransparent=False, bbox_inches=None, pad_inches=0.1)
plt.close()


fig=plt.figure(figsize=(12,6))
plot(data[datan],tp1[t0:tf],'ro')
plot(data[datan],TpLioc[datan],'-k')
plot(data[datan],TpCli[datan],'-b')
grid()
ylim((0,20))
xlabel('Ocorrencias')
ylabel('Periodo de Pico (s)')      
legend(['MIROS','WW3Lioc','WW3ClimaTempo'])   
savefig(pathnamem + 'MIROScomparaTp.png', dpi=None, facecolor='w', edgecolor='w',
orientation='portrait', papertype=None, format='png',
ransparent=False, bbox_inches=None, pad_inches=0.1)
plt.close()

fig=plt.figure(figsize=(12,6))
plot(data[datan],dp1[t0:tf],'ro')
plot(data[datan],DpLioc[datan],'-k')
plot(data[datan],DpCli[datan],'-b')
grid()
ylim((0,360))
xlabel('Ocorrencias')
ylabel('Direcao de Pico (graus)')      
legend(['MIROS','WW3Lioc','WW3ClimaTempo'])   
savefig(pathnamem + 'MIROScomparaDp.png', dpi=None, facecolor='w', edgecolor='w',
orientation='portrait', papertype=None, format='png',
ransparent=False, bbox_inches=None, pad_inches=0.1)
plt.close()


# plt.figure()
# plt.subplot(311)
# plot(data1,hs1,'ro')
# plt.ylabel('Hs (m)'), plt.grid()#, pl.legend(loc=4)
# plt.xticks(visible=False)
# ylim((0,5))
# plt.subplot(312)
# plot(data1,tp1,'ro')
# plt.ylabel('Tp (s)'), plt.grid()
# plt.xticks(visible=False)
# ylim((0,25))
# plt.subplot(313)
# plot(data1,dp1,'ro')
# plt.ylabel('Dp (graus)'), plt.grid(), plt.xlabel('Dias')

# for i in range (4,len(var)): #lon,lat,levels,time,loc...
# 	#name=var[i] para ler todos os pontos
# 	#name = loc223 para Santos loc224 para RS
# 	name='loc224'
# 	loc=fu.variables[name]
# 	spc1d=np.zeros((loc.shape[0],loc.shape[2]),'f')
# 	# dimensao das variaveis
# 	#float32 loc223(time, levels, latitude, longitude)
# 	#(265, 6, 25, 36)
# 	for t in range(0,loc.shape[0]):

# 		levels=[0.1,0.5,1,2,3,4,5,6,8,10,12,15]
# 		# espectro 2D
# 		fig=plt.figure(figsize=(8,6))
# 		contourf(loc[t,0,:,:],levels)
# 		grid()
# 		xlabel('Frequency (Hz)')
# 		ylabel('Direction (degrees)')
# 		title('WAVEWATCH III - Espectro Direcional / Directional Spectrum  '+repr(data[t].strftime("%d-%m-%Y-%H"))+'Z', fontsize=11)
# 		ax = plt.gca()
# 		pos = ax.get_position()
# 		l, b, w, h = pos.bounds
# 		cax = plt.axes([l+w+0.01, b+0.01, 0.03, h-0.01]) # setup colorbar axes.
# 		plt.colorbar(cax=cax) # draw colorbar
# 		plt.axes(ax)  # make the original axes current again
# 		savefig('spec_2D'+repr(data[t].strftime("%d%m%Y%H"))+repr(var[i])+'.jpg', dpi=None, facecolor='w', edgecolor='w',
# 		orientation='portrait', papertype=None, format='jpg',
# 		transparent=False, bbox_inches=None, pad_inches=0.1)
# 		plt.close()

# 		# espectro 1D
# 		for il in range(0,loc.shape[2]):
# 			spc1d[t,il]=sum(loc[t,0,:,il])

# 		fig=plt.figure(figsize=(8,6))
# 		plot(spc1d[t,:])
# 		grid()
# 		xlabel('Frequency (Hz)')
# 		ylabel('Power Spectrum (m^2/Hz)')         
# 		title('WAVEWATCH III - Espectro de Energia / Power Spectrum  '+repr(data[t].strftime("%d-%m-%Y-%H"))+'Z', fontsize=11)		
# 		savefig('spec_1D'+repr(data[t].strftime("%d%m%Y%H"))+repr(var[i])+'.jpg', dpi=None, facecolor='w', edgecolor='w',
# 		orientation='portrait', papertype=None, format='jpg',
# 		ransparent=False, bbox_inches=None, pad_inches=0.1)
# 		plt.close()


