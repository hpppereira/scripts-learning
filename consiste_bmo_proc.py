# -*- coding: utf-8 -*-

# Autor: Henrique P. P. Pereira
#
# Data da ultima modificacao: 05/02/2014
#
# Consistencia de parametros meteo-oceanograficos processados
#
# Obs: Por enquanto adaptado para os dados da boia MINUANO - RS
#
# Funcoes: 'range' - teste de range
#          'spike' - teste de spikes (em contrucao)
#        
# **fazer aqui todos os testes para os dados processados

# ================================================================================== #
#importa bibliotecas

from numpy import *
import numpy as np
from pylab import *
import pylab as pl
from scipy.stats import nanmean, nanstd

# ================================================================================== #

def t1(var,linf,lsup,flag):
    
    '''
    
    TESTE DE FAIXA (RANGE)
    
    Dados de entrada: var - variavel sem consistencia
                      var1 - variavel editada
                      linf - limite inferior
                      lsup - limite superior
    
    Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
                    flag - parametro + flag
       
    Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
         O flag utilizado para o teste de range eh: '1'
         Dados 'consistentes' recebem flag = '0'
    
    '''

    var1 = np.copy(var)

    for i in range(len(var)):
          
        # A condicao eh realizada na serie bruta
        if var[i] < linf or var[i] > lsup:
            
            #flag[i,0] = data1[i,0]
            flag[i] = flag[i] + '1'
            
            #o valor do dado inconsistente editado recebe 'nan'
            var1[i] = nan
            
        else:
            
            #flag[i,0] = data1[i,0]
            flag[i] = flag[i] + '0'
            
            
    return var1,flag
    

# ================================================================================== #

def t2(var,med,dp,M,flag):

    '''

    TESTE DE SPIKE
    
    Dados de entrada: var - variavel sem consistencia
                      var1 - variavel editada
                      med - media da serie
                      dp - desvio padrão da série
                      M - multiplicador do dp
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Aprovado  : flag = '0'
    Reprovado : flag = '1'
    
    '''

    var1 = np.copy(var)

    for i in range(len(var)):

        if np.abs(var[i]) > (med + M*dp):

            var1[i] = np.nan

            flag[i] = flag[i] + '1'

        else:

            flag[i] = flag[i] + '0'

    return var1,flag


# ================================================================================== #

def t3(var,lag,lim,flag):
    
    '''
    
    TESTE DE VARIABILDADE TEMPORAL
    
    Dados de entrada: var - variavel
                      var1 - variavel editada
                      lag - delta tempo para o teste (indicado ser de 0 a 3 horas)
                      lim - variacao temporal maxima (para o lag escolhido)
                      flag - matriz de flags
    
    Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
                    flag - data + flag
       
    Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
         O flag utilizado para o teste de range eh: '1'
         Dados 'consistentes' recebem flag = '0'
    
    '''

    var1 = np.copy(var)
    
    #calcula a derivada de acordo com o lag (horas)
    der = var[lag:] - var[:-lag]
    
    for i in range(len(der)):
        
                             
        if der[i] > lim or der[i] < -lim:
            
            flag[i] = flag[i] + '1'
            
            #o valor do dado inconsistente recebe 'nan'
            var1[i] = nan
            
        else:
        
            flag[i] = flag[i] + '0'


    # Coloca flag = '2' nos dados que nao foram verificados
    flag[-lag:] = [flag[-i]+'2' for i in range(1,lag+1)]
                
    return var1,flag
    
    
## ================================================================================== #

def t4(var,nvc,flag):
    
    '''
    
    TESTE VALORES CONSECUTIVOS IGUAIS
    
    Dados de entrada: var - variavel
                      var1 - variavel editada
                      nvc - numero de valores consecutivos iguais
                      flag - matriz de flags
                          
    Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
                    flag - parametro + flag                    
       
    Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
         O flag utilizado para o teste de range eh: '1'
         Dados 'consistentes' recebem flag = '0'
    
    '''

    var1 = np.copy(var)

    for i in range(len(var)-nvc):
                        
        if (var[i:i+nvc] == var[i+1:i+nvc+1]).all():
            
            flag[i] = flag[i]+'1'
            
            #o valor do dado inconsistente recebe 'nan'
            var1[i] = nan
            
        else:
            
            flag[i] = flag[i]+'0'


    # Coloca flag = '2' nos dados que nao foram verificados
    flag[-nvc:] = [flag[-i]+'2' for i in range(1,nvc+1)]
                
    return var1,flag
    

## ================================================================================== #

# def t5(var,var1,hmax,hs,flag):

    
#     '''
    
#     TESTE DE LIMITE DE FREAK-WAVE
    
#     Dados de entrada: var - variavel
#                       var1 - variavel editada
#                       hmax - altura maxima
#                       hs - altura significativa
                          
#     Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
#                     flag - parametro + flag                    
       
#     Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
#          O flag utilizado para o teste de freakwave eh: '1'
#          Dados 'consistentes' recebem flag = '0'
    
#     '''


#     for i in range(len(var)):

#       if hmax[i] / hs[i] >= 2.1:

#         flag = flag + '1'

#         #o valor do dado inconsistente recebe 'nan'
#         var1[i] = nan

#       else:

#         flag = flag + '0'

#       #flag[-nvc:] = [flag[-i]+'n' for i in range(1,nvc+1)]


#     return var1,flag




# # ================================================================================== #
    
# def t2(var,var1,M,hh,flag):
    
#     '''
    
#     TESTE SPYKE UTILIZANDO MEDIA MOVEL
    
#     Dados de entrada: var - variavel
#                       var1 - variavel editada
#                       M - multiplicador do desvio padrao
#                       despad - desvio padrao da serie
#                       hh - tempo em horas para a media movel
#                       flag - matriz de flags
    
#     Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
#                     flag - parametro + flag
       
#     Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
#          O flag utilizado para o teste de range eh: '1'
#          Dados 'consistentes' recebem flag = '0'
    
#     '''

#     for i in range(len(var)):
        
#         if var[i] < nanmean(var[i-int(hh/2):i+int(hh/2)])-M*nanstd(var[i-int(hh/2):i+int(hh/2)]) or var[i] > nanmean(var[i-hh/2:i+hh/2])+M*nanmean(var[i-int(hh/2):i+int(hh/2)]):
            
#             flag[i] = flag[i] + '1'
            
#             #o valor do dado inconsistente recebe 'nan'
#             var1[i] = nan
            
#         else:
            
#             flag[i] = flag[i] + '0'
            
#     return var1,flag
    
    
# # ================================================================================== #

