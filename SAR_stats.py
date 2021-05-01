# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 10:40:04 2021

@author: Laura e Henrique
"""

import math
import numpy as np
import pandas as pd
import geopandas as gpd
import descarteslabs as dl
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

#Reading the processed SAR data file
dsar = pd.read_csv('s1a-20170130-5km.txt', skiprows=2, sep= '\s+')

SWH = dsar['SWH'].values

# Gridding the data to match Latitude and Longitude
xi, yi = np.meshgrid(np.linspace(dsar.LON.min(),dsar.LON.max(),len(dsar)),
                     np.linspace(dsar.LAT.min(),dsar.LAT.max(),len(dsar)))

# Adding a specific parameter to the grid
zi = griddata((dsar.LON, dsar.LAT), dsar.SWH, (xi, yi), method='linear')

#Calculating statistics mean, variance and standard deviation
MEAN = np.zeros((len(dsar), len(dsar)))
VAR = np.copy(MEAN)
STD = np.copy(MEAN)

for x in range(1,len(dsar)-2):
    for y in range(1,len(dsar)-2):
        print (x, y)

        MEAN[x,y] = 1/9*((zi[x-2,y-2])+
                    (zi[x,y-2])+
                    (zi[x+2,y-2])+
                    (zi[x-2,y])+
                    (zi[x,y])+
                    (zi[x+2,y])+
                    (zi[x-2,y+2])+
                    (zi[x,y+2])+
                    (zi[x+2,y+2]))

        VAR[x,y] = 1/9*((zi[x-2,y-2]-MEAN[x,y])**2+
                        (zi[x,y-2]-MEAN[x,y])**2+
                        (zi[x+2,y-2]-MEAN[x,y])**2+
                        (zi[x-2,y]-MEAN[x,y])**2+
                        (zi[x,y]-MEAN[x,y])**2+
                        (zi[x+2,y]-MEAN[x,y])**2+
                        (zi[x-2,y+2]-MEAN[x,y])**2+
                        (zi[x,y+2]-MEAN[x,y])**2+
                        (zi[x+2,y+2]-MEAN[x,y])**2)
    
        STD[x,y] = math.sqrt(VAR[x,y])


#Plotting the parameter original data
#Fig1 = plt.contour(xi,yi,zi,15,linewidths=0.1,colors='k')
#Fig1 = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)

#Plotting the Florida map
cs=gpd.read_file('cb_2018_12_bg_500k.shp', SHAPE_RESTORE_SHX='YES')
#cs.plot()

#Plotting the parameter data above as a layer BEHIND the Florida map
fig, ax = plt.subplots(2, 2)
ax[0, 0]
cs.plot(cmap='binary')
Fig1 = plt.contour(xi,yi,zi,15,linewidths=0.1,colors='k')
Fig1 = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)
plt.plot(-82.9313,27.5903,'o') 

ax[1, 0]
#fig, ax = plt.subplots(1)
cs.plot(cmap='binary')
Fig2 = plt.contour(xi,yi,MEAN,15,linewidths=0.1,colors='k')
Fig2 = plt.contourf(xi,yi,MEAN,15,cmap=plt.cm.jet)
plt.plot(-82.9313,27.5903,'o') 
#plt.show()

ax[0, 1]
cs.plot(cmap='binary')
Fig3 = plt.contour(xi,yi,VAR,15,linewidths=0.1,colors='k')
Fig3 = plt.contourf(xi,yi,VAR,15,cmap=plt.cm.jet)
plt.plot(-82.9313,27.5903,'o') 

ax[1, 1]
cs.plot(cmap='binary')
Fig4 = plt.contour(xi,yi,STD,15,linewidths=0.1,colors='k')
Fig4 = plt.contourf(xi,yi,STD,15,cmap=plt.cm.jet)
plt.plot(-82.9313,27.5903,'o') 

plt.show()

#Plotting the original parameter points and the buoy location
#plt.plot(dsar.LON,dsar.LAT,'.')
#plt.plot(-82.9313,27.5903,'o') 
#plt.show()