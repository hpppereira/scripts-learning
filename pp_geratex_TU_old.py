# Abrir .tex em python como string, e tentar colocar figuras
# e textos de forma automatica nos locais corretos

import numpy as np
import os

#pathname = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/doc/latex/report/'
pathname = 'C:/Users/Cliente/Dropbox/ww3vale/Geral/doc/latex/report/'

# tex = np.loadtxt(pathname + 'lab_report_lioc.tex',dtype=str,delimiter=' ')
f = open(pathname + 'report_TU-ww3vale.tex')

#le linha por linha em uma lista
lines = f.read().splitlines()

#area de edicao do arquivo .tex (lines)

for i in range(3):

	lines[111] = lines[111] + ' -- testeeeee -- ' + str(i)

	#salva aquivo .tex
	np.savetxt(pathname + '/teste' + str(i) + '.tex',lines,fmt='%s')

