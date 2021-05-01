# -*- coding: utf-8 -*-
"""
created on Thu Jun 05 14:47:23 2014

@author: soutobias
"""

import numpy as np
from numpy import *
import argosqc as qc

def arredondar(num):
    return float( '%.0f' % ( num ) )

def qualitycontrol3(epoch,buoy,Lat,lon,sensor00,year,month,day,hour,minute,wspd1,gust1,wdir1,wspd2,gust2,wdir2,battery,flood,atmp,humi,dewp,pres,arad,wtmp,cloro,turb,cvel1,cdir1,cvel2,cdir2,cvel3,cdir3,wvht,wmax,dpd,mwd,spred,bhead,sensoresbons):
#    (wspd,wdir,gust,flag,flagid)=qualitycontrol3(epoca,data,variables1,variables2,lat,sensoresbons)


    wdir1flag,wspd1flag,gust1flag,wdir2flag,wspd2flag=[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch)
    gust2flag,wvhtflag,wmaxflag,dpdflag,mwdflag=[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch)
    presflag,humiflag,atmpflag,wtmpflag,dewpflag=[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch)
    cvel1flag,cdir1flag,cvel2flag,cdir2flag,cvel3flag,cdir3flag=[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch)

    wdir1flagid,wspd1flagid,gust1flagid,wdir2flagid,wspd2flagid=['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch)
    gust2flagid,wvhtflagid,wmaxflagid,dpdflagid,mwdflagid=['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch)
    presflagid,humiflagid,atmpflagid,wtmpflagid,dewpflagid=['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch)
    cvel1flagid,cdir1flagid,cvel2flagid,cdir2flagid,cvel3flagid,cdir3flagid=['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch)



    (rwvht,rdpd,rmwd,rwspd,rwdir,rgust,ratmp,rpres,rdewp,rwtmp,rapd,rhumi,rcvel,rcdir, sigmawvht,sigmapres,sigmaatmp,sigmawspd,sigmawtmp,sigmahumi,mishumi1,mishumi2,miscvel,miscvel1,miscdir,misdewp,misatmp,miswtmp,rwmax)=qc.valoresargos()

    (r1wvht,r1dpd,r1wspd,r1gust,r1atmp,r1pres,r1dewp,r1wtmp,r1apd,r1cvel,r1wmax,r2atmp,r3atmp)=qc.valoresclima()
    ##############################################
    #RUN The Qc checKs
    ##############################################
    
    #time check
    (timeflag) = qc.timecheck(epoch)

    #missing value check
    (wdir1flag,wdir1flagid)=qc.misvaluecheck(epoch,wdir1,wdir1flag,-9999,wdir1flagid)
    (wspd1flag,wspd1flagid)=qc.misvaluecheck(epoch,wspd1,wspd1flag,-9999,wspd1flagid)
    (gust1flag,gust1flagid)=qc.misvaluecheck(epoch,gust1,gust1flag,-9999,gust1flagid)
    (wdir2flag,wdir2flagid)=qc.misvaluecheck(epoch,wdir2,wdir2flag,-9999,wdir2flagid)
    (wspd2flag,wspd2flagid)=qc.misvaluecheck(epoch,wspd2,wspd2flag,-9999,wspd2flagid)
    (gust2flag,gust2flagid)=qc.misvaluecheck(epoch,gust2,gust2flag,-9999,gust2flagid)
    (mwdflag,mwdflagid)=qc.misvaluecheck(epoch,mwd,mwdflag,-9999,mwdflagid)
    (wvhtflag,wvhtflagid)=qc.misvaluecheck(epoch,wvht,wvhtflag,-9999,wvhtflagid)
    (wmaxflag,wmaxflagid)=qc.misvaluecheck(epoch,wmax,wmaxflag,-9999,wmaxflagid)
    (dpdflag,dpdflagid)=qc.misvaluecheck(epoch,dpd,dpdflag,-9999,dpdflagid)
    (presflag,presflagid)=qc.misvaluecheck(epoch,pres,presflag,-9999,presflagid)
    (dewpflag,dewpflagid)=qc.misvaluecheck(epoch,dewp,dewpflag,misdewp,dewpflagid)
    (atmpflag,atmpflagid)=qc.misvaluecheck(epoch,atmp,atmpflag,misatmp,atmpflagid)
    (wtmpflag,wtmpflagid)=qc.misvaluecheck(epoch,wtmp,wtmpflag,miswtmp,wtmpflagid)
    (cvel1flag,cvel1flagid)=qc.misvaluecheck(epoch,cvel1,cvel1flag,miscvel,cvel1flagid)
    (cvel1flag,cvel1flagid)=qc.misvaluecheck(epoch,cvel1,cvel1flag,miscvel1,cvel1flagid)
    (cdir1flag,cdir1flagid)=qc.misvaluecheck(epoch,cdir1,cdir1flag,miscdir,cdir1flagid)
    (cvel2flag,cvel2flagid)=qc.misvaluecheck(epoch,cvel2,cvel2flag,miscvel,cvel2flagid)
    (cvel2flag,cvel2flagid)=qc.misvaluecheck(epoch,cvel2,cvel2flag,miscvel1,cvel2flagid)
    (cdir2flag,cdir2flagid)=qc.misvaluecheck(epoch,cdir2,cdir2flag,miscdir,cdir2flagid)
    (cvel3flag,cvel3flagid)=qc.misvaluecheck(epoch,cvel3,cvel3flag,miscvel,cvel3flagid)
    (cvel3flag,cvel3flagid)=qc.misvaluecheck(epoch,cvel3,cvel3flag,miscvel1,cvel3flagid)
    (cdir3flag,cdir3flagid)=qc.misvaluecheck(epoch,cdir3,cdir3flag,miscdir,cdir3flagid)
    (humiflag,humiflagid)=qc.misvaluecheck(epoch,humi,humiflag,mishumi1,humiflagid)
    (humiflag,humiflagid)=qc.misvaluecheck(epoch,humi,humiflag,mishumi2,humiflagid)

    (dewpflag,dewpflagid)=qc.misvaluecheck(epoch,dewp,dewpflag,-9999,dewpflagid)
    (atmpflag,atmpflagid)=qc.misvaluecheck(epoch,atmp,atmpflag,-9999,atmpflagid)
    (wtmpflag,wtmpflagid)=qc.misvaluecheck(epoch,wtmp,wtmpflag,-9999,wtmpflagid)
    (cvel1flag,cvel1flagid)=qc.misvaluecheck(epoch,cvel1,cvel1flag,-9999,cvel1flagid)
    (cdir1flag,cdir1flagid)=qc.misvaluecheck(epoch,cdir1,cdir1flag,-9999,cdir1flagid)
    (cvel2flag,cvel2flagid)=qc.misvaluecheck(epoch,cvel2,cvel2flag,-9999,cvel2flagid)
    (cdir2flag,cdir2flagid)=qc.misvaluecheck(epoch,cdir2,cdir2flag,-9999,cdir2flagid)
    (cvel3flag,cvel3flagid)=qc.misvaluecheck(epoch,cvel3,cvel3flag,-9999,cvel3flagid)
    (cdir3flag,cdir3flagid)=qc.misvaluecheck(epoch,cdir3,cdir3flag,-9999,cdir3flagid)
    (humiflag,humiflagid)=qc.misvaluecheck(epoch,humi,humiflag,-9999,humiflagid)

    #checagem de sensores ruins
    (wdir1flag,wdir1flagid)=qc.sensorruimcheck(epoch,wdir1,wdir1flag,sensoresbons[0],wdir1flagid)
    (wspd1flag,wspd1flagid)=qc.sensorruimcheck(epoch,wspd1,wspd1flag,sensoresbons[1],wspd1flagid)
    (gust1flag,gust1flagid)=qc.sensorruimcheck(epoch,gust1,gust1flag,sensoresbons[2],gust1flagid)

    (wdir2flag,wdir2flagid)=qc.sensorruimcheck(epoch,wdir2,wdir2flag,sensoresbons[3],wdir2flagid)
    (wspd2flag,wspd2flagid)=qc.sensorruimcheck(epoch,wspd2,wspd2flag,sensoresbons[4],wspd2flagid)
    (gust2flag,gust2flagid)=qc.sensorruimcheck(epoch,gust2,gust2flag,sensoresbons[5],gust2flagid)

    (wvhtflag,wvhtflagid)=qc.sensorruimcheck(epoch,wvht,wvhtflag,sensoresbons[6],wvhtflagid)
    (wmaxflag,wmaxflagid)=qc.sensorruimcheck(epoch,wmax,wmaxflag,sensoresbons[7],wmaxflagid)
    (dpdflag,dpdflagid)=qc.sensorruimcheck(epoch,dpd,dpdflag,sensoresbons[8],dpdflagid)
    (mwdflag,mwdflagid)=qc.sensorruimcheck(epoch,mwd,mwdflag,sensoresbons[9],mwdflagid)

    (presflag,presflagid)=qc.sensorruimcheck(epoch,pres,presflag,sensoresbons[10],presflagid)
    (humiflag,humiflagid)=qc.sensorruimcheck(epoch,humi,humiflag,sensoresbons[11],humiflagid)
    (atmpflag,atmpflagid)=qc.sensorruimcheck(epoch,atmp,atmpflag,sensoresbons[12],atmpflagid)
    (wtmpflag,wtmpflagid)=qc.sensorruimcheck(epoch,wtmp,wtmpflag,sensoresbons[13],wtmpflagid)
    (dewpflag,dewpflagid)=qc.sensorruimcheck(epoch,dewp,dewpflag,sensoresbons[14],dewpflagid)

    (cvel1flag,cvel1flagid)=qc.sensorruimcheck(epoch,cvel1,cvel1flag,sensoresbons[15],cvel1flagid)
    (cdir1flag,cdir1flagid)=qc.sensorruimcheck(epoch,cdir1,cdir1flag,sensoresbons[16],cdir1flagid)
    (cvel2flag,cvel2flagid)=qc.sensorruimcheck(epoch,cvel2,cvel2flag,sensoresbons[17],cvel2flagid)
    (cdir2flag,cdir2flagid)=qc.sensorruimcheck(epoch,cdir2,cdir2flag,sensoresbons[18],cdir2flagid)
    (cvel3flag,cvel3flagid)=qc.sensorruimcheck(epoch,cvel3,cvel3flag,sensoresbons[19],cvel3flagid)
    (cdir3flag,cdir3flagid)=qc.sensorruimcheck(epoch,cdir3,cdir3flag,sensoresbons[20],cdir3flagid)


    #coarse Range check
    (wvhtflag,wvhtflagid) = qc.rangecheck(epoch, wvht,rwvht,wvhtflag,wvhtflagid)
    (wmaxflag,wmaxflagid) = qc.rangecheck(epoch, wmax,rwmax,wmaxflag,wmaxflagid)
    (dpdflag,dpdflagid) = qc.rangecheck(epoch, dpd,rdpd,dpdflag,dpdflagid)
    (mwdflag,mwdflagid) = qc.rangecheck(epoch,mwd,rmwd,mwdflag,mwdflagid)
    
    (humiflag,humiflagid) = qc.rangecheck(epoch, humi,rhumi,humiflag,humiflagid)
    (presflag,presflagid) = qc.rangecheck(epoch, pres,rpres,presflag,presflagid)
    (dewpflag,dewpflagid) = qc.rangecheck(epoch, dewp,rdewp,dewpflag,dewpflagid)
    (atmpflag,atmpflagid) = qc.rangecheck(epoch,atmp,ratmp,atmpflag,atmpflagid)
    
    (wspd1flag,wspd1flagid) = qc.rangecheck(epoch, wspd1,rwspd,wspd1flag,wspd1flagid)
    (wdir1flag,wdir1flagid) = qc.rangecheck(epoch, wdir1,rwdir,wdir1flag,wdir1flagid)
    (gust1flag,gust1flagid) = qc.rangecheck(epoch, gust1,rgust,gust1flag,gust1flagid)
    (wspd2flag,wspd2flagid) = qc.rangecheck(epoch, wspd2,rwspd,wspd2flag,wspd2flagid)
    (wdir2flag,wdir2flagid) = qc.rangecheck(epoch, wdir2,rwdir,wdir2flag,wdir2flagid)
    (gust2flag,gust2flagid) = qc.rangecheck(epoch, gust2,rgust,gust2flag,gust2flagid)
    
    (wtmpflag,wtmpflagid) = qc.rangecheck(epoch,wtmp,rwtmp,wtmpflag,wtmpflagid)
    (cvel1flag,cvel1flagid) = qc.rangecheck(epoch, cvel1,rcvel,cvel1flag,cvel1flagid)
    (cdir1flag,cdir1flagid) = qc.rangecheck(epoch, cdir1,rcdir,cdir1flag,cdir1flagid)
    (cvel2flag,cvel2flagid) = qc.rangecheck(epoch, cvel2,rcvel,cvel2flag,cvel2flagid)
    (cdir2flag,cdir2flagid) = qc.rangecheck(epoch, cdir2,rcdir,cdir2flag,cdir2flagid)
    (cvel3flag,cvel3flagid) = qc.rangecheck(epoch, cvel3,rcvel,cvel3flag,cvel3flagid)
    (cdir3flag,cdir3flagid) = qc.rangecheck(epoch, cdir3,rcdir,cdir3flag,cdir3flagid)

    #soft Range check

    (wvhtflag,wvhtflagid) = qc.rangecheckclima(epoch, wvht,r1wvht,wvhtflag,wvhtflagid)
    (wmaxflag,wmaxflagid) = qc.rangecheckclima(epoch, wmax,r1wmax,wmaxflag,wmaxflagid)
    (dpdflag,dpdflagid) = qc.rangecheckclima(epoch, dpd,r1dpd,dpdflag,dpdflagid)

    (presflag,presflagid) = qc.rangecheckclima(epoch, pres,r1pres,presflag,presflagid)
    (dewpflag,dewpflagid) = qc.rangecheckclima(epoch, dewp,r1dewp,dewpflag,dewpflagid)

    try:
        if mean(Lat)<=-27:
            (atmpflag,atmpflagid) = qc.rangecheckclima(epoch,atmp,r1atmp,atmpflag,atmpflagid)
        elif mean(Lat)>-27 and mean(Lat)<=-18: 
            (atmpflag,atmpflagid) = qc.rangecheckclima(epoch,atmp,r2atmp,atmpflag,atmpflagid)
        else:
            (atmpflag,atmpflagid) = qc.rangecheckclima(epoch,atmp,r3atmp,atmpflag,atmpflagid)
    except:
        (atmpflag,atmpflagid) = qc.rangecheckclima(epoch,atmp,r1atmp,atmpflag,atmpflagid)
        
    
    (wspd1flag,wspd1flagid) = qc.rangecheckclima(epoch, wspd1,r1wspd,wspd1flag,wspd1flagid)
    (gust1flag,gust1flagid) = qc.rangecheckclima(epoch, gust1,r1gust,gust1flag,gust1flagid)
    (wspd2flag,wspd2flagid) = qc.rangecheckclima(epoch, wspd2,r1wspd,wspd2flag,wspd2flagid)
    (gust2flag,gust2flagid) = qc.rangecheckclima(epoch, gust2,r1gust,gust2flag,gust2flagid)
    
    (wtmpflag,wtmpflagid) = qc.rangecheckclima(epoch,wtmp,r1wtmp,wtmpflag,wtmpflagid)
    (cvel1flag,cvel1flagid) = qc.rangecheckclima(epoch, cvel1,r1cvel,cvel1flag,cvel1flagid)
    (cvel2flag,cvel2flagid) = qc.rangecheckclima(epoch, cvel2,r1cvel,cvel2flag,cvel2flagid)
    (cvel3flag,cvel3flagid) = qc.rangecheckclima(epoch, cvel3,r1cvel,cvel3flag,cvel3flagid)

    #significance wave height vs max wave height
    (wvhtflag,wmaxflag,wvhtflagid,wmaxflagid) = qc.wvhtwmaxcheck(epoch,wvht,wmax,wvhtflag,wmaxflag,wvhtflagid,wmaxflagid)
    
    #wind speed vs gust speed
    (wspd1flag,gust1flag,wspd1flagid,gust1flagid) = qc.windspeedgustcheck(epoch,wspd1,gust1,wspd1flag,gust1flag,wspd1flagid,gust1flagid)
    (wspd2flag,gust2flag,wspd2flagid,gust2flagid) = qc.windspeedgustcheck(epoch,wspd2,gust2,wspd2flag,gust2flag,wspd2flagid,gust2flagid)
   
    #dew point and air temperature check
    (dewpflag,dewpflagid) = qc.dewpatmpcheck(epoch,dewp,atmp,dewpflag,atmpflag,dewpflagid)
    
    #check of effects of battery voltage in sensors    
    (presflag,presflagid) = qc.batsensorcheck(epoch,battery,pres,presflag,presflagid)    
    
    #stucksensorcheck
    (wvhtflag,wvhtflagid) = qc.stucksensorcheck(epoch, wvht,wvhtflag,12,wvhtflagid)
    (wmaxflag,wmaxflagid) = qc.stucksensorcheck(epoch, wmax,wmaxflag,12,wmaxflagid)
    
    (humiflag,humiflagid) = qc.stucksensorcheck(epoch, humi,humiflag,12,humiflagid)
    (presflag,presflagid) = qc.stucksensorcheck(epoch, pres,presflag,12,presflagid)
    (dewpflag,dewpflagid) = qc.stucksensorcheck(epoch, dewp,dewpflag,12,dewpflagid)
    (atmpflag,atmpflagid) = qc.stucksensorcheck(epoch,atmp,atmpflag,12,atmpflagid)
    
    (wspd1flag,wspd1flagid) = qc.stucksensorcheck(epoch, wspd1,wspd1flag,12,wspd1flagid)
    (wdir1flag,wdir1flagid) = qc.stucksensorcheck(epoch, wdir1,wdir1flag,12,wdir1flagid)
    (gust1flag,gust1flagid) = qc.stucksensorcheck(epoch, gust1,gust1flag,12,gust1flagid)
    (wspd2flag,wspd2flagid) = qc.stucksensorcheck(epoch, wspd2,wspd2flag,12,wspd2flagid)
    (wdir2flag,wdir2flagid) = qc.stucksensorcheck(epoch, wdir2,wdir2flag,12,wdir2flagid)
    (gust2flag,gust2flagid) = qc.stucksensorcheck(epoch, gust2,gust2flag,12,gust2flagid)
    
    (wtmpflag,wtmpflagid) = qc.stucksensorcheck(epoch,wtmp,wtmpflag,12,wtmpflagid)
    (cvel1flag,cvel1flagid) = qc.stucksensorcheck(epoch, cvel1,cvel1flag,12,cvel1flagid)
    (cdir1flag,cdir1flagid) = qc.stucksensorcheck(epoch, cdir1,cdir1flag,12,cdir1flagid)
    (cvel2flag,cvel2flagid) = qc.stucksensorcheck(epoch, cvel2,cvel2flag,12,cvel2flagid)
    (cdir2flag,cdir2flagid) = qc.stucksensorcheck(epoch, cdir2,cdir2flag,12,cdir2flagid)
    (cvel3flag,cvel3flagid) = qc.stucksensorcheck(epoch, cvel3,cvel3flag,12,cvel3flagid)
    (cdir3flag,cdir3flagid) = qc.stucksensorcheck(epoch, cdir3,cdir3flag,12,cdir3flagid)


    #related measurement check
    (wdirflag,wspdflag,gustflag,wdir,wspd,gust,wdirflagid,wspdflagid,gustflagid) = qc.relatedmeascheck3(epoch,wdir1,wspd1,gust1,wdir2,wspd2,gust2,wspd1flag, wdir1flag,gust1flag,wspd2flag, wdir2flag,gust2flag,wdir1flagid,wspd1flagid,gust1flagid,wdir2flagid,wspd2flagid,gust2flagid)

    
    #Time continuity check
    (wvhtflag,wvhtflagid) = qc.tcontinuitycheck(epoch, wvht,wvhtflag,sigmawvht,wvhtflagid,1)
    (wmaxflag,wmaxflagid) = qc.tcontinuitycheck(epoch, wmax,wmaxflag,sigmawvht,wmaxflagid,1)
    (humiflag,humiflagid) = qc.tcontinuitycheck(epoch, humi,humiflag,sigmahumi,humiflagid,1)
    (presflag,presflagid) = qc.tcontinuitycheck(epoch, pres,presflag,sigmapres,presflagid,1)
    (atmpflag,atmpflagid) = qc.tcontinuitycheck(epoch,atmp,atmpflag,sigmaatmp,atmpflagid,1)
    (wspdflag,wspdflagid) = qc.tcontinuitycheck(epoch, wspd,wspdflag,sigmawspd,wspdflagid,1)    
    (wtmpflag,wtmpflagid) = qc.tcontinuitycheck(epoch,wtmp,wtmpflag,sigmawtmp,wtmpflagid,1)


    #Frontal passage exception for time continuity
    (atmpflag,atmpflagid)=qc.frontexcepcheck1(epoch,wdir,wdirflag,atmpflag,atmpflagid)
#    (wdirflag,wdirflagid)=qc.frontexcepcheck2(epoch,wdir,wdirflag,atmpflag,atmpflagid)

    (atmpflag,atmpflagid)=qc.frontexcepcheck3(epoch,wspd,atmp,wspdflag,atmpflag,atmpflagid)
    (wspdflag,wspdflagid)=qc.frontexcepcheck4(epoch,pres,presflag,wdirflag,wdirflagid)
    
    (presflag,presflagid)=qc.frontexcepcheck5(epoch,pres,presflag,presflagid)
    (wvhtflag,wvhtflagid)=qc.frontexcepcheck6(epoch,wspd,wspdflag,wvhtflagid,wvhtflag)

    for i in range(len(cvel1)):
        if cvel1flag[i]==4 or cdir1flag[i]==4 or cvel2flag[i]==4 or cdir2flag[i]==4 or cvel3flag[i]==4 or cdir3flag[i]==4:
            if cdir1flag[i]!=4:
                cdir1flagid[i]='60'
            if cvel1flag[i]!=4:
                cvel1flagid[i]='60'
            if cvel2flag[i]!=4:
                cvel2flagid[i]='60'
            if cdir2flag[i]!=4:
                cdir2flagid[i]='60'
            if cvel3flag[i]!=4:
                cvel3flagid[i]='60'
            if cdir3flag[i]!=4:
                cdir3flagid[i]='60'

        if mwdflag[i]==4 or wvhtflag[i]==4 or wmaxflag[i]==4 or dpdflag[i]==4:
            if wvhtflag[i]!=4:
                wvhtflagid[i]='60'
            if wmaxflag[i]!=4:
                wmaxflagid[i]='60'
            if dpdflag[i]!=4:
                dpdflagid[i]='60'
            if mwdflag[i]!=4:
                mwdflagid[i]='60'

        if wdirflag[i]==4 or gustflag[i]==4 or wspdflag[i]==4:
            if wdirflag[i]!=4:
                wdirflagid[i]='60'                
            if gustflag[i]!=4:
                gustflagid[i]='60'  
            if wspdflag[i]!=4:
                wspdflagid[i]='60'  

    return wspd,wdir,gust,wdirflag,wspdflag,gustflag,wvhtflag,wmaxflag,dpdflag,mwdflag,presflag,humiflag,atmpflag,wtmpflag,dewpflag,cvel1flag,cdir1flag,cvel2flag,cdir2flag,cvel3flag,cdir3flag,wdirflagid,wspdflagid,gustflagid,wvhtflagid,wmaxflagid,dpdflagid,mwdflagid,presflagid,humiflagid,atmpflagid,wtmpflagid,dewpflagid,cvel1flagid,cdir1flagid,cvel2flagid,cdir2flagid,cvel3flagid,cdir3flagid

