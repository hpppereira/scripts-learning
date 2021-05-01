'''
Plotagem da PLEDS
para o RT06
Casos: Out e Nov
Plotar 1 semana (pledsSWAN)
'''

import os
import pleds
import matplotlib.pylab as pl

reload(pleds)

pathname = os.environ['HOME'] + '/Dropbox/ww3vale/RT06/Resultados_201511-10'

#adcp 04
espe1, dire1 = pleds.preppledsSWAN(pathname, '/spec_point_ADCP04_201510.out')
espe2, dire2 = pleds.preppledsSWAN(pathname, '/spec_point_ADCP04_201511.out')


espe1 = espe1[:,::3]
dire1 = dire1[:,::3]
espe2 = espe2[:,::3]
dire2 = dire2[:,::3]

#espe1 = espe1[:,-168:]
#dire1 = dire1[:,-168:]

#stop
#pleds.pledsSWAN(espe1,dire1,'Previsao ADCP 04 - ' + str(dia),dia,'teste_pleds.png')
pleds.pleds(espe1,dire1,'Previsao ADCP 10 - 201510','teste_pleds.png')
pleds.pleds(espe2,dire2,'Previsao ADCP 10 - 201511','teste_pleds.png')


#pleds(espe1,dire1,tit,namefig)

pl.show()