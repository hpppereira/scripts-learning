%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PROGRAMA PAR ANÁLISE E PROCESSAMENTO
%DE DADOS DE ONDAS DA BÓIA WAVESCAN
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PARTE 1 - ENTRADA DE DATAS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
aa=exist('sss');
if aa==0,

disp('qual o dia de análise (string) DD/MM/AAAA');
dia=input('dia=');
end;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PARTE 2 - PREPARO DE VALORES E ARQUIVOS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load boia7.mat % arquivo com funcao de transferencia trans
               % ajustado para as frequencias df=1/128
load lyg2.mat  % tabela de exponenciais complexas
%load lyg3.mat
degrad=2*pi/360;

a=1:360;a=a*2*pi/360;a=a';
f=1/128:1/128:0.5;

%prepara arquivos
ondachhb=[];ondachh=[];ondadirpb=[];ondadirp=[];ondasprb=[];
ondaspr=[];ondadata=[];ondahora=[];ondaerros=[];ondaenc=[];
ondakl=[];ondakm=[];elevac=[];incE=[];incN=[];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PARTE 3 - VERIFICAÇÃO DE EXISTÊNCIA DE SÉRIES NO BD
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


seriedatahorawavescan(dia)
q1=ans;bD=q1(:,1:10);bH=q1(:,12:19);
gg2=length(bH(:,1));
for i=1:gg2,g1=isempty(str2num(bH(i,1:2)));
   if g1==1,bH(i,:)='00:00:00';
   end;
end

   
   for i=1:gg2,
      
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PARTE 4 - RECUPERAÇÃO DA TDB
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[gg2 i],
    
   sData=bD(i,:);
   sHora=bH(i,:);
   
A = seriesWavescanBrutoST( sData, sHora );
  
B = seriesWavescanProcST( sData, sHora );
 
 if length(B(:,1))>1,
   chhb=B(:,2);
   dirpb=B(:,3);
   sprb=B(:,4);
end;

if length(A)> 1, 
   
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
%PARTE 6 PROCESSAMENTO DOS DADOS
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

%dere=dere-mean(dere);dern=dern-mean(dern);
etaEW=dere;
etaNS=dern;

heave=heave-mean(heave);h=heave;
% Transforma o vetor coluna de 1024 elementos
% em uma matriz com 8 colunas de 128 linhas
% e calcula FFT de heave, etaEW e etaNS

h=reshape(h,128,8);   h1=fft(h);h1=h1(2:65,:);
r=reshape(dere,128,8);r1=fft(r);r1=r1(2:65,:);
p=reshape(dern,128,8);p1=fft(p);p1=p1(2:65,:);

% Calculo dos auto-espectros

trans1=transhm.*(cos(transhf)+j*sin(transhf));

beta=f/0.43;
q1=1-beta.^2;q2=2*beta*0.1;
transrm=1./sqrt(q1.^2+q2.^2);transrm=transrm';
trans2=(q1'+j*q2');
	
g1=zeros(64,8);g2=g1;
for i=1:8,g1(:,i)=trans1;g2(:,i)=trans2;end
h1=h1.*g1;
r1=r1.*g2;p1=p1.*g2;

chh=h1.*conj(h1);chh=2*mean(chh')/128;chh=chh';
crr=r1.*conj(r1);crr=2*mean(crr')/128;crr=crr';
cpp=p1.*conj(p1);cpp=2*mean(cpp')/128;cpp=cpp';

chh(1)=0.01;
chh(1:5)=0;
dirp(1:5)=0;
chhb=[chhb(2:64);0];chhb(1:5)=0;

dirpb=[dirpb(2:64);0];dirpb(1:5)=0;


% Calculo dos espectros cruzados
crp=real(r1.*conj(p1));crp=2*mean(crp')/128;crp=crp';
qrh=imag(r1.*conj(h1));qrh=2*mean(qrh')/128;qrh=qrh';
qph=imag(p1.*conj(h1));qph=2*mean(qph')/128;qph=qph';

crh=real(r1.*conj(h1));crh=2*mean(crh')/128;crh=crh';
cph=real(p1.*conj(h1));cph=2*mean(cph')/128;cph=cph';


   
z=crr+cpp;
zz=sqrt(chh.*(crr+cpp));

% Calculos dos coeficientes de Fourier para obtencao
% de D(theta), ou seja, a distribuicao de energia por
% direcao:     S(f,theta)=S(f)*D(f,theta) 
%
% Ref: Seatex, Wavescan Manual, pag. 17
% 
g1=find(zz==0);zz(g1)=1;
g1=find(z==0);z(g1)=1;

b1=qrh./zz;

a1=qph./zz;


a2=(cpp-crr)./z;
b2=2*cpr./z;

%
% Calculo da direcao dirp com apenas os dois
% coeficientes de Fourier a1 e b1. 
%
% Obs: Metodo do Kuik

dirp=angle(a1+j*b1);dirp=dirp*360/(2*pi);
dirp=dirp-23;
g1=find(dirp<0);dirp(g1)=dirp(g1)+360;
g1=find(dirp>360);dirp(g1)=dirp(g1)-360;
h2=dirp; for i=4:20,h2(i)=mean(dirp(i-2:i+2));end
dirp=h2;
dirpb=dirpb-23;
g1=find(dirpb<0);dirpb(g1)=dirpb(g1)+360;
g1=find(dirpb>360);dirpb(g1)=dirpb(g1)-360;



km=zeros(64,1);
%número de onda medido e calculado
kl=(2*pi.*f).^2/9.81;kl=kl';
g1=find(chh~=0);
km(g1)=sqrt((crr(g1)+cpp(g1))./chh(g1));


%cálculo do spread por Kuik


rr=sqrt(a1.^2+b1.^2);
spr1=sqrt(2-2*rr);
spr=spr1.^2+(1-0.996)*(2-spr1.^2);
spr=sqrt(spr);


%onda1f

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PARTE 7 SALVAR A TDC
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

B=[heave roll pitch comp ];
  
% Grava dados na tabela de erros
setWSBRutoCorrigidoST( sData, sHora,B);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PARTE 8 SALVAR A TDP
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



% Insere os dados de altura de onda na base de dados
%setWsProcAltura( sData, sHora, VH );

% Insere os dados de espectro na base de dados
%setWsProcEspectro( sData, sHora, VS, VD, VNUM, VEPK );

% Insere os dados gerais na base de dados
%setWsProcGeral(sData,sHora,VTZM,VTZD,VTZS,VAVH,SDVH,VZMX,VAVG,VMTA,VMTB,VMTC,VMTE,VTPK,VSPK,VPED);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PARTE 9 SALVAR DADOS EM .MAT PARA RELATÓRIO
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%salvar dados em arquivos .mat
elevac=[elevac heave];
incE=[incE dere];
incN=[incN dern];
ondachhb=[ondachhb chhb];
ondachh=[ondachh chh];
ondadirpb=[ondadirpb dirpb];
ondadirp=[ondadirp dirp];
ondasprb=[ondasprb sprb];
ondaspr=[ondaspr spr];
ondadata=[ondadata;sData];
ondahora=[ondahora;sHora];
ondaerros=[ondaerros;tabela5];
ondaenc=[ondaenc;tabela6];
ondakl=[ondakl kl];
ondakm=[ondakm km];

else;
   disp( 'Não há série temporal para a data/hora especificados' )
   
end;

end;
g1=size(ondadata);g1=g1(1);
if g1>0,


bD=ondadata(1,:);a1=bD(7:10);a2=bD(4:5);a3=bD(1:2);
a4=['onda' num2str(a1) num2str(a2) num2str(a3) '.mat'];
a5=['save ' a4 ' ondakl' ' ondakm' ' ondachhb'...
      ' ondachh' ' ondadata' ' ondahora'...
      ' ondadirpb' ' ondadirp' ' ondasprb'...
      ' ondaspr' ' ondaerros' ' ondaenc' ' elevac'...
      ' incE' ' incN'];
eval(a5);

end;


