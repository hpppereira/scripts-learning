##Rotina de consistencia para a boia axys

from numpy import *
from pylab import *

def consiste_bruto(t,eta,dspy,dspx,arq):

	##arq = nome do arquivo (para verificar validade da mensagem recebida)

	#flag de dados consistentes
	flag = ''

	#1-verifica a validade na mensagem recebida
	
	#se os dados foram programados para serem enviados em hora cheia (min=00),
	#observa se os mesmos estao diferentes de 00
		
	if arq[10:12] <> '00':

		flag = flag + '1'


	#2- verifica se todos os valores estao zerados
	if (eta==0).all():

		flag = flag + '2'

	#3- verifica comprimento do vetor
	if len(eta) < 1024:

		flag = flag + '3'

	#3- verifica se todos os valores de eta sao muito proximos de zero
	if ( (eta < 0.1).all() and (eta > - 0.1).all() ):

		flag = flag + '4'

	#5- verifica valores consecutivos nulos (por enquanto, 5 valores iguais (ncn))
	#fazer com o eta, dspx e dspy

	ncn = 5
	for i in range(len(eta)-ncn):

		if (eta[i:i+ncn] == 0).all():

			flag = flag + '5'

			break

	#6- verifica valores consecutivos iguais (nci)

	nci = 5
	for i in range(len(eta)-(nci+1)):

		if (eta[i:i+nci] == eta[i+1:i+1+nci]).all():

			flag = flag + '6'

			break

	#7- teste de range (de acordo com o limite dos equipamentos)

	#limites de range
	lrmax = 20
	lrmin = -20

	if ( (eta > lrmax).any() or (eta < lrmin).any() ):

		flag = flag + '7'

		#plota series reprovadas
		#figure(), plot(eta), title(arq), show()

	#8- teste de spike (limites regionais, que podem selecionar valores importantes)

	lsmax = 5
	lsmin = -5
	
	if ( (eta > lsmax).any() or (eta < lsmin).any() ):

		flag = flag + '8'

		#plota series reprovadas
		#figure(), plot(eta), title(arq), show()








	#se nao reprovou em nenhum teste
	if flag == '':

		flag = '0'

	#teste de valores consecutivos iguais (verificar quantos valores)
	# elif flag == 0:

	# 	for i in range(len(eta)-3):

	# 		if eta[i:i+3] == eta[i]:

	# 			flag = 1


	return flag


#def consiste_processado():