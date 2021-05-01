## Verifica valores fora do limite de medicao de cada sensor

from copy import copy

#------------------------------------------------------------#
#temperatura do ar
def tar(tar2):
    '''Teste de valores fora do
limite do sensor'''

    #indices dos erros
    iflagtar2=[]
    #numero do flag
    flagtar2=[]
    #quantidade de erro
    cflagtar2=[]
    
    for i in range(0,len(tar2)):

        if tar2[i]<-52 or tar2[i]>60:

            #cria vetor com indices dos erros
            iflagtar2.append(i)
                
    #quantidade de erros na serie
    cflagtar2=len(iflagtar2)

    #cria flags de 0 a 2
    if cflagtar2==0:
        
        #se nao tiver erro, flagtar2=0
        flagtar2='0'
    
    elif cflagtar2<=6:
        
        #se tiver ate 6 erros (1% da serie)
        flagtar2='1'    

    else:
        
        #se tiver mais que 6 erros na serie, flagtar=2
        flagtar2='2'
    
    return iflagtar2,cflagtar2,flagtar2

#------------------------------------------------------------#
#umidade relativa
def ur(ur2):
    '''Teste de valores fora do
limite do sensor'''

    #indices dos erros
    iflagur2=[]
    #numero do flag
    flagur2=[]
    #quantidade de erro
    cflagur2=[]
    
    for i in range(0,len(ur2)):

        if ur2[i]<0 or ur2[i]>100:

            #cria vetor com indices dos erros
            iflagur2.append(i)
                
    #quantidade de erros na serie
    cflagur2=len(iflagur2)

    #cria flags de 0 a 2
    if cflagur2==0:
        
        #se nao tiver erro, flagur2=0
        flagur2='0'
    
    elif cflagur2<=6:
        
        #se tiver ate 6 erros (1% da serie)
        flagur2='1'    

    else:
        
        #se tiver mais que 6 erros na serie, flagur=2
        flagur2='2'
    
    return iflagur2,cflagur2,flagur2

#------------------------------------------------------------#
#pressao atmosferica
def pr(pr2):
    '''Teste de valores fora do
limite do sensor'''

    #indices dos erros
    iflagpr2=[]
    #numero do flag
    flagpr2=[]
    #quantidade de erro
    cflagpr2=[]
    
    for i in range(0,len(pr2)):

        if pr2[i]<600 or pr2[i]>1100:

            #cria vetor com indices dos erros
            iflagpr2.append(i)
                
    #quantidade de erros na serie
    cflagpr2=len(iflagpr2)

    #cria flags de 0 a 2
    if cflagpr2==0:
        
        #se nao tiver erro, flagpr2=0
        flagpr2='0'
    
    elif cflagpr2<=6:
        
        #se tiver ate 6 erros (1% da serie)
        flagpr2='1'    

    else:
        
        #se tiver mais que 6 erros na serie, flagpr=2
        flagpr2='2'
    
    return iflagpr2,cflagpr2,flagpr2

#------------------------------------------------------------#
#velocidade do vento
def velv(velv2):
    '''Teste de valores fora do
limite do sensor'''

    #indices dos erros
    iflagvelv2=[]
    #numero do flag
    flagvelv2=[]
    #quantidade de erro
    cflagvelv2=[]
    
    for i in range(0,len(velv2)):

        if velv2[i]<0 or velv2[i]>60:

            #cria vetor com indices dos erros
            iflagvelv2.append(i)
                
    #quantidade de erros na serie
    cflagvelv2=len(iflagvelv2)

    #cria flags de 0 a 2
    if cflagvelv2==0:
        
        #se nao tiver erro, flagvelv2=0
        flagvelv2='0'
    
    elif cflagvelv2<=6:
        
        #se tiver ate 6 erros (1% da serie)
        flagvelv2='1'    

    else:
        
        #se tiver mais que 6 erros na serie, flagvelv=2
        flagvelv2='2'
    
    return iflagvelv2,cflagvelv2,flagvelv2

#------------------------------------------------------------#
#velocidade do vento
def dirv(dirv2):
    '''Teste de valores fora do
limite do sensor'''

    #indices dos erros
    iflagdirv2=[]
    #numero do flag
    flagdirv2=[]
    #quantidade de erro
    cflagdirv2=[]
    
    for i in range(0,len(dirv2)):

        if dirv2[i]<0 or dirv2[i]>360:

            #cria vetor com indices dos erros
            iflagdirv2.append(i)
                
    #quantidade de erros na serie
    cflagdirv2=len(iflagdirv2)

    #cria flags de 0 a 2
    if cflagdirv2==0:
        
        #se nao tiver erro, flagdirv2=0
        flagdirv2='0'
    
    elif cflagdirv2<=6:
        
        #se tiver ate 6 erros (1% da serie)
        flagdirv2='1'    

    else:
        
        #se tiver mais que 6 erros na serie, flagdirv=2
        flagdirv2='2'
    
    return iflagdirv2,cflagdirv2,flagdirv2

