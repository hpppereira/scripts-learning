%% Programa principal para analisar os dados de onda gerado pela subrotina 'geraonda3'.

%
%Desenvolvido por:
% Henrique Patricio P. Pereira
% E-mail: henriqueppp@oceanica.ufrj.br
% Data da ultima modificacao: 11/11/2013

clear,clc,close all
%% Chama subrotina geraonda3
%Direo mdia
tetamean=input('Entre com a direcao das ondas: ');

[neta,netax,netay,netaxx,netayy,velx,vely,velz,velzz,velzzz,pr,dt] = geraonda3 (tetamean);
%neta - elevao
%netax - inclinao em x
%netay - inclinao em y
%netaxx - curvatura em x
%netayy - curvatura em y
%velx - velocidade horizontal em x
%vely - velocidade horizontal em y
%velz - velocidade vertical superficial (Dneta/Dt)
%velzz - velocidade vertical (Equao integral - papaer RAPPORT)
%velzzz - velocidade vertical (Dpot.vel/Dz)
%dt - intervalo de amostragem

neta=flipud(neta');
netax=flipud(netax');
netay=flipud(netay');
netaxx=flipud(netaxx');
netayy=flipud(netayy');
velx=flipud(velx');
vely=flipud(vely');
velz=flipud(velz');
velzz=flipud(velzz');
velzzz=flipud(velzzz');
pr=flipud(pr');

%% Espectros
[aaeta]=espec(neta',dt); %Espec. de neta
[aaxy]=espec2(velx',vely',dt); %Espec. cruzado entre 'Vx' e 'Vy'
[aaxz]=espec2(velx',velzzz',dt); %Espec. cruzado entre 'Vx' e 'Vz'
[aayz]=espec2(vely',velzzz',dt); %Espec. cruzado entre 'Vy' e 'Vz'
[aaxp]=espec2(velx',pr',dt); %Espec. cruzado entre 'Vx' e 'presso'
[aayp]=espec2(vely',pr',dt); %Espec. cruzado entre 'Vy' e 'presso'

%% Plot de Presso, Vel x, Vel y e Vel z
figure (1)

subplot(4,3,1:2)
plot(pr)
title('Presso')
ylabel('mbar')
axis tight
subplot(4,3,3)
plot(aayp(:,1),aayp(:,3)),axis tight
title('Auto-espectro da Presso')
xlabel('Frequncia (Hz)'),ylabel('(mbar)/Hz')
subplot(4,3,4:5)
plot(velx)
title('Vx')
ylabel('m/s')
axis([1 length(velx) -2 2])
subplot(4,3,6)
plot(aaxy(:,1),aaxy(:,2)),axis tight
title('Auto-espectro de Vx')
ylabel('(m/s)/Hz')
subplot(4,3,7:8)
plot(vely)
title('Vy')
ylabel('m/s')
axis([1 length(vely) -2 2])
subplot(4,3,9)
plot(aaxy(:,1),aaxy(:,3)),axis tight
title('Auto-espectro de Vy')
ylabel('(m/s)/Hz')
subplot(4,3,10:11)
plot(velzzz)
title('Vz')
ylabel('m/s')
axis([1 length(vely) -2 2])
xlabel('Tempo (segundos)')
subplot(4,3,12)
plot(aaxz(:,1),aaxz(:,3)),axis tight
title('Auto-espectro de Vz')
xlabel('Frequncia (Hz)')
ylabel('(m/s)/Hz')

%% Plot de (velx,velzzz) e (vely,velzzz)
%Faz o movimento orbital
figure (2)

t=20;

subplot(2,1,1)
hold on
plot(neta(1:100),'b')
plot(velx(1:100),'r')
plot(vely(1:100),'k')
plot(velzzz(1:100),'g')
axis tight
title('Elevao e Velocidades orbitais X,Y e Z')
xlabel('Registros')
ylabel('Eta (m) / Velocidade (m/s)')
legend('Eta','Vel x','Vel y','Vel z')
hold off

subplot(2,2,3)
plot(velx(1:t),velzzz(1:t),'b-*'), axis equal
title('Velx,Velz'),xlabel('Vel x'),ylabel('Vel z');

%Colocar sequencia nos pontos (ex: p1,p2..)
k=0;
for i=1:t
    k=k+1;
    n=num2str(k);
    text(velx(i,1),velzzz(i,1),[n])    
end

subplot(2,2,4)
plot(vely(1:t),velzzz(1:t),'b-*'), axis equal
title('Vely,Velz'),xlabel('Vel y'),ylabel('Vel z');

%Colocar sequencia nos pontos (ex: p1,p2..)
k=0;
for i=1:t
    k=k+1;
    n=num2str(k);
    text(vely(i,1),velzzz(i,1),[n])    
end
title('Vel y, Vel z')
xlabel('Vel y')
ylabel('Vel z')

%% Plot dos auto-espectros de Vx, Vy e Vz
figure (3)
subplot(3,2,1)
plot(velx,'b'),axis tight
title('Velocidade X')
xlabel('Registros')
ylabel('Velocidade (m/s)')
subplot(3,2,2)
plot(aaxy(:,1),aaxy(:,2),'b'),axis tight
title('Auto-espectro de Vx')
xlabel('Frequncia (Hz)')
ylabel('Energia')
subplot(3,2,3)
plot(vely,'r'),axis tight
title('Velocidade Y')
xlabel('Registros')
ylabel('Velocidade (m/s)')
subplot(3,2,4)
plot(aaxy(:,1),aaxy(:,3),'r'),axis tight
title('Auto-espectro de Vy')
xlabel('Frequncia (Hz)')
ylabel('Energia')
subplot(3,2,5)
plot(velzzz,'k'),axis tight
title('Velocidade Z')
xlabel('Registros')
ylabel('Velocidade (m/s)')
subplot(3,2,6)
plot(aaxz(:,1),aaxz(:,3),'k'),axis tight
title('Auto-espectro de Vz')
xlabel('Frequncia (Hz)')
ylabel('Energia')

%% Plot dos espectros cruzados %%
%%
%Auto-espectro de Vx e Vy
figure (4)
subplot(2,2,1)
hold on
plot(aaxy(:,1),aaxy(:,2),'b'), grid on
plot(aaxy(:,1),aaxy(:,3),'r'), grid on
axis tight
title('Auto espectro de Vx e Vy')
xlabel('Frequncia')
ylabel('Energia')
legend('Vx','Vy')
hold off

%Amplitude do espectro cruzado de Vx e Vy
subplot(2,2,2)
plot(aaxy(:,1),aaxy(:,6)), grid on
axis tight
title('Amplitude do espectro cruzado de Vx e Vy')
xlabel('Frequncia')
ylabel('Energia')

%Fase do espectro cruzado de Vx e Vy
subplot(2,2,3)
plot(aaxy(:,1),aaxy(:,7)), grid on
axis tight
title('Fase do espectro cruzado de Vx e Vy')
xlabel('Frequncia')
ylabel('Energia')

%Espectro de coerncia de Vx e Vy
subplot(2,2,4)
hold on
plot(aaxy(:,1),aaxy(:,8),'b'), grid on
plot(aaxy(:,1),aaxy(:,11),'r'), grid on
axis tight
title('Espectro de Coerncia de Vx e Vy')
xlabel('Frequncia')
ylabel('Coerncia')
hold off

%% 
%Auto-espectro de Vx e Vz
figure (5)
subplot(2,2,1)
hold on
plot(aaxz(:,1),aaxz(:,2),'b'), grid on
plot(aaxz(:,1),aaxz(:,3),'r'), grid on
axis tight
title('Auto espectro de Vx e Vz')
xlabel('Frequncia')
ylabel('Energia')
legend('Vx','Vz')
hold off

%Amplitude do espectro cruzado de Vx e Vz
subplot(2,2,2)
plot(aaxz(:,1),aaxz(:,6)), grid on
axis tight
title('Amplitude do espectro cruzado de Vx e Vz')
xlabel('Frequncia')
ylabel('Energia')

%Fase do espectro cruzado de Vx e Vz
subplot(2,2,3)
plot(aaxz(:,1),aaxz(:,7)), grid on
axis tight
title('Fase do espectro cruzado de Vx e Vz')
xlabel('Frequncia')
ylabel('Energia')

%Espectro de coerncia de Vx e Vz
subplot(2,2,4)
hold on
plot(aaxz(:,1),aaxz(:,8),'b'), grid on
plot(aaxz(:,1),aaxz(:,11),'r'), grid on
axis tight
title('Espectro de Coerncia de Vx e Vz')
xlabel('Frequncia')
ylabel('Coerncia')
hold off

%%  Plot do espectro cruzado
%Auto-espectro de Vy e Vz
figure (6)
subplot(2,2,1)
hold on
plot(aayz(:,1),aayz(:,2),'b'), grid on
plot(aayz(:,1),aayz(:,3),'r'), grid on
axis tight
title('Auto espectro de Vy e Vz')
xlabel('Frequncia')
ylabel('Energia')
legend('Vy','Vz')
hold off

%Amplitude do espectro cruzado de Vy e Vz
subplot(2,2,2)
plot(aayz(:,1),aayz(:,6)), grid on
axis tight
title('Amplitude do espectro cruzado de Vy e Vz')
xlabel('Frequncia')
ylabel('Energia')

%Fase do espectro cruzado de Vy e Vz
subplot(2,2,3)
plot(aayz(:,1),aayz(:,7)), grid on
axis tight
title('Fase do espectro cruzado de Vy e Vz')
xlabel('Frequncia')
ylabel('Energia')

%Espectro de coerncia de Vy e Vz
subplot(2,2,4)
hold on
plot(aayz(:,1),aayz(:,8),'b'), grid on
plot(aayz(:,1),aayz(:,11),'r'), grid on
axis tight
title('Espectro de Coerncia de Vy e Vz')
xlabel('Frequncia')
ylabel('Coerncia')
hold off

%% Plot dos trs tipos de velocidade vertical (deta/dt (velz); Formula Rapport (velzz); dPot.vel/dZ (velzzz))

figure (7)
subplot(3,1,1)
plot(velz)
title('Vel.z (deta/dt)'),ylabel('m/s')
axis tight
subplot(3,1,2)
plot(velzz)
title('Vel. z Rapport'),ylabel('m/s')
axis tight
subplot(3,1,3)
plot(velzzz)
title('Vel. z (dPot.Vel/dZ)'),ylabel('m/s'),xlabel('Registros')
axis tight

%% Plot do neta, velx e vel z sobrepostas

figure (8)
hold on
plot(neta(1:100),'b','linewidth',2.5)
plot(velx(1:100),'r','linewidth',2)
plot(vely(1:100),'y','linewidth',2)
plot(velzzz(1:100),'k','linewidth',2)
axis tight
title('Elevao e Velocidades orbitais')
xlabel('Registros')
ylabel('Eta (m) / Velocidade (m/s)')
legend('Eta','Vel x','Vel y','Vel z')
grid on

%% Plot do neta, netax, netay, netaxx e netayy sobrepostas

figure (9)
hold on
plot(neta,'b')
plot(netax,'r','linewidth',1.5)
plot(netay,'y')
plot(netaxx,'k','linewidth',1.5)
plot(netayy,'g')
axis tight
title('Elevao / Inclinao em X,Y / Curvatura X,Y')
xlabel('Registros')
ylabel('Eta (m) / inclinao')
legend('Eta','Incl. X','Incl. Y','Curv. X','Curv. Y')
grid on

%% Plot do Neta e da Vel. Z (Desl. posterior - Desl. anterior)/deltat = velocidade

for i=1:length(neta)-1
    velocidadez(i)=(neta(i+1)-neta(i))/dt;
end
    
figure (10)
subplot(2,1,1)
plot(neta,'b'), hold on
plot(velocidadez,'r'), hold off, axis tight
title('Elevao e Vel. Z')
xlabel('Registros')
ylabel('Eta (m) / Velocidade (m/s)')
legend('Eta','(Eta(i+1)- Eta(i))/deltat')

subplot(2,1,2)
plot(neta,'b'), hold on
plot(velzzz,'r'), hold off, axis tight
title('Elevao (neta) e Vel. Z (dPot.Vel/dZ)')
xlabel('Registros')
ylabel('Eta (m) / Velocidade (m/s)')
legend('Eta','Vel. z')

%% Plot de comparao entre as 3 velocidades verticais

figure (11)
plot(velocidadez,'b','linewidth',1.5), hold on
plot(velz,'y')
plot(velzz,'r')
plot(velzzz,'k'), hold off, axis tight
title('Velocidade orbital vertical')
xlabel('Registros')
ylabel('Vel. vertical (m/s)')
legend('Velicidadez','Velz','Velzz','Velzzz')
    
%% Plot tempo e freq
figure (12)
subplot(2,1,1)
plot(neta)
xlabel('Tempo'),ylabel('metros'), title('Elevao'), axis tight
subplot(2,1,2)
plot(aaeta(:,1),aaeta(:,2))
xlabel('Frequncia (Hz)'),ylabel('m/Hz'), title('Auto-espectro da Elevao'), axis tight

%% Plot de Vy,Vz e Vx,Vz com e sem flipud para onde vai e de onde vem, respectivamente
%Numero de pontos a serem plotados
t=10;

%Passar vetor de velocidade para coluna (para fazer o flipud)
% velx=velx';
% vely=vely';
% velzzz=velzzz';

%Inverter direo de onda (de onde vai para onde vem ou vice-versa) *Verificar no inicio da rotina se o flipud est comentado
velx1=flipud(velx); %Para onde vai
vely1=flipud(vely);
velzzz1=flipud(velzzz);

%Plot de Vx,Vz
figure
plot(velx(1:t),velzzz(1:t),'b-*'), axis equal
title('Velx,Velz'),xlabel('Vel x'),ylabel('Vel z');

%Colocar sequencia nos pontos (ex: p1,p2..)
k=0;
for i=1:t
    k=k+1;
    n=num2str(k);
    text(velx(i,1),velzzz(i,1),['p',n])    
end

hold on

plot(velx1(1:t),velzzz1(1:t),'r-*'), axis equal
title('Velx,Velz'),xlabel('Vel x'),ylabel('Vel z');
legend('com flipud <---',' sem flipud --->')

%Colocar sequencia nos pontos (ex: p1,p2..)
k=0;
for i=1:t
    k=k+1;
    n=num2str(k);
    text(velx1(i,1),velzzz1(i,1),['p',n])    
end
hold off

%Plot de Vy,Vz
figure
plot(vely(1:t),velzzz(1:t),'b-*'), axis equal
xlabel('Vel y'),ylabel('Vel z');

%Colocar sequencia nos pontos (ex: p1,p2..)
k=0;
for i=1:t
    k=k+1;
    n=num2str(k);
    text(vely(i,1),velzzz(i,1),['p',n])    
end

hold on

plot(vely1(1:t),velzzz1(1:t),'r-*'), axis equal
title('Vely,Velz'),xlabel('Vel y'),ylabel('Vel z');
legend('com flipud <---',' sem flipud --->')

%Colocar sequencia nos pontos (ex: p1,p2..)
k=0;
for i=1:t
    k=k+1;
    n=num2str(k);
    text(vely1(i,1),velzzz1(i,1),['p',n])    
end
hold off

%Plot de VxVz e VyVz no mesmo grfico, utilizando o flipud
figure
n=15;
plot(velx(1:n),velzzz(1:n),'b*-'), hold on
plot(vely(1:n),velzzz(1:n),'r*-'), axis equal
legend('VxVz','VyVz'), xlabel('Vel.x , Vel.y'), ylabel('Vel.z'), title('Velocidade orbital - 180 graus')

k=0;
for i=1:n
    k=k+1;
    n=num2str(k);
    text(velx(i,1),velzzz(i,1),['p',n])    
    text(vely(i,1),velzzz(i,1),['p',n])     
end
hold off



