# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 13:46:48 2015

@author: lioc
"""
import re
#from datetime import datetime
#from datetime import timedelta
import time  
import csv
from telnetlib import Telnet

def diffdates(d1, d2):
    #Date format: %Y-%m-%d %H:%M:%S
    return (time.mktime(time.strptime(d2,"%Y-%m-%d %H:%M:%S")) -
               time.mktime(time.strptime(d1, "%Y-%m-%d %H:%M:%S")))

#def Argos(n_argos_boia,nome_arq):
n_argos_boia = "69008"
nome_arq = "teste"
programa = "05655"
saida = []
comando = "PRV,5655,DS,,"
try:
    tn = Telnet("65.210.29.2")
    #tn.set_debuglevel(9)
except Exception,e:
    print e
#---Login
try:
    tn.read_until("Username: ", 10)
    tn.write("convidado" + "\n\r")
    tn.read_until("Password: ", 5)
    tn.write("marinha" + "\n\r")
    print "Login com servidor de dados realizado..."# ,tn.read_until('SERVER', 5)
    print "Realizando coleta de dados para boia " + str(n_argos_boia) + "..."
except Exception,e:
    print e
#---Comando para coleta de dados
#print comando
tn.write(str(comando) + str(n_argos_boia) + "\n\r")
dados = tn.read_until('SERVER', 5)
print "Dado recebidos: \n\r"
tn.close()
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
    print str(dados.count(";")) + " linhas recebidas..."
    print dadoslimpos
else:
    print "Sem dados disponíveis ou sem autorização de acesso."

contador = 0
checkpoint = 0
resultado = []
bat = []
final= []
with open(str(nome_arq) + '.csv', 'w') as csvfile:
    #date, bat, hs, tp, dp, hmax, ws1, wg1, wd1, ws2, wg2, wd2, at, rh, dwp, pr, sst
     fieldnames = ['date','bat','hs','tp','dp','hmax','ws1','wg1','wd1','ws2','wg2','wd2','airt','rh','dwp','pr','sst']
     writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore', delimiter = ',')
     writer.writeheader()    
   
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
#                print "novo resultado:"
#                print resultado
            print len(resultado)
            if len(resultado) == 47:
                print str(len(resultado)) + 'a'
                print str(resultado)
                if resultado[15] == "01":
                    print 'mensagem 01'
                    bat.append([str(resultado[12]) + " " + str(resultado[13]), str(resultado[26]), resultado[30],resultado[31],resultado[32]])
                if resultado[15] == "02":
                    print 'mensagem 02'
                    final = [str(resultado[12]) + " " + str(resultado[13]),"bat",resultado[35],resultado[37],resultado[38],resultado[36],resultado[17],resultado[18],resultado[19],"ws2","wg2","wd2",resultado[20],resultado[21],resultado[22],resultado[23],resultado[24]]
            if len(resultado) == 40 or len(resultado) == 41 or len(resultado) == 43:
                print str(len(resultado)) + 'b'
                print str(resultado)
                if resultado[15] == "01":# or resultado[8] == "01":
                    print 'mensagem 01'
                    bat.append([str(resultado[12]) + " " + str(resultado[13]), str(resultado[26]), resultado[30],resultado[31],resultado[32]])
                if resultado[15] == "02" or resultado[8] == "02":
                    print 'mensagem 02'
                    final = [str(resultado[12]) + " " + str(resultado[13]),"bat",resultado[35],resultado[37],resultado[38],resultado[36],resultado[17],resultado[18],resultado[19],"ws2","wg2","wd2",resultado[20],resultado[21],resultado[22],resultado[23],resultado[24]]
            if len(resultado) == 34 or len(resultado) == 35:
                print str(len(resultado)) + 'c'
                if resultado[8] == "01":
                    print 'mensagem 01'
                    print str(resultado)
                    bat.append([str(resultado[5]) + " " + str(resultado[6]), str(resultado[19]), resultado[23],resultado[24],resultado[25]])
                if resultado[8] == "02":
                    print 'mensagem 02'
                    print str(resultado)
                    final = [str(resultado[5]) + " " + str(resultado[6]),"bat",resultado[29],resultado[30],resultado[31],resultado[29],resultado[10],resultado[11],resultado[12],"ws2","wg2","wd2",resultado[13],resultado[14],resultado[15],resultado[16],resultado[17]]
            
            delta = 0
            indice = 0
            if final != [] and bat!=[]:
                #delta = abs(final[0] - bat[0][0])
                delta = diffdates(final[0],bat[0][0])
                k = 0                    
                for item in bat[1:]:
                    k = k +1
                    if delta < diffdates(final[0],bat[k][0]):
                        delta = diffdates(final[0],bat[k][0])
                        indice = k
                        #limite máximo em segundos para pegar msg SENSOR00=02
                #print delta
                        #2400 = 40 min
                if abs(delta)<2400:
                    final[9] = bat[indice][2]
                    final[10] = bat[indice][3]
                    final[11] = bat[indice][4]
                    final[1] = bat[indice][1]
                else:
                    final[9] = ""
                    final[10] = ""
                    final[11] =""
                    final[1] = ""
                    
           # print "bat:"        
           # print bat
           # print str(delta) + " indice: " + str(indice) + "-- final:"
           # print final           
            if bat==[] and final!=[]:
                final[9] = ""
                final[10] = ""
                final[11] =""
                final[1] = ""

             
             #writer.writerow({'date': final[0], 'bat': final[1], 'hs': final[2], 'tp': final[3] })
            if final != []: 
                with open(str(nome_arq) + '.csv', 'a') as csvfile:
                 #print "incluindo linha:" + str(final)
                 writer = csv.DictWriter(csvfile, lineterminator='\n', fieldnames=fieldnames, extrasaction='ignore', delimiter = ',')
                 writer.writerow({'date': final[0],'bat': final[1],'hs': final[2],'tp': final[3],'dp': final[4],'hmax': final[5],'ws1': final[6],'wg1': final[7],'wd1': final[8],'ws2': final[9],'wg2': final[10],'wd2': final[11],'at': final[12],'rh': final[13],'dwp': final[14],'pr': final[15],'sst': final[16] })


#Argos(69008,"teste")

#format = "%Y-%m-%d %H:%M:%S"
#print (datetime.now() + timedelta(days=1)).strftime(format)
#print datetime.now().strftime(format)
#print diffdates(datetime.now().strftime(format) , (datetime.now() + timedelta(days=1)).strftime(format))
#print diffdates((datetime.now() + timedelta(days=1)).strftime(format),datetime.now().strftime(format))