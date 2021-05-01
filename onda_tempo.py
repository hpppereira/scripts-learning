# Calcula parametros de onda no dominio do tempo
#
# Elaborado por Henrique P. P. Pereira (henriqueppp@peno.coppe.ufrj.br)
#
# Ultima modificacao: 01/11/2012
#
# Dados de entrada: t - vetor de tempo  
#                   eta - vetor de elevacao
#                   h - profundidade
# Dados de saida: 
#[Hs,H10,Hmed,Hmin,Hmax,Tmed,Tmin,Tmax,THmax,HTmax,Lmed,Lmax,Lmin,Cmed]
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

##Importa bibliotecas
from numpy import *
from pylab import find
import regressao ; from regressao import reglin

##carrega arquivo de onda
[eta,vx,vy,vz]=loadtxt('/home/hppp/Dropbox/Tese_Mestrado/consistencia_python/1_registro45.txt', unpack=True)
#[eta,vx,vy,vz] = loadtxt('/home/henrique/Dropbox/Tese_Mestrado/consistencia_python/1_registro45.txt', unpack=True)

#cria vetor de tempo
t = linspace(1,1024,1024)

#profundidade da aquisicao
h = 500

#nivel medio
nm = mean(eta)

#contador de zero ascendente
contza = 0

#cria vetor de nivel medio
xnm = []
ixnm = []

#acha os indices que cruza o zero ascendente
for i in range(len(eta)):

    if eta[i] < nm and eta[i+1] > nm: #condicao de zero ascendente

        contza = contza + 1; #conta zero ascendente

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
THmax = periodo[THmax]

#calcula a altura associada ao periodo maximo
HTmax = find(periodo == Tmax)
HTmax = altura[HTmax]

#calcula o comprimento das ondas em aguas intermediarias (L=2pi/k), calculo do k
#pela iteracao

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