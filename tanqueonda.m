clear
clc
%Cinemática da particula para ondas progressivas

% Deslocamento da supericie (eta)

%x=linspace(0,11*pi,1024)'; %Eixo x q achava q poderia ser, mas nao é.
x=(1:1024)'; %eixo x
tempo=(1:1024)'; %Tempo
t=1; %Intervalo de tempo
H=2; %Altura de onda
L=20; %Comprimento de onda (m)
Lfundo=20;     %9.8*10/(2*pi/10); %Comprimento (para o graf. do deslocamento em águas prof, um em baixo do outro)
T=10; %Periodo da onda
k=2*pi/L; %Numero de onda
kfundo=2*pi/Lfundo; %numero de onda (para o graf. do deslocamento em águas prof, um em baixo do outro)
fa=2*pi/T; %Frequencia angular
h=100; %Profundidade local
g=9.8; %Ac. gravidade
redisp=g*k*tanh(k*h); %Relação de dispersão
cel=L/T; %Celeridade da onda (m/s)
z=linspace(0,0,1024)'; %Cota para achar as velocidade para Z=0
%z=(1:1024)'; %Valor da cota para criar gráfico de deslocamento em diferentes profundidade (espiral)
for i=1:length(x)
    
    %Elevação (eta)
    eta(i,1)=H/2*cos((k*x(i,1))-(fa*t)); %O 'cos((k*x(i,1))-(fa*t)) multipicado por algum numero muda a fase da onda
    etafundo(i,1)=H/2*cos((kfundo*x(i,1))-(fa*t)); 
    
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
    
    %Velocidade horizontal 
    u(i,1)=(H*fa*cosh(k)*(h+z(i,1))*cos(k*x(i,1)-fa*t))/(2*sinh(k*h));
    %u(i,1)=abs(u(i,1)); %Coloca os valores de vel positivos
    
    %Velocidade horizontal introduzindo a relação de disperção
    udisp(i,1)=(H*g*k*cosh(k)*(h+z(i,1))*cos(k*x(i,1)-fa*t))/(2*fa*cosh(k*h));
    %udisp(i,1)=abs(udisp(i,1)); %Coloca os valores de vel positivos
    
    %Aceleração horizontal
    acelh(i,1)=(H*g*k*cosh(k)*(h+z(i,1))*sin(k*x(i,1)-fa*t))/(2*cosh(k*h));
    
    %Velocidade vertical
    wdisp(i,1)=(H*g*k*sinh(k)*(h+z(i,1))*sin(k*x(i,1)-fa*t))/(2*fa*cosh(k*h));
    
    
    %Aceleração vertical
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
    desh1(i,1)=-A*sin(k*x(i,1)-fa*t);
    desv1(i,1)=B*cos(k*x(i,1)-fa*t);
end

%Equação da elipse
%%%el=(desh1/A).^2+(desv1/B).^2; ==1??


a=input('Digite 1 para as ondas se propagando em águas rasas (h/L<1/20), 2 - Intermediárias (1/20<h/L<1/2) e 3 - Profundas (h/L>1/2): ');
if a==1 %Se for em águas rasas
    L=100;
    h=5;
    if h/L<=(1/20) %Se for menor ou igual a 1/20
        disp('A onda está se propagando em águas rasas, Prof(h)=4m, Compr.onda(L)=100m');
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
            movie(M,0) %(M,0) para o gráfico só rodar uma vez
            hold off
        end
    end

elseif a==2
    h=6;
    L=100;
    if h/L<(1/2) & h/L>(1/20)
        disp('A onda está se propagando em águas intermediárias, com prof(h)=6m e Compr.onda(L)=100m; quais são as equações para águas intemediárias mineiro po?!');
    end
elseif a==3
       h=51;
       L=100;
       if h/L>=1/2
           disp('A onda está se propagando em águas profundas, com Prof(h)=51m e Compr.onda(L)=100m.');
           Af=(H/2)*exp(k*z);
           Bf=Af;    
           for i=1:length(x)
               deshf(i,1)=-Af*sin(k*x(i,1)-fa*t); %Deslocamento horizontal para águas profundas
               desvf(i,1)=Bf*cos(k*x(i,1)-fa*t); %Deslocamento vertical para águas profundas
           end
           grf=input('Digite ´1´ para plotar o gráfico em animação e ´0´ para continuar o rotina: ');
           if grf==1      
              z=input('Digite um valor para cota entre 0 (sup) à -60 (fundo) para o gráfico de movimento da particula: ');    
              plot(deshf,desvf,'r')
              for i=1:160 % Animação com 160 frames
                  hold on
                  axis([-1 1 -1 1])
                  plot(deshf(i,1),desvf(i,1),'*-')  % Fazer o gráfico do deslocamento
                  M(i)=getframe %Filme do movimento
              end
              movie(M)
              hold off
           end
       end
end


%%% Gráfico de movimento da particula por cota para águas rasas ( z= 0 à -4) %%% 
zr=[0:-1:-5]';
h=4; %Profundidade para águas rasas
for j=1:length(zr)
    Ar(j,1)=(H*T/4*pi)*sqrt(g/h); %Não depende de z
    Br(j,1)=(H/2)*(1+(zr(j,1)/h));   
    for i=1:length(x) %Vai fazer a conta para cada cota
        deshr(i,j)=-Ar(j,1)*sin(k*x(i,1)-fa*t); %Deslocamento horizontal para águas rasas
        desvr(i,j)=Br(j,1)*cos(k*x(i,1)-fa*t); %Deslocamento vertical para águas rasas
    end
end
figure
hold on
title('Deslocamento da particula em águas rasas')
plot(deshr(:,1),desvr(:,1)) %Deslocamento para z=0
plot(deshr(:,2),desvr(:,2),'r') %Deslocamento para z=-1
plot(deshr(:,3),desvr(:,3),'g') %Deslocamento para z=-2
plot(deshr(:,4),desvr(:,4),'y') %Deslocamento para z=-3
plot(deshr(:,5),desvr(:,5),'m') %Deslocamento para z=-4
plot(deshr(:,5),desvr(:,5),'m') %Deslocamento para z=-5
legend('z=0','z=-1','z=-2','z=-3','z=-4','z=-5')
hold off


%%% Gráfico de movimento da particula por cota para águas profundas ( z= 0 à -51) %%% 
zf=[0:-10:-60]';
h=51; %Profundidade para águas profundas
for j=1:length(zf)
    Af(j,1)=(H/2)*exp(k*zf(j,1));
    Bf(j,1)=Af(j,1);           
    for i=1:length(x)
        deshf(i,j)=-Af(j,1)*sin(k*x(i,1)-fa*t);%*30; %Deslocamento horizontal para águas profundas->multiplicado por 30 para aumentar a largura da elipse
        desvf(i,j)=Bf(j,1)*cos(k*x(i,1)-fa*t);%*8.5; %Deslocamento vertical para águas profundas
    end   
end

figure
hold on
title('Deslocamento da particula em águas profundas')
plot(deshf(:,1),desvf(:,1)) %Deslocamento para z=0
plot(deshf(:,2),desvf(:,2),'r') %Deslocamento para z=-10
plot(deshf(:,3),desvf(:,3),'g') %Deslocamento para z=-20
plot(deshf(:,4),desvf(:,4),'y') %Deslocamento para z=-30
plot(deshf(:,5),desvf(:,5),'m') %Deslocamento para z=-40
plot(deshf(:,6),desvf(:,6),'k') %Deslocamento para z=-50
legend('z=0','z=-10','z=-20','z=-30','z=-40','z=-50')
hold off


%%% Colocar os deslocamentos um em baixo do outro %%%

% Águas Profundas
figure
hold on
title('Gráfico dos deslocamentos da particula em águas profundas')
xlabel('X (m)')
ylabel('Cota (m)')
neta=eta(380:610);
netafundo=etafundo(380:450);
plot(netafundo,'b*-') 
desh0f=deshf(:,1)+23;
desv0f=desvf(:,1)-0;
plot(desh0f,desv0f,'c.-')
desh10f=deshf(:,2)+23;
desv10f=desvf(:,2)-10;
plot(desh10f,desv10f,'r.-')
desh20f=deshf(:,3)+23;
desv20f=desvf(:,3)-20;
plot(desh20f,desv20f,'g.-')
desh30f=deshf(:,4)+23;
desv30f=desvf(:,4)-30;
plot(desh30f,desv30f,'y.-')
desh40f=deshf(:,5)+23;
desv40f=desvf(:,5)-40;
plot(desh40f,desv40f,'m.-')
desh50f=deshf(:,6)+23;
desv50f=desvf(:,6)-50;
plot(desh50f,desv50f,'k.-')
axis ([0 length(netafundo) min(zf) max(netafundo)])
legend('eta','z=0','z=-10','z=-20','z=-30','z=-40','z=-50')
hold off

%Águas rasas
figure
hold on
title('Gráfico dos deslocamentos da particula em águas rasas')
xlabel('X (m)')
ylabel('Cota (m)')
plot(neta,'b*-') 
axis ([0 length(neta) min(zr) max(neta)])
desh0r=deshr(:,1)+117;
desv0r=desvr(:,1)-0;
plot(desh0r,desv0r,'c.-')
desh1r=deshr(:,2)+117;
desv1r=desvr(:,2)-1.8;
plot(desh1r,desv1r,'r.-')
desh2r=deshr(:,3)+117;
desv2r=desvr(:,3)-3.2;
plot(desh2r,desv2r,'g.-')
desh3r=deshr(:,4)+117;
desv3r=desvr(:,4)-4.2;
plot(desh3r,desv3r,'y.-')
desh4r=deshr(:,5)+117;
desv4r=desvr(:,5)-4.8;
plot(desh4r,desv4r,'m.-')
neta=eta(380:610);
legend('eta','z=0','z=-1','z=-2','z=-3','z=-4')
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

% for g=1:200
%     plot(deshr(g,1),desvr(g,1),'*-');   % Fazer o gráfico do deslocamento
%     M(g)=getframe %Filme do movimento
%     hold on
%     axis([-25 25 -1 1])            
% end  
%     movie(M,1)
%     hold off






% z=0; %moviemnto da partícula é igual a zero 'superfície':
% if h/L<=1/20 %Se for menor ou igual a 1/20
%     disp('A onda está se propagando em águas rasas');
%     Ar=(H*T/4*pi)*sqrt(g/h); %Não depende de z
%     Br=(H/2)*(1+(z/h));   
%     for i=1:length(x) %Vai fazer a conta para cada cota
%         
%         deshr(i,1)=-Ar*sin(k*x(i,1)-fa*t); %Deslocamento horizontal para águas rasas
%         desvr(i,1)=Br*cos(k*x(i,1)-fa*t); %Deslocamento vertical para águas rasas
%         
%     end
% elseif h/L<(1/2) & h/L>(1/20)
%     disp('A onda está se propagando em águas intermediárias');
% elseif h/L>=1/2
%     disp('A onda está se propagando em águas profundas');
%     Af=(H/2)*exp(k*z);
%     Bf=Af;           
%         for i=1:length(x)
%             
%             deshf(i,1)=-Af*sin(k*x(i,1)-fa*t); %Deslocamento horizontal para águas profundas
%             desvf(i,1)=Bf*cos(k*x(i,1)-fa*t); %Deslocamento vertical para águas profundas
% 
%         end
% end
 
 



