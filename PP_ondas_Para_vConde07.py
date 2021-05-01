from numpy import *
from pylab import *
import proc_onda 		#modulo para processamento dos dados no tempo e frequencia

sen = loadtxt('/home/henrique/Desktop/Para_ondas/vConde07.sen')
whd = loadtxt('/home/henrique/Desktop/Para_ondas/vConde07.whd')
wad = loadtxt('/home/henrique/Desktop/Para_ondas/vConde07.wad')

ast_wstart = whd[:,22]
ast_wsize = whd[:,23]

pr_dbar = wad[:,2]
velx = wad[:,5]
vely = wad[:,6]
velz = wad[:,7]

cont = len(pr_dbar)/1024

vx1 = zeros((1024,cont))
vy1 = zeros((1024,cont))
vz1 = zeros((1024,cont))
eta1 = zeros((1024,cont))
pr1 = zeros((1024,cont))

j = -1

for i in arange(0,len(pr_dbar),1024):

	j = j + 1
	
	eta1[:,j] = pr_dbar[i:i+1024] - mean(pr_dbar[i:i+1024])

	pr1[:,j] = pr_dbar[i:i+1024]

	vx1[:,j] = velx[i:i+1024]

	vy1[:,j] = vely[i:i+1024]

	vz1[:,j] = velz[i:i+1024]


#cria arquivo texto com os parameros calculados
# arq1 = open('Saida.txt','w')

# #cria arquivo texto com flags
# arq2 = open('Flags.txt','w')

# #cabecalho do arquivo (arq1) criado
# arq1.write('Data Hora Hs H10 Hmax Tmed THmax HTmax hm0 tp dirtp' '\n')

# #cria cabecalho do arquivo (arq2) criado
# arq2.write('Data Hora Flag' '\n')

#profundidade da aquisicao (m)
h = 13

#freq. de amostragem
df = 2 #Hz
dt = 1./df #intervalo de amostragem

#comprimento do vetor
comp = len(eta1[:,0]*.5)

#cria vetor de tempo
t = arange(dt,comp+dt,dt)

#graus de liberdade
gl = 32

#aplicacao da janela de hanning (han = 1 : hanning / han=0 : retangular)
han = 0

# ================================================================================== #
##Lista de variaveis a serem criadas durante o programa

# lista_arq = [] 			  #lista do nome dos arquivos que passaram pela consistencia
# lista_inconsistente = []  #lista de arquivos inconsistentes (nao serao processados)
# lista_consistente = []    #lista de arquivos consistentes (serao processados)
# lista_flag = []			  #lista de flags dos arquivos que passaram pela consistencia (colocar data e hora)
mat_onda = []			  #matriz com os parametros de onda calculados = [Hs, H10, Hmax, Tmed, Tmax, THmax, HTmax, hm0, tp, dirtp]
# data2 = []
# hora2 = []
# data_hora2 = [] #variavel para saida grafica
#ano = []
#mes = []
#dia = []
#hora = []
# eta_mat_cons = zeros((len(eta),cont))    # _mat - cada coluna eh uma hora
# dspx_mat_cons = zeros((len(eta),cont))   # _proc - matriz de dados com series temporais
# dspy_mat_cons = zeros((len(eta),cont))   #dos dados aprovados na consistencia
# eta_mat_incons = zeros((len(eta),cont))   
# dspx_mat_incons = zeros((len(eta),cont))  # _bruto - matriz de dados com series temporais
# dspy_mat_incons = zeros((len(eta),cont))  #dos dados reprovados na consistencia
# eta_mat_cons[:,:] = nan  #cria matriz com nan para nao confundir na plotagem com zeros no final
# dspx_mat_cons[:,:] = nan #caso o vetor seja menor que 1024 pontos
# dspy_mat_cons[:,:] = nan
# eta_mat_incons[:,:] = nan
# dspx_mat_incons[:,:] = nan
# dspy_mat_incons[:,:] = nan
	
aespec = [] #cada linha eh um espectro (vetor em coluna)

# ================================================================================== #
## Le os dados de um arquivo e processa

#colunas do eta_mat (cada coluna eh uma hora)
j = -1 #contador arquivo incconsistente
k = -1 #contados arquivo consistente

#for i in range(len(lista)): #le todos os arquivos da lista
for i in range(cont):		  #le os arquivos escolhidos
#for i in range(1):
	
	#atribui o nome do arquivo a variavel 'arq'
	#arq = eta[:,i]

	#cria variavel com o 'str' do nome dos arquivos
	#lista_arq.append(arq)

	#atribui as variaveis em 'dados' e a data em 'data'
	#dados, data = carrega_axys.dados_hne(arq)

	#data e hora de todos os arquivos (consistentes e inconsistentes)
	#data1=data[2]+'/'+data[1]+'/'+data[0]   #data
	#hora1=data[3]+':'+data[4]				#hora
	#data_hora1 = data1+'-'+hora1			#data_hora (para fazer grafico plot_date)


	#define variaveis para fazer o teste de consistencia
	#fazer consistencia previa dos dados
	##verificar o tamanho da serie
	##verificar valores consecutivos iguais

	#t = dados[:,0]
	eta = eta1[:,i]
	vx = vx1[:,i]
	vy = vy1[:,i]
	vz = vz1[:,i]

	eta = resize(eta,(len(eta),1))
	vx = resize(vx,(len(vx),1))
	vy = resize(vy,(len(vy),1))
	vz = resize(vz,(len(vz),1))

	# ================================================================================== #
	## Faz a consistencia dos dados

	#importa modulo de consistencia

	# flag = consistencia_axys.consiste_bruto(t,eta,dspy,dspx,arq)

	# if flag <> '0': #Dados que receberem flags (nao serao processados)


	# 	#lista arquivos com dados inconsisentes
	# 	lista_inconsistente.append(int(arq[0:12]))

	# 	#cria lista de flags de todos os arquivos
	# 	lista_flag.append([data_hora1,flag])

	# 	#cria matriz com series temporais reprovadas na consistencia
	# 	j = j + 1 #contador

	# 	eta_mat_incons[0:len(eta),j] = eta
	# 	dspx_mat_incons[0:len(dspx),j] = dspx
	# 	dspy_mat_incons[0:len(dspy),j] = dspy
		
	# 	# ================================================================================== #
	# 	## Cria variaveis de data e hora para os arquivos inconsistenes

	# 	# data1_inc=data[2]+'/'+data[1]+'/'+data[0]   #data
	# 	# hora1_inc=data[3]+':'+data[4]				#hora
	# 	# data_hora1_inc = data1+'-'+hora1				#data_hora (para fazer grafico plot_date)

	# 	arq2.write('%s %s %s \n' % (data1, hora1, flag))

	# else: #Dados consistentes, passam pela rotina de processamento

	# 	#lista arquivos corretos
	# 	lista_consistente.append(int(arq[0:12]))

	# 	#cria lista de flags de todos os arquivos
	# 	lista_flag.append([data_hora1,flag])

		#cria variavel string com data e flag (para facilitar na visualizacao)
		# data_flag[]

		# ================================================================================== #
		## Cria variaveis de data e hora

		# data1=data[2]+'/'+data[1]+'/'+data[0]   #data
		# hora1=data[3]+':'+data[4]				#hora
		# data_hora1 = data1+'-'+hora1				#data_hora

		# ================================================================================== #
		## Comprime o comprimento das variaveis em potencia de 2

		# t = dados[0:2**10,0]
		# eta = dados[0:2**10,1]
		# dspy = dados[0:2**10,2]
		# dspx = dados[0:2**10,3]

		# ================================================================================== #
		#cria matriz com series temporais reprovadas na consistencia

		# k = k + 1 #contador para o eta_mat

		# eta_mat_cons[0:len(eta),k] = eta
		# dspx_mat_cons[0:len(dspx),k] = dspx
		# dspy_mat_cons[0:len(dspy),k] = dspy

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

	sai_ondafreq, f, snx = proc_onda.onda_freq(t,eta,vx,vy,gl,han,h)

	aespec.append(snx)

		#definicao dos parametros de onda no dominio da frequencia
	[hm0, tp, dirtp] = sai_ondafreq

		# ================================================================================== #	
		## Cria variavel com os parametros calculados

		#			  0    1    2     3     4     5      6     7    8    9
	mat_onda.append([Hs, H10, Hmax, Tmed, Tmax, THmax, HTmax, hm0, tp, dirtp])
		# hora2.append(hora1)
		# data2.append(data1)
		# data_hora2.append(data_hora1)

		# ================================================================================== #	
		## Monta arquivo texto de saida

		#parametros de onda processados
		# arq1.write('%s %s %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f \n'
		#  % (data1, hora1, Hs, H10, Hmax, Tmed, THmax, HTmax, hm0, tp, dirtp))

		# #flags
		# arq2.write('%s %s %s \n' % (data1, hora1, flag))

# ================================================================================== #	
## Transforma em matriz os parametros (linha=registros , coluna=parametros)

espec_mat = array(aespec).T

mat_onda = array(mat_onda)

#tomar cuidado, pois alguns vetores que tem o comprimento menor que 1024, vai ser
#preenchido com nan, isso mascara o comprimento real do vetor quando se faz usa o 'len'
#para ver o comprimento real do vetor, melhor verificar plotando a figura, ou descobrir um 
#jeito de calcular o comprimento exluindo os nan
# eta_mat_incons = eta_mat_incons[0:len(eta),0:j+1]
# dspx_mat_incons = dspx_mat_incons[0:len(dspx),0:j+1]
# dspy_mat_incons = dspy_mat_incons[0:len(dspy),0:j+1]

# eta_mat_cons = eta_mat_cons[0:len(eta),0:k+1]
# dspx_mat_cons = dspx_mat_cons[0:len(dspx),0:k+1]
# dspy_mat_cons = dspy_mat_cons[0:len(dspy),0:k+1]

# #quantidade de dados conistentes e inconsistentes

# cont_incons = len(lista_inconsistente)
# cont_cons = len(lista_consistente)


# #transforma em um array com data e flag
# lista_flag = array(lista_flag)

# ================================================================================== #	
## deixa a matriz apenas com os dados processados	

# eta_mat = eta_mat[:,0:j]
# dspx_mat = dspx_mat[:,0:j]
# dspy_mat = dspy_mat[:,0:j]

# ================================================================================== #	
## Salva o arquivo de saida
# arq1.close()
# arq2.close()

# ================================================================================== #	
## Cria graficos
#graficos_axys.graf(data_hora2,mat_onda,eta_mat,dspx_mat,dspy_mat)










# figure()
# plot(sen[:,14]), title('Pressao - .sen - dt=10min')

# figure()
# plot(ast_wstart), title('ast window start')

# figure()
# plot(ast_wsize), title('ast window size')

# figure()
# plot(pr_dbar), title('pressao em dbar')

# figure()
# plot(velx), title('velx')

# figure()
# plot(vely), title('vely')

# figure()
# plot(velz), title('velz')



# show()