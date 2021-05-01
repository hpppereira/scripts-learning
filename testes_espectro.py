#testes espectro

##Importa bibliotecas
from numpy import *
import numpy as np
from scipy import fft

[t,eta,dspx,dspy] = loadtxt('/home/hppp/Dropbox/Tese_Mestrado/consistencia_python/arq_200905010000.txt', unpack=True)


a = fft(eta)
