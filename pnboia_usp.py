# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 13:49:10 2017

@author: tobia
"""
import time
import datetime
import numpy as np
import re
from math import radians, cos, sin, asin, sqrt
import csv
import MySQLdb
import operator
from numpy import *
from pylab import find
import sys
import psycopg2


def bancodedados_usp():


    local="54.212.252.17"
    usr="pnboiamarinha"
    password="%%marinha@1032"
    data_base="pnboia"

    return local,usr,password,data_base

def bancodedados_usppostgre():

    local="goosbrasil.org"
    usr="marinha"
    password="%%marinha@1032"
    data_base="goosbrasil"

    return local,usr,password,data_base

def time2epoch1(Year,Month,Day,Hour,Minute):
        
    Epoch = [0]*len(Year)
    
    if Minute==0:
        for i in xrange(len(Year)):
            Epoch[i]=(datetime.datetime(int(Year[i]),int(Month[i]),int(Day[i]),int(Hour[i]),0) - datetime.datetime(1970,1,1)).total_seconds()
    else:
        for i in xrange(len(Year)):
            Epoch[i]=(datetime.datetime(int(Year[i]),int(Month[i]),int(Day[i]),int(Hour[i]),int(Minute[i])) - datetime.datetime(1970,1,1)).total_seconds()

    return Epoch


def buscabd_usp2(boiasu,boiasu2):
           
    #(local,usr,password,data_base)=bancodedados3()
    variables3=['Epoca','flag','ano','mes','dia','hora','lon','lat','position_status','battery_voltage','solar_current','boot_times','flood_level','Wspd1','Gust1','Wdir1','avg_wind_int2','avg_wind_gust2','avg_wind_dir2','temp_air','rel_humid','dew_point','pressure','sst','buoy_heading','clh','turb','avg_radiation','CM_int1','CM_dir1','CM_int2','CM_dir2','CM_int3','CM_dir3','HS','H_max','Tp','Mn_dir','Mn_spread']
    for i in xrange(len(variables3)):
        exec("%studo=[]"%variables3[i])
    
    variables2=['argos_id1','id_sat','n_msg_sat','freq_sat','n_msg_db','best_db','n_ident_msg','quali_ind','n_lin_msg','Lat02','Lon02','Lat_sat','Lon_sat','Date_sat','Time_sat']
    for i in xrange(len(variables2)):
        exec("%studo=[]"%variables2[i])
    buoytudo,IDtudo,Minutetudo,fontetudo=[],[],[],[]
    
    varfinal1=['id_argos','flag','Epoca','lon','lat']
    varfinal2=['position_status','battery_voltage','solar_current','boot_times','flood_level','avg_wind_int1','wind_gust1','wind_dir1','avg_wind_int2','avg_wind_gust2','avg_wind_dir2']
    varfinal3=['avg_wind_int1_f2','wind_gust1_f2','wind_dir1_f2','temp_air','rel_humid','dew_point','pressure','sst','buoy_heading','clh','turb','avg_radiation','CM_int1','CM_dir1','CM_int2','CM_dir2','CM_int3','CM_dir3','HS','H_max','Tp','Mn_dir','Mn_spread']
    varfinal4=['Wspd1','Gust1','Wdir1']
    epoch_25 = time.strftime('%Y-%m-%d', time.gmtime(time.time()-3600*24*42))
    
    #(y_24,m_24,d_24,h_24,minu,ii,iii,iiii,iiii)=time.gmtime(time.time()-3600*24*5)
    print('xxx')
       
    #variables=['id_argos','flag','yyyy','mm','dd','hour','minuto','lon','lat','position_status','battery_voltage','solar_current','boot_times','flood_level','avg_wind_int1','wind_gust1','wind_dir1','avg_wind_int2','avg_wind_gust2','avg_wind_dir2','spare1','spare2','spare3','spare4','spare5','spare6','spare7','avg_wind_int1_f2','wind_gust1_f2','wind_dir1_f2','temp_air','rel_humid','dew_point','pressure','sst','buoy_heading','clh','turb','avg_radiation','CM_int1','CM_dir1','CM_int2','CM_dir2','CM_int3','CM_dir3','HS','H_max','Tp','Mn_dir','Mn_spread','cod']
    
    variables=['id_argos','boia_id','data','flag','battery_voltage','solar_current','boot_times','flood_level','avg_wind_int1','wind_gust1','wind_dir1','avg_wind_int2','avg_wind_gust2','avg_wind_dir2','spare1','spare2','spare3','spare4','spare5','spare6','spare7','avg_wind_int1_f2','wind_gust1_f2','wind_dir1_f2','temp_air','rel_humid','dew_point','pressure','sst','sst1000','buoy_heading','clh','turb','avg_radiation','CM_int1','CM_dir1','CM_int2','CM_dir2','CM_int3','CM_dir3','HS','H_max','Tp','Mn_dir','Mn_spread','spare24','spare25','position_status']
    
    
    for i in xrange(len(variables)):
        exec("%s=[]"%variables[i])
    lat,lon=[],[]
    
    #(local,usr,password,data_base)=bancodedados_usppostg()
    (local,usr,passw,data_base)=bancodedados_usppostgre()
    
    # conecta ao banco de dados propriamente dito   
    db = psycopg2.connect(dbname=data_base, user=usr, host=local, password=passw)
    
    
    # cria o cursor que permitir realizar queries ao BD
    cur=db.cursor()

    (boias,boias2)=boiasfuncionando()


    for i in xrange(len(boias)):
        if boiasu2=='RIOGRANDE':
            if boiasu2==boias2[i]:
                estaid=7
        elif boiasu2=='SANTACATARINA':
            if boiasu2==boias2[i]:
                estaid=10
        elif boiasu2=='SANTOS':
            if boiasu2==boias2[i]:
                estaid=5
        elif boiasu2=='GUANABARA':
            if boiasu2==boias2[i]:
                estaid=4
        elif boiasu2=='VITORIA':
            if boiasu2==boias2[i]:
                estaid=14
        elif boiasu2=='PORTOSEGURO':
            if boiasu2==boias2[i]:
                estaid=3
        elif boiasu2=='RECIFE':
            if boiasu2==boias2[i]:
                estaid=9
       
    cur.execute("SELECT * FROM pnboia_medidaboiafixaargos WHERE boia_id=%s \
        AND date>='%s' ORDER BY date, flag"%(estaid,epoch_25))
    for row in cur.fetchall():
        for i in xrange(len(variables)):
            exec("%s.append(row[i])"%variables[i])
    print('xxx')
    Epoca=[0]*len(data)
    for i in xrange(len(data)):   
        Epoca[i]=(datetime.datetime(data[i].year,data[i].month,data[i].day,data[i].hour,0) - datetime.datetime(1970,1,1)).total_seconds()
        lat.append('-9999')
        lon.append('-9999')
        if data[i].minute<=30:
            Epoca[i]=Epoca[i]-3600
    print('xxx')
    c=0
    for i in xrange(len(Epoca)):
        if int(Epoca[i])>=(time.time()-3600*24*42):
            Epoca[c]=Epoca[i];
            for i32 in xrange(len(variables)):
                exec("%s[c]=%s[i]"%(variables[i32],variables[i32]))
            lat[c]=lat[i]
            lon[c]=lon[i]
            c=c+1
    print(len(Epoca))
    Epoca=Epoca[0:c]
    print(len(Epoca))
    for i32 in xrange(len(variables)):
        exec("%s=%s[0:c]"%(variables[i32],variables[i32]))
    lat=lat[0:c]
    lon=lon[0:c]
    
    
    #variables10=['id_argos','flag','Epoca','lon','lat','position_status','battery_voltage','solar_current','boot_times','flood_level','avg_wind_int1','wind_gust1','wind_dir1','avg_wind_int2','avg_wind_gust2','avg_wind_dir2','spare1','spare2','spare3','spare4','spare5','spare6','spare7','avg_wind_int1_f2','wind_gust1_f2','wind_dir1_f2','temp_air','rel_humid','dew_point','pressure','sst','buoy_heading','clh','turb','avg_radiation','CM_int1','CM_dir1','CM_int2','CM_dir2','CM_int3','CM_dir3','HS','H_max','Tp','Mn_dir','Mn_spread','spare24','spare25']
    
    variables10=['id_argos','flag','Epoca','lon','lat','position_status','battery_voltage','solar_current','boot_times','flood_level','avg_wind_int1','wind_gust1','wind_dir1','avg_wind_int2','avg_wind_gust2','avg_wind_dir2','avg_wind_int1_f2','wind_gust1_f2','wind_dir1_f2','temp_air','rel_humid','dew_point','pressure','sst','buoy_heading','clh','turb','avg_radiation','CM_int1','CM_dir1','CM_int2','CM_dir2','CM_int3','CM_dir3','HS','H_max','Tp','Mn_dir','Mn_spread']
    
    
    for ii in xrange(len(varfinal4)):
        exec("%s=[0]*len(Epoca)" % (varfinal4[ii]))
    
    c=0      
    n=9 #número de iteracoes    
    
    for nn in xrange(n):
        print(nn)
        c,i=0,0 
        for w in xrange(len(Epoca)):
            if i<=(len(Epoca)-2):
                if Epoca[i]==Epoca[i+1]:
                    if int(flag[i])==int(flag[i+1]):
                        if int(flag[i])==1:
                            Wspd1[c]=avg_wind_int1[i]
                            Wdir1[c]=wind_dir1[i]
                            Gust1[c]=wind_gust1[i]
                        else:
                            Wspd1[c]=avg_wind_int1_f2[i]
                            Wdir1[c]=wind_dir1_f2[i]
                            Gust1[c]=wind_gust1_f2[i]
                        for ii in xrange(len(variables10)):
                            exec("%s[c]=%s[i]"% (variables10[ii],variables10[ii]))
                        c=c+1
                        i=i+2
                    else:
                        if int(flag[i])==1:
                            Wspd1[c]=avg_wind_int1[i]
                            Wdir1[c]=wind_dir1[i]
                            Gust1[c]=wind_gust1[i]
                            for ii in xrange(len(varfinal1)):
                                exec("%s[c]=%s[i]"% (varfinal1[ii],varfinal1[ii]))
                            for ii in xrange(len(varfinal2)):
                                exec("%s[c]=%s[i]"% (varfinal2[ii],varfinal2[ii]))
                            for ii in xrange(len(varfinal3)):
                                exec("%s[c]=%s[i+1]"% (varfinal3[ii],varfinal3[ii]))
                        else:
                            Wspd1[c]=avg_wind_int1_f2[i]
                            Wdir1[c]=wind_dir1_f2[i]
                            Gust1[c]=wind_gust1_f2[i]
                            for ii in xrange(len(varfinal1)):
                                exec("%s[c]=%s[i+1]"% (varfinal1[ii],varfinal1[ii]))
                            for ii in xrange(len(varfinal2)):
                                exec("%s[c]=%s[i+1]"% (varfinal2[ii],varfinal2[ii]))
                            for ii in xrange(len(varfinal3)):
                                exec("%s[c]=%s[i]"% (varfinal3[ii],varfinal3[ii]))
                        c=c+1
                        i=i+2
                        continue
                else:
                    if int(flag[i])==1:
                        Wspd1[c]=avg_wind_int1[i]
                        Wdir1[c]=wind_dir1[i]
                        Gust1[c]=wind_gust1[i]
                    else:
                        Wspd1[c]=avg_wind_int1_f2[i]
                        Wdir1[c]=wind_dir1_f2[i]
                        Gust1[c]=wind_gust1_f2[i]
                    for ii in xrange(len(variables10)):
                        exec("%s[c]=%s[i]"% (variables10[ii],variables10[ii]))
                    c=c+1
                    i=i+1
                    continue
            elif i==(len(Epoca)-1):
                if int(flag[i])==1:
                    Wspd1[c]=avg_wind_int1[i]
                    Wdir1[c]=wind_dir1[i]
                    Gust1[c]=wind_gust1[i]
                else:
                    Wspd1[c]=avg_wind_int1_f2[i]
                    Wdir1[c]=wind_dir1_f2[i]
                    Gust1[c]=wind_gust1_f2[i]
                for ii in xrange(len(variables10)):
                    exec("%s[c]=%s[i]"% (variables10[ii],variables10[ii]))
                i=i+1
                c=c+1
            else:
                continue
        print(c)  
        for ii in xrange(len(variables10)):
            exec("%s=%s[0:c]"% (variables10[ii],variables10[ii]))
        for ii in xrange(len(varfinal4)):
            exec("%s=%s[0:c]"% (varfinal4[ii],varfinal4[ii]))
        
    ano,mes,dia,hora=[0]*len(Epoca),[0]*len(Epoca),[0]*len(Epoca),[0]*len(Epoca)
    for ie in xrange(c):       
        [ano[ie],mes[ie],dia[ie],hora[ie],minuto,seg,dd,ddd,dddd]=time.gmtime(float(Epoca[ie]))
        for i in xrange(len(variables3)):
            exec("%studo.append(str(%s[ie]))"%(variables3[i],variables3[i]))
        for i in xrange(len(variables2)):
            exec("%studo.append(str(%s))"%(variables2[i],-9999))
        buoytudo.append(str(boiasu2))
        IDtudo.append(str(boiasu))                    
        Minutetudo.append(str(21))
        fontetudo.append(str(1))
    
    print('xxx')
    if Epocatudo!=[]:
        print(max(Epocatudo))
    print('xxx')    
    datausp = np.array([argos_id1tudo,Epocatudo,buoytudo,IDtudo,flagtudo,lattudo,lontudo,anotudo,mestudo,diatudo,horatudo,Minutetudo,id_sattudo,n_ident_msgtudo,n_msg_sattudo,freq_sattudo,n_msg_dbtudo,best_dbtudo,quali_indtudo,n_lin_msgtudo,battery_voltagetudo,position_statustudo,solar_currenttudo,boot_timestudo,flood_leveltudo,buoy_headingtudo,Wspd1tudo,Wdir1tudo,Gust1tudo,avg_wind_int2tudo,avg_wind_dir2tudo,avg_wind_gust2tudo,temp_airtudo,pressuretudo,dew_pointtudo,rel_humidtudo,avg_radiationtudo,ssttudo,clhtudo,turbtudo,CM_int1tudo,CM_dir1tudo,CM_int2tudo,CM_dir2tudo,CM_int3tudo,CM_dir3tudo,HStudo,H_maxtudo,Tptudo,Mn_dirtudo,Mn_spreadtudo,Lon02tudo,Lat02tudo,Lon_sattudo,Lat_sattudo,Date_sattudo,Time_sattudo,fontetudo])
    datausp = datausp.transpose()
    datausp1=sorted(datausp, key=operator.itemgetter(1,2))
    header="argosid_tudo,Epocatudo,buoytudo,IDtudo,flagtudo,lattudo,lontudo,anotudo,mestudo,diatudo,horatudo,Minutetudo,id_sattudo,n_ident_msgtudo,n_msg_sattudo,freq_sattudo,n_msg_dbtudo,best_dbtudo,quali_indtudo,n_lin_msgtudo,battery_voltagetudo,position_statustudo,solar_currenttudo,boot_timestudo,flood_leveltudo,buoy_headingtudo,Wspd1tudo,Wdir1tudo,Gust1tudo,avg_wind_int2,avg_wind_dir2,avg_wind_gust2,temp_airtudo,pressuretudo,dew_pointtudo,rel_humidtudo,avg_radiationtudo,ssttudo,clhtudo,turbtudo,CM_int1tudo,CMdir1tudo,CM_int2tudo,CMdir2tudo,CM_in21tudo,CMdir2tudo,HStudo,H_maxtudo,Tptudo,Mn_dirtudo,Mn_spreadtudo,Lon02tudo,Lat02tudo,Lon_sattudo,Lat_sattudo,Date_sattudo,Time_sattudo,fontetudo"
    np.savetxt("c:\\ndbc\\sql\\dados\\usp\\2_consolidado.csv", datausp1,'%s',delimiter=",",header=header)
    
    db.close()

    return datausp1

def boiasfuncionando():

    boias=['SANTOS','VITORIA']
    boias2=[69150,146448]

    return boias,boias2
    
#############
## início da rotina
#############


variables=['argos_id1','Epoca','buoy','ID','sensor00','Lat','Lon','Year','Month','Day','Hour','Minute','id_sat','n_msg_sat','freq_sat','n_msg_db','best_db','n_ident_msg','quali_ind','n_lin_msg','Battery','loc_class','Solar','boot_times','flood','bHead','Wspd1','Wdir1','Gust1','Wspd2','Wdir2','Gust2','Atmp','Pres','Dewp','Humi','Arad','Wtmp','Cloro','Turb','Cvel1','Cdir1','Cvel2','Cdir2','Cvel3','Cdir3','Wvht','Wmax','Dpd','Mwd','Spred','Lat02','Lon02','Lat_sat','Lon_sat','Date_sat','Time_sat']

(boias,boias2)=boiasfuncionando()

for s in xrange(len(boias)):

    Data1=buscabd_usp2(boias[s],boias2[s])
    
    
    for i in xrange(len(variables)):
        for ii in xrange(len(Data1)):
            if Data1[ii][i]==9999 or Data1[ii][i]==99.99 or  Data1[ii][i]==None or  Data1[ii][i]=='None':            
                Data1[ii][i]=-9999
            else:
                continue

    for ii in xrange(len(variables)):
        exec("%s=[0]*len(Data1)" % (variables[ii]))
    
    c=0
    
    for i in xrange(len(Data1)):
        if int(Data1[i][3])==int(boias[s]):
            for ii in xrange(len(variables)):
                if variables[ii]=='Epoca':
                    exec("%s[c]=float(Data1[i][ii])"% (variables[ii]))                                        
                else:
                    exec("%s[c]=Data1[i][ii]"% (variables[ii]))
            c=c+1
        else:
            continue
    
    for ii in xrange(len(variables)):
        exec("%s=%s[0:c]"% (variables[ii],variables[ii]))
      
    # transformando o que é missing value em None  
    for ii in xrange(len(variables)):
        for i in xrange(len(Year)):
            exec("var=%s[i]"% (variables[ii]))            
            if var==9999 or var==99.99 or var==None or var=='-9999'  or var=='-99999'  or var==-99999 or var=='' or var=='99.99' or var=='-9999.0' or var==-9999.0:
              exec("%s[i]=-9999"% (variables[ii]))
            else:
                continue
    
    # criação da variável de entrada para a rotina de aplicação de QC    
    data1=[]
    data1=[Year,Month,Day,Hour,Minute,Wdir1,Wspd1,Gust1,Wdir2,Wspd2,Gust2,Wvht,Wmax,Dpd,Mwd,Pres,Humi,Atmp,Wtmp,Dewp,Cvel1,Cdir1,Cvel2,Cdir2,Cvel3,Cdir3,Battery]
    
    dados_boia=[]
    for i in xrange(len(dados_disp)):
        if dados_disp[i][0]==boias[s]:
            dados_boia.append(dados_disp[i])
    #rotina de aplicação do QC
#    try:
    if len(Epoca)>=3:
        (data,flag,flagid,Wspd1flag,Wspd1flagid,Wspd2flag,Wspd2flagid)=qualitycontrol2(Epoca,data1,variables1,variables2,dados_boia)
        
#        variables1=['Year','Month','Day','Hour','Minute','Wdir1','Wspd1','Gust1','Wdir2','Wspd2','Gust2','Wvht','Wmax','Dpd','Mwd','Pres','Humi','Atmp','Wtmp','Dewp','Cvel1','Cdir1','Cvel2','Cdir2','Cvel3','Cdir3','Battery']
#        variables2=['Wdir1','Wspd1','Gust1','Wdir2','Wspd2','Gust2','Wvht','Wmax','Dpd','Mwd','Pres','Humi','Atmp','Wtmp','Dewp','Cvel1','Cdir1','Cvel2','Cdir2','Cvel3','Cdir3']          
#        variables3=['Wdir','Wspd','Gust','Wvht','Wmax','Dpd','Mwd','Pres','Humi','Atmp','Wtmp','Dewp','Cvel1','Cdir1','Cvel2','Cdir2','Cvel3','Cdir3']          

#    except:
#        exec("logging.debug('%s Erro7=: Nao foi possivel rodar os testes de qualificacao')" % (temporeal))
#        sys.exit(1)          

#    try:
#        (posflag)=latlonqc(Lat,Lon,Epoca,s)
#    except:
#        exec("logging.debug('%s Erro8=: Nao foi possivel rodar os testes de controle de posicao da boia')" % (temporeal))
#        sys.exit(1)              
    
    #renomeando as variáveis para salvar o arquivo final    

        for ii in xrange(len(variables1a)):
            exec("%s=data[ii]"% (variables1a[ii]))
    
        for ii in xrange(len(variables3)):
            exec("%sflag=flag[ii]"% (variables3[ii]))
            exec("%sflagid=flagid[ii]"% (variables3[ii]))        


        for i in xrange(len(Wdir)):
            aw=int(Year[i])-2002    
            if boias2[s]=='SANTACATARINA':
                decmag=17.59
                decvar=0.13
            elif boias2[s]=='SANTOS':
                decmag=20.01
                decvar=0.11
            elif boias2[s]=='RIOGRANDE':
                decmag=14.87
                decvar=0.14
            elif boias2[s]=='CABOFRIO':
                decmag=21.08
                decvar=0.09
            elif boias2[s]=='PORTOSEGURO':
                decmag=23.35
                decvar=0.04
            elif boias2[s]=='RECIFE':
                decmag=21.74
                decvar=0.03
            elif boias2[s]=='VITORIA':
                decmag=22.9
                decvar=0.05
            elif boias2[s]=='GUANABARA':
                decmag=21.31
                decvar=0.08
            print(decmag)
            print(decvar)
            var=Cdir1[i]
            if var!=9999 or var!=99.99 or var!=None or var!='-9999'  or var!='-99999'  or var!=-99999 or var!='' or var!='99.99' or var!='-9999.0' or var!=-9999.0:
                Cdir1[i]=int(arredondar(float(Cdir1[i])-(decmag+(decvar*aw))))
                if float(Cdir1[i])>360:
                    Cdir1[i]=float(Cdir1[i])-360
                elif float(Cdir1[i])<0:
                    Cdir1[i]=float(Cdir1[i])+360
            var=Cdir2[i]
            if var!=9999 or var!=99.99 or var!=None or var!='-9999'  or var!='-99999'  or var!=-99999 or var!='' or var!='99.99' or var!='-9999.0' or var!=-9999.0:
                Cdir2[i]=int(arredondar(float(Cdir2[i])-(decmag+(decvar*aw))))
                if float(Cdir2[i])>360:
                    Cdir2[i]=float(Cdir2[i])-360
                elif float(Cdir2[i])<0:
                    Cdir2[i]=float(Cdir2[i])+360      
            var=Cdir3[i]
            if var!=9999 or var!=99.99 or var!=None or var!='-9999'  or var!='-99999'  or var!=-99999 or var!='' or var!='99.99' or var!='-9999.0' or var!=-9999.0:
                Cdir3[i]=int(arredondar(float(Cdir3[i])-(decmag+(decvar*aw))))
                if float(Cdir3[i])>360:
                    Cdir3[i]=float(Cdir3[i])-360
                elif float(Cdir3[i])<0:
                    Cdir3[i]=float(Cdir3[i])+360
            var=Wdir[i]
            if var!=9999 or var!=99.99 or var!=None or var!='-9999'  or var!='-99999'  or var!=-99999 or var!='' or var!='99.99' or var!='-9999.0' or var!=-9999.0:
                Wdir[i]=int(arredondar(float(Wdir[i])-(decmag+(decvar*aw))))
                if float(Wdir[i])>360:
                    Wdir[i]=float(Wdir[i])-360
                elif float(Wdir[i])<0:
                    Wdir[i]=float(Wdir[i])+360      
            var=Mwd[i]
            if var!=9999 or var!=99.99 or var!=None or var!='-9999'  or var!='-99999'  or var!=-99999 or var!='' or var!='99.99' or var!='-9999.0' or var!=-9999.0:
                Mwd[i]=int(arredondar(float(Mwd[i])-(decmag+(decvar*aw))))
                if float(Mwd[i])>360:
                    Mwd[i]=float(Mwd[i])-360
                elif float(Mwd[i])<0:
                    Mwd[i]=float(Mwd[i])+360   
  
    
#   salvando os arquivos finais em TXT  
    
    
#    data = np.array([argos_id1,Epoca,buoy,ID,Lat,Lon,Year,Month,Day,Hour,Minute,id_sat,n_ident_msg,n_msg_sat,freq_sat,n_msg_db,best_db,quali_ind,n_lin_msg,Battery,loc_class,Solar,boot_times,flood,bHead,Wspd,Wdir,Gust,Atmp,Pres,Dewp,Humi,Arad,Wtmp,Cloro,Turb,Cvel1,Cdir1,Cvel2,Cdir2,Cvel3,Cdir3,Wvht,Wmax,Dpd,Mwd,Spred,Lon02,Lat02,Lon_sat,Lat_sat,Date_sat,Time_sat])
#    data = data.transpose()
#    header="Epoca,buoy,ID,Lat,Lon,Year,Month,Day,Hour,Minute,id_sat,n_ident_msg,n_msg_sat,freq_sat,n_msg_db,best_db,quali_ind,n_lin_msg,Battery,loc_class,Solar,boot_times,flood,bHead,Wspd,Wdir,Gust,Atmp,Pres,Dewp,Humi,Arad,Wtmp,Cloro,Turb,Cvel1,Cdir1,Cvel2,Cdir2,Cvel3,Cdir3,Wvht,Wmax,Dpd,Mwd,Spred"
#    np.savetxt("c:\\ndbc\\sql\\dados\\tratados2"+str(boias[s])+".csv", data,'%s',delimiter=" ",header=header)
    
    ##############################################################################
    #
    # ETAPA 15 - PREPARANDO OS ARQUIVOS PARA ALIMENTAR AS TABELAS DE DADOS QUALIFICADOS
    #
    ##############################################################################
    
    #padronizando o missing value para 9999

    if len(Epoca)>=3:
        for ii in xrange(len(variables0)):
            for i in xrange(len(Year)):
                exec("var=%s[i]"% (variables0[ii]))            
                if var==9999 or var==99.99 or var==None or var=='-9999'  or var=='-99999'  or var==-99999 or var=='' or var=='99.99' or var=='-9999.0' or var==-9999.0 or var=='-99999.0':
                    exec("%s[i]=-9999"% (variables0[ii]))
                else:
                    continue
        
        #preparando os arquivos para salvar todos os dados tratados juntos para alimentacao do banco    
    
        for ii in xrange(len(ID)):
            if int(idValid[s][1])==int(ID[ii]):
                if float(Epoca[ii])>float(idValid[s][2]):
                    for iw in xrange(len(variables0)):
                        exec("%stratados1.append(%s[ii])"% (variables0[iw],variables0[iw]))
                    for iw in xrange(len(variables3)):
                        exec("%sflagtratados1.append(%sflag[ii])"% (variables3[iw],variables3[iw]))
                        exec("%sflagidtratados1.append(%sflagid[ii])"% (variables3[iw],variables3[iw]))                


print('done')

print(len(argos_id1tratados1))

##############################################################################
#
# ETAPA 16 - SALVANDO OS TXT DE TODOS OS DADOS PARA OS DADOS QUALIFICADOS
#
##############################################################################
Data=[]
Data=np.array([argos_id1tratados1,Epocatratados1,buoytratados1,IDtratados1,Lattratados1,Lontratados1,Yeartratados1,Monthtratados1,Daytratados1,Hourtratados1,Minutetratados1,id_sattratados1,n_ident_msgtratados1,n_msg_sattratados1,freq_sattratados1,n_msg_dbtratados1,best_dbtratados1,quali_indtratados1,n_lin_msgtratados1,Batterytratados1,loc_classtratados1,Solartratados1,boot_timestratados1,floodtratados1,bHeadtratados1,Wspdtratados1,Wspdflagtratados1,Wspdflagidtratados1,Wdirtratados1,Wdirflagtratados1,Wdirflagidtratados1,Gusttratados1,Gustflagtratados1,Gustflagidtratados1,Atmptratados1,Atmpflagtratados1,Atmpflagidtratados1,Prestratados1,Presflagtratados1,Presflagidtratados1,Dewptratados1,Dewpflagtratados1,Dewpflagidtratados1,Humitratados1,Humiflagtratados1,Humiflagidtratados1,Aradtratados1,Wtmptratados1,Wtmpflagtratados1,Wtmpflagidtratados1,Clorotratados1,Turbtratados1,Cvel1tratados1,Cvel1flagtratados1,Cvel1flagidtratados1,Cdir1tratados1,Cdir1flagtratados1,Cdir1flagidtratados1,Cvel2tratados1,Cvel2flagtratados1,Cvel2flagidtratados1,Cdir2tratados1,Cdir2flagtratados1,Cdir2flagidtratados1,Cvel3tratados1,Cvel3flagtratados1,Cvel3flagidtratados1,Cdir3tratados1,Cdir3flagtratados1,Cdir3flagidtratados1,Wvhttratados1,Wvhtflagtratados1,Wvhtflagidtratados1,Wmaxtratados1,Wmaxflagtratados1,Wmaxflagidtratados1,Dpdtratados1,Dpdflagtratados1,Dpdflagidtratados1,Mwdtratados1,Mwdflagtratados1,Mwdflagidtratados1,Spredtratados1,Lon02tratados1,Lat02tratados1,Lon_sattratados1,Lat_sattratados1,Date_sattratados1,Time_sattratados1])
Data = Data.transpose()
Data1=sorted(Data, key=operator.itemgetter(1,3))
header="argos_id1tratados,Epocatratados,buoytratados,IDtratados,Lattratados,Lontratados,Yeartratados,Monthtratados,Daytratados,Hourtratados,Minutetratados,id_sattratados,n_ident_msgtratados,n_msg_sattratados,freq_sattratados,n_msg_dbtratados,best_dbtratados,quali_indtratados,n_lin_msgtratados,Batterytratados,loc_classtratados,Solartratados,boot_timestratados,floodtratados,bHeadtratados,Wspdtratados,Wspdflagtratados,Wspdflagidtratados,Wdirtratados,Wdirflagtratados,Wdirflagidtratados,Gusttratados,Gustflagtratados,Gustflagidtratados,Atmptratados,Atmpflagtratados,Atmpflagidtratados,Prestratados,Presflagtratados,Presflagidtratados,Dewptratados,Dewpflagtratados,Dewpflagidtratados,Humitratados,Humiflagtratados,Humiflagidtratados,Aradtratados,Wtmptratados,Wtmpflagtratados,Wtmpflagidtratados,Clorotratados,Turbtratados,Cvel1tratados,Cvel1flagtratados,Cvel1flagidtratados,Cdir1tratados,Cdir1flagtratados,Cdir1flagidtratados,Cvel2tratados,Cvel2flagtratados,Cvel2flagidtratados,Cdir2tratados,Cdir2flagtratados,Cdir2flagidtratados,Cvel3tratados,Cvel3flagtratados,Cvel3flagidtratados,Cdir3tratados,Cdir3flagtratados,Cdir3flagidtratados,Wvhttratados,Wvhtflagtratados,Wvhtflagidtratados,Wmaxtratados,Wmaxflagtratados,Wmaxflagidtratados,Dpdtratados,Dpdflagtratados,Dpdflagidtratados,Mwdtratados,Mwdflagtratados,Mwdflagidtratados,Spredtratados,Lon02tratados,Lat02tratados,Lon_sattratados,Lat_sattratados,Date_sattratados,Time_sattratados"
np.savetxt("c:\\ndbc\\sql\\dados\\argos_tratados3.csv", Data1,'%s',delimiter=",",header=header)


