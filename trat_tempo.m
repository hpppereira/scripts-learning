function[VH,VHC,VT,SDVH,VAVG,VAVH,VTZD,VTZM,VTZS,VZMX] = trat_tempo(heave,DT)
%
% Funcao para geracao de parametros no dominio do tempo
% a partir das series temporais de heave 
%
% C.I. Fisch / J.A. LIma 21/07/99
%
% +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
%                    Análise no Dominio do Tempo
%
% Identificacao de zeros do registro
a1=sign(heave);a2=diff(a1);
%a3=ordem do valor anterior a um cruz. de zeros descendente
%a4=ordem do valor anterior a um cruz. de zeros ascendente
a3=find(a2==-2);a4=find(a2==2);
%a5=ordem dos mínimos;%a6=ordem dos máximos;
a1=diff(heave);a1=sign(a1);a1=diff(a1);a1=[0;a1];
a5=find(a1==2);a6=find(a1==-2);
%a7=máximos positivos
a8=find(heave(a6)>0);a9=a6(a8);a7=heave(a6(a8));
%a10 - para plotagem dos máximos positivos
a10=zeros(length(heave),1);a10(a9)=heave(a9);

%cálculo do número de ondas (alturas de ondas de zero descendente);
VH=[];h5=[];VT=[];
for i=1:max(size(a3))-1,
   g=[a3(i)+1:a3(i+1)];
   g2=max(heave(g));g3=min(heave(g));
   tdz1=interp1([heave(a3(i)) heave(a3(i)+1)],[DT*a3(i) DT*(a3(i)+1)],[0]);
   tdz2=interp1([heave(a3(i+1)) heave(a3(i+1)+1)],[DT*a3(i+1) DT*(a3(i+1)+1)],[0]);
   VT(i)=tdz2-tdz1;
   h5=[h5;a3(i)+find(heave(g)==max(heave(g)))];
   VH(i)=g2-g3;
   VHC(i)=g2;
end;
VH=VH';VT=VT';VHC=VHC';
g1=find(VH==max(VH));g1=g1(1);
VTZM=VT(g1);   % Periodo associado a Altura Maxima VZMX
VTZD=mean(VT); % Periodo medio de zero descendente

% TESTAR COM O PARENTE:
%aq1=abs(heave(a4));
%aq2=aq1./(aq1+heave(a4+1));
%peras=diff(a4+aq2);
%aq1=heave(a3);aq2=aq1+abs(heave(a3+1));
%aq2=aq2./aq1;
%perds=diff(a3+aq2);
%perma=mean(peras);permd=mean(perds);
%perm1=2*pi*VMTA/VMTB;
%return


%Nc= número de cristas
%Nc=max(size(h1));
%Tc=1/Nc;

[h1 h2]=sort(VH);

h4=round(length(VH)/3);
h1=flipud(h1);h1=h1(1:h4);
h2=flipud(h2);h2=h2(1:h4);

VTZS=mean(VT(h2)); % Periodo Significativo de zero descendentes

VAVH=mean(VH(h2));%altura significativa no tempo
SDVH=std(VH);%desvio padrão das alturas de zero descendente
VZMX=max(VH);%onda máxima no período.
VAVG=mean(VH);%onda média no período

% Listando parametros no dominio do tempo para o SIMO
Altura_Significativa_VAVH=VAVH;
%Altura_Media_VAVG=VAVG
%Altura_Maxima_CavaCrista_VZMX=VZMX
%Periodo_Significativo_VTZS=VTZS
%Periodo_Medio_Zero_Descend_VTZD=VTZD
%Periodo_da_Altura_Maxima_VTZM=VTZM

% ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++