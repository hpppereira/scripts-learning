#rotina criada em maio.2018 ( Stella) para processamento dos dados do CTD_CastAway

import gsw 
from gsw._wrapped_ufuncs import SP_from_C
import numpy as np
import pandas as pd
from glob import glob

def remove_top(p,var,il=.2):
    index = np.where(p>=il)[0] 
    return p[index], var[index]

def remove_upcast(p,var):
    i = np.where(p==p.max())[0][0]
    return p[0:i+1],var[0:i+1] 

def despike(p,var,dd=19):
    dep = p.shape[0]-1
    di,df = 0,dd
    while df <= dep:
        mean, std = np.mean(var[di:df+1]), np.std(var[di:df+1])
        index = np.logical_or(var[di:df+1]>mean+2*std,var[di:df+1]<mean-2*std)
        index = np.arange(di,df+1)[index] 
        var[index],p[index] = np.nan, np.nan
        di+=dd
        df+=dd   
    index = ~np.isnan(var)
    return p[index],var[index]

def loopedit(p,var):
    dpdz=np.diff(p); j,p0=0,p[0]
    for i in range(len(dpdz)):
        if dpdz[i]<0 and j==0:
            p0,i0=p[i],i
            j+=1
        if j != 0 and p[i]>p0:
            p[i0:i],var[i0:i]=np.nan,np.nan
            j=0
    index = ~np.isnan(var)
    return p[index],var[index]


def bina(p,var,box=1):
    stt,end = .2,p.max()
    nvar = []
    while stt <= end:
        index = (p>=stt)&(p<stt+box)
        nvar.append(np.mean(var[index]))
        stt+=box
    nvar = np.array(nvar)
    index = np.argwhere(np.isnan(nvar))
    for i in index:
        nvar[i]=nvar[i-1]
    return nvar

#################################################

if __name__ == "__main__":
    dname ="C:/Users/Morel2/Google Drive/CEBIMAR/Buzios/Ponto Deia/20170505/RAW/"
    Files = glob(dname+'*.csv')
    Files.sort()
    i = 1
   
    
    for fname in Files:
        data= np.loadtxt(fname,delimiter= ',',skiprows=29,usecols= [1,2,3])
        p, t, con = data[:,0], data[:,1], (data[:,2])/1000
            
        SP = SP_from_C(con,t,p)
        var=(np.array([p,t,SP])).T

        rtpT, rtT = remove_top(np.copy(p),t)
        rtpS, rtS = remove_top(np.copy(p),SP)

        rupS,ruS = remove_upcast(np.copy(rtpS),np.copy(rtS))
        rupT,ruT = remove_upcast(np.copy(rtpT),np.copy(rtT))

        rdpS,rdS = despike(rupS[~np.isnan(rupS)],ruS[~np.isnan(ruS)])
        rdpT,rdT = despike(rupT[~np.isnan(rupT)],ruT[~np.isnan(ruT)])

        lepS,leS = loopedit(rdpS,rdS)
        lepT,leT = loopedit(rdpT,rdT)

        biS = bina(lepS,leS,box=.2)
        biT = bina(lepT,leT,box=.2)

        pr=np.arange(.2,lepT.max(),.2)

        if len(biS)<len(pr): biS = np.append(biS,biS[-1])
        if len(biT)<len(pr): biT = np.append(biT,biT[-1])

        df= (np.array([pr+0.1,biT,biS])).T
        
        
        np.savetxt(dname+'processados/perfil%i.csv'%i, df, fmt='%.8f', delimiter=',', header='p(dbar),T(degreeC),S(PPS)')
        
        print ("Perfil %i" %i)
        
        i+=1
        
    
    
    
           
