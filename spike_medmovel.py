# ================================================================================== #
    
def t2(var,var1,M,hh,flag):
    
    '''
    
    TESTE SPYKE UTILIZANDO MEDIA MOVEL
    
    Dados de entrada: var - variavel
                      var1 - variavel editada
                      M - multiplicador do desvio padrao
                      despad - desvio padrao da serie
                      hh - tempo em horas para a media movel
                      flag - matriz de flags
    
    Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
                    flag - parametro + flag
       
    Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
         O flag utilizado para o teste de range eh: '1'
         Dados 'consistentes' recebem flag = '0'
    
    '''

    for i in range(len(var)):
        
        if var[i] < nanmean(var[i-int(hh/2):i+int(hh/2)])-M*nanstd(var[i-int(hh/2):i+int(hh/2)]) or var[i] > nanmean(var[i-hh/2:i+hh/2])+M*nanmean(var[i-int(hh/2):i+int(hh/2)]):
            
            flag[i] = flag[i] + '1'
            
            #o valor do dado inconsistente recebe 'nan'
            var1[i] = nan
            
        else:
            
            flag[i] = flag[i] + '0'
            
    return var1,flag
    
    
# ================================================================================== #