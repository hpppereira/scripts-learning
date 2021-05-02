%%
clear all; close all; clc

%%
%%%%%%%%%%%%%%%%%%%%
%%% Selecionando %%%
%%%%%%%%%%%%%%%%%%%%

adcp=3;% Indique o ADCP da análise

mensal=1;% Indique se já existe o arquivo com todos os dados
% 1- Existe; 2-Precisa criar
%%% Informações Necessárias para Criar o Arquivo Completo
% ano_ini=2013;
% mes_ini=1;
% num=3;% Número de Meses

estHs=[];estTp=[];estDp=[];
%%
%%% Loop para fazer todos ADCPs em uma rodada

%%
%%% ADCP e Mês de Interesse

nome=sprintf('%s%d','ADCP0',adcp);
disp(nome)

% break
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Carregando Resultados do Modelo %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if mensal==1
    
    disp('Carrega dados completos')

    dado=load(sprintf('%s%d%s','RT3_ADCP',(adcp),'.txt'));
    %%% Tempo; Time; Hsig[m]; PkDir [degr]; RTpeak[sec]; X-Windv[m/s]; Y-Windv[m/s]; Hswell [m]; Dspr[degr]

elseif mensal==2

    disp('Cria dados completos')

    data_inicio=sprintf('%s%d%s%d','Ano:',ano_ini,' Mes:',mes_ini);
    disp(data_inicio)

    %%% Lê resultados do SWAN (todo hindcast)
    ano=ano_ini; mes=mes_ini;tempo01=[];temp02=[];tempo02=[];
    
    for t=1:num
        
        %%% Lendo Arquivos
        %%% Time; Hsig[m]; PkDir [degr]; RTpeak[sec]; X-Windv[m/s]; Y-Windv[m/s]; Hswell [m]; Dspr[degr]        
        if mes<10
            if adcp==1
                temp01=load(sprintf('%s%d%s%d%s','C:\Users\Talitha\Desktop\SWAN_RT3\hindcast\',ano,'0',mes,'\table_point.out'));
            else
                temp01=load(sprintf('%s%d%s%d%s%d%s','C:\Users\Talitha\Desktop\SWAN_RT3\hindcast\',ano,'0',mes,'\table_point_ADCP0',adcp,'.out'));
            end
        else
            if adcp==1
                temp01=load(sprintf('%s%d%d%s','C:\Users\Talitha\Desktop\SWAN_RT3\hindcast\',ano,mes,'\table_point.out'));
            else
                temp01=load(sprintf('%s%d%d%s%d%s','C:\Users\Talitha\Desktop\SWAN_RT3\hindcast\',ano,mes,'\table_point_ADCP0',adcp,'.out'));
            end
        end
        
        %%% Cria tempo
        tam01=length(temp01)-1
        if mes==1||mes==3||mes==5||mes==7||mes==8||mes==10||mes==12
            % Janeiro, Março, Maio, Julho, Agosto, Outobro, Dezembro
            for DD=1:31
                for HH=0:23
                    tempo02=[tempo02;ano mes DD HH 0 0];
                end
            end
        elseif mes==2
            if tam01==672 %Fevereiro Normal
                for DD=1:28
                    for HH=0:23
                        tempo02=[tempo02;ano mes DD HH 0 0];
                    end
                end
            elseif tam01==29 %Fevereiro Bissexto
                disp ('Ano Bissexto')            
                break
            else
                disp ('Verificar Mes')            
                break
            end
        elseif mes==4||mes==6||mes==9||mes==11 % Abril, Junho, Setembro, Novembro
            disp ('Verificar Mes')            
            break
        else
            disp ('Verificar Mes')
            break
        end
        
        clear DD HH

        %%% Criando número de data
        tempo03=datenum(tempo02(:,1),tempo02(:,2),tempo02(:,3),tempo02(:,4),tempo02(:,5),tempo02(:,6));
        tempo02=[];

        %%% Criando variável Dado
        temp02=[temp02; tempo03 temp01(1:tam01,:)];
        clear temp01 tempo03 tam01

        %%% Salvando mês e dia da análise
        tempo01=[tempo01;ano mes];
        
        %%% Contador do tempo
        mes=mes+1;
        if mes>12
            mes=1;
            ano=ano+1;
        end
    end
    
    %%% Salvar Arquivo
    dado=temp02;
    save ((sprintf('%s%d%s','RT3_ADCP',(adcp),'.txt')),'dado','-ascii')
    
    clear ano mes t temp02 tempo02
    
end

% break
clear ano_ini mes_ini num 
%%

%%% 1-Tempo; Time; 3-Hsig[m]; 4-PkDir [degr]; 5-RTpeak[sec]; X-Windv[m/s]; Y-Windv[m/s]; Hswell [m]; Dspr[degr]        

Hs=[dado(:,3)];
Tp=[dado(:,5)];
Dp=[dado(:,4)];
tempo=[dado(:,1)];

% break
clear dado
%%
%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Tabela Parâmetros %%%
%%%%%%%%%%%%%%%%%%%%%%%%%

%%% Média %%% 90º Percentil %%% Máximo

%%% Estatatística: Percentil (0% 50% 90% 100%), Média e Desvio Padrão

estHs=[estHs;adcp prctile(Hs,[0,50,90,100]) nanmean(Hs) nanstd(Hs)];
estTp=[estTp;adcp prctile(Tp,[0,50,90,100]) nanmean(Tp) nanstd(Tp)];
estDp=[estDp;adcp prctile(Dp,[0,50,90,100]) nanmean(Dp) nanstd(Dp)];

% break
%%
%%%%%%%%%%%%%%%%%%
%%% Histograma %%%
%%%%%%%%%%%%%%%%%%

tam=length(tempo);

clHs=0:0.5:6;
valHs=(hist(Hs,clHs))./tam;

figure ()
hist(Hs,clHs)
title(nome)
grid on
% ytick(double(clHs))
break
close all
%%


%%
%%% Distribuição Conjunta



%%
%%%%%%%%%%%%%%%%%%%%
%%% Rosa de Onda %%%
%%%%%%%%%%%%%%%%%%%%


