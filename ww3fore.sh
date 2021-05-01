#!/bin/sh
#Retrieve forecast data from WW3 using wgrib2

# for f in wnd10m.cdas1.201304*
# do
# 	echo "processing $f"
#         wgrib2 $f -lon -40.2087 -20.3402 -vt -ext_name > CFSR_VALE_ADCP01_201304.out
#         #wgrib2 $f -lon -47.366 -28.500 -vt -ext_name > CFSR_FLN_201206.out
#         #wgrib2 $f -lon -44.933 -25.283 -vt -ext_name > CFSR_SAN_201206.out 
#     #    head -n -2 temp.out >> CFSR_Florian.out
# done

wgrib2 nww3.t00z.grib.grib2 -lon -40.2087 -20.3402 -vt -ext_name > RIG/NWW3_RIG.out
wgrib2 nww3.t00z.grib.grib2 -lon -47.3660 -28.5000 -vt -ext_name > RIG/NWW3_FLN.out
wgrib2 nww3.t00z.grib.grib2 -lon -44.9330 -25.2830 -vt -ext_name > RIG/NWW3_SAN.out 

grep -n 'UGRD' RIG/NWW3_RIG.out | cut -f5 -d: | cut -f2 -d= > RIG/time_RIG.txt
grep -n 'WIND' RIG/NWW3_RIG.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > RIG/WIND_RIG.txt
grep -n 'UGRD' RIG/NWW3_RIG.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > RIG/UGRD_RIG.txt
grep -n 'VGRD' RIG/NWW3_RIG.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > RIG/VGRD_RIG.txt
grep -n 'WDIR' RIG/NWW3_RIG.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > RIG/WDIR_RIG.txt
grep -n 'HTSGW' RIG/NWW3_RIG.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > RIG/HTSGW_RIG.txt
grep -n 'PERPW' RIG/NWW3_RIG.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > RIG/PERPW_RIG.txt
grep -n 'WVDIR' RIG/NWW3_RIG.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > RIG/WVDIR_RIG.txt
grep -n 'DIRPW' RIG/NWW3_RIG.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > RIG/DIRPW_RIG.txt
grep -n 'WVHGT' RIG/NWW3_RIG.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > RIG/WVHGT_RIG.txt
grep -n 'SWELL' RIG/NWW3_RIG.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > RIG/SWELL_RIG.txt
grep -n 'PERSW' RIG/NWW3_RIG.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > RIG/PERSW_RIG.txt
grep -n 'SWPER' RIG/NWW3_RIG.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > RIG/SWPER_RIG.txt
grep -n 'DIRSW' RIG/NWW3_RIG.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > RIG/DIRSW_RIG.txt
grep -n 'SWDIR' RIG/NWW3_RIG.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > RIG/SWDIR_RIG.txt

