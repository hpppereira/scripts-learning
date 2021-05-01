'''
Envia e-mail do boletim da BMOBR05
'''

import os
import datetime as dt

pathname = os.environ['HOME'] + '/Dropbox/projetos/BMOP/Processamento/boletim/'
filename = 'boletim_BMOBR05'

arq = "'Boletim BMOBR 05 - %s'" %dt.datetime.strftime(dt.datetime.now(),'%d/%m/%Y')

#email com copia oculta
os.system("/usr/bin/mutt -s " + arq + " -b pereira.henriquep@gmail.com \
										-b marcelo@ambidados.com \
                                        -a " + pathname + filename + '.pdf' + " -- ufrjlioc@gmail.com < /dev/null")

