#!/bin/sh
# izabel nogueira - LIOC
# extrai valor do grb2

#colocar o ano que vc quer extrair os valores (no caso 2010)
# mudar coordenadas do ponto (-lon -38.44 -13.27) lon/lat
# nesse exemplo eu extrai mais de um ponto (#RosmanP22,#RosmanP23,#RosmanP32...)
for f in wnd10m.cdas1.201407*
do
    echo "processing $f"
        # wgrib2 $f -lon -40.2087 -20.3402 -vt -ext_name > CFSR_VALE_ADCP01_201304.out
        # wgrib2 $f -lon -47.366 -28.500 -vt -ext_name > CFSR_FLN_201206.out
        # wgrib2 $f -lon -44.933 -25.283 -vt -ext_name > CFSR_SAN_2013.out 
        wgrib2 $f -lon -49.966 -31.566 -vt -ext_name > CFSR_RIG_2013.out 
    #    head -n -2 temp.out >> CFSR_Florian.out
done

grep -n 'UGRD' CFSR_RIG_201407.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > uCFSR_RIG_201407.txt
grep -n 'VGRD' CFSR_RIG_201407.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > vCFSR_RIG_201407.txt
grep -n 'UGRD' CFSR_RIG_201407.out | cut -f5 -d: | cut -f2 -d= > time_CFSR_RIG_201407.txt