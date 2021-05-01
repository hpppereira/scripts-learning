# -*- coding: cp1252 -*-

#agora vai, iniciando

#carrega arquivo
#tempo (s)","temp ar","Umid (%)","pressao (hpa)","vel vent","dir vento","temp agua"
#data=open('C:\Python26\meteo.txt','r')

#importa modulos
#import numpy as np
#from scipy import *
import matplotlib.pyplot as plt

#import numpy as np ; from numpy import *

t,tar,ur,pr,velv,dirv,tag=loadtxt('/home/hppp/Dropbox/aprendendopython/meteo.txt', unpack=True)

f1=plt.figure()
plt.plot(t,tar)
plt.title('temp do ar')
f2=plt.figure()
plt.plot(t,ur)
f3=plt.figure()
plt.hist(tar)

#plt.show()
#plt.close()

import soma
a=soma.soma(3)


