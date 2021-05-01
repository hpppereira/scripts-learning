# Rotina para adicionar os dados brutos do PNBOIA
# no banco de dados
#
# Instalacao
# pip3 install git+git://github.com/davispuh/MySQL-for-Python-3
# apt-get install libmysqlclient-dev
# pip install mysql-python

# import MySQLdb
import re
import time  
import csv
from telnetlib import Telnet
import datetime
import numpy as np
import operator
import argosqc as qc
import smtplib
# from pylab import find
# from convert2 import *
import pandas as pd
import sqlalchemy
import MySQLdb
from pandas.io import sql


def boiasfuncionando(bancodedados):
    
    db = MySQLdb.connect(bancodedados['local'],
                         bancodedados['usr'],
                         bancodedados['password'],
                         bancodedados['data_base'])
    
    cur=db.cursor()

    boias=[]
    cur.execute("SELECT estacao_id, argos_id,nome, argos_id, argos_id FROM pnboia_estacao WHERE sit=1")
    for row in cur.fetchall():
        boias.append(row)

    cur.close()
    db.close()

    return boias

def baixar_dados(boia):
    programa = "05655"
    saida = []
    comando = "PRV,5655,DS,,"
    usern="SANTOS_BR"
    passw="IPN_G09"

    try:
        tn = Telnet("65.210.29.2")
    except :
        pass

    #---Login

    try:
        tn.read_until(b"Username: ")
        tn.write(usern.encode('ascii') + b"\n")
        
        tn.read_until(b"Password: ")
        tn.write(passw.encode('ascii') + b"\n")
    
        print ("Login com servidor de dados realizado...")# ,tn.read_until('SERVER', 5)
        print ("Realizando coleta de dados para boia " + str(boia) + "...")

    except:
        pass


    #---Comando para coleta de dados
    #print comando
    print(str(comando) + str(boia) + "\n\r")
    tn.write(passw.encode('ascii') + b"\n")
    comando1=comando+str(boia)
    tn.write(comando1.encode('ascii') + b"\n")
    
    dados = tn.read_until(b'SERVER',5)
    print ("Dado recebidos: \n\r")
    tn.close()
    dados=dados.decode("utf-8")
    if dados[0:7] != "No data":
        dados = dados.replace("\r\n",";")
        dados = re.sub("\s+", ",", dados.strip())
        dados = dados.replace(";,", ";");
        dados = dados.replace(";;", ";");
        dados = dados.replace("/" + programa, programa);
        dados = dados.replace(":,", ":");
        dados = dados.replace(";ARGOS,READY;/ARGOS,READY;/","")
        dados = dados.replace(",?,",",")
        dados = dados.replace(",?","")
        dados = dados + ";;"
        dadoslimpos = dados.replace(";","\n")
        print (str(dados.count(";")) + " linhas recebidas...")
    else:
        print ("Sem dados disponíveis ou sem autorização de acesso.")
    contador = 0
    checkpoint = 0
    resultado = []
    bat = []
    final= []
    
    #with open(str(nome_arq) + '.csv', 'w') as csvfile:
    #    #date, bat, hs, tp, dp, hmax, ws1, wg1, wd1, ws2, wg2, wd2, at, rh, dwp, pr, sst
    #     fieldnames = ['date','bat','hs','tp','dp','hmax','ws1','wg1','wd1','ws2','wg2','wd2','airt','rh','dwp','pr','sst']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore', delimiter = ',')
    #     writer.writeheader()
       
    while contador != dados.count(";"):
        linha = dados[checkpoint:dados.index(";",checkpoint)]
        checkpoint = dados.index(";",checkpoint) + 1
        contador = contador + 1
        if programa in linha[0:6]:
            saida = []
            saidadois = []
            saida = linha.split(",")
            linha = dados[checkpoint:dados.index(";",checkpoint)]
            checkpoint = dados.index(";",checkpoint) + 1
            contador = contador + 1
            if ":" in linha:
                saidadois = linha.split(",")
                linha = dados[checkpoint:dados.index(";",checkpoint)]
                checkpoint = dados.index(";",checkpoint) + 1
                contador = contador + 1
                while programa not in linha[0:6] and contador < dados.count(";") and ":" not in linha:
                    saidadois.extend(linha.split(","))
                    linha = dados[checkpoint:dados.index(";",checkpoint)]
                    checkpoint = dados.index(";",checkpoint) + 1
                    contador = contador + 1
                resultado = saida
                resultado.extend(saidadois)
                try:
                    if len(resultado) >= 42:
                        if int(float(resultado[15])) == 1:
                            bat.append([int(resultado[1]),str(resultado[8]),str(resultado[9]),str(resultado[12]),str(resultado[13]),str(resultado[15]),str(resultado[16]),str(resultado[17]),str(resultado[18]),str(resultado[19]),str(resultado[20]),str(resultado[21]),str(resultado[22]),str(resultado[23]),str(resultado[24]),str(resultado[25]),str(resultado[26]),str(resultado[27]),str(resultado[28]),str(resultado[29]),str(resultado[30]),str(resultado[31]),str(resultado[32]),str(resultado[33]),str(resultado[34]),str(resultado[35]),str(resultado[36]),str(resultado[37]),str(resultado[38]),str(resultado[39]),str(resultado[40])])
                        if int(float(resultado[15])) == 2:
                            bat.append([int(resultado[1]),str(resultado[8]),str(resultado[9]),str(resultado[12]),str(resultado[13]),str(resultado[15]),str(resultado[16]),str(resultado[17]),str(resultado[18]),str(resultado[19]),str(resultado[20]),str(resultado[21]),str(resultado[22]),str(resultado[23]),str(resultado[24]),str(resultado[25]),str(resultado[26]),str(resultado[27]),str(resultado[28]),str(resultado[29]),str(resultado[30]),str(resultado[31]),str(resultado[32]),str(resultado[33]),str(resultado[34]),str(resultado[35]),str(resultado[36]),str(resultado[37]),str(resultado[38]),str(resultado[39]),str(resultado[40])])
                    if len(resultado) == 40 or len(resultado) == 41:
                        if int(float(resultado[8])) == 1:
                            bat.append([int(resultado[1]),"-9999","-9999",str(resultado[5]),str(resultado[6]),str(resultado[8]),str(resultado[9]),str(resultado[10]),str(resultado[11]),str(resultado[12]),str(resultado[13]),str(resultado[14]),str(resultado[15]),str(resultado[16]),str(resultado[17]),str(resultado[18]),str(resultado[19]),str(resultado[20]),str(resultado[21]),str(resultado[22]),str(resultado[23]),str(resultado[24]),str(resultado[25]),str(resultado[26]),str(resultado[27]),str(resultado[28]),str(resultado[29]),str(resultado[30]),str(resultado[31]),str(resultado[32]),str(resultado[33]),str(resultado[34])])
                        if int(float(resultado[8])) == 2:
                            bat.append([int(resultado[1]),"-9999","-9999",str(resultado[5]),str(resultado[6]),str(resultado[8]),str(resultado[9]),str(resultado[10]),str(resultado[11]),str(resultado[12]),str(resultado[13]),str(resultado[14]),str(resultado[15]),str(resultado[16]),str(resultado[17]),str(resultado[18]),str(resultado[19]),str(resultado[20]),str(resultado[21]),str(resultado[22]),str(resultado[23]),str(resultado[24]),str(resultado[25]),str(resultado[26]),str(resultado[27]),str(resultado[28]),str(resultado[29]),str(resultado[30]),str(resultado[31]),str(resultado[32]),str(resultado[33]),str(resultado[34])])
                    if len(resultado) == 35 or len(resultado) == 34:
                        if int(float(resultado[8])) == 1:
                            bat.append([int(resultado[1]),"-9999","-9999",str(resultado[5]),str(resultado[6]),str(resultado[8]),str(resultado[9]),str(resultado[10]),str(resultado[11]),str(resultado[12]),str(resultado[13]),str(resultado[14]),str(resultado[15]),str(resultado[16]),str(resultado[17]),str(resultado[18]),str(resultado[19]),str(resultado[20]),str(resultado[21]),str(resultado[22]),str(resultado[23]),str(resultado[24]),str(resultado[25]),str(resultado[26]),str(resultado[27]),str(resultado[28]),str(resultado[29]),str(resultado[30]),str(resultado[31]),str(resultado[32]),str(resultado[33]),0])
                        if int(float(resultado[8])) == 2:
                            bat.append([int(resultado[1]),"-9999","-9999",str(resultado[5]),str(resultado[6]),str(resultado[8]),str(resultado[9]),str(resultado[10]),str(resultado[11]),str(resultado[12]),str(resultado[13]),str(resultado[14]),str(resultado[15]),str(resultado[16]),str(resultado[17]),str(resultado[18]),str(resultado[19]),str(resultado[20]),str(resultado[21]),str(resultado[22]),str(resultado[23]),str(resultado[24]),str(resultado[25]),str(resultado[26]),str(resultado[27]),str(resultado[28]),str(resultado[29]),str(resultado[30]),str(resultado[31]),str(resultado[32]),str(resultado[33]),0])
                except:
                    print(resultado)
    
    for i in range(len(bat)):
        bat[i][3]=datetime.datetime.strptime(bat[i][3]+" "+bat[i][4], '%Y-%m-%d %H:%M:%S')
    
    return bat

def read_real_time():
    pass

def ultimodado(boia, bancodedados):

    db = MySQLdb.connect(bancodedados['local'],
                         bancodedados['usr'],
                         bancodedados['password'],
                         bancodedados['data_base'])
    
    cur=db.cursor()

    c1=[]

    cur.execute("SELECT data FROM argos_bruto WHERE argos_id=%s\
    ORDER BY data DESC limit 1" % boia)
    for row in cur.fetchall():
        c1.append(row)
    if c1!=[]:
        c1=c1[0][0]
    else:
        c1=datetime.datetime(1900, 1, 1, 00, 00, 00)
    return c1


if __name__ == '__main__':

    bancodados = {'local': "lioc-chm.mysql.uhserver.com",
                  'usr': "chmlioc",
                  'password': "Coppe1@",
                  'data_base':"lioc_chm"}

    boias=boiasfuncionando(bancodados)

    for boia in boias:
        boia=str(boia[1])
        bat = baixar_dados(boia)
        last=ultimodado(boia, bancodados)
        df = pd.DataFrame(columns=['msg_id', 'lat', 'lon', 'argos_id', 'data', 'year',
                                   'month', 'day', 'hour', 'atmp',
                                   'humi', 'dewp', 'pres', 'wtmp', 'bhead',
                                   'cloro', 'turb','arad', 'cvel1', 'cdir1',
                                   'cvel2', 'cdir2', 'cvel3', 'cdir3', 'wvht',
                                   'wmax', 'dpd', 'mwd', 'spr','battery',
                                   'flood', 'wspd1', 'gust1', 'wdir1', 'wspd2', 'gust2', 'wdir2'])
        for i in range(len(bat)):
            l = bat[i]
            if l[3]>last:
                if l[5]=='01':
                    df = df.append({'argos_id': boia,'lat': l[1], 'lon': l[2], 'data': l[3],
                                    'msg_id': l[5],'year':l[6],'month':l[7],'day':l[8],'hour':l[9],
                                    'battery':l[16],'flood':l[19],'wspd1':l[20],'gust1':l[21],
                                    'wdir1':l[22],'wspd2':l[23],'gust2':l[24],'wdir2':l[25]},
                                    ignore_index=True)
                elif l[5] == '02':
                    df = df.append({'argos_id': boia,'lat': l[1], 'lon': l[2], 'data': l[3],
                                    'msg_id': l[5],'wspd1':l[7],'gust1':l[8],'wdir1':l[9],
                                    'atmp':l[10],'humi':l[11],'dewp':l[12],'pres':l[13],
                                    'wtmp':l[14],'bhead':l[16],'cloro':l[17],'turb':l[18],
                                    'arad':l[19],'cvel1':l[20],'cdir1':l[21],'cvel2':l[22],
                                    'cdir2':l[23],'cvel3':l[24],'cdir3':l[25],'wvht':l[26],
                                    'wmax':l[27],'dpd':l[28],'mwd':l[29],'spr':l[30]},
                                    ignore_index=True)

        df.set_index('data', inplace=True)
        
        db = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                       format(bancodados['usr'],
                                                              bancodados['password'], 
                                                              bancodados['local'],
                                                              bancodados['data_base']))
        df.to_sql(con=db, name='argos_bruto', if_exists='append')


