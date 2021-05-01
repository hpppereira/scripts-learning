clear,clc,close all
%%%%%%%TESTES%%%%%%%%%
%Cinemática da particula para ondas progressivas

% Deslocamento da supericie (eta)

%x=linspace(0,11*pi,1024)'; %Eixo x q achava q poderia ser, mas nao é.
x=(1:1024)'; %eixo x
t=1; %Intervalo de tempo
H=2; %Altura de onda
L=156; %Comprimento de onda (m) em águas profundas
Lr=50; %Comprimento de onda (m) em águas rasas
T=10; %Periodo da onda (s)
k=2*pi/L; %Numero de onda águas profundas
kr=2*pi/Lr; %%Numero de onda águas rasas
fa=2*pi/T; %Frequencia angular
h=100; %Profundidade local (m)
g=9.8; %Ac. gravidade (m/s)
redisp=g*k*tanh(k*h); %Relação de dispersão para L=160m
redispr=g*kr*tanh(kr*h); %Relação de dispersão para L=50m
cel=L/T; %Celeridade da onda (m/s) para L=160m
celr=Lr/T; %Celeridade da onda (m/s) para L=50m
z=linspace(0,0,1024)'; %Cota para achar as velocidade para Z=0
%z=(1:1024)'; %Valor da cota para criar gráfico de deslocamento em diferentes profundidade (espiral)
for i=1:length(x)
    
    %Elevação (eta)
    eta(i,1)=H/2*cos((k*x(i,1))-(fa*t));  %Para L=160m
    etar(i,1)=H/2*cos((kr*x(i,1))-(fa*t));  %Para L=50m
    
    %Cota
    %z(i,1)=-(100+eta(i,1)); 
    
    %Potencial de velocidade
    pot(i,1)=(-(H/2)*g*cosh(k)*(h+z(i,1))*sinh(k*x(i,1)-fa*t))/(2*fa*cosh(k*h)); 

    %Potencial de vel introduzindo a relação de dispersão
    potdisp(i,1)=(-(H/2)*cel*cosh(k)*(h+z(i,1))*sin(k*x(i,1)-fa*t))/(2*sinh(k*h)); 
    
    %Plot da elevação com o potencial de velocidade    
%     plot(eta)
%     hold on
%     plot(potdisp,'r')
%     hold off
    
    %Velocidade horizontal %%%Porque os valores dao negativo??
    u(i,1)=(H*fa*cosh(k)*(h+z(i,1))*cos(k*x(i,1)-fa*t))/(2*sinh(k*h));
    %u(i,1)=abs(u(i,1)); %Coloca os valores de vel positivos
    
    %Velocidade horizontal introduzindo a relação de dispersão
    udisp(i,1)=(H*g*k*cosh(k)*(h+z(i,1))*cos(k*x(i,1)-fa*t))/(2*fa*cosh(k*h));
    %udisp(i,1)=abs(udisp(i,1)); %Coloca os valores de vel positivos
    
    %Aceleração horizontal
    acelh(i,1)=(H*g*k*cosh(k)*(h+z(i,1))*sin(k*x(i,1)-fa*t))/(2*cosh(k*h));
    
    %Velocidade vertical
    wdisp(i,1)=(H*g*k*sinh(k)*(h+z(i,1))*sin(k*x(i,1)-fa*t))/(2*fa*cosh(k*h));
    
    
    %Aceleração vertical introduzindo a relação de dispersão
    acelv(i,1)=(H*g*k*sinh(k)*(h+z(i,1))*cos(k*x(i,1)-fa*t))/(2*cosh(k*h));
    
    %Deslocamento Horizontal da Particula
    desh(i,1)=(-H*g*k*cosh(k)*(h+z(i,1))*sin(k*x(i,1)-fa*t))/(2*(fa)^2*cosh(k*h));
    
    %Deslocamento horizontal usando a relação de dispersão
    deshd(i,1)=(-H*cosh(k)*(h+z(i,1))*sin(k*x(i,1)-fa*t))/(2*sinh(k*h));
    
    %Deslocamento vertical usando a relação de dispersão
    desvd(i,1)=(-H*sinh(k)*(h+z(i,1))*cos(k*x(i,1)-fa*t))/(2*sinh(k*h));
    
    
    %plot(deshd,desvd) %Cria gráfico de deslocamento (espiral)
    
end


A=max(deshd); %Valor do raio no eixo x
B=max(desvd); %Valor do raio no eixo y

%Deslocamento com os valores de A e B
for i=1:length(x)
    deshA(i,1)=-A*sin(k*x(i,1)-fa*t);
    desvB(i,1)=B*cos(k*x(i,1)-fa*t);
end

%Equação da elipse
%%%el=(desh1/A).^2+(desv1/B).^2; ==1??


a=input('Digite 1 para as ondas se propagando em águas rasas (h/L<1/20), 2 - Intermediárias (1/20<h/L<1/2) ou 3 - Profundas (h/L>1/2): ');
if a==1 %Se for em águas rasas
    L=150;
    h=5;
    if h/L<=(1/20) %Se for menor ou igual a 1/20
        disp('A onda está se propagando em águas rasas, Prof(h)=5m, Compr.onda(L)=160m');              
        z=input('Digite um valor para cota entre 0 (sup) à -5 (fundo) para o gráfico de movimento da particula: ') ;
        Ar=(H*T/4*pi)*sqrt(g/h); %Não depende de z
        Br=(H/2)*(1+(z/h)); 
        for i=1:length(x) %Vai fazer a conta para cada cota
             deshr(i,1)=-Ar*sin(k*x(i,1)-fa*t); %Deslocamento horizontal para águas rasas
             desvr(i,1)=Br*cos(k*x(i,1)-fa*t); %Deslocamento vertical para águas rasas 
        end
        grr=input('Digite ´1´ para plotar o gráfico em animação e ´0´ para continuar a rotina: ');
        if grr==1
           plot(deshr,desvr,'r')
           for i=1:160 % Animação com 160 frames
               hold on
               axis([-25 25 -1 1])
               plot(deshr(i,1),desvr(i,1),'*');   % Fazer o gráfico do deslocamento
               M(i)=getframe %Filme do movimento
           end
           movie(M,0)
           hold off  
        end
    end 
    
elseif a==2 %Se for em águas intermediárias
    Lo=1.56*T^2;
    ko=2*pi/Lo;
    h=10;
    kc=linspace(ko,2,20)'; % Valores chutados de 'k' para achar o k.h em águas intermediárias
    fangular=2*pi/T; % Frequencia angular
    fangular2=fangular^2; % % Frequencia angular ao quadrado (Relação de dispersão)

    for i=1:length(kc)
        lin1(i,1)=tanh(kc(i,1)*h);
        lin2(i,1)=(fangular2*h)/(g*kc(i,1)*h);
    end

    hold on
    plot(lin1,'b.-');
    plot(lin2,'r.-');
    hold off

    disp('Clique no ponto de cruzamento entre as duas curvas e aperte ´Enter´')
    a=ginput;
    kh1=a(1,1); % Valor do k.h (eixo x) onde as duas curvas se cruzam
    k1=kh1/h; % Valor de k
    Lint=2*pi/k1; %Comprimento de onda minimo para estar em águas intermediárias



    
    if h/L<(1/2) & h/L>(1/20)
        disp(['A onda está se propagando em águas intermediárias, com prof(h)=10m e Compr.onda(L)=',num2str(L),'; quais são as equações para águas intemediárias mineiro po?!']);
    end
elseif a==3 % Se for em águas profundas
       h=80;
       L=160;
       if h/L>=1/2
           disp('A onda está se propagando em águas profundas, com Prof(h)=80m e Compr.onda(L)=160m.');    
           z=input('Digite um valor para cota entre 0 (sup) à -80 (fundo) para o gráfico de movimento da particula: ');    
           Af=(H/2)*exp(k*z);
           Bf=Af;           
           for i=1:length(x)
               deshf(i,1)=-Af*sin(k*x(i,1)-fa*t); %Deslocamento horizontal para águas profundas
               desvf(i,1)=Bf*cos(k*x(i,1)-fa*t); %Deslocamento vertical para águas profundas
           end
           grf=input('Digite ´1´ para plotar o gráfico em animação e ´0´ para continuar a rotina: ');
           if grf==1
               for i=1:160
                   hold on
                   axis([-1 1 -1 1])
                   plot(deshf(i,1),desvf(i,1),'*-')  % Fazer o gráfico do deslocamento
                   M(i)=getframe %Filme do movimento
               end
               movie(M,0)
               hold off
           end
       end
end


%%%Deslocamento da Particula em águas RASAS para x1 e z1 igual a 0 (Ponto de referencia = 0,0)
zr=[0:-1:-5]';
h=5; %Profundidade para águas rasas
for j=1:length(zr)
    Ar(j,1)=(H*T/4*pi)*sqrt(g/h); %Não depende de z
    Br(j,1)=(H/2)*(1+(zr(j,1)/h));   
    for i=1:length(x) %Vai fazer a conta para cada cota
        deshr1(i,j)=-Ar(j,1)*sin(k*x(i,1)-fa*t); %Deslocamento horizontal para águas rasas
        desvr1(i,j)=Br(j,1)*cos(k*x(i,1)-fa*t); %Deslocamento vertical para águas rasas
    end
end

% figure
% hold on
% title('Deslocamento da particula em águas rasas')
% plot(deshr1(:,1),desvr1(:,1)) %Deslocamento para z=0
% plot(deshr1(:,2),desvr1(:,2),'r') %Deslocamento para z=-1
% plot(deshr1(:,3),desvr1(:,3),'g') %Deslocamento para z=-2
% plot(deshr1(:,4),desvr1(:,4),'y') %Deslocamento para z=-3
% plot(deshr1(:,5),desvr1(:,5),'m') %Deslocamento para z=-4
% plot(deshr1(:,6),desvr1(:,6),'k') %Deslocamento para z=-5
% legend('z=0','z=-1','z=-2','z=-3','z=-4','z=-5')
% hold off


%%%Deslocamento da Particula em águas PROFUNDAS para x1 e z1 igual a 0 (Ponto de referencia = 0,0)
zf=[0:-10:-160]';
h=160; %Profundidade para águas profundas
for j=1:length(zf)
    Af(j,1)=(H/2)*exp(k*zf(j,1));
    Bf(j,1)=Af(j,1);           
    for i=1:length(x)
        deshf1(i,j)=-Af(j,1)*sin(k*x(i,1)-fa*t);%*30; %Deslocamento horizontal para águas profundas->multiplicado por 30 para aumentar a largura da elipse
        desvf1(i,j)=Bf(j,1)*cos(k*x(i,1)-fa*t);%*12; %Deslocamento vertical para águas profundas
    end   
end

figure
hold on
title('Deslocamento da particula em águas profundas')
plot(deshf1(:,1),desvf1(:,1)) %Deslocamento para z=0
plot(deshf1(:,2),desvf1(:,2),'r') %Deslocamento para z=-10
plot(deshf1(:,3),desvf1(:,3),'g') %Deslocamento para z=-20
plot(deshf1(:,4),desvf1(:,4),'y') %Deslocamento para z=-30
plot(deshf1(:,5),desvf1(:,5),'m') %Deslocamento para z=-40
plot(deshf1(:,6),desvf1(:,6),'k') %Deslocamento para z=-50
plot(deshf1(:,7),desvf1(:,7),'r') %Deslocamento para z=-60
plot(deshf1(:,8),desvf1(:,8),'g') %Deslocamento para z=-70
plot(deshf1(:,9),desvf1(:,9),'y') %Deslocamento para z=-80
plot(deshf1(:,10),desvf1(:,10),'m') %Deslocamento para z=-90
plot(deshf1(:,11),desvf1(:,11),'k') %Deslocamento para z=-100
plot(deshf1(:,12),desvf1(:,12),'r') %Deslocamento para z=-110
plot(deshf1(:,13),desvf1(:,13),'g') %Deslocamento para z=-120
plot(deshf1(:,14),desvf1(:,14),'y') %Deslocamento para z=-130
plot(deshf1(:,15),desvf1(:,15),'m') %Deslocamento para z=-140
plot(deshf1(:,16),desvf1(:,16),'k') %Deslocamento para z=-150
plot(deshf1(:,17),desvf1(:,17),'m') %Deslocamento para z=-160
legend('z=0','z=-10','z=-20','z=-30','z=-40','z=-50','z=-60','z=-70','z=-80','z=-100','z=-110','z=-120','z=-130','z=-140','z=-150','z=-160')
hold off


%%% Colocar os deslocamentos um em baixo do outro %%%

% Águas Profundas
figure
for i=1:160

hold on
title('Gráfico dos deslocamentos da particula em águas profundas')
xlabel('X (m)')
ylabel('Cota (m)')
neta=eta(380:610);
plot(neta,'b*-') 
desh0f=deshf1(i,1)+117;
desv0f=desvf1(i,1)-8;
plot(desh0f,desv0f,'c.-')
desh10f=deshf1(i,2)+117;
desv10f=desvf1(i,2)-23;
plot(desh10f,desv10f,'r.-')
desh20f=deshf1(i,3)+117;
desv20f=desvf1(i,3)-35;
plot(desh20f,desv20f,'g.-')
desh30f=deshf1(i,4)+117;
desv30f=desvf1(i,4)-43;
plot(desh30f,desv30f,'y.-')
desh40f=deshf1(i,5)+117;
desv40f=desvf1(i,5)-50;
plot(desh40f,desv40f,'m.-')
desh50f=deshf1(i,6)+117;
desv50f=desvf1(i,6)-55;
plot(desh50f,desv50f,'k.-')
axis ([0 length(neta) -60 max(neta)])
legend('eta','z=0','z=-10','z=-20','z=-30','z=-40','z=-50')
hold off
%M(i)=getframe
end
%movie(M)

%Águas rasas
figure
hold on
title('Gráfico dos deslocamentos da particula em águas rasas')
xlabel('X (m)')
ylabel('Cota (m)')
neta=eta(380:610);
plot(neta,'b*-') 
desh0r=deshr1(:,1)+117;
desv0r=desvr1(:,1)-0;
plot(desh0r,desv0r,'c.-')
desh1r=deshr1(:,2)+117;
desv1r=desvr1(:,2)-1;
%plot(desh1r,desv1r,'r.-')
desh2r=deshr1(:,3)+117;
desv2r=desvr1(:,3)-2;
plot(desh2r,desv2r,'g.-')
desh3r=deshr1(:,4)+117;
desv3r=desvr1(:,4)-3;
plot(desh3r,desv3r,'y.-')
desh4r=deshr1(:,5)+117;
desv4r=desvr1(:,5)-4;
plot(desh4r,desv4r,'m.-')
desh5r=deshr1(:,6)+117;
desv5r=desvr1(:,6)-5;
plot(desh5r,desv5r,'k.-')
axis ([0 length(neta) min(zr) max(neta)])
legend('eta','z=0','z=-1','z=-2','z=-3','z=-4','z=-5')
hold off
   

%%% Plot do Eta, Velocidade e Aceleração (Horizontal e Vertical)

figure
subplot(5,1,1)
plot(eta(10:length(eta)),'k')
title('Gráfico dos parâmetros de velocidade e aceleração em relação à elevação (eta)') 
ylabel('Elevação (m)')
subplot(5,1,2)
plot(udisp(10:length(eta)),'r')
ylabel('Vel.Horizontal')
subplot(5,1,3)
plot(acelh(10:length(eta)),'r')
ylabel('Acel.Horizontal')
subplot(5,1,4)
plot(wdisp(10:length(eta)))
ylabel('Vel.Vertical')
subplot(5,1,5)
plot(acelv(10:length(eta)))
ylabel('Acel.Vertical')
xlabel('Registros')
    
    
    



