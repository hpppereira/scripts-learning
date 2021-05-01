# -*- coding: utf-8 -*-
#
#consistencia dos dados brutos de boias meteo-oceanograficas
#
#Autor: Henrique P. P. Pereira
#
#Data da ultima modificacao: 27/03/2014
# 
#Funcoes: 'nome_arq' - verifica se os minutos estao diferente de '00' no nome do arquivo
#		  'range' - teste de range
#         'spike' - teste de spikes (em contrucao)
# .... fazer aqui todos os testes para os dados processados


# ================================================================================== #
#importa bibliotecas

import numpy as np
import pylab as pl
import copy as cp

# ================================================================================== #

def t1hne(arq,flag):
    
    '''

    VALIDADE DO NOME DO ARQUIVO  (Boias Axys) /n
    * Ex: 200905101100.HNE
    * Verifica se os minutos estao igual a '00'
    * Para dados programados para serem enviados em hora cheia (min=00)
    
    Dados de entrada: arq - nome do arquivo
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Posicao (indice) em 'lista_flag' : 0
    Aprovado  : flag = '0'
    Reprovado : flag = '1'
    
    '''
		
    if arq[10:12] <> '00':

        flag = flag + '1'
        
    else:
        
        flag = flag + '0'
        
    return flag

# ================================================================================== #

def t2hne(serie,flag): #modificar a entrada para entrar com qlq tamanho de vetor, devido aos tbm dados meteorologicos
    
    '''

    COMPRIMENTO DA SERIE
    * Verifica se o comprimento da serie eh menor que 1024
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Posicao (indice) em 'lista_flag' : 1
    Aprovado  : flag = '0'
    Reprovado : flag = '1'
    
    '''
    
    #2- verifica comprimento do vetor
    if len(pl.find(np.isnan(serie)==False)) < 1024:

        flag = flag + '1'
        
    else:
        
        flag = flag + '0'
        
    return flag

# ================================================================================== #

def t1(serie,N,flag):
    
    '''

    TESTE DE GAP
    * Verifica valores consecutivos faltando
    
    Dados de entrada: serie - (ex: elevacao, deslocamento ..)
                      N - numero de valores consecutivos aceitaveis para estar
                      faltando
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Aprovado  : flag = '0'
    Reprovado : flag = '1'
    
    '''
    
    for i in range(len(serie)-N):
        
        if np.isnan(serie[i:i+N]).all() == True:

            flag = flag + '1'
            
            #se achou um gap, para o teste
            break

    if flag <> '1':

        flag = flag + '0'

    return flag


# ================================================================================== #

def t2(serie,med,dp,N,M,P,flag):
    
    '''

    TESTE DE SPIKE
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      med - média da série
                      dp - desvio padrão da série
                      N% - limite total de spikes
                      M - multiplicador do dp
                      P - numero de iteracoes
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Aprovado  : flag = '0'
    Reprovado : flag = '1'
    
    '''

    #retira o primeiro e ultimo valor, caso o spike ocorra nessas
    #posicoes, nao sera editado, pois da erro (melhorar)
    vetc = cp.copy(serie)

    #M1 = 0
    #M2 = 0
    #quantidade maxima de spikes
    N = len(serie) * N / 100 #transforma em %

    #procura valores na serie maior do que o limite
    sp = pl.find(np.abs(serie) > (M * dp) )
    
    #verifica quantidade total de spikes
    M1 = len(sp)

    #valor inicial para numero de spikes (caso tenha spikes sera incrementada durante o programa)
    M2 = 0

    # ----------------#
    # Realiza edicoes #

    #se a quantidade de spikes for maior que zero
    if M1 > 0:

        #numero de vezes que serao realizadas edicoes (retirada de spikes)
        for j in range(P):

            #recalcula o numero de spikes
            sp = pl.find(np.abs(vetc[1:-1]) > (M * dp) )

            #coloca o valor medio no lugar do spike
            for i in range(len(sp)):

                vetc[sp[i]] = np.mean([ vetc[sp[i]-1] , vetc[sp[i]+1] ])

        #verifica se ainda permaneceu com spikes depois das iteracoes
        #Quantidade total de spikes depois das P iteracoes  
        M2 = len(sp)

    if M1 > N or M2 > 0:
    
        flag = flag + '1'
    
    else:
    
        flag = flag + '0'

    return flag, vetc
    
# ================================================================================== #

def t3(serie,flag):
    
    '''

    VALORES PROXIMOS DE ZERO
    * Verifica variacoes menores que 20 cm
    * Verifica se todos os valores de eta sao muito proximos de zero
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Posicao (indice) em 'lista_flag' : 3
    Aprovado  : flag = '0'
    Reprovado : flag = '1'
    
    '''

    if ( (serie < 0.1).all() and (serie > - 0.1).all() ):

        flag = flag + '1'
        
    else:
        
        flag = flag + '0'
        
    return flag




# ================================================================================== #

def t4(serie,ncn,flag):
    
    '''

    VERIFICA VALORES CONSECUTIVOS NULOS
    * Verifica valores consecutivos nulos
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      ncn - numero de valores consecutivos nulos testados
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Posicao (indice) em 'lista_flag' : 4
    Aprovado  : flag = '0'
    Reprovado : flag = '1'
    
    '''
    
    for i in range(len(serie)-ncn):
        
        if (serie[i:i+ncn] == 0).all():

            flag = flag + '1'
            
            break
            
        else:
            
            flag = flag + '0'
            
            break
            
    return flag
            

# ================================================================================== #

def t5(serie,nci,flag):
    
    '''

    VERIFICA VALORES CONSECUTIVOS IGUAIS
    * Verifica valores consecutivos iguais
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      nci - numero de valores consecutivos iguais testados
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Posicao (indice) em 'lista_flag' : 5
    Aprovado  : flag = '0'
    Reprovado : flag = '1'
    
    '''
    
    for i in range(len(serie)-(nci+1)):
        
        if (serie[i:i+nci] == serie[i+1:i+1+nci]).all():

            flag = flag + '1'
            
            break
        
        else:
            
            flag = flag + '0'
            
            break
            
    return flag
            

# ================================================================================== #

def t6(serie,linf,lsup,flag):
    
    '''

    VERIFICA VALORES QUE EXCEDEM DO LIMITE GROSSEIRO
    * Verifica valores que excedem limites grosseiros
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      linf - limite inferior
                      lsup - limite superior
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Posicao (indice) em 'lista_flag' : 6
    Aprovado  : flag = '0'
    Reprovado : flag = '1'
    
    '''
    
    if ( (serie > lsup).any() or (serie < linf).any() ):
        
        flag = flag + '1'
        
    else:
        
        flag = flag + '0'
    
    return flag    
    
# ================================================================================== #

# def t7(serie,linf,lsup,flag):
    
#     '''

#     CHECK-RATIO??? nos dados processados, nao?
#     * Verifica valores que excedem limites grosseiros
    
#     Dados de entrada: serie - (eta, dspx, dspy)


