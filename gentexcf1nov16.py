# -*- coding: utf-8 -*-
#!/usr/local/bin/python

'''
Programa para rodar o .tex
da previsao global com dados da NDBC
'''

#import numpy as np
import os
#import jinja2
#from jinja2 import Template
#import datetime as dt
#import codecs
#from datetime import datetime
#import pandas as pd

#caminho do template .tex e nome do arquivo 
pathname = os.environ['HOME'] + '/Dropbox/BMOP/Processamento/boletim/CF1_BMOBR05_2016Nov/'

filename = 'Boletim_CF01.tex'

#filename_bkp = filename + '_%s' %dt.datetime.strftime(dt.datetime.now(),'%Y%m%d')

#gera o pdf
os.system('cd ' + pathname + '\n' + 
		  '/usr/bin/pdflatex ' + pathname + filename +'\n')# + 
		  # 'cp ' + pathname + filename + '.pdf ' + pathname + filename_bkp + '.pdf' + '\n')