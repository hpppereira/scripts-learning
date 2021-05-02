curso_aula4

import datetime as dt

dt.timedelta #intervalo de tempo, em dias


hoje = dt.date.today()

agora = dt.datetime.now()

amanha = hoje + dt.timedelta(1)

import os #operacoes com o sistema operacional

! #serve para executar diretamente no shell

!touch #cria arquivo no shell

import sys

sys.path #onde encontra os programas

sys.platform


#um metodo é uma funcao dentro de uma classe
e uma classe pode estar dentro de um modulo

para criar a sintaxe de classe, escrever class e dar tab

classes tem metodos e atributo, o atributo pode ser outra classe


class ClassName(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		
uma docstring pode ser acessada por:
ClassName?

Lidando com erro

def dividir(a,b):
	try:
		c = a/b
		return c
	except ZeroDivisionError:
		print "Divisão por zero nao existe"
	except TypeError
		print "Não é possivel divisao com strings"


#função lamba
serve para criar funcoes
Ex: quadrado = lambda x: x ** 2

import re
serve para selecionar os dados que vc quer em 
uma linha estranha

plt.close('all')

