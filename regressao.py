# -*- coding: utf-8 -*-
### CALCULO DOS COEFICIENTES DA REGRESSAO LINEAR ###

# Desenvolvido por: Henrique P. P. Pereira - heniqueppp@oceanica.ufrj.br

# Data da ultima modificacao: 09/04/13

# ================================================================================== #
##Importa bibliocas utilizadas

import numpy
from numpy import sum, mean, array

# ================================================================================== #

def reglin(x,y):

    '''
    # ================================================================================== #
    #
    # Calcula os coeficiente de uma regressao linear
    #
    # Dados de entrada: vetor 'x' e 'y' com 2 valores cada
    #
    #Exemplo: x=array([139.88,139.92]);
    #         y=array([-3.99,11.87]);
    #
    # Dados de saida: coeficientes 'a' e 'b'
    #
    # ================================================================================== #
    '''
    
    x=array(x) #transforma array
    y=array(y) #transforma em array
    
    n=len(x);    #comprimento da matriz x --> 2
    xy=x*y;        #multiplica a matriz x*y
    somaxy=sum(xy); #somatório de x*y
    somax=sum(x);   #somatório de x
    somay=sum(y);   #somatório de y
    medxy=mean(xy); #média de x*y
    somax2=sum(x**2);   #somatório de (x^2)
    medx2=(mean(x)**2); #média de x^2 --> (media de x)^2
    somaxquad=somax**2;  #(somatório de x)^2

    b=(somax2*somay-somaxy*somax)/(n*somax2-somaxquad);
    a=(n*somaxy-somax*somay)/(n*somax2-somaxquad);


    return a,b
