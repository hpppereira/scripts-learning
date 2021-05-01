'''
Evolucao especrtal com e sem triad
'''

import os
import numpy as np

pathname = os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/mod/'

esp_mod_tri  = np.loadtxt(pathnamem + 'espe1d_mod_201302_comtriad_ADCP04.txt')
freq_mod_tri = np.loadtxt(pathnamem + 'freq_mod_201302_comtriad_ADCP04.txt')
date_swn, hm0_swn_tri, tp_swn_tri, dp_swn_tri = np.loadtxt(os.environ['HOME'] + '/Dropbox/ww3vale/trocas/msc_isa/Espectros/triad/201302/comtriad/table_point_adcp04.out',
 skiprows=7, usecols=(0,1,3,2), unpack=True)

esp_mod  = np.loadtxt(pathnamem + 'espe1d_mod_201302_semtriad_ADCP04.txt')
freq_mod = np.loadtxt(pathnamem + 'freq_mod_201302_semtriad_ADCP04.txt')
date_swn, hm0_swn, tp_swn, dp_swn = np.loadtxt(os.environ['HOME'] + '/Dropbox/ww3vale/trocas/msc_isa/Espectros/triad/201302/semtriad/table_point_adcp04.out',
 skiprows=7, usecols=(0,1,3,2), unpack=True)


#carrega parametros do modelo
