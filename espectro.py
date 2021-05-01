### PROGRAMA QUE CALCULA O ESPECTRO SIMPLES E CRUZADO DE SERIER REAIS ###
#
# Desenvolvido por: Henrique P. P. Pereira - heniqueppp@oceanica.ufrj.br
#
# Data da ultima modificacao: 09/04/13
#
# ================================================================================== #
#Funcao espec1: calcula o espectro simples de uma serie real
#
#Funcao espec2: calculo o espectro cruzado entre duas series reais
#
# ================================================================================== #
#
# Subrotinas chamadas: carrega_axys.lista_hne
#                      carrega_axys.dados_hne
#                      consistencia_axys.consiste
#                      proc_onda.onda_tempo
#                      proc_onda.onda_freq
#                      graficos_axys.graf
#
# ================================================================================== #

# ================================================================================== #
##Importa bibliocas utilizadas

from numpy import *         #modulo de trabalhar com matriz
import numpy as np          #chama numpy como np
from scipy import fft       #importa funcao fft

# ================================================================================== #


def espec1(x,dt,gl,han):

    '''
    #======================================================================#
    #
    # Calcula o espectro simples de uma serie real
    #
    # Dados de entrada: x = serie real (potencia de 2)
    #                   dt = intervalo de amostragem
    #                   gl = graus de liberdade (2=espec. bruto)
    #                   han = janela de hanning (h=1 - hanning, h=0 - retangular)
    #
    # Dados de saida: [aa] - col 0: vetor de frequencia
    #                        col 1: autoespectro
    #                        col 2: intervalo de confianca inferior
    #                        col 3: intervalo de confianca superior
    #
    #======================================================================#
    '''

    #retira a media
    x=x-np.mean(x)

    #comprimento da serie
    N1=len(x)

    #quantidade de linhas a ser rearranjada
    l=2*N1/gl 
    
    #quantidade de colunas a ser rearranjada
    c=gl/2 

    #rearranja o vetor com 'l' linhas e 'c' colunas fazendo a leitura em colunas = 'F'
    a=np.reshape(x,(l,c),'F')

    #comprimento do vetor da matriz rearranjada
    N=len(a)

    #cria vetores a serem preenchidos com os valores da fft
    mat1=np.zeros((l,c)) #matriz com fft
    mat2=np.zeros((l,1)) #vetor com a media da fft

    for i in range(c):

        #janela de hanning
        if han==1:

            #aplica janela de hanning
            a[:,i]=a[:,i]*np.hanning(len(a))

            #calcula a fft para cada coluna
            fftx=fft(a[:,i])

            #separa componentes reais e imaginarias
            xre=np.real(fftx)
            xim=np.imag(fftx)

            #calcula o espectro para cada coluna
            mat1[:,i]=2*dt*(xre*xre+xim*xim)/(N*0.375) #0.375 eh a correcao da janela

        #janela retangular
        elif han==0:

            #calcula a fft para cada coluna
            fftx=fft(a[:,i])

            #separa componentes reais e imaginarias
            xre=np.real(fftx)
            xim=np.imag(fftx)
            #calcula o espectro para cada coluna
            mat1[:,i]=2*dt*(xre*xre+xim*xim)/N
    
    for i in range(l):

        #faz a media dos espectros calculados em cada coluna
        mat2[i,0]=np.mean(mat1[i,:])
    
    #espectro de uma dimensao (divide o espectro pela metade)
    ss=(mat2[0:N/2])

    #calcula os intervalos de confianca para 95% (espec JL)
    icinf=ss*gl/26.12
    icsup=ss*gl/5.63
    
    #frequencia de corte
    fc=1/(2.*dt)

    #vetor de frequencia
    f=arange(fc/(len(ss)),fc+fc/(len(ss)),fc/(len(ss)))

    #cria matriz de saida (cada variavel em uma coluna)
    aa=array([f,ss,icinf,icsup])
    aa=aa.T #transpoe a matriz

    return aa

# ================================================================================== #



def espec2(x,y,dt,gl,han):

    '''
    # ================================================================================== #
    #
    # Calcula o espectro cruzado entre duas series reais
    #
    # Dados de entrada: x = serie real 1 (potencia de 2)
    #                   y = serie real 2 (potencia de 2)
    #                   dt = intervalo de amostragem
    #                   gl = graus de liberdade (2=espec. bruto)
    #                   han = janela de hanning (h=1 - hanning, h=0 - retangular)
    #
    # Dados de saida: [aa2] - col 0: vetor de frequencia
    #                         col 1: autoespectro de x
    #                         col 2: autoespectro de y
    #                         col 3: amplitude do espectro cruzado
    #                         col 4: co-espectro
    #                         col 5: quad-espectro
    #                         col 6: espectro de fase
    #                         col 7: espectro de coerencia
    #                         col 8: intervalo de confianca inferior do espectro cruzado
    #                         col 9: intervalo de confianca superior do espectro cruzado
    #                         col 10: intervalo de confianca da coerencia (erro para gl=2)
    #
    # ================================================================================== #
    '''

    #retira a media
    x=x-np.mean(x)
    y=y-np.mean(y)

    #comprimento da serie
    N1=len(x)

    #quantidade de linhas a ser rearranjada
    l=2*N1/gl
    
    #quantidade de colunas a ser rearranjada
    c=gl/2 

    #rearranja o vetor com 'l' linhas e 'c' colunas fazendo a leitura em colunas = 'F'
    a=np.reshape(x,(l,c),'F') #serie x
    b=np.reshape(y,(l,c),'F') #serie y

    #comprimento do vetor de acordo com os graus de liberdade
    N=len(a)

    #cria vetores a serem preenchidos com os valores da fft
    mat1x=np.zeros((l,c)) #matriz com fft - x
    mat1y=np.zeros((l,c)) #matriz com fft - y
    
    mat2x=np.zeros((l,1)) #vetor com medias da fft - x
    mat2y=np.zeros((l,1)) #vetor com medias da fft - y

    mat1co=np.zeros((l,c)) #matriz de coespectro
    mat1qd=np.zeros((l,c)) #matriz de quadespectro
    mat1fase=np.zeros((l,c)) #matriz com espectros de fase
    mat1amp=np.zeros((l,c)) #matriz com espectros de amplitude cruz
    mat1coer=np.zeros((l,c)) #matriz com espectros de coerencia

    mat2co=np.zeros((l,1)) #vetor com medias do coespectro
    mat2qd=np.zeros((l,1)) #vetor com medias do quadespectro
    mat2fase=np.zeros((l,1)) #vetor com medias do espectro de fase
    mat2amp=np.zeros((l,1)) #vetor com medias do espectro de amplitude cruz 
    mat2coer=np.zeros((l,1)) #vetor com medias do espectro de coerencia

    for i in range(c):

        #janela de hanning
        if han==1:

            #SERIE X

            #aplica a janela de hanning
            a[:,i]=a[:,i]*np.hanning(len(a))

            #calcula fft
            fftx=fft(a[:,i])

            #separa componentes reais e imaginarias
            xre=np.real(fftx)
            xim=np.imag(fftx)

            #calcula o espectro para cada coluna
            mat1x[:,i]=2*dt*(xre*xre+xim*xim)/(N*0.375) #0.375 eh a correcao da janela

            #SERIE Y

            #aplica a janela
            b[:,i]=b[:,i]*np.hanning(len(b))

            #calcula fft
            ffty=fft(b[:,i])

            #separa componentes reais e imaginarias
            yre=np.real(ffty)
            yim=np.imag(ffty)

            #calcula o espectro para cada coluna
            mat1y[:,i]=2*dt*(yre*yre+yim*yim)/(N*0.375) #0.375 eh a correcao da janela

            # SERIES CRUZADAS

            #calcula o co-esoectro para cada coluna
            mat1co[:,i]=2*dt*(xre*yre+xim*yim)/(N*0.375)

            #calcula o quad-espectro para cada coluna
            mat1qd[:,i]=2*dt*(xim*yre-xre*yim)/(N*0.375)

            #calculo do espectro de fase
            mat1fase[:,i]=np.arctan(mat1qd[:,i]/mat1co[:,i])*180/np.pi

            #calculo do espectro de amplitude cruzada
            mat1amp[:,i]=np.sqrt(mat1qd[:,i]**2+mat1co[:,i]**2)

            #calculo do espectro de coerencia
            mat1coer[:,i]=(mat1co[:,i]**2+mat1qd[:,i]**2)/(mat1x[:,i]*mat1y[:,i])

        #janela retangular                
        elif han==0:

            #SERIE X

            #calcula fft
            fftx=fft(a[:,i])

            #separa componentes reais e imaginarias
            xre=np.real(fftx)
            xim=np.imag(fftx)

            #calcula o espectro para cada coluna
            mat1x[:,i]=2*dt*(xre*xre+xim*xim)/N #0.375 eh a correcao da janela

            #SERIE Y

            #calcula fft
            ffty=fft(b[:,i])

            #separa componentes reais e imaginarias
            yre=np.real(ffty)
            yim=np.imag(ffty)

            #calcula o espectro para cada coluna
            mat1y[:,i]=2*dt*(yre*yre+yim*yim)/N

            # SERIES CRUZADAS

            #calcula o co e quad espectro para cada coluna
            mat1co[:,i]=2*dt*(xre*yre+xim*yim)/N
            mat1qd[:,i]=2*dt*(xim*yre-xre*yim)/N

            #calculo do espectro de fase
            mat1fase[:,i]=np.arctan(mat1qd[:,i]/mat1co[:,i])*180/np.pi

            #calculo do espectro de amplitude cruzada
            mat1amp[:,i]=np.sqrt(mat1qd[:,i]**2+mat1co[:,i]**2)

            #calculo do espectro de coerencia
            mat1coer[:,i]=(mat1co[:,i]**2+mat1qd[:,i]**2)/(mat1x[:,i]*mat1y[:,i])
    
    for i in range(l):
        
        #faz a media dos espectros calculados
        mat2x[i,0]=np.mean(mat1x[i,:])
        mat2y[i,0]=np.mean(mat1y[i,:])
        mat2co[i,0]=np.mean(mat1co[i,:])
        mat2qd[i,0]=np.mean(mat1qd[i,:])
        mat2fase[i,0]=np.mean(mat1fase[i,:])
        mat2amp[i,0]=np.mean(mat1amp[i,:])
        mat2coer[i,0]=np.mean(mat1coer[i,:])

    #auto-espectro de x de uma dimensao
    ssx=(mat2x[0:N/2])

    #auto-espectro de y de uma dimensao
    ssy=(mat2y[0:N/2])

    #co-espectro de uma dimensao
    coxy=(mat2co[0:N/2])

    #quad-espectro de uma dimensao
    qdxy=(mat2qd[0:N/2])

    #espectro de fase de uma dimensao
    fasexy=(mat2fase[0:N/2])

    #espectro de ampl cruzada de uma dimensao
    ssxy=(mat2amp[0:N/2])

    #espectro de coerencia de uma dimensao
    coerxy=(mat2coer[0:N/2])

    #frequencia de corte
    fc=1/(2.*dt)

    #vetor de frequencia
    f=arange(fc/(len(ssxy)),fc+fc/(len(ssxy)),fc/(len(ssxy)))

    #intervalo de confianca para a amplitude do espectro cruzado
    icinf=ssxy*14/26.12
    icsup=ssxy*14/5.63

    #intervalo de confianca para coerencia
    iccoer=zeros(len(ssxy))
    iccoer[:]=1-(0.05**(1/(14/2.0-1)))

    #Obs: Os intervalos de confianca dependem do Grau de Liberdade.  No caso usou-se GL=14.

    #cria matriz de saida (cada variavel em uma coluna)
    #          0  1   2    3   4     5    6      7      8     9     10
    aa2=array([f,ssx,ssy,ssxy,coxy,qdxy,fasexy,coerxy,icinf,icsup,iccoer])
    aa2=aa2.T #transpoe a matriz

    return aa2

#--------------------------------------------------------------------#

