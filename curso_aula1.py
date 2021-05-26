''' comentario 
em varias 
linhas '''

# True = 1
#False =~1

#Ex:

has_name = True

has_name = False

"String \"com aspas \" escapadas"

#ou

'String ""asas"" '

#Quebra de linha
'''string com quebra \n
de linha '''

u'isso é uma string unicode'

#concatenar uma string
frase = 'Isso' + 'é' + 'uma string'

regua = '=' * 80

palavra = 'sem falta'
valor = 500

'Precisamos de R$%i !!!' %valor

'Precisamos de R$%0.2f, %s !!!' %(valor,palavra)

#Lisas e tuplas

lista_vazia = []
lista_de_compras = ['alface', 'tomate' , 'banana']

lista_dentro_de_listas = [[1,2,3]
						   1,2,3]]

#tuplas sao listas imutaveis

(32,5,3,8)

#ou

32,5,3,8

lista_de_compras[0]

lista_de_compras[:2] #até o elemento 2

lista_de_compras[2:] #do segundo em diante

lista_de_compras[-1] #o ultimo elemento

lista_de_compras[0:3:2]

#Dicionarios - palavra-chave: valor
#atribui uma palavra chave para cada conjunto de dados

vazio = {}

compras = {'salada' : ['alface', 'tomate', 'cebola'],
			'frutas' : ['melao', 'maca', 'laranja']}

#adicionar palavra ao Dicionarios

#deleta variavel
#del variavel

#no ipython, para deletar todas as variaveis
#reset

#colar, equivale ao ctrl+v
#paste

#exec, equivale ao eval no matlab
#atribui nome de variaveis em forma dinamica

pais = 'Brazil'

exec "'hello = 'Hello %s" %pais

#importacoes

import matplotlib

import datetime

from matplotlib import pyplot as plt

#ou

import matplotlib.pyplot as plt

#importa tudo
from matplotlib import *

#mostra submodulos
dir()

#ver variaveis
whos

#help no ipython
matplotlib?

#identacao, utilizar 4 espacos

#for utilizando continue e break

#continue, pula o valor e continua fazendo o break
#break, para de executar e para o loop

#definindo funcoes

def potencia(a,b):
	a**b

#utiliza valor por default
def potencia(a,b=0):

#caso o usuario nao entre com o valor de b
#utiliza se b=0

#funcao pass, utilizado dentro do else

#verificar se um valor esta em uma lista

for n in sequencia:
	if n in [1,2,3]:

		print alguma coisa


#poder da instrospeccao
#metodos da string
#só funciona com string

para ver o que da pra fazer uma string
a='b'
a. da um tab

#funciona para listas tbm

.append() - acrescenta valor

.extend() - acrescenta lista

#serve para os dicionarios

#range - cria lista

#funcao enumarate


