#Programa de pos-processamento para o congresso oceans
#Avalia as saidas em .txt do processamento tradicional e 
#pela DAAT

import os
import numpy as np
import pylab as pl

pl.close('all')

ponda = np.loadtxt(os.environ['HOME'] + '/Google Drive/oceans/electrum/rot/saida/paramw_rs.out',delimiter=',')
espe = np.loadtxt(os.environ['HOME'] + '/Google Drive/oceans/electrum/rot/saida/espe1.out',delimiter=',')
dire = np.loadtxt(os.environ['HOME'] + '/Google Drive/oceans/electrum/rot/saida/dire1.out',delimiter=',')
energ = np.loadtxt(os.environ['HOME'] + '/Google Drive/oceans/electrum/rot/saida/energ.out',delimiter=',')

#a faixa 2 parece seguir melhor o sea


#graficos

pl.figure()
pl.plot(ponda[:,-1],'ob')
pl.plot(dire[2,:],'or') #faixa 1
pl.legend(['trad','daat'])
pl.title('Direcao')
pl.xlabel('Horas')
pl.ylabel('Graus')

# pl.plot(dire[2,:],'o') #faixa 2
# pl.plot(dire[4,:],'o') #faixa 3
# pl.plot(dire[6,:],'o') #faixa 4
# pl.twinx()
# pl.plot(ponda[:,-2],'og')
pl.show()