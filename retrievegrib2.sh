#!/bin/sh
#Retrieve forecast data from WW3 using wgrib2

wgrib2 -match ":(VGRD|UGRD|TMP): 100mb" nww3.t00z.grib.grib2 -lon -40.2087 -20.3402 -csv csvfile

# for f in wnd10m.cdas1.201304*
# do
# 	echo "processing $f"
#         wgrib2 $f -lon -40.2087 -20.3402 -vt -ext_name > CFSR_VALE_ADCP01_201304.out
#         #wgrib2 $f -lon -47.366 -28.500 -vt -ext_name > CFSR_FLN_201206.out
#         #wgrib2 $f -lon -44.933 -25.283 -vt -ext_name > CFSR_SAN_201206.out 
#     #    head -n -2 temp.out >> CFSR_Florian.out
# done
