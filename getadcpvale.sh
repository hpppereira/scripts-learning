#!/bin/bash

#roda a rotina em python que gera os dados da hora atual
/usr/local/python/anaconda/bin/python /home/lioc/Dropbox/ww3vale/TU/rot/getadcpvale.py

#concatena dados da boia 4
cat /home/lioc/Dropbox/ww3vale/TU/dados/ADCP/operacional/aux_TU_boia04.out >> /home/lioc/Dropbox/ww3vale/TU/dados/ADCP/operacional/TU_boia04.out

#concatena dados da boia 10
cat /home/lioc/Dropbox/ww3vale/TU/dados/ADCP/operacional/aux_TU_boia10.out >> /home/lioc/Dropbox/ww3vale/TU/dados/ADCP/operacional/TU_boia10.out
