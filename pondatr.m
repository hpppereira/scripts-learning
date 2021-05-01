%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PROGRAMA PARA CONVERTER SÉRIES DE HEAVE
%ROLL E PITCH EM SÉRIES DE HEAVE, E DERIVADAS
%dereEW e dereNS e corrigir erros
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PARTE 1 - ENTRADA DE ARQUIVOS mensais
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

mes=8;
a1=[num2str(mes)];
if mes<10,a1=['0' a1];end;
for ii=1:26,
   a2=[num2str(ii)];
   if ii<10,a2=['0' a2];end
   for kk=0:23,
      
      a4=[a2 a1 num2str(kk)];
      a5=['ondadat' a4 '.mat'];
      exist(a5,'file');
   if ans==2,
      a7=['load '  a5 ];
      eval(a7)
   
[ii kk]
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PARTE 2 - PREPARO DE VALORES E ARQUIVOS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

degrad=2*pi/360;
a=1:360;a=a*2*pi/360;a=a';
      
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PARTE 4 - PREPARAR ARQUIVOS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

hprc=A;
heave=hprc(:,2)*2;
roll=hprc(:,3);
pitch=hprc(:,4);
comp=hprc(:,5);
        
   
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PARTE 5 - ANALISE DE QUALIDADE
%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

tabela5=zeros(4,3);
tabela6=zeros(4,3);
ee1=[-10;10;0.001;5];
ee2=[-30;30;0.001;5]; 
tabelaerr=[ee1 ee2 ee2];
matr=[heave roll pitch];

for i=1:3,
   
   vet=matr(:,i);

%análise de domínio;
g1=find(vet<tabelaerr(1,i));
tabela5(1,i)=length(g1);
if length(g1)>0,
   g0=[0;g1;1025];g2=diff(g0);
   g3=length(g1);
   for k=1:length(g1),
      if g2(k)>1,
         vet(g1(k))=(vet(g1(k)-1)+vet(g1(k)+1))/2;
         g3=g3-1;
      end;
      tabela6(1,i)=g3;
   end;
end;

g1=find(vet>tabelaerr(2,i));
tabela5(2,i)=length(g1);
if length(g1)>0,
   g0=[0;g1;1025];g2=diff(g0);
   g3=length(g1);
   for k=1:length(g1),
      if g2(k)>1,
         vet(g1(k))=(vet(g1(k)-1)+vet(g1(k)+1))/2;
         g3=g3-1;
      end;
      tabela6(2,i)=g3;
   end;
end;

%valores sucessivos
g=reshape(vet,16,length(vet)/16);
g2=std(g);g1=find(g2<tabelaerr(3,i));
if length(g1)>0,tabela5(3,i)=length(g1)*16;
tabela6(3,i)=length(g1)*16;   
end;

%análise de spikes
%a análise de spikes em séries temporais será feita
%pelo cálculo do desvio padrão de um conjunto de valores


g=reshape(vet,4,(length(vet)/4));
g2=std(g);g1=find(g2>tabelaerr(4,i)*mean(g2));
if 	length(g1)>0,
   tabela5(4,i)=length(g1);
   tabela6(4,i)=length(g1);
   for k=1:length(g1),
      z1=(g1(k)-1)*4+1;
      z2=vet(z1:z1+3);
      z3=max(z2);z4=find(z2==z3);
      z5=z1-1+z4;
      z10=z5-1;z11=z5+1;
      if z5==1,z10=2;
      end;
      if z5==1024,z11=1023;
      end;
      vet(z5)=(vet(z10)+vet(z11))/2;
      tabela6(4,i)=tabela6(4,i)-1;
   end;
  end;
matr(:,i)=vet;  
  
end;
heave=matr(:,1);
roll=matr(:,2);
pitch=matr(:,3);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PARTE 6 TRANSFORMAÇÃO DAS SÉRIES
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Rotina para transformar 4 series temporais 
% (heave,roll,pitch,compass) em (heave,etaEW,etaNS)
% Importante: heave = metros
%             roll  = graus
%             pitch = graus
%             compass = graus (relativo ao Norte Magnetico)
%
%             heave = metros
%             etaEW = derivada ou "slope" na direcao Leste_Oeste
%             etaNS = derivada ou "slope" na direcao Norte_Sul
%
%             
dere=zeros(1024,1);
dern=dere;tpitch=dere;
troll=dere;


rrad=degrad*roll;
prad=degrad*pitch;
crad=degrad*comp;

%filtro moving average de 3 pontos para compass
g1=[];
g2=[crad(1:3);crad;crad(1022:1024)];
for i=3:1026,g1=[g1;mean(g2(i-2:i+2))];
end;
crad=g1;


sroll=sin(rrad);
croll=cos(rrad);

spitch=-sin(prad);
cpitch=cos(prad);

scomp=sin(crad);
ccomp=cos(crad);

g1=find(cpitch~=0);
tpitch(g1)=spitch(g1)./cpitch(g1);

g1=find(cpitch==0);

if length(g1)>0,
tpicth(g1)=spitch(g1)*1e+20;
end;
tp=tpitch;

g1=find(croll~=0);
troll(g1)=sroll(g1)./croll(g1);
g1=find(croll==0);

if length(g1)>0,
troll(g1)=sroll*1e+20;
end;
tr=troll;

a=-tpitch.*sroll;
v=croll.^2 - a.^2;

g1=find(v>=0);
b=sqrt(v(g1));
c=sroll(g1);
aa=-b.*spitch(g1);
bb=a(g1).*spitch(g1)-c.*cpitch(g1);
cc=b.*cpitch(g1);

g2=find(cc>0);
dere(g1(g2))=-(aa(g2).*scomp(g1(g2))-bb(g2).*ccomp(g1(g2)))./cc(g2);
dern(g1(g2))=-(aa(g2).*ccomp(g1(g2))+bb(g2).*scomp(g1(g2)))./cc(g2);



A=[heave dere dern]; 

erros=[];
b1=num2str(kk);
if kk<10,b1=['0' b1];end
b2=[a2 a1 b1];
a8=['save ' 'ondatr' b2 '.mat ' 'A'];
eval(a8);
if sum(sum(tabela5))>0,
   erros=[erros tabela5 tabela6];
   a9=['save ' 'erros' a4 '.mat ' 'erros'];
   eval(a9);	
end;

end;
end;
end;