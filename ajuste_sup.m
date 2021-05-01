%
% Ajuste de superficie em espaço multidimensional de grau n=2 
% Função polinomial
% Ricardo Martins Campos e José Antonio 25/10/2011
%
% O arquivo saidaOnda1h_BS_axys13e15_bs4_matlab.txt contem as saidas do
% programa onda1h para as boias axys13, 15 e wavescanBS4. Atencao pois
% existe aprox 2 graus de longitude de distancia entre as boias.
%
ccc

a=load('saidaOnda1h_BS_axys13e15_bs4.txt');


vcar1=a(:,32);
s2=a(:,69); % coluna com s2_VTPK1
% s2=a(:,68); % coluna com s2_VEPK1

% Calculando media e mediana de VCAR1
int_vcar1=(0.5:1:7.5)';
nt=length(int_vcar1);
s2_media_vcar1=ones(nt,1)*NaN;s2_mediana_vcar1=ones(nt,1)*NaN;s2_per70_vcar1=ones(nt,1)*NaN;
for j=1:nt
    k=find(vcar1 > int_vcar1(j)-0.5 & vcar1 <= int_vcar1(j)+0.5);
    if ~isempty(k)
        s2_media_vcar1(j)=mean(s2(k));
        s2_mediana_vcar1(j)=median(s2(k));
        s2_per70_vcar1(j)=percentile(s2(k),0.7);
    end
end

% Figura para comparar os diferentes parametros estatísticos
% figure;plot(int_vcar1,s2_media_vcar1,'b+');hold
% on;plot(int_vcar1,s2_mediana_vcar1,'kd');plot(int_vcar1,s2_per70_vcar1,'r*')

% Avaliacao inicial do ajuste polinomial, grau 2.
% [P,S] = polyfit(int_vcar1,s2_media_vcar1,2);
% fitg2=P(1).*(int_vcar1.^2)+P(2).*int_vcar1+P(3);
% figure;plot(int_vcar1,s2_media_vcar1,'k');hold on;plot(int_vcar1,fitg2,'r')
% xlabel('vcar1');ylabel('s2_VEPK1');title('Ajuste regressao linerar com polyfit, pol. grau 2')


% Calculando media e mediana de VTPK1
vtpk1=a(:,33);
int_vtpk1=(4.5:1:16.5)';
nt=length(int_vtpk1);
s2_media_vtpk1=ones(nt,1)*NaN;s2_mediana_vtpk1=ones(nt,1)*NaN;s2_per70_vtpk1=ones(nt,1)*NaN;
for j=1:nt
    k=find(vtpk1 > int_vtpk1(j)-0.5 & vtpk1 <= int_vtpk1(j)+0.5);
    if ~isempty(k)
        s2_media_vtpk1(j)=mean(s2(k));
        s2_mediana_vtpk1(j)=median(s2(k));
        s2_per70_vtpk1(j)=percentile(s2(k),0.7);
    end
end


% Avaliacao inicial do ajuste polinomial, grau 2.
% [P,S] = polyfit(int_vtpk1,s2_media_vtpk1,2);
% fitg2=P(1).*(int_vtpk1.^2)+P(2).*int_vtpk1+P(3);
% figure;plot(int_vtpk1,s2_media_vtpk1,'k');hold on;plot(int_vtpk1,fitg2,'r')
% xlabel('vtpk1');ylabel('s2_VEPK1');title('Ajuste regressao linerar com polyfit, pol. grau 2')



% Selecionando os intervalos simultaneos de VCAR1, VTPK1 e S2_VTPK1
nx=length(int_vcar1);ny=length(int_vtpk1);
s2_media_vcar1_vtpk1=ones(nx,ny)*NaN;s2_mediana_vcar1_vtpk1=ones(nx,ny)*NaN;s2_per70_vcar1_vtpk1=ones(nx,ny)*NaN;
tam=ones(nx,ny)*NaN;
for jx=1:length(int_vcar1)
    for jy=1:length(int_vtpk1)
        k=find(vcar1 > int_vcar1(jx)-0.5 & vcar1 <= int_vcar1(jx)+0.5 & vtpk1 > int_vtpk1(jy)-0.5 & vtpk1 <= int_vtpk1(jy)+0.5 );
        if ~isempty(k)
            tam(jx,jy)=length(k);
            s2_media_vcar1_vtpk1(jx,jy)=mean(s2(k));
            s2_mediana_vcar1_vtpk1(jx,jy)=median(s2(k));
            s2_per70_vcar1_vtpk1(jx,jy)=percentile(s2(k),0.7);
        end
    end
end


tam

% Plotagem da superticie já selecionada em intervalos vcar vtpk.
[X,Y]=meshgrid(int_vcar1,int_vtpk1');
figure;plot3(X,Y,s2_media_vcar1_vtpk1','*');xlabel('vcar1');ylabel('vtpk1');zlabel('s2 VEPK1');grid on
title('Selecao dos dados em intervalos VCAR1 e VTPK1')
%figure;SURF(X,Y,s2_media_vcar1_vtpk1');axis tight;xlabel('vcar1');ylabel('vtpk1');zlabel('s2 VEPK1');
%title('Selecao dos dados em intervalos VCAR1 e VTPK1')

% keyboard
% -----------------------------------------------------------------------
% Ajuste da superficie com função reglin.m

% Nuvem de dados (total) a ser ajustado
x1=a(:,32:33); % vcar1 vtpk1
v1=a(:,68); % s2_vekp1
figure;plot3(x1(:,1),x1(:,2),v1,'k*');grid on;
xlabel('vcar1');ylabel('vtpk1');zlabel('s2 VEPK1')
title('Dados de entrada a serem ajustados')

% Ajuste da superficie a nuvem geral de pontos (total)
param.n0=2;
param.mod='mqs';
[y2,model] = reglin(x1,x1,v1,param);
% Variavel alvo (s2) ajustada
sv1=sort(v1);sy2=sort(y2);
figure;plot(sv1,'b*');hold on;plot(sy2,'r+');ylabel('s2 VEPK1')
title('Ajuste feito pela funcao reglin')

% conferindo o valor dos coeficientes do ajuste polinomial
coef=model.teta; coefb=coef;
for i=1:length(v1)
    nz(i)=coef(1) + (coef(2).*x1(i,1)) + (coef(3).*x1(i,2)) + (coef(4).*x1(i,1).^2) + (coef(5).*x1(i,2).^2);
end
% Plotagem de s2 ajustado. Deve ser igual a figura anterior
sv1=sort(v1);snz=sort(nz);
figure;plot(sv1,'b*');hold on;plot(snz,'r+');ylabel('s2 VEPK1')
title('Ajuste feito com os parametros da regressao linear, grau 2')

% Superficie ajustada à nuvem de pontos
figure;plot3(x1(:,1),x1(:,2),v1,'k*');hold on;plot3(x1(:,1),x1(:,2),nz,'r+')
xlabel('vcar1');ylabel('vtpk1');zlabel('s2 VEPK1');grid on
title('Superficie de ajuste feito com os parametros da regressao linear, grau 2')


% resize para fazer ajuste com um unico vetor.
s=size(X);s=s(2);
nx=[X(:,1)'];   % int_vcar1
for i=1:(s-1)
  nx=[nx X(:,i+1)'];
end
nx=nx';

s=size(Y);s=s(2);
ny=[Y(:,1)'];  % int_vtpk1
for i=1:(s-1)
  ny=[ny Y(:,i+1)'];
end
ny=ny';

s=size(s2_media_vcar1_vtpk1);s=s(1);
ns2=[s2_media_vcar1_vtpk1(1,:)];
for i=1:(s-1)
  ns2=[ns2 s2_media_vcar1_vtpk1(i+1,:)];
end
ns2=ns2';

k=find(ns2>0); %retira os NaN dos intervalos que nao tem valores
nx=nx(k);ny=ny(k);ns2=ns2(k);
x1=[nx ny]; % int_vcar1 int_vtpk1

% Faz ajuste à superficie já intervalada
param.n0=2;
param.mod='mqs';
[y2,model] = reglin(x1,x1,ns2,param);

% figure;plot(ns2,'k*');hold on;plot(y2,'r+');ylabel('s2 VEPK1')
% title('Ajuste feito pela funcao reglin')
sns2=sort(ns2);sy2=sort(y2);
figure;plot(sns2,'k*');hold on;plot(sy2,'r+');ylabel('s2 VEPK1')
title('Ajuste feito com os parametros da regressao linear, grau 2')

coef=model.teta
for i=1:length(ns2)
    %nz(i)=(coef(5).*nx1_1(i).^2) + (coef(4).*nx1_1(i)) + (coef(3).*nx1_2(i).^2) + (coef(2).*nx1_1(i)) + coef(1);
    ans2(i)=coef(1) + (coef(2).*x1(i,1)) + (coef(3).*x1(i,2)) + (coef(4).*x1(i,1).^2) + (coef(5).*x1(i,2).^2);
end
% Figura com a superficie dos dados intervalados e a ajustada
figure;plot3(x1(:,1),x1(:,2),ns2,'k*');hold on;plot3(x1(:,1),x1(:,2),ans2,'r+')
xlabel('vcar1');ylabel('vtpk1');zlabel('s2 VEPK1');grid on
title('Superficie de ajuste feito com os parametros da regressao linear por intervalos, grau 2')

%keyboard
% spreading final (Tucker&Pitt 2001)
sigma_sns2=((2./(sns2+1)).^0.5).*(180/pi);
sigma_sy2=((2./(sy2+1)).^0.5).*(180/pi);
[sigma_sns2 ind]=sort(sigma_sns2);
sigma_sy2=sigma_sy2(ind);
figure;plot(sigma_sns2,'k*');hold on;plot(sigma_sy2,'r+');ylabel('sigma (espalhamento em graus) baseado em s2 VEPK1')
title('Ajuste feito com os parametros da regressao linear, grau 2')

max(max(sigma_sns2))
max(max(sigma_sy2))



% Segunda Simulação usando os coeficientes de ajuste para hs e tp elevados
% Extrapolacao da superficie!
tp=(3.5:1:22.5)';
hs=(0.5:1:11.5)';

[hs,tp]=meshgrid(hs,tp);


s=size(hs);s=s(2);
nhs=[hs(:,1)'];   % int_vcar1
for i=1:(s-1)
  nhs=[nhs hs(:,i+1)'];
end
nhs=nhs';

s=size(tp);s=s(2);
ntp=[tp(:,1)'];  % int_vtpk1
for i=1:(s-1)
  ntp=[ntp tp(:,i+1)'];
end
ntp=ntp';

sim=coef(1) + (coef(2).*nhs) + (coef(3).*ntp) + (coef(4).*nhs.^2) + (coef(5).*ntp.^2);
% Spreading (desvio padrao circular) final em graus(Tucker&Pitt 2001)
sigma_sim=((2./(sim+1)).^0.5).*(180/pi);
%sigma_sim=sort(sigma_sim);
figure;plot3(nhs,ntp,sigma_sim,'r*')
xlabel('Hs');ylabel('Tp');zlabel('Sigma (spreading,desvio padrao circular)');grid on
title('Superficie de ajuste extrapolada feita com os parametros da regressao linear por intervalos, grau 2')



sim=coefb(1) + (coefb(2).*nhs) + (coefb(3).*ntp) + (coefb(4).*nhs.^2) + (coefb(5).*ntp.^2);
% Spreading (desvio padrao circular) final em graus(Tucker&Pitt 2001)
sigma_sim=((2./(sim+1)).^0.5).*(180/pi);
%sigma_sim=sort(sigma_sim);
figure;plot3(nhs,ntp,sigma_sim,'r*')
xlabel('Hs');ylabel('Tp');zlabel('Sigma (spreading,desvio padrao circular)');grid on
title('Superficie de ajuste extrapolada feita com os parametros da regressao linear com todos os dados, grau 2')


% 
% Parametro S (s2 vepk). Superficie  
%sigma_sim=sort(sigma_sim);
sim=coef(1) + (coef(2).*nhs) + (coef(3).*ntp) + (coef(4).*nhs.^2) + (coef(5).*ntp.^2);
figure;plot3(nhs,ntp,sim,'r*')
xlabel('Hs');ylabel('Tp');zlabel('s2 vepk');grid on
title('Superficie de ajuste extrapolada feita com os parametros da regressao linear por intervalos, grau 2')





% Ajuste literatura 
% Wang DW. Estimation of wave directional spreading in severe seas. In:
% Proceedings of the second international offshore and polar engineering
% conference. 1992. p. 146–53.
Lp=(9.81.*ntp)./(2*pi);
Sl=0.2.*((nhs./Lp).^(-1.28));
figure;plot3(nhs,ntp,Sl,'r*')
xlabel('Hs');ylabel('Tp');zlabel('Sl');grid on
title('Superficie de ajuste extrapolada usando SL - Wang 1992')

