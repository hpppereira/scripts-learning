# -*- coding: utf-8 -*-

# Abrir .tex em python como string, e tentar colocar figuras
# e textos de forma automatica nos locais corretos

import numpy as np
import os
import jinja2
from jinja2 import Template
import datetime as dt
import codecs


#caminho do template .tex
pathname = os.environ['HOME'] + '/Dropbox/ww3vale/TU/boletim/'

###############################################################################
# #teste

# # tex = np.loadtxt(pathname + 'lab_report_lioc.tex',dtype=str,delimiter=' ')
# f = open(pathname + 'boletim_TU.tex')

# #le linha por linha em uma lista
# lines = f.read().splitlines()

# #area de edicao do arquivo .tex (lines)
# for i in range(3):

# 	lines[55] = lines[55] + ' -- testeeeee -- ' + str(i)

# 	#salva aquivo .tex
# 	np.savetxt(pathname + '/teste' + str(i) + '.tex',lines,fmt='%s')

###############################################################################
# teste 2

# t = Template("Hello {{ something }}!")
# t.render(something="World") #escreve e frase com a palavra substituida


# t = Template("My favorite numbers: {% for n in range(1,10) %}{{n}} " "{% endfor %}")
# t.render()


###############################################################################
#This tells Jinja how to handle LaTeX syntax

latex_jinja_env = jinja2.Environment(
    block_start_string = '\BLOCK{',
    block_end_string = '}',
    variable_start_string = '\VAR{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%-',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    #loader = jinja2.FileSystemLoader(os.path.abspath('.'))
    loader = jinja2.FileSystemLoader(pathname)
)

# Modify to specify the template (colocar o template que vai ser mudado - fazer um de modelo com os \VAR)
template = latex_jinja_env.get_template('boletim_TU.tex')

#nome do arquivo a ser salvo
filename = 'boletim_TU_' + dt.datetime.strftime(dt.datetime.now(),'%Y%m%d') + '.tex'

#cria um arquivo para ser sobrescrito
#outfile = open(pathname + filename,'w')
outfile = codecs.open(pathname + filename,'w','utf-8')


#cria arquivo com os valores substituidos
outfile.write(template.render(Ondas='TESTE'))

#salva 
outfile.close()

os.system("pdflatex " + pathname + filename)


