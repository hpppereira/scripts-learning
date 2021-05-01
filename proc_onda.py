### CALCULA PARAMETROS DE ONDA NO DOMINIO DO TEMPO E FREQUENCIA ###
#
# Desenvolvido por: Henrique P. P. Pereira - heniqueppp@oceanica.ufrj.br
#
# Data da ultima modificacao: 09/04/13
#
# ================================================================================== #
# Funcao 'onda_tempo': Processamento de dados de onda no dominio do tempo
# 
# Funcao 'onda_fre1': Processamento de dados de onda no dominio da frequencia
#
# ================================================================================== #
#
# Subrotinas chamadas: 'onda_tempo' - regressao.reglin
#
#					   'onda_freq'  - numeronda.numeronda
#									- espectro.espec1
#									- espectro.espec2
#
# ================================================================================== #

# ================================================================================== #
##Importa bibliocas utilizadas

from numpy import * 								#modul0 para trabalhar com matrizes
from pylab import find								#importa a funcao find
import regressao ; from regressao import reglin    	#modulo de regressao linear
from numeronda import numeronda						#modulo de numero de onda (k)
from espectro import espec1, espec2                 #modulo espectral

# ================================================================================== #

def onda_tempo(t,eta,h):

	'''
	#======================================================================#
	#
	# Calcula parametros de onda no dominio do tempo
	#
	# Dados de entrada: t - vetor de tempo  
	#                   eta - vetor de elevacao
	#                   h - profundidade
	# Dados de saida: 
	#[Hs,H10,Hmin,Hmax,Hmed,Tmin,Tmax,Tmed,THmax,HTmax,Lmin,Lmax,Lmed,Cmed]
	#				  Hs - altura significativa
	#                 H10 - altura de 1/10 das maiores
	#                 Hmin - altura minima
	#                 Hmax - altura maxima
	#                 Hmed - altura media
	#                 Tmin - periodo minimo
	#                 Tmax - altura maxima
	#                 Tmed - periodo medio
	#                 THmax - periodo associado a altura maxima
	#				  HTmax - altura associada ao periodo maximo
	#                 Lmin - comprimento de onda minimo
	#				  Lmax - comprimento de onda maximo
	#                 Lmed - comprimento de onda medio
	#                 Cmed -  celeridade media
	#
	# Funcao chamada: regressao.reglin
	#
	#======================================================================#
	'''

	#nivel medio
	nm = mean(eta)

	#contador de zero ascendente
	contza = 0

	#cria vetor de nivel medio
	xnm = []
	ixnm = []

	#acha os indices que cruza o zero ascendente
	for i in range(len(eta)-1):

	    if eta[i] < nm and eta[i+1] > nm: #condicao de zero ascendente

	        contza = contza + 1 #conta zero ascendente

	        x = [t[i] , t[i+1]] #cria vetor x para regressao linear
	        
	        y = [eta[i] , eta[i+1]] #cria vetor y para regressao linear

	        [a,b] = reglin(x,y) #chama subrotina de regressao linear

	        xnm.append((nm - b) / a) #acha o tempo que a elevacao eh igual ao nm

	        ixnm.append(i) #acha indices do tempo que cruzao o zero ascendente

	#quantidade de onda no registro
	contonda = contza - 1

	#calcula altura e periodo de cada onda
	altura = []
	periodo = []

	for i in range(len(ixnm)-1):

	   	altura.append(max(eta[ixnm[i]:ixnm[i+1]]) - min(eta[ixnm[i]:ixnm[i+1]]))

	   	periodo.append(xnm[i+1] - xnm[i])

	#coloca as alturas em ordem crescente
	Hss = sort(altura); 
	Hss = flipud(Hss)

	#calcula altura significativa (H 1/3)
	div = len(Hss) / 3 #calcula o divisor
	Hs = mean(Hss[0:div+1]) #altura significativa (media das um terco maiores)

	#calcula a altura das 1/10 maiores (H 1/10)
	div1 = len(Hss) / 10
	H10 = mean(Hss[0:div1+1]) #altura da media das um decimo maiores

	#altura maxima
	Hmax = max(altura)

	#altura minima
	Hmin = min(altura)

	#altura media
	Hmed = mean(altura)

	#periodo maximo
	Tmax = max(periodo)

	#periodo minimo
	Tmin = min(periodo)

	#periodo medio
	Tmed = mean(periodo)

	#calcula o periodo associado a altura maxima
	THmax = find(altura == Hmax)
	THmax = periodo[THmax[0]]

	#calcula a altura associada ao periodo maximo
	HTmax = find(periodo == Tmax)
	HTmax = altura[HTmax[0]]

	#calcula o comprimento das ondas em aguas intermediarias (L=2pi/k),
	#calculo do k pela iteracao

	#comprimento de onda em aguas profundas
	T = array(periodo) #transforma o periodo em array
	Lo = 1.56 * T**2 #comprimento de onda em aguas profundas

	L = list(copy(Lo)) #cria vetor de comprimento em lista
	L.append(0) #coloca mais um valor para ser substiruido no 'for'
	L = array(L) #passa o comprimento para array para fazer a conta no 'for'

	for j in range(len(L)-1):

		for i in range(100):

			L[j] = Lo[j]*tanh((2*pi) / L[j] * h) #comprimento de onda em aguas intermediarias (rel. disp)

		L[j+1] = L[j]

	#comprimento de onda em aguas intermediarias
	L = L[0:len(Lo)]

	#comprimento de onda maximo
	Lmax = max(L)

	#comprimento de onda minimo
	Lmin = min(L)

	#comprimento de onda medio
	Lmed = mean(L)

	#celeridade das ondas
	C = 1.56 * T

	#celeridade maxima
	Cmax = max(C)

	#celeridade minima
	Cmin = min(C)

	#celeridade media
	Cmed = mean(C)

	#vetor de saida
	sai_ondatempo = [Hs,H10,Hmin,Hmax,Hmed,Tmin,Tmax,Tmed,THmax,HTmax,Lmin,Lmax,Lmed,Cmed]

	return sai_ondatempo

#======================================================================#



def onda_freq(t,eta,dspy,dspx,gl,han,h):

	'''
	#======================================================================#
	#
	# Calcula parametros de onda no dominio da frequencia
	#
	# Dados de entrada: dt - intervalo de amostragem
	#                   h - profundidade
	#                   eta - vetor de elevacao
	#                   etax - vetor de deslocamento em x
	#                   etay - vetor de deslocamento em y
	#
	# Dados de saida: f - vetor de frequencias
	#                 an - auto-espectro de eta
	#                 anx - auto-espectro de etax
	#                 any - auto-espectro de etay
	#                 a1, b1 - coeficientes de fourier de 1 ordem
	#                 diraz - vetor de direcao azimutal em graus
	#                 dirm - vetor de direcao media
	#                 dirtp - direcao associado a frequencia de pico
	#                 fp - frequencia de pico
	#                 tp - periodo de pico
	#                 hm0 - altura significativa
	#
	# Funcoes chamadas: espectro.espec
	#                   espectro.espec2
	#
	#======================================================================#
	'''

	#intervalo de tempo
	dt = t[1]-t[0]

	#calculo do espectro simples da elevacao
	aan = espec1(eta,dt,gl,han)

	#calculo dos espectros cruzados da elevacao e deslocamentos horizontais
	aannx = espec2(eta,dspx,dt,gl,han)
	aanny = espec2(eta,dspy,dt,gl,han)

	#vetor de frequencia
	f = aan[:,0]

	#calculo do numero de onda
	k = numeronda(h,f,len(f))

	#definicao dos parametros dos espectros

	#auto-espectro de eta
	sn = aan[:,1]

	#auto-espectro de dsp x
	snx = aannx[:,2]

	#auto-espectro de dsp y
	sny = aanny[:,2]

	#quad-espectro de eta e dsp x
	qnnx = aannx[:,5]

	#quad-espectro de eta e dsp y
	qnny = aanny[:,5]

	#calculo da direcao de onda

	a1 = []
	b1 = []
	dirr = []

	for i in range(len(f)):

		#calculo dos coeficientes de fourier
		a1.append( qnnx[i] / (k[i]*pi*sn[i]) )
		b1.append( qnny[i] / (k[i]*pi*sn[i]) )

		#cria numero imaginario com os coeficientes
		imag = complex(a1[i],b1[i])

		#calcula a direcao em radianos
		dirr.append(angle(imag))

	#vetor de diracao para array
	dirr = array(dirr)

	#passa direcao de rad para graus
	dirg = dirr * 180 / pi

	#passa de trigonometrico para azimute
	diraz = 270 - dirg

	#muda de onde a onda vai para onde ela vem
	#diraz = diraz - 180

	#condicao para valores maiores que 360 e menores que 0

	for i in range(len(diraz)):

		if diraz[i] > 360:

			diraz[i] = diraz[i]-360

		elif diraz[i] < 0:

			diraz[i] = diraz[i] + 360

	#calcula parametros de onda


	#acha o indice da frequencia de pico
	ind = int(find(sn == max(sn)))

	#periodo de pico

	tp = 1/f[ind]

	#frequencia de pico
	fp = 1/tp

	#altura significativa (Hm0)

	#variacao de frequencia
	df = f[1] - f[0]

	#momento de espectral m0
	m0 = sum(sn)*df

	#calculo da altura significativa
	hm0 = 4.01*sqrt(m0)

	#direcao do periodo de pico
	dirtp = diraz[ind]

	#passa variaveis para numero
	#tp = float(tp)
	#dirtp = float(dirtp)

	sai_ondafreq = [hm0, tp, dirtp]

	return sai_ondafreq, f, snx