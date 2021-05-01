#!/bin/sh
# izabel nogueira - LIOC
# rotina para pegar os valores de Hs, Tp e Dp dos dados tirados do grib2 por probeWWIII
#grep -n 'DIRPW'  WWIII_55E15N.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > dp48W0.5S.txt
#grep -n 'PERPW'  WWIII_55E15N.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > tp48W0.5S.txt
#grep -n 'HTSGW'  WWIII_55E15N.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > hs48W0.5S.txt
#grep -n 'UGRD'  WWIII_55E15N.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > u48W0.5S.txt
#grep -n 'VGRD'  WWIII_55E15N.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > v48W0.5S.txt
#grep -n 'HTSGW'  WWIII_55E15N.out | cut -f5 -d: | cut -f2 -d= > time48W0.5S.txt
grep -n 'UGRD'  CFSR_P22.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > uP22.txt
grep -n 'VGRD'  CFSR_P22.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > vP22.txt
grep -n 'UGRD'  CFSR_P23.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > uP23.txt
grep -n 'VGRD'  CFSR_P23.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > vP23.txt
grep -n 'UGRD'  CFSR_P32.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > uP32.txt
grep -n 'VGRD'  CFSR_P32.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > vP32.txt
grep -n 'UGRD'  CFSR_P33.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > uP33.txt
grep -n 'VGRD'  CFSR_P33.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > vP33.txt
grep -n 'UGRD'  CFSR_P42.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > uP42.txt
grep -n 'VGRD'  CFSR_P42.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > vP42.txt
grep -n 'UGRD'  CFSR_P43.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > uP43.txt
grep -n 'VGRD'  CFSR_P43.out | cut -f4 -d: | cut -f3 -d, | cut -f2 -d= > vP43.txt
grep -n 'VGRD'  CFSR_P43.out | cut -f5 -d: | cut -f2 -d= > time.txt
