%
% Ajuste de superficie em espaço multidimensional de grau n=2 
% Função polinomial
% Ricardo Martins Campos e José Antonio 25/10/2011
%
% O arquivo saidaOnda1h_BS_axys13e15_bs4_matlab.txt contem as saidas do
% programa onda1h para as boias axys13, 15 e wavescanBS4. Atencao pois
% existe aprox 2 graus de longitude de distancia entre as boias.
%
% sm=0.5*(0.0526.*exp(0.4.*tp)+6)+0.5*((0.08376.*(hs.^2.608))+6)
% s70=0.15*(hs^2.064)+0.1*(exp(tp*0.3049))+5
% s70=0.1*(hs^2.3)+0.02*(exp(tp*0.43))+5
% s70=0.2*(x^2)+0.05*(exp(y*0.34))+6

% s70=0.3*(x^2)+0.1*(exp(y*0.3))+6
% 35*tanh((6/15)*x-3)+35*tanh((6/24)*y-3)+a

%1*(x^b)+10*(tanh((10/21)*y-8))+e

clear all;close all

a=load('saidaOnda1h_BS_axys13e15.txt');

s=(a(:,68)+a(:,70))./2; 

vcar1=a(:,32);
int_vcar1=(0.5:1:7.5)';

vtpk1=a(:,33);
int_vtpk1=(4.5:1:16.5)';

vped1=a(:,36);

%s=s(vped1>100 & vped1<240);
%vcar1=vcar1(vped1>100 & vped1<240);
%vtpk1=vtpk1(vped1>100 & vped1<240);

% Selecionando os intervalos simultaneos de VCAR1, VTPK1 e S2_VTPK1
nx=length(int_vcar1);ny=length(int_vtpk1);
s2_media_vcar1_vtpk1=ones(nx,ny)*NaN;s2_mediana_vcar1_vtpk1=ones(nx,ny)*NaN;s2_per70_vcar1_vtpk1=ones(nx,ny)*NaN;
tam=ones(nx,ny)*NaN;
for jx=1:length(int_vcar1)
    for jy=1:length(int_vtpk1)
        k=find(vcar1 > int_vcar1(jx)-0.5 & vcar1 <= int_vcar1(jx)+0.5 & vtpk1 > int_vtpk1(jy)-0.5 & vtpk1 <= int_vtpk1(jy)+0.5 );
        if ~isempty(k)
            tam(jx,jy)=length(k);
            s2_media_vcar1_vtpk1(jx,jy)=mean(s(k));
            s2_mediana_vcar1_vtpk1(jx,jy)=median(s(k));
           % s2_per70_vcar1_vtpk1(jx,jy)=percentile(s(k),0.7);
        end
    end
end


tam

% Plotagem da superticie já selecionada em intervalos vcar vtpk.
[X,Y]=meshgrid(int_vcar1,int_vtpk1');
figure;plot3(X,Y,s2_media_vcar1_vtpk1','k*');xlabel('vcar1');ylabel('vtpk1');zlabel('Sm');grid on
% title('Selecao dos dados em intervalos VCAR1 e VTPK1')



sm= 0.5.*(0.01171.*(exp(-0.4206.*Y))+6) + 0.5.*(0.08376.*(X.^(2.608))+6);
hold on ;plot3(X,Y,sm,'r+');



% Ajuste literatura 
% Wang DW. Estimation of wave directional spreading in severe seas. In:
% Proceedings of the second international offshore and polar engineering
% conference. 1992. p. 146–53.
% Lp=(9.81.*ntp)./(2*pi);
%Sl=0.2.*((nhs./Lp).^(-1.28));
%figure;plot3(nhs,ntp,Sl,'r*')
%xlabel('Hs');ylabel('Tp');zlabel('Sl');grid on
%title('Superficie de ajuste extrapolada usando SL - Wang 1992')

