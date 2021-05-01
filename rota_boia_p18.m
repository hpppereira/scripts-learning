function [etaEW,etaNS] = rota_boia_p18(roll,pitch,compas)
% Rotina para rotacao das series temporais de um referencial
% fixo na boia oceanografica (x,y,z) para um referencial
% associado ao Norte Magnetico.
%
% Elaborado: Jose A. Lima 15/07/99 a partir do Mfile wave1
%            do Prof. Carlos E. Parente Ribeiro
%
% Baseado na: Subroutine Rotate (em Fortran), fornecida por
%             J.Mathisen da Oceanor para a boia Seatex
%
% Esta rotina transforma 3 series temporais (roll,pitch,compass) em 
% (etaEW,etaNS)
% Importante: roll  = inclinacao ou slope EW em graus
%             pitch = inclinacao ou slope NS em graus
%             compass = graus (relativo ao Norte Magnetico)
%
%             heave = metros
%             etaEW = deslocamento na direcao Leste_Oeste (em m)
%             etaNS = deslocamento na direcao Norte_Sul (em m)
%
%             
degrad=2*pi/360;

dere=zeros(length(roll),1);
dern=dere;tpitch=dere;

rrad=degrad*roll;
prad=degrad*pitch;
crad=degrad*compas;

rrad=rrad-mean(rrad);
prad=prad-mean(prad);

% Parente faz uma media movel de tres pontos na serie compas
g1=[];
g2=[crad(1);crad;crad(end)];
for i=2:length(roll)+1,g1=[g1;mean(g2(i-1:i+1))];
end;
crad=g1;

sroll=sin(rrad);
croll=cos(rrad);
spitch=sin(prad); % Cuidado com o referencial aqui !!!!
cpitch=cos(prad);
scomp=sin(crad);
ccomp=cos(crad);

g1=find(cpitch~=0);
tpitch(g1)=spitch(g1)./cpitch(g1);
g1=find(cpitch==0);
tpicth(g1)=spitch(g1)*1e+20;

a=-tpitch.*sroll;
v=croll.^2 - a.^2;

g1=find(v>=0);
b=sqrt(v(g1));
c=sroll(g1);
aa=-b.*spitch(g1);
bb=a(g1).*spitch(g1)-c.*cpitch(g1);
cc=b.*cpitch(g1);

g2=find(cc~=0);
dere(g1(g2))=-(aa(g2).*scomp(g1(g2))-bb(g2).*ccomp(g1(g2)))./cc(g2); 
% A proxima linha foi corrigida pelo Prof. Parente em 30/07/99
dern(g1(g2))=-(aa(g2).*ccomp(g1(g2))+bb(g2).*scomp(g1(g2)))./cc(g2);
dere=dere-mean(dere);dern=dern-mean(dern);

% Atribuindo valores para vetores com derivadas ou "slopes" 
etaEW=dere;
etaNS=dern;
