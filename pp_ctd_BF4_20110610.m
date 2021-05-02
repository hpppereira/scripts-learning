%% Tratamento de dados do CTD bota fora 4 campo 3, dia 10/06/2011
clear,clc,close all
% Serie / Meas / Sal. / TºC / Turb (FTU) / Dens / Prof / Dia / Mes / Ano / Hora / Min / Seg
%   1       2      3      4      5           6      7     8     9     10    11    12     13

%% Carregar dados brutos do ctd
%Não pode ter lacuna nos dados, nem na série nem na medição

dados=load('ctd_20110610.txt');
%retira valores que nao entraram na agua
dados1=dados(find(dados(:,7)>=0),:);
%coloca as medidas em ordem
meas=[1:length(dados1)]';
dados1(:,2)=meas;

%condição para ajustas as séries de forma que fique sem lacunas
% 
% for i=2:length(dados1)-1
%     
%     if dados1(i,1)>dados(i-1,1) & dados(i,1)==dados(i+1,1)
%         
%         dados1(i:length(dados1),1)=dados1(i:length(dados1),1)-1;
%               
%     end
% end


%% Chamar rotina de tratamento de dados

saida=sd200turb_mod(dados1);
bf=saida;
%bf==>> serie / prof / sal / TºC / turb (FTU) / ano / mes / dia / hora / min
%        1      2      3     4        5         6     7     8     9     10  

%% Gráfico 'contour' de todos os perfis
%Escala
s=0:35;
t=0:35;
tu=0:35;
%Cria vetor de tempo em décimos de hora
dh(:,1)=bf(:,9)+(bf(:,10)/60);
%Cria vetor do eixo x em dias julianos
xi=linspace(min(dh),max(dh),length(bf));
%Cria vetor do eixo y com as profundidades
yi=linspace(max(bf(:,2)),-12,min(bf(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i=griddata(dh,bf(:,2),bf(:,3),xi,yi);
%Cria matriz da temperatura no tempo e nas profundidades
temp_i=griddata(dh,bf(:,2),bf(:,4),xi,yi);
%Cria matriz da temperatura no tempo e nas profundidades
turb_i=griddata(dh,bf(:,2),bf(:,5),xi,yi);


%Plot da salinidade/temperatura/turbidez

figure
subplot(3,1,1)
[C1,h1]=contourf(xi,yi,sal_i);
title('Salinidade - Todos os perfis')
ylabel('Profundidade (m)')
colorbar
shading flat
clabel(C1,h1)

subplot(3,1,2)
[C2,h2]=contourf(xi,yi,temp_i);
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat
clabel(C2,h2)

subplot(3,1,3)
[C3,h3]=contourf(xi,yi,turb_i);
title('Turbidez (FTU)')
xlabel('Décimo de hora')
ylabel('Profundidade (m)')
colorbar
shading flat
clabel(C3,h3)
zlim([0 10])

%% Selecionar dados por perfil

for i=1:length(bf)
    if bf(i,1)<=5
        perf_1(i,:)=bf(i,:);
    elseif bf(i,1)>5 && bf(i,1)<=10
        perf_2(i,:)=bf(i,:);
    elseif bf(i,1)>10 && bf(i,1)<=15
        perf_3(i,:)=bf(i,:);
    elseif bf(i,1)>15 && bf(i,1)<=20
        perf_4(i,:)=bf(i,:);
    elseif bf(i,1)>20 && bf(i,1)<=25
        perf_5(i,:)=bf(i,:);        
    elseif bf(i,1)>25 && bf(i,1)<=30
        perf_6(i,:)=bf(i,:);
     elseif bf(i,1)>30 && bf(i,1)<=35
        perf_7(i,:)=bf(i,:);       
    elseif bf(i,1)>35 && bf(i,1)<=40
        perf_8(i,:)=bf(i,:);        
    elseif bf(i,1)>40 && bf(i,1)<=45
        perf_9(i,:)=bf(i,:);        
    elseif bf(i,1)>45 && bf(i,1)<=50
        perf_10(i,:)=bf(i,:);        
    elseif bf(i,1)>50 && bf(i,1)<=55
        perf_11(i,:)=bf(i,:);
    elseif bf(i,1)>55 && bf(i,1)<=60
        perf_12(i,:)=bf(i,:);  
    elseif bf(i,1)>60 && bf(i,1)<=65
        perf_13(i,:)=bf(i,:); 
    elseif bf(i,1)>65 && bf(i,1)<=70
        perf_14(i,:)=bf(i,:); 
    elseif bf(i,1)>70 && bf(i,1)<=75
        perf_15(i,:)=bf(i,:); 
    end
end
        
%Retirar os zeros das matrizes perfis

perf_2=perf_2(find(perf_2(:,1)>0),:);
perf_3=perf_3(find(perf_3(:,1)>0),:);
perf_4=perf_4(find(perf_4(:,1)>0),:);
perf_5=perf_5(find(perf_5(:,1)>0),:);
perf_6=perf_6(find(perf_6(:,1)>0),:);
perf_7=perf_7(find(perf_7(:,1)>0),:);
perf_8=perf_8(find(perf_8(:,1)>0),:);
perf_9=perf_9(find(perf_9(:,1)>0),:);
perf_10=perf_10(find(perf_10(:,1)>0),:);
perf_11=perf_11(find(perf_11(:,1)>0),:);
perf_12=perf_12(find(perf_12(:,1)>0),:);
perf_13=perf_13(find(perf_13(:,1)>0),:);
perf_14=perf_14(find(perf_14(:,1)>0),:);
perf_15=perf_15(find(perf_15(:,1)>0),:);

%% Plot da salinidade/temperatura/turbidez perfil 1
%Cria vetor de tempo em décimos de hora
dh1(:,1)=perf_1(:,9)+(perf_1(:,10)/60);
%Cria vetor do eixo x em décimos de hora
xi1=linspace(min(dh1),max(dh1),length(perf_1));
%Cria vetor do eixo y com as profundidades
yi1=linspace(max(perf_1(:,2)),-12,min(perf_1(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i1=griddata(dh1,perf_1(:,2),perf_1(:,3),xi1,yi1,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
temp_i1=griddata(dh1,perf_1(:,2),perf_1(:,4),xi1,yi1,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
turb_i1=griddata(dh1,perf_1(:,2),perf_1(:,5),xi1,yi1,'cubic');


%Plot da salinidade/temperatura/turbidez
figure (2)
subplot(3,3,1:3)
contourf(xi1,yi1,sal_i1)
title('Salinidade - Perfil 1')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,4:6)
contourf(xi1,yi1,temp_i1)
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,7:9)
contourf(xi1,yi1,turb_i1)
title('Turbidez (FTU)')
xlabel('Décimos de hora')
ylabel('Profundidade (m)')
colorbar
shading flat

%% Plot da salinidade/temperatura/turbidez perfil 2
%Cria vetor de tempo em décimos de hora
dh2(:,1)=perf_2(:,9)+(perf_2(:,10)/60);
%Cria vetor do eixo x em décimos de hora
xi2=linspace(min(dh2),max(dh2),length(perf_2));
%Cria vetor do eixo y com as profundidades
yi2=linspace(max(perf_2(:,2)),-12,min(perf_2(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i2=griddata(dh2,perf_2(:,2),perf_2(:,3),xi2,yi2,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
temp_i2=griddata(dh2,perf_2(:,2),perf_2(:,4),xi2,yi2,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
turb_i2=griddata(dh2,perf_2(:,2),perf_2(:,5),xi2,yi2,'cubic');

%Plot
figure (3)
subplot(3,3,1:3)
contourf(xi2,yi2,sal_i2)
title('Salinidade - Perfil 2')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,4:6)
contourf(xi2,yi2,temp_i2)
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,7:9)
contourf(xi2,yi2,turb_i2)
title('Turbidez (FTU)')
xlabel('Décimos de hora')
ylabel('Profundidade (m)')
colorbar
shading flat

%% Plot da salinidade/temperatura/turbidez perfil 3
%Cria vetor de tempo em décimos de hora
dh3(:,1)=perf_3(:,9)+(perf_3(:,10)/60);
%Cria vetor do eixo x em décimos de hora
xi3=linspace(min(dh3),max(dh3),length(perf_3));
%Cria vetor do eixo y com as profundidades
yi3=linspace(max(perf_3(:,2)),-12,min(perf_3(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i3=griddata(dh3,perf_3(:,2),perf_3(:,3),xi3,yi3,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
temp_i3=griddata(dh3,perf_3(:,2),perf_3(:,4),xi3,yi3,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
turb_i3=griddata(dh3,perf_3(:,2),perf_3(:,5),xi3,yi3,'cubic');

%Plot
figure (4)
subplot(3,3,1:3)
contourf(xi3,yi3,sal_i3)
title('Salinidade - Perfil 3')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,4:6)
contourf(xi3,yi3,temp_i3)
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,7:9)
contourf(xi3,yi3,turb_i3)
title('Turbidez (FTU)')
xlabel('Décimos de hora')
ylabel('Profundidade (m)')
colorbar
shading flat

%% Plot da salinidade/temperatura/turbidez perfil 4
%Cria vetor de tempo em décimos de hora
dh4(:,1)=perf_4(:,9)+(perf_4(:,10)/60);
%Cria vetor do eixo x em décimos de hora
xi4=linspace(min(dh4),max(dh4),length(perf_4));
%Cria vetor do eixo y com as profundidades
yi4=linspace(max(perf_4(:,2)),-12,min(perf_4(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i4=griddata(dh4,perf_4(:,2),perf_4(:,3),xi4,yi4,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
temp_i4=griddata(dh4,perf_4(:,2),perf_4(:,4),xi4,yi4,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
turb_i4=griddata(dh4,perf_4(:,2),perf_4(:,5),xi4,yi4,'cubic');

%Plot
figure (5)
subplot(3,3,1:3)
contourf(xi4,yi4,sal_i4)
title('Salinidade - Perfil 4')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,4:6)
contourf(xi4,yi4,temp_i4)
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,7:9)
contourf(xi4,yi4,turb_i4)
title('Turbidez (FTU)')
xlabel('Décimos de hora')
ylabel('Profundidade (m)')
colorbar
shading flat

%% Plot da salinidade/temperatura/turbidez perfil 5
%Cria vetor de tempo em décimos de hora
dh5(:,1)=perf_5(:,9)+(perf_5(:,10)/60);
%Cria vetor do eixo x em décimos de hora
xi5=linspace(min(dh5),max(dh5),length(perf_5));
%Cria vetor do eixo y com as profundidades
yi5=linspace(max(perf_5(:,2)),-12,min(perf_5(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i5=griddata(dh5,perf_5(:,2),perf_5(:,3),xi5,yi5,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
temp_i5=griddata(dh5,perf_5(:,2),perf_5(:,4),xi5,yi5,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
turb_i5=griddata(dh5,perf_5(:,2),perf_5(:,5),xi5,yi5,'cubic');

%Plot
figure (6)
subplot(3,3,1:3)
contourf(xi5,yi5,sal_i5)
title('Salinidade - Perfil 5')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,4:6)
contourf(xi5,yi5,temp_i5)
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,7:9)
contourf(xi5,yi5,turb_i5)
title('Turbidez (FTU)')
xlabel('Décimos de hora')
ylabel('Profundidade (m)')
colorbar
shading flat

%% Plot da salinidade/temperatura/turbidez perfil 6
%Cria vetor de tempo em décimos de hora
dh6(:,1)=perf_6(:,9)+(perf_6(:,10)/60);
%Cria vetor do eixo x em décimos de hora
xi6=linspace(min(dh6),max(dh6),length(perf_6));
%Cria vetor do eixo y com as profundidades
yi6=linspace(max(perf_6(:,2)),-12,min(perf_6(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i6=griddata(dh6,perf_6(:,2),perf_6(:,3),xi6,yi6,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
temp_i6=griddata(dh6,perf_6(:,2),perf_6(:,4),xi6,yi6,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
turb_i6=griddata(dh6,perf_6(:,2),perf_6(:,5),xi6,yi6,'cubic');

%Plot
figure (7)
subplot(3,3,1:3)
contourf(xi6,yi6,sal_i6)
title('Salinidade - Perfil 6')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,4:6)
contourf(xi6,yi6,temp_i6)
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,7:9)
contourf(xi6,yi6,turb_i6)
title('Turbidez (FTU)')
xlabel('Décimos de hora')
ylabel('Profundidade (m)')
colorbar
shading flat

%% Plot da salinidade/temperatura/turbidez perfil 7
%Cria vetor de tempo em décimos de hora
dh7(:,1)=perf_7(:,9)+(perf_7(:,10)/60);
%Cria vetor do eixo x em décimos de hora
xi7=linspace(min(dh7),max(dh7),length(perf_7));
%Cria vetor do eixo y com as profundidades
yi7=linspace(max(perf_7(:,2)),-12,min(perf_7(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i7=griddata(dh7,perf_7(:,2),perf_7(:,3),xi7,yi7,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
temp_i7=griddata(dh7,perf_7(:,2),perf_7(:,4),xi7,yi7,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
turb_i7=griddata(dh7,perf_7(:,2),perf_7(:,5),xi7,yi7,'cubic');

%Plot
figure (8)
subplot(3,3,1:3)
contourf(xi7,yi7,sal_i7)
title('Salinidade - Perfil 7')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,4:6)
contourf(xi7,yi7,temp_i7)
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,7:9)
contourf(xi7,yi7,turb_i7)
title('Turbidez (FTU)')
xlabel('Décimos de hora')
ylabel('Profundidade (m)')
colorbar
shading flat

%% Plot da salinidade/temperatura/turbidez perfil 8
%Cria vetor de tempo em décimos de hora
dh8(:,1)=perf_8(:,9)+(perf_8(:,10)/60);
%Cria vetor do eixo x em décimos de hora
xi8=linspace(min(dh8),max(dh8),length(perf_8));
%Cria vetor do eixo y com as profundidades
yi8=linspace(max(perf_8(:,2)),-12,min(perf_8(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i8=griddata(dh8,perf_8(:,2),perf_8(:,3),xi8,yi8,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
temp_i8=griddata(dh8,perf_8(:,2),perf_8(:,4),xi8,yi8,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
turb_i8=griddata(dh8,perf_8(:,2),perf_8(:,5),xi8,yi8,'cubic');

%Plot
figure (9)
subplot(3,3,1:3)
contourf(xi8,yi8,sal_i8)
title('Salinidade - Perfil 8')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,4:6)
contourf(xi8,yi8,temp_i8)
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,7:9)
contourf(xi8,yi8,turb_i8)
title('Turbidez (FTU)')
xlabel('Décimos de hora')
ylabel('Profundidade (m)')
colorbar
shading flat

%% Plot da salinidade/temperatura/turbidez perfil 9
%Cria vetor de tempo em décimos de hora
dh9(:,1)=perf_9(:,9)+(perf_9(:,10)/60);
%Cria vetor do eixo x em décimos de hora
xi9=linspace(min(dh9),max(dh9),length(perf_9));
%Cria vetor do eixo y com as profundidades
yi9=linspace(max(perf_9(:,2)),-12,min(perf_9(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i9=griddata(dh9,perf_9(:,2),perf_9(:,3),xi9,yi9,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
temp_i9=griddata(dh9,perf_9(:,2),perf_9(:,4),xi9,yi9,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
turb_i9=griddata(dh9,perf_9(:,2),perf_9(:,5),xi9,yi9,'cubic');

%Plot
figure (10)
subplot(3,3,1:3)
contourf(xi9,yi9,sal_i9)
title('Salinidade - Perfil 9')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,4:6)
contourf(xi9,yi9,temp_i9)
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,7:9)
contourf(xi9,yi9,turb_i9)
title('Turbidez (FTU)')
xlabel('Décimos de hora')
ylabel('Profundidade (m)')
colorbar
shading flat

%% Plot da salinidade/temperatura/turbidez perfil 10
%Cria vetor de tempo em décimos de hora
dh10(:,1)=perf_10(:,9)+(perf_10(:,10)/60);
%Cria vetor do eixo x em décimos de hora
xi10=linspace(min(dh10),max(dh10),length(perf_10));
%Cria vetor do eixo y com as profundidades
yi10=linspace(max(perf_10(:,2)),-12,min(perf_10(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i10=griddata(dh10,perf_10(:,2),perf_10(:,3),xi10,yi10,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
temp_i10=griddata(dh10,perf_10(:,2),perf_10(:,4),xi10,yi10,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
turb_i10=griddata(dh10,perf_10(:,2),perf_10(:,5),xi10,yi10,'cubic');

%Plot
figure (11)
subplot(3,3,1:3)
contourf(xi10,yi10,sal_i10)
title('Salinidade - Perfil 10')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,4:6)
contourf(xi10,yi10,temp_i10)
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,7:9)
contourf(xi10,yi10,turb_i10)
title('Turbidez (FTU)')
xlabel('Décimos de hora')
ylabel('Profundidade (m)')
colorbar
shading flat

%% Plot da salinidade/temperatura/turbidez perfil 11
%Cria vetor de tempo em décimos de hora
dh11(:,1)=perf_11(:,9)+(perf_11(:,10)/60);
%Cria vetor do eixo x em décimos de hora
xi11=linspace(min(dh11),max(dh11),length(perf_11));
%Cria vetor do eixo y com as profundidades
yi11=linspace(max(perf_11(:,2)),-12,min(perf_11(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i11=griddata(dh11,perf_11(:,2),perf_11(:,3),xi11,yi11,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
temp_i11=griddata(dh11,perf_11(:,2),perf_11(:,4),xi11,yi11,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
turb_i11=griddata(dh11,perf_11(:,2),perf_11(:,5),xi11,yi11,'cubic');

%Plot
figure (12)
subplot(3,3,1:3)
contourf(xi11,yi11,sal_i11)
title('Salinidade - Perfil 11')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,4:6)
contourf(xi11,yi11,temp_i11)
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,7:9)
contourf(xi11,yi11,turb_i11)
title('Turbidez (FTU)')
xlabel('Décimos de hora')
ylabel('Profundidade (m)')
colorbar
shading flat

%% Plot da salinidade/temperatura/turbidez perfil 12
%Cria vetor de tempo em décimos de hora
dh12(:,1)=perf_12(:,9)+(perf_12(:,10)/60);
%Cria vetor do eixo x em décimos de hora
xi12=linspace(min(dh12),max(dh12),length(perf_12));
%Cria vetor do eixo y com as profundidades
yi12=linspace(max(perf_12(:,2)),-12,min(perf_12(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i12=griddata(dh12,perf_12(:,2),perf_12(:,3),xi12,yi12,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
temp_i12=griddata(dh12,perf_12(:,2),perf_12(:,4),xi12,yi12,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
turb_i12=griddata(dh12,perf_12(:,2),perf_12(:,5),xi12,yi12,'cubic');

%Plot
figure (13)
subplot(3,3,1:3)
contourf(xi12,yi12,sal_i12)
title('Salinidade - Perfil 12')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,4:6)
contourf(xi12,yi12,temp_i12)
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,7:9)
contourf(xi12,yi12,turb_i12)
title('Turbidez (FTU)')
xlabel('Décimos de hora')
ylabel('Profundidade (m)')
colorbar
shading flat

%% Plot da salinidade/temperatura/turbidez perfil 13
%Cria vetor de tempo em décimos de hora
dh13(:,1)=perf_13(:,9)+(perf_13(:,10)/60);
%Cria vetor do eixo x em décimos de hora
xi13=linspace(min(dh13),max(dh13),length(perf_13));
%Cria vetor do eixo y com as profundidades
yi13=linspace(max(perf_13(:,2)),-12,min(perf_13(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i13=griddata(dh13,perf_13(:,2),perf_13(:,3),xi13,yi13,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
temp_i13=griddata(dh13,perf_13(:,2),perf_13(:,4),xi13,yi13,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
turb_i13=griddata(dh13,perf_13(:,2),perf_13(:,5),xi13,yi13,'cubic');

%Plot
figure (14)
subplot(3,3,1:3)
contourf(xi13,yi13,sal_i13)
title('Salinidade - Perfil 13')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,4:6)
contourf(xi13,yi13,temp_i13)
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,7:9)
contourf(xi13,yi13,turb_i13)
title('Turbidez (FTU)')
xlabel('Décimos de hora')
ylabel('Profundidade (m)')
colorbar
shading flat

%% Plot da salinidade/temperatura/turbidez perfil 14
%Cria vetor de tempo em décimos de hora
dh14(:,1)=perf_14(:,9)+(perf_14(:,10)/60);
%Cria vetor do eixo x em décimos de hora
xi14=linspace(min(dh14),max(dh14),length(perf_14));
%Cria vetor do eixo y com as profundidades
yi14=linspace(max(perf_14(:,2)),-12,min(perf_14(:,2))*-1)';

%Cria matriz da salinidade no tempo e nas profundidades
sal_i14=griddata(dh14,perf_14(:,2),perf_14(:,3),xi14,yi14,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
temp_i14=griddata(dh14,perf_14(:,2),perf_14(:,4),xi14,yi14,'cubic');
%Cria matriz da temperatura no tempo e nas profundidades
turb_i14=griddata(dh14,perf_14(:,2),perf_14(:,5),xi14,yi14,'cubic');

%Plot
figure (15)
subplot(3,3,1:3)
contourf(xi14,yi14,sal_i14)
title('Salinidade - Perfil 14')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,4:6)
contourf(xi14,yi14,temp_i14)
title('Temperatura (ºC)')
ylabel('Profundidade (m)')
colorbar
shading flat

subplot(3,3,7:9)
contourf(xi14,yi14,turb_i14)
title('Turbidez (FTU)')
xlabel('Décimos de hora')
ylabel('Profundidade (m)')
colorbar
shading flat

%% dados estatísticos

%Cálculo da média da salinidade
med_s(1,1)=mean(perf_1(:,3));
med_s(2,1)=mean(perf_2(:,3));
med_s(3,1)=mean(perf_3(:,3));
med_s(4,1)=mean(perf_4(:,3));
med_s(5,1)=mean(perf_5(:,3));
med_s(6,1)=mean(perf_6(:,3));
med_s(7,1)=mean(perf_7(:,3));
med_s(8,1)=mean(perf_8(:,3));
med_s(9,1)=mean(perf_9(:,3));
med_s(10,1)=mean(perf_10(:,3));
med_s(11,1)=mean(perf_11(:,3));
med_s(12,1)=mean(perf_12(:,3));
med_s(13,1)=mean(perf_13(:,3));
med_s(14,1)=mean(perf_14(:,3));

%Cálculo do máximo da salinidade
max_s(1,1)=max(perf_1(:,3));
max_s(2,1)=max(perf_2(:,3));
max_s(3,1)=max(perf_3(:,3));
max_s(4,1)=max(perf_4(:,3));
max_s(5,1)=max(perf_5(:,3));
max_s(6,1)=max(perf_6(:,3));
max_s(7,1)=max(perf_7(:,3));
max_s(8,1)=max(perf_8(:,3));
max_s(9,1)=max(perf_9(:,3));
max_s(10,1)=max(perf_10(:,3));
max_s(11,1)=max(perf_11(:,3));
max_s(12,1)=max(perf_12(:,3));
max_s(13,1)=max(perf_13(:,3));
max_s(14,1)=max(perf_14(:,3));

%Cálculo do mínimo da salinidade
min_s(1,1)=min(perf_1(:,3));
min_s(2,1)=min(perf_2(:,3));
min_s(3,1)=min(perf_3(:,3));
min_s(4,1)=min(perf_4(:,3));
min_s(5,1)=min(perf_5(:,3));
min_s(6,1)=min(perf_6(:,3));
min_s(7,1)=min(perf_7(:,3));
min_s(8,1)=min(perf_8(:,3));
min_s(9,1)=min(perf_9(:,3));
min_s(10,1)=min(perf_10(:,3));
min_s(11,1)=min(perf_11(:,3));
min_s(12,1)=min(perf_12(:,3));
min_s(13,1)=min(perf_13(:,3));
min_s(14,1)=min(perf_14(:,3));

%Cálculo da média da temperatura
med_temp(1,1)=mean(perf_1(:,4));
med_temp(2,1)=mean(perf_2(:,4));
med_temp(3,1)=mean(perf_3(:,4));
med_temp(4,1)=mean(perf_4(:,4));
med_temp(5,1)=mean(perf_5(:,4));
med_temp(6,1)=mean(perf_6(:,4));
med_temp(7,1)=mean(perf_7(:,4));
med_temp(8,1)=mean(perf_8(:,4));
med_temp(9,1)=mean(perf_9(:,4));
med_temp(10,1)=mean(perf_10(:,4));
med_temp(11,1)=mean(perf_11(:,4));
med_temp(12,1)=mean(perf_12(:,4));
med_temp(13,1)=mean(perf_13(:,4));
med_temp(14,1)=mean(perf_14(:,4));

%Cálculo do máximo da temperatura
max_temp(1,1)=max(perf_1(:,4));
max_temp(2,1)=max(perf_2(:,4));
max_temp(3,1)=max(perf_3(:,4));
max_temp(4,1)=max(perf_4(:,4));
max_temp(5,1)=max(perf_5(:,4));
max_temp(6,1)=max(perf_6(:,4));
max_temp(7,1)=max(perf_7(:,4));
max_temp(8,1)=max(perf_8(:,4));
max_temp(9,1)=max(perf_9(:,4));
max_temp(10,1)=max(perf_10(:,4));
max_temp(11,1)=max(perf_11(:,4));
max_temp(12,1)=max(perf_12(:,4));
max_temp(13,1)=max(perf_13(:,4));
max_temp(14,1)=max(perf_14(:,4));

%Cálculo do mínimo da temperatura
min_temp(1,1)=min(perf_1(:,4));
min_temp(2,1)=min(perf_2(:,4));
min_temp(3,1)=min(perf_3(:,4));
min_temp(4,1)=min(perf_4(:,4));
min_temp(5,1)=min(perf_5(:,4));
min_temp(6,1)=min(perf_6(:,4));
min_temp(7,1)=min(perf_7(:,4));
min_temp(8,1)=min(perf_8(:,4));
min_temp(9,1)=min(perf_9(:,4));
min_temp(10,1)=min(perf_10(:,4));
min_temp(11,1)=min(perf_11(:,4));
min_temp(12,1)=min(perf_12(:,4));
min_temp(13,1)=min(perf_13(:,4));
min_temp(14,1)=min(perf_14(:,4));

%Cálculo da média da turbidez
med_turb(1,1)=mean(perf_1(:,5));
med_turb(2,1)=mean(perf_2(:,5));
med_turb(3,1)=mean(perf_3(:,5));
med_turb(4,1)=mean(perf_4(:,5));
med_turb(5,1)=mean(perf_5(:,5));
med_turb(6,1)=mean(perf_6(:,5));
med_turb(7,1)=mean(perf_7(:,5));
med_turb(8,1)=mean(perf_8(:,5));
med_turb(9,1)=mean(perf_9(:,5));
med_turb(10,1)=mean(perf_10(:,5));
med_turb(11,1)=mean(perf_11(:,5));
med_turb(12,1)=mean(perf_12(:,5));
med_turb(13,1)=mean(perf_13(:,5));
med_turb(14,1)=mean(perf_14(:,5));

%Cálculo do máximo da turbidez
max_turb(1,1)=max(perf_1(:,5));
max_turb(2,1)=max(perf_2(:,5));
max_turb(3,1)=max(perf_3(:,5));
max_turb(4,1)=max(perf_4(:,5));
max_turb(5,1)=max(perf_5(:,5));
max_turb(6,1)=max(perf_6(:,5));
max_turb(7,1)=max(perf_7(:,5));
max_turb(8,1)=max(perf_8(:,5));
max_turb(9,1)=max(perf_9(:,5));
max_turb(10,1)=max(perf_10(:,5));
max_turb(11,1)=max(perf_11(:,5));
max_turb(12,1)=max(perf_12(:,5));
max_turb(13,1)=max(perf_13(:,5));
max_turb(14,1)=max(perf_14(:,5));

%Cálculo do mínimo da tubrbidez
min_turb(1,1)=min(perf_1(:,5));
min_turb(2,1)=min(perf_2(:,5));
min_turb(3,1)=min(perf_3(:,5));
min_turb(4,1)=min(perf_4(:,5));
min_turb(5,1)=min(perf_5(:,5));
min_turb(6,1)=min(perf_6(:,5));
min_turb(7,1)=min(perf_7(:,5));
min_turb(8,1)=min(perf_8(:,5));
min_turb(9,1)=min(perf_9(:,5));
min_turb(10,1)=min(perf_10(:,5));
min_turb(11,1)=min(perf_11(:,5));
min_turb(12,1)=min(perf_12(:,5));
min_turb(13,1)=min(perf_13(:,5));
min_turb(14,1)=min(perf_14(:,5));

