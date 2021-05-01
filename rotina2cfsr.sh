#!/bin/sh
# izabel nogueira - LIOC
# rotina para pegar os valores de Hs, Tp e Dp dos dados tirados do grib2 por probeWWIII
# CFSR_P22.out - arquivo gerado quando vc roda a rotina1.
# uP22.txt e vP22.txt arquivos com a serie de u e v para o ponto de interesse
# time.txt data para as quais vc extraiu os valores de u e v

grep -n 'UGRD' CFSR_IlhaRasa_201410.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > uCFSR_IlhaRasa_201410.txt
grep -n 'VGRD' CFSR_IlhaRasa_201410.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > vCFSR_IlhaRasa_201410.txt
grep -n 'UGRD' CFSR_IlhaRasa_201410.out | cut -f5 -d: | cut -f2 -d= > time_IlhaRasa_201410.txt


#grep -n 'UGRD' CFSR_FLN_201206.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > uCFSR_FLN_201206.txt
#grep -n 'VGRD' CFSR_FLN_201206.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > vCFSR_FLN_201206.txt
#grep -n 'UGRD' CFSR_FLN_201206.out | cut -f5 -d: | cut -f2 -d= > time_FLN_201206.txt

#grep -n 'UGRD' CFSR_SAN_201206.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > uCFSR_SAN_201206.txt
#grep -n 'VGRD' CFSR_SAN_201206.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > vCFSR_SAN_201206.txt
#grep -n 'UGRD' CFSR_SAN_201206.out | cut -f5 -d: | cut -f2 -d= > time_SAN_201206.txt
