#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 12:36:22 2018

@author: saaitama
"""
import pandas as pd
import numpy as np

for i in range(22):
    a= pd.DataFrame()
    b= pd.DataFrame()
    a = pd.read_csv('p{}_hs_1979_2009.txt'.format(i+1), sep=r"\s*", skiprows= 1, header= None)
    b = pd.read_csv('p{}_t02_1979_2009.txt'.format(i+1), sep=r"\s*", skiprows= 1, header= None)
    a.columns = ["Date", "Longitud", "Latitud", "Hs"]
    b.columns = ["Date", "Longitud", "Latitud", "Tp"]
    a["Tp"] = b["Tp"]
    d = []
    m = []
    an = []
    for j in a.Date:
        d.append(j[-2:])
        m.append(j[5:7])
        an.append(j[:4])
    hr = []
    hr1 =np.arange(0,24)
    for k in range(int(len(a)/24)):
        for n in hr1:
            hr.append(n)
    a["Hora"] = hr
    a["Dia"] = d
    a["Mes"] = m
    a["Anio"] = an
    a.to_csv("p{}.csv".format(i+1))