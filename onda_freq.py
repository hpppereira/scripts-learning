# Calcula parametros de onda no dominio da frequencia
#
# Elaborado por Henrique P. P. Pereira (henriqueppp@peno.coppe.ufrj.br)
#
# Ultima modificacao: 01/11/2012
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
# Subrotinas chamadas: spec
#                      spec2
#                      numeronda

##Importa bibliotecas
from numpy import *
from pylab import find
from espectro import espec1, espec2
from numeronda import numeronda

##carrega arquivo de onda (pc henrique)
#[t,eta,dspx,dspy]=loadtxt('/home/henrique/Dropbox/Tese_Mestrado/consistencia_python/arq_200905010000.txt', unpack=True)

##carrega arquivo de onda (coppe)
[t,eta,dspy,dspx] = loadtxt('/home/hppp/Dropbox/Tese_Mestrado/consistencia_python/arq_200905010000.txt', unpack=True)



#comprime o tamanho do vetor para potencia de 2
t = t[0:1024]
eta = eta[0:1024]
dspy = dspy[0:1024]
dspx = dspx[0:1024]

#profundidade
h=500

#intervalo de tempo
dt = t[1]-t[0]

#janela
han = 0

#graus de liberdade
gl = 32

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

#periodo de pico
tp = float(1./(f[find(sn == max(sn))]))

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
dirtp = float(diraz[find(f==fp)])








