%%
clear all; close all; clc

% load vale_adcp1.out
% %# data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02
% load ADCP01
% %%% 1-Time 2-Day 3-Month 4-Year 5-Hour 6-?Min 
% %%% 7-Hm0 8-H10 9-Hmax 10-DirTp 11-SprTp 12-MeanDir 13-Tp 14-Tm02

%%
%%%%%%%%%%%%%%%%%%%%
%%% Selecionando %%%
%%%%%%%%%%%%%%%%%%%%

adcp=3;% Indique o ADCP da análise

ano=2013; %Indique o ano da análise
mes=7;% Indique o mês da análise

num=8;% Número de Configurações testadas

plote=5;%Indique quais plotes você quer ver
%0-NADA % 1-Grades; 2-Tempo; 3-Física
%4-Compara apenas Conf01 e Conf03
%5-Compara apenas Conf01 e Conf02

mensal=1;% Indique se já existe o dado do ADCP separado para o mês
% 1- Existe; 2-Precisa criar

%%
%%% ADCP e Mês de Interesse

nome=sprintf('%s%d','ADCP0',adcp);
disp(nome)

if adcp==1
    disp('ADCP01 só tem Conf01, Conf02 e Conf03')
    num=3;
    disp('ADCP01 só tem teste de grade')
    plote=5;%Compara apenas Conf01 e Conf02
end

if mes==2
    disp('Fevereiro: Cenário de Bom Tempo')
elseif mes==7
    disp('Julho: Cenário de Mau Tempo')
else
    disp('Verificar Mês')
    break
end

% break
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Carregando Resultados do Modelo %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% Lê resultados do SWAN (todas as configurações)
conf=[];
HsSWAN=[];TpSWAN=[];DpSWAN=[];

for c=1:num;
    
    clear temp02
    
    conf=[conf;sprintf('%s%d','Configuracao',c)];
    
    if adcp==1
        temp01=load(sprintf('%s%d%s%d%s%d%s','C:\Users\Talitha\Desktop\SWAN_RT3\SWAN_COARSE\ConfigRT3_',c,'\20130',mes,'\table_point_adcp',adcp,'.out'));
        % 1-Time 2-Hs(m) 3-Dp(º) 4-Tp(s) 5-u 6-v 7-HSwell(m) 8-DSpr(º)
    else
        temp01=load(sprintf('%s%d%s%d%s%d%s','C:\Users\Talitha\Desktop\SWAN_RT3\SWAN_FINE\ConfigRT3_',c,'r\20130',mes,'\table_point_ADCP0',adcp,'.out'));
    end

    tam=(length(temp01))-1;
    temp02=temp01(1:tam,:);
    HsSWAN=[HsSWAN,temp02(:,2)];
    TpSWAN=[TpSWAN,temp02(:,4)];
    DpSWAN=[DpSWAN,temp02(:,3)];
    
    clear temp01 

end

% break
clear c temp02
% break
%%
%%%%%%%%%%%%%%%%%%%%
%%% Dado do ADCP %%%
%%%%%%%%%%%%%%%%%%%%

%%% Lê dado do ADCP

if mensal==1
    disp('Carrega dado Mensal')
    dado=load(sprintf('%s%d%s%d%s%d%s','ADCP',(adcp),'_',(ano),'_',(mes),'.txt'));
    % tempo, data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02
    tempo=dado(:,1);
else
    disp('Cria dado Mensal')
    dado=load (sprintf('%s%d','vale_adcp',(adcp),'.out'));
    %  data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02

    %%% Cria tempo
    temp03=[];
    if mes==2
        disp('Fevereiro')
        for DD=1:28
            for HH=0:23
                temp03=[temp03;ano mes DD HH 0 0];
            end
        end
elseif mes==7
    disp('Julho')
    for DD=1:31
        for HH=0:23
            temp03=[temp03;ano mes DD HH 0 0];
        end
    end
    else
        disp ('Verificar Mes')
        break
    end
    % break
    clear DD HH

    %%% Criando número de data
    tempo=datenum(temp03(:,1),temp03(:,2),temp03(:,3),temp03(:,4),temp03(:,5),temp03(:,6));

    % break
    %%% Lê a data do arquivo do adcp
    tempo1=num2str(dado(:,1));
    yy=str2num(tempo1(:,1:4));
    mm=str2num(tempo1(:,5:6));
    dd=str2num(tempo1(:,7:8));
    ho=str2num(tempo1(:,9:10));
    % mi=str2num(tempo1(:,11:12));
    dado=[yy mm dd ho zeros(length(yy),1) zeros(length(yy),1) dado];

    % break
    clear tempo1 yy mm dd ho
    % break

    %%% Sepera o trecho nos dados medidos
    temp04=dado(find(dado(:,1)==ano),:);
    temp05=temp04(find(temp04(:,2)==mes),:);
    
    % break
    clear temp04
    % break

    %%% Verifica se tenho o mesmo número de linhas em medidos e modelados
    tam02=length(temp05);
    if tam==tam02
        disp('Mesmo n linhas')
        %%% Salvar arquivo para o mes
        dadon=[tempo temp05(:,7:15)];
        save ((sprintf('%s%d%s%d%s%d%s','ADCP',(adcp),'_',(ano),'_',(mes),'.txt')),'dadon','-ascii')
        dado=dadon;
        clear dadon
    else
        disp('Problema com n linhas')
%         break
        testea=find(temp03(1:tam02,4)~=temp05(:,4));
        disp(temp03(testea(1),1:4))
        disp(temp05(testea(1),1:4))
%         break
        [l c]=size(temp05);clear l
        inc(1:c)=NaN;
        inc(1:6)=temp03(testea(1),:);
        temp05=[temp05(1:(testea(1)-1),:); inc;temp05(testea(1):tam02,:)];
        tam02a=length(temp05);
        clear tam02 testea c
        if tam==tam02a
            disp('Corrigido (1) n linhas')
            clear inc tam02a
        else
            disp('Problema com n linhas (1)')
%             break
            clc
            testeb=find(temp03(1:tam02a,4)~=temp05(:,4));
            disp(temp03(testeb(1),1:4))
            disp(temp05(testeb(1),1:4))
%             break
            inc2=inc;
            inc2(1:6)=temp03(testeb(1),:);
            temp05=[temp05(1:(testeb(1)-1),:); inc2;temp05(testeb(1):tam02a,:)];
            tam02b=length(temp05);
            clear tam02a testeb
            if tam==tam02b
                disp('Corrigido (2) n linhas')
                testec=find(temp03(:,4)~=temp05(:,4))
                clear inc inc2 tam02b testec
        %%% Salvar arquivo para o mes
        dadon=[tempo temp05(:,7:15)];
        save ((sprintf('%s%d%s%d%s%d%s','ADCP',(adcp),'_',(ano),'_',(mes),'.txt')),'dadon','-ascii')
        dado=dadon;
        clear dadon
            else
                disp('Problema com n linhas (2)')
                break
            end
        end
    end

    % break
%     clear tam02 temp03 temp05
end

% break
%%
%%% Sepera dados medidos
    % tempo, data, 3-hm0, h10, hmax, 6-dirtp, sprtp, meandir, 9-tp, tm02
HsMED=dado(:,3);
TpMED=dado(:,9);
DpMED=dado(:,6);

% break
clear dado
%%
%%% Procurando erros nos resultados

%%
%%% Sinal suavizado c/ media de 3 pontos (filtro media-movel)
%%% Adaptado de Izabel Nogueira

Hst=[];
for p=1:tam
    if p==1
        Hst=[Hst; HsMED(p) HsMED(p) HsMED(p+1) HsMED(p) HsMED(p+2)];
    elseif p==2
        Hst=[Hst; HsMED(p) HsMED(p-1) HsMED(p+1) HsMED(p) HsMED(p+2)];
    elseif p==tam-1
        Hst=[Hst; HsMED(p) HsMED(p-1) HsMED(p+1) HsMED(p-2) HsMED(p)];
    elseif p==tam
        Hst=[Hst; HsMED(p) HsMED(p-1) HsMED(p) HsMED(p-2) HsMED(p)];        
    else
        Hst=[Hst; HsMED(p) HsMED(p-1) HsMED(p+1) HsMED(p-2) HsMED(p+2)];
    end
end
Hs_mm=nanmean(Hst,2);

    %%% Altura Significativa (Hs)
    figure()
    plot(tempo,HsMED,'color',[0.5 0.5 0.5])%Cinza-médio
    hold on
    plot(tempo,Hs_mm,'k')
    ylabel ('Hs (m)')
    title(datestr((tempo(1)),'mmmyyyy'))
    legend(nome,'Média Móvel')
    xlim([tempo(1) tempo(tam)])
    % ylim([0 2])%0.2 %([0 0.7]) ADCP02 Fevereiro
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d','RT3_mmovel_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

% break
clear Hst p
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Gráficos da Série Temporal %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% Gráficos comparando as configurações
%%% Variável plote indica o teste:  1-Grades; 2-Tempo; 3-Física

%%% Gráficos para cada parâmetro (Hs, Tp e Dp) e Subplot com os três
%%% parâmetros

%%% Salvar figuras como teste_parametro/subplot_ano_mes_adcp
    
if plote==0
    
    close all
    
elseif plote==1

    disp('Testes de Grade')
    
    %%% Altura Significativa (Hs)
    figure()
    plot(tempo,Hs_mm,'color',[0.5 0.5 0.5])%Cinza-médio
    hold on
    %%% Testes Grade:
    plot(tempo,HsSWAN(:,1),'b')
    plot(tempo,HsSWAN(:,2),'color',[0.5 0 0])%Vermelho escuro
    plot(tempo,HsSWAN(:,3),'g') %troquei esta cor
    ylabel ('Hs (m)')
    title(datestr((tempo(1)),'mmmyyyy'))
    legend(nome,'Conf01','Conf02','Conf03')
    xlim([tempo(1) tempo(tam)])
    % ylim([0 2])%0.2 %([0 0.7]) ADCP02 Fevereiro
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_grade_Hs_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

    %%% Período de Pico (Tp)
    figure()
    plot(tempo,TpMED,'.','color',[0.5 0.5 0.5])
    hold on
    %%% Testes Grade:
    plot(tempo,TpSWAN(:,1),'.b')
    plot(tempo,TpSWAN(:,2),'.','color',[0.5 0 0])%Vermelho escuro
    plot(tempo,TpSWAN(:,3),'.g') %troquei esta cor
    ylabel('Tp (s)')
    title(datestr((tempo(1)),'mmmyyyy'))
    legend(nome,'Conf01','Conf02','Conf03')%Comparação% 
    % ylim([2 18]) % ([0 18]) ADCP02 Fevereiro
    xlim([tempo(1) tempo(tam)])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_grade_Tp_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

    %%% Direção de Pico (Dp)
    figure()
    plot(tempo,DpMED,'.','color',[0.5 0.5 0.5])
    hold on
    % plot(tempo,DpMED-23.5,'.k')
    %%% Testes Grade:
    plot(tempo,DpSWAN(:,1),'.b')
    plot(tempo,DpSWAN(:,2),'.','color',[0.5 0 0])%Vermelho escuro
    plot(tempo,DpSWAN(:,3),'.g') %troquei esta cor
    % ylabel('Dp declinaçao (º)')
    ylabel('Dp (º)')
    title(datestr((tempo(1)),'mmmyyyy'))
    % legend(nome,'-23,5º','Conf01','Conf02','Conf03')
    legend(nome,'Conf01','Conf02','Conf03')
    % ylim([140 340])%ADCP02 ([80 260])Fevereiro
    % ylim([80 180])%ADCP03 (Fevereiro)
    xlim([tempo(1) tempo(tam)])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_grade_Dp_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

    %%% Subplot
    figure()
    subplot(3,1,1) %%% Altura Significativa (Hs)
    plot(tempo,Hs_mm,'color',[0.5 0.5 0.5])%Cinza-médio
    hold on
    %%% Testes Grade:
    plot(tempo,HsSWAN(:,1),'b')
    plot(tempo,HsSWAN(:,2),'color',[0.5 0 0])%Vermelho escuro
    plot(tempo,HsSWAN(:,3),'g') %troquei esta cor
    ylabel ('Hs (m)')
    title(datestr((tempo(1)),'mmmyyyy'))
    xlim([tempo(1) tempo(tam)])
    if adcp==1
        ylim([0 3])% ADCP01
    else
        ylim([0 2]) % ADCP02 e ADCP03
    end
    datetick('x',19,'keepticks','keeplimits')
    grid on

    legend(nome,'Conf01','Conf02','Conf03','Orientation','horizontal')

    subplot(3,1,2) %%% Período de Pico (Tp)
    plot(tempo,TpMED,'.','color',[0.5 0.5 0.5])
    hold on
    %%% Testes Grade:
    plot(tempo,TpSWAN(:,1),'.b')
    plot(tempo,TpSWAN(:,2),'.','color',[0.5 0 0])%Vermelho escuro
    plot(tempo,TpSWAN(:,3),'.g') %troquei esta cor
    ylabel('Tp (s)')
    xlim([tempo(1) tempo(tam)])
    ylim([0 20])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    subplot(3,1,3) %%% Direção de Pico (Dp)
    plot(tempo,DpMED,'.','color',[0.5 0.5 0.5])
    hold on
    % plot(tempo,DpMED-23.5,'.k')
    %%% Testes Grade:
    plot(tempo,DpSWAN(:,1),'.b')
    plot(tempo,DpSWAN(:,2),'.','color',[0.5 0 0])%Vermelho escuro
    plot(tempo,DpSWAN(:,3),'.g') %troquei esta cor
    % ylabel('Dp declinaçao (º)')
    ylabel('Dp (º)')
    xlim([tempo(1) tempo(tam)])
    ylim([0 360])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_grade_subplot_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )
    
    plot=4;

elseif plote==2
    
    disp('Teste de Passo de Tempo')
    
    %%% Altura Significativa (Hs)
    figure()
    plot(tempo,Hs_mm,'color',[0.5 0.5 0.5])%Cinza-médio
    hold on
    %%% Teste Passo de Tempo:
    plot(tempo,HsSWAN(:,3),'g') %troquei esta cor
    plot(tempo,HsSWAN(:,4),'.','color',[1 0.4 0])%Laranja
    ylabel ('Hs (m)')
    title(datestr((tempo(1)),'mmmyyyy'))
    legend(nome,'90s','60s')
    xlim([tempo(1) tempo(tam)])
    % ylim([0 2])%0.2 %([0 0.7]) ADCP02 Fevereiro
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_tempo_Hs_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

    %%% Período de Pico (Tp)
    figure()
    plot(tempo,TpMED,'.','color',[0.5 0.5 0.5])
    hold on
    %%% Teste Passo de Tempo:
    plot(tempo,TpSWAN(:,3),'.g') %troquei esta cor
    plot(tempo,TpSWAN(:,4),'o','color',[1 0.4 0])%Laranja
    ylabel('Tp (s)')
    title(datestr((tempo(1)),'mmmyyyy'))
    legend(nome,'90s','60s')
    % ylim([2 18]) % ([0 18]) ADCP02 Fevereiro
    xlim([tempo(1) tempo(tam)])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_tempo_Tp_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

    %%% Direção de Pico (Dp)
    figure()
    plot(tempo,DpMED,'.','color',[0.5 0.5 0.5])
    hold on
    % plot(tempo,DpMED-23.5,'.k')
    %%% Teste Passo de Tempo:
    plot(tempo,DpSWAN(:,3),'.g') %troquei esta cor
    plot(tempo,DpSWAN(:,4),'o','color',[1 0.4 0])%Laranja
    % ylabel('Dp declinaçao (º)')
    ylabel('Dp (º)')
    title(datestr((tempo(1)),'mmmyyyy'))
    % legend(nome,'-23,5º','Conf01','Conf02','Conf03')
    legend(nome,'90s','60s')
    % ylim([140 340])%ADCP02 ([80 260])Fevereiro
    % ylim([80 180])%ADCP03 (Fevereiro)
    xlim([tempo(1) tempo(tam)])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_tempo_Dp_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

    %%% Subplot
    figure()
    subplot(3,1,1) %%% Altura Significativa (Hs)
    plot(tempo,Hs_mm,'color',[0.5 0.5 0.5])%Cinza-médio
    hold on
    %%% Teste Passo de Tempo:
    plot(tempo,HsSWAN(:,3),'g') %troquei esta cor
    plot(tempo,HsSWAN(:,4),'.','color',[1 0.4 0])%Laranja
    ylabel ('Hs (m)')
    title(datestr((tempo(1)),'mmmyyyy'))
    xlim([tempo(1) tempo(tam)])
    if adcp==1
        ylim([0 3])% ADCP01
    else
        ylim([0 2]) % ADCP02 e ADCP03
    end
    datetick('x',19,'keepticks','keeplimits')
    grid on

    legend(nome,'90s','60s','Orientation','horizontal')
    
    subplot(3,1,2) %%% Período de Pico (Tp)
    plot(tempo,TpMED,'.','color',[0.5 0.5 0.5])
    hold on
    %%% Teste Passo de Tempo:
    plot(tempo,TpSWAN(:,3),'.g') %troquei esta cor
    plot(tempo,TpSWAN(:,4),'o','color',[1 0.4 0])%Laranja
    ylabel('Tp (s)')
    xlim([tempo(1) tempo(tam)])
    ylim([0 20])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    subplot(3,1,3) %%% Direção de Pico (Dp)
    plot(tempo,DpMED,'.','color',[0.5 0.5 0.5])
    hold on
    % plot(tempo,DpMED-23.5,'.k')
    %%% Teste Passo de Tempo:
    plot(tempo,DpSWAN(:,3),'.g') %troquei esta cor
    plot(tempo,DpSWAN(:,4),'o','color',[1 0.4 0])%Laranja
    % ylabel('Dp declinaçao (º)')
    ylabel('Dp (º)')
    xlim([tempo(1) tempo(tam)])
    ylim([0 360])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_tempo_subplot_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

elseif plote==3
    
    disp('Teste Fisica')
    
    %%% Altura Significativa (Hs)
    figure()
    plot(tempo,Hs_mm,'color',[0.5 0.5 0.5])%Cinza-médio
    hold on
    %%% Teste Fisica:
    plot(tempo,HsSWAN(:,5),'r')
    plot(tempo,HsSWAN(:,6),'color',[0 0.5 0])%Verde-escuro
    plot(tempo,HsSWAN(:,7),'c')
    plot(tempo,HsSWAN(:,8),'color',[0.67 0 1])%Violeta    
    ylabel ('Hs (m)')
    title(datestr((tempo(1)),'mmmyyyy'))
    legend(nome,'Conf05','Conf06','Conf07','Conf08')
    xlim([tempo(1) tempo(tam)])
    % ylim([0 2])%0.2 %([0 0.7]) ADCP02 Fevereiro
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_fisica_Hs_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

    %%% Período de Pico (Tp)
    figure()
    plot(tempo,TpMED,'.','color',[0.5 0.5 0.5])
    hold on
    %%% Teste Fisica:
    plot(tempo,TpSWAN(:,5),'.r')
    plot(tempo,TpSWAN(:,6),'.','color',[0 0.5 0])%Verde-escuro
    plot(tempo,TpSWAN(:,7),'.c')
    plot(tempo,TpSWAN(:,8),'.','color',[0.67 0 1])%Violeta 
    ylabel('Tp (s)')
    title(datestr((tempo(1)),'mmmyyyy'))
    legend(nome,'Conf05','Conf06','Conf07','Conf08')
    % ylim([2 18]) % ([0 18]) ADCP02 Fevereiro
    xlim([tempo(1) tempo(tam)])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_fisica_Tp_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

    %%% Direção de Pico (Dp)
    figure()
    plot(tempo,DpMED,'.','color',[0.5 0.5 0.5])
    hold on
    % plot(tempo,DpMED-23.5,'.k')
    %%% Teste Fisica:
    plot(tempo,DpSWAN(:,5),'.r')
    plot(tempo,DpSWAN(:,6),'.','color',[0 0.5 0])%Verde-escuro
    plot(tempo,DpSWAN(:,7),'.c')
    plot(tempo,DpSWAN(:,8),'.','color',[0.67 0 1])%Violeta 
    
    title(datestr((tempo(1)),'mmmyyyy'))
    ylabel('Dp (º)')
    % ylabel('Dp declinaçao (º)')
    % legend(nome,'-23,5º','Conf01','Conf02','Conf03')
    legend(nome,'Conf05','Conf06','Conf07','Conf08')
    % ylim([140 340])%ADCP02 ([80 260])Fevereiro
    % ylim([80 180])%ADCP03 (Fevereiro)
    xlim([tempo(1) tempo(tam)])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=sprintf('%s%d%s%d%s%d%s','RT3_fisica_Dp_',(ano),'_',(mes),'_ADCP',(adcp));
    print( gcf, '-dpng', nf )

    %%% Subplot
    figure()
    subplot(3,1,1) %%% Altura Significativa (Hs)
    plot(tempo,Hs_mm,'color',[0.5 0.5 0.5])%Cinza-médio
    hold on
    %%% Teste Fisica:
    plot(tempo,HsSWAN(:,5),'r')
    plot(tempo,HsSWAN(:,6),'color',[0 0.5 0])%Verde-escuro
    plot(tempo,HsSWAN(:,7),'c')
    plot(tempo,HsSWAN(:,8),'color',[0.67 0 1])%Violeta    
    ylabel ('Hs (m)')
    title(datestr((tempo(1)),'mmmyyyy'))
    xlim([tempo(1) tempo(tam)])
    if adcp==1
        ylim([0 3])% ADCP01
    else
        ylim([0 2]) % ADCP02 e ADCP03
    end
    datetick('x',19,'keepticks','keeplimits')
    grid on

    legend(nome,'Conf05','Conf06','Conf07','Conf08','Orientation','horizontal')

    subplot(3,1,2) %%% Período de Pico (Tp)
    plot(tempo,TpMED,'.','color',[0.5 0.5 0.5])
    hold on
    %%% Teste Fisica:
    plot(tempo,TpSWAN(:,5),'.r')
    plot(tempo,TpSWAN(:,6),'.','color',[0 0.5 0])%Verde-escuro
    plot(tempo,TpSWAN(:,7),'.c')
    plot(tempo,TpSWAN(:,8),'.','color',[0.67 0 1])%Violeta 
    ylabel('Tp (s)')
    xlim([tempo(1) tempo(tam)])
    ylim([0 20])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    subplot(3,1,3) %%% Direção de Pico (Dp)
    plot(tempo,DpMED,'.','color',[0.5 0.5 0.5])
    hold on
    % plot(tempo,DpMED-23.5,'.k')
    %%% Teste Fisica:
    plot(tempo,DpSWAN(:,5),'.r')
    plot(tempo,DpSWAN(:,6),'.','color',[0 0.5 0])%Verde-escuro
    plot(tempo,DpSWAN(:,7),'.c')
    plot(tempo,DpSWAN(:,8),'.','color',[0.67 0 1])%Violeta 
    % ylabel('Dp declinaçao (º)')
    ylabel('Dp (º)')
    xlim([tempo(1) tempo(tam)])
    ylim([0 360])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_fisica_subplot_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

elseif plote==4
        
    disp('Testes de Grade SWAN_FINE')
    
    %%% Altura Significativa (Hs)
    figure()
    plot(tempo,Hs_mm,'color',[0.5 0.5 0.5])%Cinza-médio
    hold on
    %%% Testes Grade:
    plot(tempo,HsSWAN(:,1),'b')
    plot(tempo,HsSWAN(:,3),'g') %troquei esta cor
    ylabel ('Hs (m)')
    title(datestr((tempo(1)),'mmmyyyy'))
    legend(nome,'Conf01','Conf03')
    xlim([tempo(1) tempo(tam)])
    % ylim([0 2])%0.2 %([0 0.7]) ADCP02 Fevereiro
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_grade_fine_Hs_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

    %%% Período de Pico (Tp)
    figure()
    plot(tempo,TpMED,'.','color',[0.5 0.5 0.5])
    hold on
    %%% Testes Grade:
    plot(tempo,TpSWAN(:,1),'.b')
    plot(tempo,TpSWAN(:,3),'.g') %troquei esta cor
    ylabel('Tp (s)')
    title(datestr((tempo(1)),'mmmyyyy'))
    legend(nome,'Conf01','Conf03')%Comparação% 
    % ylim([2 18]) % ([0 18]) ADCP02 Fevereiro
    xlim([tempo(1) tempo(tam)])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_grade_fine_Tp_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

    %%% Direção de Pico (Dp)
    figure()
    plot(tempo,DpMED,'.','color',[0.5 0.5 0.5])
    hold on
    % plot(tempo,DpMED-23.5,'.k')
    %%% Testes Grade:
    plot(tempo,DpSWAN(:,1),'.b')
    plot(tempo,DpSWAN(:,3),'.g') %troquei esta cor
    % ylabel('Dp declinaçao (º)')
    ylabel('Dp (º)')
    title(datestr((tempo(1)),'mmmyyyy'))
    % legend(nome,'-23,5º','Conf01','Conf02','Conf03')
    legend(nome,'Conf01','Conf03')
    % ylim([140 340])%ADCP02 ([80 260])Fevereiro
    % ylim([80 180])%ADCP03 (Fevereiro)
    xlim([tempo(1) tempo(tam)])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_grade_fine_Dp_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

    %%% Subplot
    figure()
    subplot(3,1,1) %%% Altura Significativa (Hs)
    plot(tempo,Hs_mm,'color',[0.5 0.5 0.5])%Cinza-médio
    hold on
    %%% Testes Grade:
    plot(tempo,HsSWAN(:,1),'b')
    plot(tempo,HsSWAN(:,3),'g') %troquei esta cor
    ylabel ('Hs (m)')
    title(datestr((tempo(1)),'mmmyyyy'))
    xlim([tempo(1) tempo(tam)])
    if adcp==1
        ylim([0 3])% ADCP01
    else
        ylim([0 2]) % ADCP02 e ADCP03
    end
    datetick('x',19,'keepticks','keeplimits')
    grid on

    legend(nome,'Conf01','Conf03','Orientation','horizontal')

    subplot(3,1,2) %%% Período de Pico (Tp)
    plot(tempo,TpMED,'.','color',[0.5 0.5 0.5])
    hold on
    %%% Testes Grade:
    plot(tempo,TpSWAN(:,1),'.b')
    plot(tempo,TpSWAN(:,3),'.g') %troquei esta cor
    ylabel('Tp (s)')
    xlim([tempo(1) tempo(tam)])
    ylim([0 20])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    subplot(3,1,3) %%% Direção de Pico (Dp)
    plot(tempo,DpMED,'.','color',[0.5 0.5 0.5])
    hold on
    % plot(tempo,DpMED-23.5,'.k')
    %%% Testes Grade:
    plot(tempo,DpSWAN(:,1),'.b')
    plot(tempo,DpSWAN(:,3),'.g') %troquei esta cor
    % ylabel('Dp declinaçao (º)')
    ylabel('Dp (º)')
    xlim([tempo(1) tempo(tam)])
    ylim([0 360])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_grade_fine_subplot_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )
    
    plot=5;

elseif plote==5

    disp('Testes de Grade SWAN_COARSE')
    
    %%% Altura Significativa (Hs)
    figure()
    plot(tempo,Hs_mm,'color',[0.5 0.5 0.5])%Cinza-médio
    hold on
    %%% Testes Grade:
    plot(tempo,HsSWAN(:,1),'b')
    plot(tempo,HsSWAN(:,2),'color',[0.5 0 0])%Vermelho escuro
    ylabel ('Hs (m)')
    title(datestr((tempo(1)),'mmmyyyy'))
    legend(nome,'Conf01','Conf02')
    xlim([tempo(1) tempo(tam)])
    % ylim([0 2])%0.2 %([0 0.7]) ADCP02 Fevereiro
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_grade_coarse_Hs_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

    %%% Período de Pico (Tp)
    figure()
    plot(tempo,TpMED,'.','color',[0.5 0.5 0.5])
    hold on
    %%% Testes Grade:
    plot(tempo,TpSWAN(:,1),'.b')
    plot(tempo,TpSWAN(:,2),'.','color',[0.5 0 0])%Vermelho escuro
    ylabel('Tp (s)')
    title(datestr((tempo(1)),'mmmyyyy'))
    legend(nome,'Conf01','Conf02')%Comparação% 
    % ylim([2 18]) % ([0 18]) ADCP02 Fevereiro
    xlim([tempo(1) tempo(tam)])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_grade_coarse_Tp_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

    %%% Direção de Pico (Dp)
    figure()
    plot(tempo,DpMED,'.','color',[0.5 0.5 0.5])
    hold on
    % plot(tempo,DpMED-23.5,'.k')
    %%% Testes Grade:
    plot(tempo,DpSWAN(:,1),'.b')
    plot(tempo,DpSWAN(:,2),'.','color',[0.5 0 0])%Vermelho escuro
    % ylabel('Dp declinaçao (º)')
    ylabel('Dp (º)')
    title(datestr((tempo(1)),'mmmyyyy'))
    % legend(nome,'-23,5º','Conf01','Conf02','Conf03')
    legend(nome,'Conf01','Conf02')
    % ylim([140 340])%ADCP02 ([80 260])Fevereiro
    % ylim([80 180])%ADCP03 (Fevereiro)
    xlim([tempo(1) tempo(tam)])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_grade_coarse_Dp_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

    %%% Subplot
    figure()
    subplot(3,1,1) %%% Altura Significativa (Hs)
    plot(tempo,Hs_mm,'color',[0.5 0.5 0.5])%Cinza-médio
    hold on
    %%% Testes Grade:
    plot(tempo,HsSWAN(:,1),'b')
    plot(tempo,HsSWAN(:,2),'color',[0.5 0 0])%Vermelho escuro
    ylabel ('Hs (m)')
    title(datestr((tempo(1)),'mmmyyyy'))
    xlim([tempo(1) tempo(tam)])
    if adcp==1
        ylim([0 3])% ADCP01
    else
        ylim([0 2]) % ADCP02 e ADCP03
    end
    datetick('x',19,'keepticks','keeplimits')
    grid on

    legend(nome,'Conf01','Conf02','Orientation','horizontal')

    subplot(3,1,2) %%% Período de Pico (Tp)
    plot(tempo,TpMED,'.','color',[0.5 0.5 0.5])
    hold on
    %%% Testes Grade:
    plot(tempo,TpSWAN(:,1),'.b')
    plot(tempo,TpSWAN(:,2),'.','color',[0.5 0 0])%Vermelho escuro
    ylabel('Tp (s)')
    xlim([tempo(1) tempo(tam)])
    ylim([0 20])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    subplot(3,1,3) %%% Direção de Pico (Dp)
    plot(tempo,DpMED,'.','color',[0.5 0.5 0.5])
    hold on
    % plot(tempo,DpMED-23.5,'.k')
    %%% Testes Grade:
    plot(tempo,DpSWAN(:,1),'.b')
    plot(tempo,DpSWAN(:,2),'.','color',[0.5 0 0])%Vermelho escuro
    % ylabel('Dp declinaçao (º)')
    ylabel('Dp (º)')
    xlim([tempo(1) tempo(tam)])
    ylim([0 360])
    datetick('x',19,'keepticks','keeplimits')
    grid on

    nf=(sprintf('%s%d%s%d%s%d%s','RT3_grade_coarse_subplot_',(ano),'_',(mes),'_ADCP',(adcp)));
    print( gcf, '-dpng', nf )

end
clear nf Hs_mm
%%
% %%% Antigas 'y' 'g'
% % % legend('ADCP02','SWAN 60x45','SWAN 120x90','WW3')
% % % legend('ADCP02',''0m OFF all','0,8m OFF all?','0m Diffrac')
% % % legend('ADCP02','Padrão','Com Fricção','Fricção e NM 0,8m','Com Difração')

% % legend(...,'Orientation','horizontal','Location','South')
% % legend(...,'Orientation','horizontal','Location','BestOutside')

%%% Fazer direção com pontos tbm...

%%% Conferir cores %%% legenda

% break
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Série Temporal das Configurações %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% Subplot de Hs, Tp e Dp para cada configuração

% % salvar figuras como subplot_mes_adcp_configuracao
% 
% [num a]=size(conf);
% clear a
% 
% for c=1:num
%     figure()
%     subplot(3,1,1) %%% Altura Significativa (Hs)
%     plot(tempo,Hs_mm,'color',[0.5 0.5 0.5])%Cinza-médio
%     hold on
%     plot(tempo,HsSWAN(:,c))
%     ylabel ('Hs (m)')
%     xlim([tempo(1) tempo(tam)])
%     % ylim([0 2]) % ylim[(0.1 0.8]) % Fevereiro  %Julho %([0 1]) ADCP02 FEV
%     datetick('x',19,'keepticks','keeplimits')
%     grid on
%     
%     title(datestr((tempo(1)),'mmmyyyy'))
%     legend(nome,conf(c),'Orientation','horizontal')
% 
%     subplot(3,1,2) %%% Período de Pico (Tp)
%     plot(tempo,TpMED,'.','color',[0.5 0.5 0.5])
%     hold on
%     plot(tempo,TpSWAN(:,c),'.')
%     ylabel('Tp (s)')
%     xlim([tempo(1) tempo(tam)])
%     % ylim([2 18])% ylim([4 18]) %Fevereiro % ylim([ ]) % Julho
%     %ylim([0 20])
%     datetick('x',19,'keepticks','keeplimits')
%     grid on
% 
%     subplot(3,1,3) %%% Direção de Pico (Dp)
%     plot(tempo,DpMED,'.','color',[0.5 0.5 0.5])
%     hold on
%     plot(tempo,DpSWAN(:,c),'.')
%     ylabel('Dp (º)')
%     xlim([tempo(1) tempo(tam)])
% %     ylim([0 360])% ylim([140 340])%ADCP02 % ylim([100 180])%ADCP03
%     % ([100 200])([0 400]) ([0 200])
%     datetick('x',19,'keepticks','keeplimits')
%     grid on
% end

% break
%%
%%% Estatística Mensal

%%% Estatatística 01: Percentil (0% 50% 90% 100%), Média e Desvio Padrão

estHs01=[0 prctile(HsMED,[0,50,90,100]) nanmean(HsMED) nanstd(HsMED)];
estTp01=[0 prctile(TpMED,[0,50,90,100]) nanmean(TpMED) nanstd(TpMED)];
estDp01=[0 prctile(DpMED,[0,50,90,100]) nanmean(DpMED) nanstd(DpMED)];

for pp=1:num
    estHs01=[estHs01; pp prctile(HsSWAN(:,pp),[0,50,90,100]) nanmean(HsSWAN(:,pp)) nanstd(HsSWAN(:,pp))];
    estTp01=[estTp01; pp prctile(TpSWAN(:,pp),[0,50,90,100]) nanmean(TpSWAN(:,pp)) nanstd(TpSWAN(:,pp))];
    estDp01=[estDp01; pp prctile(DpSWAN(:,pp),[0,50,90,100]) nanmean(DpSWAN(:,pp)) nanstd(DpSWAN(:,pp))];
end

% break
clear pp tam

%%
%%% Retira dados com NaN da série

temp06=find(isnan(HsMED)==0);

HsMEDs=HsMED(temp06);
TpMEDs=TpMED(temp06);
DpMEDs=DpMED(temp06);
tempoS=tempo(temp06);
clear HsMED TpMED DpMED tempo

HsSWANs=HsSWAN(temp06,:);
TpSWANs=TpSWAN(temp06,:);
DpSWANs=DpSWAN(temp06,:);
clear HsSWAN TpSWAN DpSWAN

clear temp06

%%% Refazer est01 para comparar e controlar..

% break
%%
%%% Estatística 02: Bias, EQM (MSE), RMSE, 

tam03=length(tempoS);

estHs02=[];estTp02=[];estDp02=[];

for ppp=1:num
    
    %%% BIAS (tendenciosidade/vício)
    biasHs=mean(HsSWANs(:,ppp)-HsMEDs);
    biasTp=mean(TpSWANs(:,ppp)-TpMEDs);
    biasDp=mean(DpSWANs(:,ppp)-DpMEDs);

    %%% Erro médio Quadrático
    emqHs=sum((HsSWANs(:,ppp)-HsMEDs).^2)/tam03;%Pq .^???
    rmseHs=sqrt(emqHs);
    emqTp=sum((TpSWANs(:,ppp)-TpMEDs).^2)/tam03;
    rmseTp=sqrt(emqTp);
    emqDp=sum((DpSWANs(:,ppp)-DpMEDs).^2)/tam03;
    rmseDp=sqrt(emqDp);
    
    %%% Índice de Espalhamento (baseado rotina Izabel)
    SIHs= rmseHs/mean(HsMEDs);
    SITp= rmseTp/mean(TpMEDs);
    SIDp= rmseDp/mean(DpMEDs);
    
    %%% Correlação
    corHs=corr(HsMEDs,HsSWANs(:,ppp));
    corTp=corr(TpMEDs,TpSWANs(:,ppp));
    corDp=corr(DpMEDs,DpSWANs(:,ppp));

    estHs02=[estHs02; ppp biasHs emqHs rmseHs SIHs corHs];
    estTp02=[estTp02; ppp biasTp emqTp rmseTp SITp corTp];
    estDp02=[estDp02; ppp biasDp emqDp rmseDp SIDp corDp];

end

% break
clear tam03 ppp
clear biasHs emqHs rmseHs SIHs corHs
clear biasTp emqTp rmseTp SITp corTp
clear biasDp emqDp rmseDp SIDp corDp

% save('teste.txt','conf','-ascii')
