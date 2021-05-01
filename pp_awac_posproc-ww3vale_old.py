'''
	pos processamento dos 
	dados da vale bruto processados pelo lioc
'''

import numpy as np
from datetime import datetime
import pylab as pl

#  0    1    2    3     4   5    6     7   8 
# ano, mes, dia, hora, hs, hmax, hm0, tp, dp
pathname = '/home/hp/Dropbox/ww3vale_old/Geral/TU/rot/saida/bruto/'
paramw1 = np.loadtxt(pathname + 'paramw1.out')
paramw2 = np.loadtxt(pathname + 'paramw2.out')
paramw3 = np.loadtxt(pathname + 'paramw3.out')
paramw4 = np.loadtxt(pathname + 'paramw4.out')

# datas com datetime
data1 = [ datetime(int(paramw1[i,0]),int(paramw1[i,1]),int(paramw1[i,2]),int(paramw1[i,3])) for i in range(len(paramw1)) ]
data2 = [ datetime(int(paramw2[i,0]),int(paramw2[i,1]),int(paramw2[i,2]),int(paramw2[i,3])) for i in range(len(paramw2)) ]
data3 = [ datetime(int(paramw3[i,0]),int(paramw3[i,1]),int(paramw3[i,2]),int(paramw3[i,3])) for i in range(len(paramw3)) ]
data4 = [ datetime(int(paramw4[i,0]),int(paramw4[i,1]),int(paramw4[i,2]),int(paramw4[i,3])) for i in range(len(paramw4)) ]


pl.figure()
pl.subplot(311)
pl.title('ADCP-1')
# pl.plot(data1,paramw1[:,4],'o',label='Hs')
pl.plot(data1,paramw1[:,6],'o',label='Hm0')
pl.plot(data1,paramw1[:,5],'o',label='Hmax')
pl.legend(loc=0)
pl.subplot(312)
pl.plot(data1,paramw1[:,7],'o',label='Tp')
pl.legend()
pl.subplot(313)
pl.plot(data1,paramw1[:,8],'o',label='Dp')
pl.legend()	

pl.figure()
pl.subplot(311)
pl.title('ADCP-2')
# pl.plot(data2,paramw2[:,4],'o',label='Hs')
pl.plot(data2,paramw2[:,6],'o',label='Hm0')
pl.plot(data2,paramw2[:,5],'o',label='Hmax')
pl.legend()
pl.subplot(312)
pl.plot(data2,paramw2[:,7],'o',label='Tp')
pl.legend()
pl.subplot(313)
pl.plot(data2,paramw2[:,8],'o',label='Dp')
pl.legend()	

pl.figure()
pl.title('ADCP-3')
pl.subplot(311)
# pl.plot(data3,paramw3[:,4],'o',label='Hs')
pl.plot(data3,paramw3[:,6],'o',label='Hm0')
pl.plot(data3,paramw3[:,5],'o',label='Hmax')
pl.legend()
pl.subplot(312)
pl.plot(data3,paramw3[:,7],'o',label='Tp')
pl.legend()
pl.subplot(313)
pl.plot(data3,paramw3[:,8],'o',label='Dp')
pl.legend()	

pl.figure()
pl.subplot(311)
pl.title('ADCP-4')
# pl.plot(data4,paramw4[:,4],'o',label='Hs')
pl.plot(data4,paramw4[:,6],'o',label='Hm0')
pl.plot(data4,paramw4[:,5],'o',label='Hmax')
pl.legend()
pl.subplot(312)
pl.plot(data4,paramw4[:,7],'o',label='Tp')
pl.legend()
pl.subplot(313)
pl.plot(data4,paramw4[:,8],'o',label='Dp')
pl.legend()	

pl.show()