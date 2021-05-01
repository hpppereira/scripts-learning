### PROGRAMA PRINCIPAL PARA PROCESSAMENTO DE DADOS DA BOIA AXYS ###
#
# Desenvolvido por: Henrique P. P. Pereira - heniqueppp@oceanica.ufrj.br
#
# Data da ultima modificacao: 09/04/13
#
# ================================================================================== #
# Cria uma variavel 'lista' com os arquivos HNE que estao dentro do 'pathname', 
# le e processa cada arquivo HNE listado. Passa por uma consitencia, onde sao 
# listados os arquivos incosistentes e consistentes atribuindo um flag. Processa
# os arquivos consistentes. Chama o modulo 'proc_onda' para processamento dos
# dados no dominio do tempo e frequencia. Cria uma variavel 'mat_onda' contendo
# os parametros calculados. Cria uma tabela 'saida.txt' com os parametros. Cria
# graficos dos parametros.
#
# ================================================================================== #
#
# Subrotinas chamadas: carrega_axys.lista_hne
#					   carrega_axys.dados_hne
#					   consistencia_axys.consiste_bruto
#					   consistencia_axys.consiste_processado
#					   proc_onda.onda_tempo
#					   proc_onda.onda_freq
#					   graficos_axys.graf
#
# ================================================================================== #

# ================================================================================== #
##Importa bibliocas utilizadas

from numpy import *		#modulo para trabalhar com matrizes
from pylab import find 	#importa funcao find
import carrega_axys 	#modulo de listar e atribuir valores dos dados
import proc_onda 		#modulo para processamento dos dados no tempo e frequencia
import consistencia_axys
import graficos_axys 	#modulo de grafico

# ================================================================================== #
##Dados de entrada

#caminho onde estao os arquivos .HNE
pathname = '/home/hppp/Dropbox/Tese_Mestrado/CQ_Python/Boia_MB_RS/'

#cria arquivo texto com os parameros calculados
arq1 = open('Saida.txt','w')

#cria arquivo texto com flags
arq2 = open('Flags.txt','w')

#cabecalho do arquivo (arq1) criado
arq1.write('Data Hora Hs H10 Hmax Tmed THmax HTmax hm0 tp dirtp' '\n')

#cria cabecalho do arquivo (arq2) criado
arq2.write('Data Hora Flag' '\n')

#escolhe a data inicial e final para ser processada (opcional, mudar no 'for')
z0 = '200904181610'+'.HNE'
z1 = '201001121700'+'.HNE'

#profundidade da aquisicao
h = 500

#graus de liberdade
gl = 32

#aplicacao da janela de hanning (han = 1 : hanning / han=0 : retangular)
han = 0

# ================================================================================== #
##Lista arquivos .HNE que estao dentro do diretorio 'pathname'

#cria lista com o nome dos arquivos
lista = carrega_axys.lista_hne(pathname)

# ================================================================================== #
##Lista de variaveis a serem criadas durante o programa

lista_arq = [] 			  #lista do nome dos arquivos que passaram pela consistencia
lista_inconsistente = []  #lista de arquivos inconsistentes (nao serao processados)
lista_consistente = []    #lista de arquivos consistentes (serao processados)
lista_flag = []			  #lista de flags dos arquivos que passaram pela consistencia (colocar data e hora)
mat_onda = []			  #matriz com os parametros de onda calculados = [Hs, H10, Hmax, Tmed, Tmax, THmax, HTmax, hm0, tp, dirtp]
data2 = []
hora2 = []
data_hora2 = [] #variavel para saida grafica
#ano = []
#mes = []
#dia = []
#hora = []
eta_mat_cons = zeros((1500,len(lista)))    # _mat - cada coluna eh uma hora
dspx_mat_cons = zeros((1500,len(lista)))   # _proc - matriz de dados com series temporais
dspy_mat_cons = zeros((1500,len(lista)))   #dos dados aprovados na consistencia
eta_mat_incons = zeros((1500,len(lista)))   
dspx_mat_incons = zeros((1500,len(lista)))  # _bruto - matriz de dados com series temporais
dspy_mat_incons = zeros((1500,len(lista)))  #dos dados reprovados na consistencia
eta_mat_cons[:,:] = nan  #cria matriz com nan para nao confundir na plotagem com zeros no final
dspx_mat_cons[:,:] = nan #caso o vetor seja menor que 1024 pontos
dspy_mat_cons[:,:] = nan
eta_mat_incons[:,:] = nan
dspx_mat_incons[:,:] = nan
dspy_mat_incons[:,:] = nan
	

# ================================================================================== #
## Le os dados de um arquivo e processa

#acha o indice na variavel lista dos arquivos escolhidos para serem processados 
p0 = find(array(lista) == z0)
p1 = find(array(lista) == z1) + 1

#colunas do eta_mat (cada coluna eh uma hora)
j = -1 #contador arquivo incconsistente
k = -1 #contados arquivo consistente

#for i in range(len(lista)): #le todos os arquivos da lista
for i in range(p0,p1):		  #le os arquivos escolhidos
#for i in range(1):
	
	#atribui o nome do arquivo a variavel 'arq'
	arq = lista[i]

	#cria variavel com o 'str' do nome dos arquivos
	lista_arq.append(arq)

	#atribui as variaveis em 'dados' e a data em 'data'
	dados, data = carrega_axys.dados_hne(arq)

	#data e hora de todos os arquivos (consistentes e inconsistentes)
	data1=data[2]+'/'+data[1]+'/'+data[0]   #data
	hora1=data[3]+':'+data[4]				#hora
	data_hora1 = data1+'-'+hora1			#data_hora (para fazer grafico plot_date)


	#define variaveis para fazer o teste de consistencia
	#fazer consistencia previa dos dados
	##verificar o tamanho da serie
	##verificar valores consecutivos iguais

	t = dados[:,0]
	eta = dados[:,1]
	dspy = dados[:,2]
	dspx = dados[:,3]

	# ================================================================================== #
	## Faz a consistencia dos dados

	#importa modulo de consistencia

	flag = consistencia_axys.consiste_bruto(t,eta,dspy,dspx,arq)

	if flag <> '0': #Dados que receberem flags (nao serao processados)


		#lista arquivos com dados inconsisentes
		lista_inconsistente.append(int(arq[0:12]))

		#cria lista de flags de todos os arquivos
		lista_flag.append([data_hora1,flag])

		#cria matriz com series temporais reprovadas na consistencia
		j = j + 1 #contador

		eta_mat_incons[0:len(eta),j] = eta
		dspx_mat_incons[0:len(dspx),j] = dspx
		dspy_mat_incons[0:len(dspy),j] = dspy
		
		# ================================================================================== #
		## Cria variaveis de data e hora para os arquivos inconsistenes

		# data1_inc=data[2]+'/'+data[1]+'/'+data[0]   #data
		# hora1_inc=data[3]+':'+data[4]				#hora
		# data_hora1_inc = data1+'-'+hora1				#data_hora (para fazer grafico plot_date)

		arq2.write('%s %s %s \n' % (data1, hora1, flag))

	else: #Dados consistentes, passam pela rotina de processamento

		#lista arquivos corretos
		lista_consistente.append(int(arq[0:12]))

		#cria lista de flags de todos os arquivos
		lista_flag.append([data_hora1,flag])

		#cria variavel string com data e flag (para facilitar na visualizacao)
		# data_flag[]

		# ================================================================================== #
		## Cria variaveis de data e hora

		# data1=data[2]+'/'+data[1]+'/'+data[0]   #data
		# hora1=data[3]+':'+data[4]				#hora
		# data_hora1 = data1+'-'+hora1				#data_hora

		# ================================================================================== #
		## Comprime o comprimento das variaveis em potencia de 2

		t = dados[0:2**10,0]
		eta = dados[0:2**10,1]
		dspy = dados[0:2**10,2]
		dspx = dados[0:2**10,3]

		# ================================================================================== #
		#cria matriz com series temporais reprovadas na consistencia

		k = k + 1 #contador para o eta_mat

		eta_mat_cons[0:len(eta),k] = eta
		dspx_mat_cons[0:len(dspx),k] = dspx
		dspy_mat_cons[0:len(dspy),k] = dspy

		# ================================================================================== #	
		## Processamento no dominio do tempo
		
		#Dados de entrada: t - vetor de tempo
		#				   eta - elevacao
		#				   h - profundidade
		#Dados de saida: sai_ondatempo - vetor com parametros de onda calculados no dominio do tempo

		sai_ondatempo = proc_onda.onda_tempo(t,eta,h)

		#definicao dos parametros de onda no dominio do tempo
		[Hs,H10,Hmin,Hmax,Hmed,Tmin,Tmax,Tmed,THmax,HTmax,Lmin,Lmax,Lmed,Cmed] = sai_ondatempo

		# ================================================================================== #	
		## Processamento no dominio da frequencia

		#Dados de entrada: t - vetor de tempo
		#				   eta - elevacao
		#				   dspy - deslocamento norte
		#				   dspx - deslocamento leste
		#				   gl - graus de liberdade
		#				   han - aplicacao da janela de hanning (1 = hanning ; 0 = retangular)
		#				   h - profundidade
		#Dados de saida: sai_ondafreq - vetor com parametros de onda calculados no dominio da freq.

		sai_ondafreq = proc_onda.onda_freq(t,eta,dspy,dspx,gl,han,h)

		#definicao dos parametros de onda no dominio da frequencia
		[hm0, tp, dirtp] = sai_ondafreq

		# ================================================================================== #	
		## Cria variavel com os parametros calculados

		#				  0    1    2     3     4     5      6     7    8    9
		mat_onda.append([Hs, H10, Hmax, Tmed, Tmax, THmax, HTmax, hm0, tp, dirtp])
		hora2.append(hora1)
		data2.append(data1)
		data_hora2.append(data_hora1)

		# ================================================================================== #	
		## Monta arquivo texto de saida

		#parametros de onda processados
		arq1.write('%s %s %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f \n'
		 % (data1, hora1, Hs, H10, Hmax, Tmed, THmax, HTmax, hm0, tp, dirtp))

		#flags
		arq2.write('%s %s %s \n' % (data1, hora1, flag))

# ================================================================================== #	
## Transforma em matriz os parametros (linha=registros , coluna=parametros)
mat_onda = array(mat_onda)

#tomar cuidado, pois alguns vetores que tem o comprimento menor que 1024, vai ser
#preenchido com nan, isso mascara o comprimento real do vetor quando se faz usa o 'len'
#para ver o comprimento real do vetor, melhor verificar plotando a figura, ou descobrir um 
#jeito de calcular o comprimento exluindo os nan
eta_mat_incons = eta_mat_incons[0:len(eta),0:j+1]
dspx_mat_incons = dspx_mat_incons[0:len(dspx),0:j+1]
dspy_mat_incons = dspy_mat_incons[0:len(dspy),0:j+1]

eta_mat_cons = eta_mat_cons[0:len(eta),0:k+1]
dspx_mat_cons = dspx_mat_cons[0:len(dspx),0:k+1]
dspy_mat_cons = dspy_mat_cons[0:len(dspy),0:k+1]

#quantidade de dados conistentes e inconsistentes

cont_incons = len(lista_inconsistente)
cont_cons = len(lista_consistente)


#transforma em um array com data e flag
lista_flag = array(lista_flag)

# ================================================================================== #	
## deixa a matriz apenas com os dados processados	

# eta_mat = eta_mat[:,0:j]
# dspx_mat = dspx_mat[:,0:j]
# dspy_mat = dspy_mat[:,0:j]

# ================================================================================== #	
## Salva o arquivo de saida
arq1.close()
arq2.close()

# ================================================================================== #	
## Cria graficos
#graficos_axys.graf(data_hora2,mat_onda,eta_mat,dspx_mat,dspy_mat)