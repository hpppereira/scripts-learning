%% Programa para c�lculo da dire��o das ondas geradas pela rotina 'geraonda3'
%
%Desenvolvido por:
% Henrique Patricio P. Pereira
% E-mail: henriqueppp@oceanica.ufrj.br
% Data da ultima modificacao: 11/11/2013

%%
clear,clc,close all

%% Chama subrotina 'geraonda3'
%Entrar com a dire��o m�dia
tetamean=input('Entre com a dire��o das ondas: ');

%Chama subrotina 'geraonda3'
[neta,netax,netay,netaxx,netayy,velx,vely,velz,velzz,velzzz,pr,dt,h,z,d,g]=geraonda3(tetamean);
%neta - eleva��o
%netax - inclina��o em x
%netay - inclina��o em y
%netaxx - curvatura em x
%netayy - curvatura em y
%velx - velocidade horizontal em x
%vely - velocidade horizontal em y
%velz - velocidade vertical superficial (Dneta/Dt)
%velzz - velocidade vertical (Equa��o integral - papaer RAPPORT)
%velzzz - velocidade vertical (Dpot.vel/Dz) (utilizar esta pois varia com o z e � maios parecida com a velz quando z=0)
%pr - press�o (peso especifico = 1.025 g/cm^3)
%dt - intervalo de amostragem
%d - densidade 1025 g/cm3

%% Plot das s�ries dos par�metros de onda
figure
subplot(2,1,1)
[AX,H1,H2]=plotyy(1:length(neta),neta,1:length(pr),pr,'plot');
set(get(AX(1),'Ylabel'),'String','Eta (m)') ;
set(get(AX(2),'Ylabel'),'String','Press�o (mbar)'); 
title('S�rie') 
subplot(2,1,2)
plot(neta),hold on
plot(velx,'r')
plot(vely,'k')
plot(velzzz,'g'), hold off
title('S�rie'),xlabel('Tempo (registros)'),ylabel('(m) ; (m/s)')
legend('Eta','Vel x','Vel y','Vel z')

%% Espectros
[aaeta]=espec(neta,dt); %Espec. de neta
[aaxy]=espec2(velx,vely,dt); %Espec. cruzado entre 'Vx' e 'Vy'
[aaxz]=espec2(velx,velzzz,dt); %Espec. cruzado entre 'Vx' e 'Vz'
[aayz]=espec2(vely,velzzz,dt); %Espec. cruzado entre 'Vy' e 'Vz'
[aaxp]=espec2(velx,pr,dt); %Espec. cruzado entre 'Vx' e 'press�o'
[aayp]=espec2(vely,pr,dt); %Espec. cruzado entre 'Vy' e 'press�o'

%Plot dos autoespectros
figure
subplot(2,1,1)
plot(aaxp(:,1),aaxp(:,3),'c') %auto-espec da press�o
legend('Press�o')
title('Auto-Espectro'),xlabel('Frequ�ncia'),ylabel('Energia')
subplot(2,1,2)
hold on
plot(aaeta(:,1),aaeta(:,2),'b') %auto-espec de eta
plot(aaxy(:,1),aaxy(:,2),'r') %auto-espec de vel x
plot(aaxy(:,1),aaxy(:,3),'k') %auto-espec de vel y
plot(aaxz(:,1),aaxz(:,3),'g') %auto-espec de vel z
legend('Eta','Vel x','Vel y','Vel z')
title('Auto-Espectro'),xlabel('Frequ�ncia'),ylabel('Energia')
hold off

%% Vari�veis de entrada para a rotina 'numeronda'
%deltat
deltat=1;
%Profundidade
%h=200; %Vem da subrotina geraonda3
%Cota
%z=0; %Vem da subrotina geraonda3
%Comprimento da s�rie
reg=length(neta)
%Comprimento da matriz do espectro da s�rie (reg/2)
reg2=reg/2;
%Frequencia de corte
fc=1/(2*deltat);
%Vetor de frequencia
deltaf=(fc*2/reg:fc*2/reg:fc)';

%% Chama subrotina numonda (vari�vel de sa�da - 'k')
[k]=numeronda(h,deltaf,reg2)'; 
figure
plot(deltaf,k)
title(['N�mero de onda (k) para h=',num2str(h),' e z=',num2str(z)]),xlabel('Frequ�ncia'),ylabel('k')

%% Calcular a fun��o de transfer�ncia de Vx, Vy e Vz e P para cada frequencia
%Calculo para Vx
for i=1:length(velx)/2
    U(i,1)=2*pi*deltaf(i,1)*((cosh(k(i,1)*(h+z)))/(sinh(k(i,1)*h)));
end

%Calculo para Vy (Vx=Vy)
V=U;

%Calculo para Vz
for i=1:length(velzz)/2
    W(i,1)=2*pi*deltaf(i,1)*((sinh(k(i,1)*(h+z)))/(sinh(k(i,1)*h)));
end

%Calculo para Press�o
for i=1:length(pr)/2
    P(i,1)=d*g*((cosh(k(i,1)*(h+z)))/cosh(k(i,1)*h));
end

figure
subplot(2,1,1)
plot(deltaf,P,'y')
title(['Fun��o de transferencia de P para h=',num2str(h),' e z=',num2str(z)]),xlabel('Frequ�ncia'),ylabel('P')
legend('P')
subplot(2,1,2)
plot(deltaf,U,'r','linewidth',1.5),hold on
plot(deltaf,V,'k')
plot(deltaf,W,'g'), hold off
title(['Fun��o de transferencia de U, V e W para h=',num2str(h),' e z=',num2str(z)]),xlabel('Frequ�ncia'),ylabel('U, V e W')
legend('U','V','W')
    
%% Calcula o Espectro simples (S(f)) com a fun��o de transfer�ncia
%Cria vari�veis com os co-espectros (calculados pela espec2)
cuu=aaxy(:,2); %auto-espec de U (mesma coisa que o co-espec de U e U)
cvv=aaxy(:,3); %auto-espec de V (mesma coisa que o co-espec de V e V)
cww=aaxz(:,3); %auto-espec de W (mesma coisa que o co-espec de W e W)
cpp=aaxp(:,3); %auto-espec de P (mesma coisa que o co-espec de P E P)
cup=aaxp(:,4); %co-espec de U e P
cvp=aayp(:,4); %co-espec de W e P

%Fun��o de transfer�ncia ao quadrado
U2=U.^2;
V2=V.^2;
W2=W.^2;
P2=P.^2;

%Calculo de S(f) com a fun��o de transfer�ncia de 2 formas
sf1=(cuu./U2)+(cvv./V2); %auto-espec vel x e vel y (fun��o de trasferencia) forma do papaer rapport - utilizando vel u e v
sf11=(cuu+cvv)./U2; %auto-espec vel x e vel y (fun��o de trasferencia) forma do relatorio do joao - utilizando vel u e v
sf2=cww./W2; %igual nos 2 papers - utiliza a velz 
sf3=cpp./P2; %igual nos 2 papers - utiliza a press�o

%Plot para comparar S(f) simples e S(f) utilizando a fun��o de transfer�ncia
figure
subplot(2,1,1)
hold on
plot(aaeta(:,1),aaeta(:,2),'b') %auto-espec de eta
plot(aaxy(:,1),aaxy(:,2),'r') %auto-espec de vel x
plot(aaxy(:,1),aaxy(:,3),'k') %auto-espec de vel y
plot(aaxz(:,1),aaxz(:,3),'g') %auto-espec de vel z
plot(aaxp(:,1),aaxp(:,3),'y') %auto-espec da press�o
legend('Eta','Vel x','Vel y','Vel z','Press�o')
title('Auto-Espectro'),xlabel('Frequ�ncia'),ylabel('Energia)')
hold off
subplot(2,1,2)
hold on
plot(deltaf,sf1,'b','linewidth',1.5), hold on
plot(deltaf,sf11,'r')
plot(deltaf,sf2,'g')
plot(deltaf,sf3,'y'), hold off
title('Auto-espectro utilizando a fun��o de transfer�ncia'), xlabel('Frequ�ncia'),ylabel('Energia')
legend('U e V - 1','U e V - 2','W','P')
hold off

%% Filtra as altas e baixas frequ�ncias dos espectros com fun��o de transfer�ncia 
% Filtra as frequ�ncia que n�o tem mais energia
% Retira os valores de energia nas freq�encias menores que 0.04 (25 seg) e maiores que 0.2 (5 seg)
sf1_corr=sf1;
sf11_corr=sf11;
sf2_corr=sf2;
sf3_corr=sf3;

for i=1:length(sf1)
    if deltaf(i,1)<0.04
        
        sf1_corr(i,1)=0;
        sf11_corr(i,1)=0;
        sf2_corr(i,1)=0;
        sf3_corr(i,1)=0;

        
    elseif deltaf(i,1)>0.2
        
        sf1_corr(i,1)=0;
        sf11_corr(i,1)=0;
        sf2_corr(i,1)=0;
        sf3_corr(i,1)=0;
        
    end
end

%Plot do auto-espectro filtrando as altas e baixas frequ�ncias
figure
plot(deltaf,sf1_corr,'b','linewidth',1.5), hold on
plot(deltaf,sf11_corr,'r')
plot(deltaf,sf2_corr,'k')
plot(deltaf,sf3_corr,'y'), hold off
title('Auto-espectro utilizando a fun��o de transfer�ncia FILTRADO em 0.2<f<0.04'), xlabel('Frequ�ncia'),ylabel('Energia')
legend('Rapport (U e V)','Rel. joao (U e V)','W','P')

%% C�lculo dos coeficientes 'a1' e 'b1'

for i=1:length(deltaf)
    
    a1(i,1)=cup(i,1)/(U(i,1)*P(i,1)*aaeta(i,2)*pi);
    
    b1(i,1)=cvp(i,1)/(V(i,1)*P(i,1)*aaeta(i,2)*pi);
    
end
    
%% C�lculo da dire��o m�dia em radianos

for i=1:length(deltaf)
    
    dirrad(i,1)=atan(b1(i,1)/a1(i,1));
    
end

%Passa de rad. para grau
dirt=dirrad.*(180/pi);

%Plot da dire��o em arco trigonom�trico
% figure
% subplot(2,1,1)
% plot(deltaf,sf1_corr,'b','linewidth',1.5), hold on
% plot(deltaf,sf11_corr,'r')
% plot(deltaf,sf2_corr,'k')
% plot(deltaf,sf3_corr,'g'), hold off
% title('Auto-espectro utilizando a fun��o de transfer�ncia FILTRADO em 0.25<f<0.04'), xlabel('Frequ�ncia'),ylabel('S(f)')
% legend('Rapport (U e V)','Rel. joao (U e V)','W','P')
% subplot(2,1,2)
% plot(deltaf,dirgrau)
% title('Dire��o (trigonom�trico)'),xlabel('Frequ�ncia'),ylabel('Dire��o')

%% Fun��o de corre��o angular - Transforma de trigonom�trico para azimute
%Chama subrotina para corre��o angular
[diraz]=trig_para_azim(dirt);

%Plot da dire��o em azimute
figure
subplot(2,1,1)
plot(deltaf,aaeta(:,2))
title('Auto-Espectro da Eleva��o'), xlabel('Frequ�ncia'),ylabel('Energia')
subplot(2,1,2)
plot(deltaf,diraz)
title('Dire��o (azimute)'),xlabel('Frequ�ncia'),ylabel('Dire��o (graus)')

%% Calcula par�metros de onda
%Periodo de pico no espectro de eta
fp=aaeta(find(aaeta(:,2)==max(aaeta(:,2))),1);
tp=1/fp;
%Altura Hm0 calculado pela espectro de eta
df=deltaf(2)-deltaf(1);
m0=0;

%Integral do espec de eta
for i=1:length(aaeta)
    m0=m0+(aaeta(i,2)*df);
end

%Calculo da alt. sig, usando  momento espectral zero
Hm0=4.01*sqrt(m0);

%cria matriz para [f diraz] para o c�lculo da dire��o de pico
fdir=[deltaf,diraz];
%Dire��o de pico
dirtp=fdir(find(fdir(:,1)==fp),2);

%% Chama subrotina cos2s
[Gs,ht,Gsi,hti,s1,s1p,g0]=FEA_cos2s(deltaf,a1,b1,diraz,dirrad,dirtp,fp,dt);

%Filtra as frequ�ncia que n�o tem mais energia
diraz_corr=diraz;
ht_corr=ht;
dti_corr=hti;
s1_corr=s1;
en_eta=aaeta(:,2);
en_eta_corr=en_eta;

for i=1:length(deltaf)
    if deltaf(i,1)<0.04
        
        diraz_corr(i,1)=0;
        ht_corr(i,1)=0;
        dti_corr(i,1)=0;
        en_eta_corr(i,1)=0;
        s1_corr(i,1)=0;
        
    elseif deltaf(i,1)>0.25
        
        diraz_corr(i,1)=0;
        ht_corr(i,1)=0;
        dti_corr(i,1)=0;
        en_eta_corr(i,1)=0;
        s1_corr(i,1)=0;
        
    end
end

%Plot do s1 em fun��o da frequ�ncia
figure
subplot(2,1,1)
plot(deltaf,en_eta_corr)
title('Auto-Espectro da Eleva��o'), xlabel('Frequ�ncia'),ylabel('Energia')
subplot(2,1,2)
plot(deltaf,s1_corr)
title('Par�metro de Espalhamento angular �s1�'),xlabel('Frequ�ncia'),ylabel('s1')

%% C�lculo do espectro direcional 'E(f,teta)'
%'sid' � o 's' da fun��o de espalhamento idealizada para o calculo do espectro direcional, varia de 1 a 16
sid=1;
ed=hti(:,sid).*en_eta;

%Plot do espectro direcional
[XI,YI]=meshgrid(diraz_corr,deltaf,'nearest');
[XI,YI,ZI] = griddata(diraz,deltaf,ed,XI,YI);

figure
mesh(XI,YI,ZI)
title('Espectro direcional'),xlabel('Dire��o'),ylabel('Frequ�ncia (Hz)'),colorbar

