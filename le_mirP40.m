function [sdata,shora,VF,VS,f,theta,esp_dir,VMTA,VAVH,VTPK1,VSPK1,VPED1,VEPK1,VTPK2,VSPK2, ...
          VPED2,VEPK2,VMED,VTZA,VTZS,VTZM,VZMX,HCSP,HCDT,vel_corr,continua1] = le_mirP40(arqdwv,fid3)
% OBS:USAR PARA LER ARQUIVOS  DA P-40 (Sem cabecalho de hora PETRONAV)    %% Alterado por Dante 21/10/02
%
% Parametros que faltam:
% VSO,VTPK,kVTPK,VSPK,VMTB,VMTC,VMTD,VMTE,NDT,noverlap,w,VD,VPED,VNUM,VESP,VEPK,
% Spico,fSpico,dSpico,Scava,fScava,dScava,alfa,gama,VMTA1,VMTB1,VMTC1,VMTD1,VMTE1,VCAR1,
% VMTA2,VMTB2,VMTC2,VMTD2,VMTE2,VCAR2,VMTA3,VMTB3,VMTC3,VMTD3,VMTE3,VCAR3,VTPK3,VSPK3,VEPK3,VPED3
% 
% Funcao para leitura dos parametros de ondas e correntes,
% e espectros de ondas dos arquivos *.sad
%
% *** MUITO IMPORTANTE : ******************************************************
%    	O SOFTWARE ORIGINAL DA MIROS FORNECE O RUMO DA ONDA, OU SEJA,
%     A DIRECAO PARA ONDE O TREM DE ONDAS ENCONTRA-SE INDO. DESTE
%     MODO, TORNOU-SE NECESSARIO PROCEDER UMA ROTACAO DE 180 GRAUS
%     EM TODAS AS DIRECOES ABSOLUTAS FORNECIDAS NOS ARQUIVOS "*.sad"
%     DE FORMA A FORNECER AS DIRECOES DE ONDA CONFORME PADROES 
%     INTERNACIONAIS (DIRECAO DE ONDE A ONDA VEM)
%
%     Arquivo *.sad    ==> Funcao le_mirP40 ==>  Dados de saida
%   (Direcao para onde      Rotacao          ( Direcao de onde
%      a onda vai )                             a onda vem )
% *****************************************************************************
%
% Ler os parametros:
% parametro 6 = Momento espectral de Ordem 0 (VMTA)
%           7 = Altura Significativa (VAVH)
%           8 = Periodo de Pico 1 (VTPK1)
%           9 = Ordenada do Pico 1 (VSPK1)
%          10 = Direcao de Pico 1 (VPED1)
%          11 = Direcao Media do Espectro do Pico 1 (nao tem na base)
%          12 = Spread direcional do Pico 1 (VEPK1) 
%          13 = Altura de Onda do Pico 2
%          14 = Periodo de Pico 2 (VTPK2)
%          15 = Ordenada do Pico 2 (VSPK2)
%          16 = Direcao de Pico 2 (VPED2)
%          17 = Direcao Media do Espectro do Pico 2 (nao tem na base)
%          18 = Spread direcional do Pico2 (VEPK2)
%          19 = Distribuição Direcional do Pico (????)
%          20 = Direcao Media de Propagação(VMED)
%          21 = Spread Direcional Total (nao tem na base)
%          22 = Periodo Medio de Zero Ascendente (VTZA só que no domínio da frequência)  
%          23 = Periodo Medio (nao tem na base)
%          24 = Velocidade da Corrente de Superficie(HCSP)
%          25 = Direcao da Corrente de Superficie(HCDT)
%          26 = Componente E-W magnetica da Corrente de Superficie( )
%          27 = Componente N-S magnetica da Corrente de Superficie( )
%          28 = Desvio entre Corrente Medida e Estimada (???- nao tem na base)
%          29 = Altura Maxima de Onda (HMax)
%          30 = Periodo Significativo (VTZS) 
%          31 = Periodo de Onda Maxima (VTZM)
%          32 = Periodo de Onda Maxima de VAVH  
%          33 = Altura Maxima de zero ascendente(VZMX)
%
% parametro  98-138 Espectro do setor 1
%           139-179 Espectro do setor 2
%           180-220 Espectro do setor 3
%           221-261 Espectro do setor 4
%           262-302 Espectro do setor 5
%           303-343 Espectro do setor 6
%
% Parametro 344-349 Correntes Superficiais por setor
%
% J.A. Lima 09/09/2002
%
% Leitura do arquivo 'arqdwv' com parametros
string1=fscanf(fid3,'%s',1);
continua1=1;

% Inicializando variaveis para exportacao da rotina
%VF=[];VS=[];f=[];theta=[];esp_dir=[];VMTA=[];VAVH=[];VTPK1=[];VSPK1=[];VPED1=[];
%VEPK1=[];VTPK2=[];VSPK2=[];VPED2=[];VEPK2=[];VMED=[];VTZA=[];VTZS=[];VTZM=[];VZMX=[];
%HCSP=[];,HCDT=[];vel_corr=[];sdata=[];shora=[];

% Imprime arquivo de dados que serah lido
arqdwv;

while (continua1)
   if feof(fid3)==1
      VF=[];VS=[];f=[];theta=[];esp_dir=[];
      VMTA=[];VAVH=[];VTPK1=[];VSPK1=[];VPED1=[];
      VEPK1=[];VTPK2=[];VSPK2=[];VPED2=[];VEPK2=[];
      VMED=[];VTZA=[];VTZS=[];VTZM=[];VZMX=[];
      sdata=[];shora=[];HCSP=[];,HCDT=[];vel_corr=[];
%      fclose(fid3); %Alterado por João Marcos 04/09/2002 12:31 h
	   return
   end
       
   if length(string1) == 10
      % Teste para identificar posicao de inicio da serie usando a data com 10 posicoes
      if (string1(3) == '-') 
         sdata=string1;
         sdata(3)='/';sdata(6)='/';
         % pause
         continua1=0;
      else
         string1=fscanf(fid3,'%s',1);
      end
   else
      string1=fscanf(fid3,'%s',1);
   end
   
end

% Le o string com hora. Caso nao seja hora, cancela leitura.
string1=fscanf(fid3,'%s',1);
if string1(3) == ':'
   shora=string1(1:5);
else
   VF=[];VS=[];f=[];theta=[];esp_dir=[];VMTA=[];VAVH=[];VTPK1=[];VSPK1=[];VPED1=[];
   VEPK1=[];VTPK2=[];VSPK2=[];VPED2=[];VEPK2=[];VMED=[];VTZA=[];VTZS=[];VTZM=[];VZMX=[];
   HCSP=[];,HCDT=[];vel_corr=[];
   continua1=1;
   % fclose(fid3);  % Alterado por Jose Antonio 10/09/2002
   return
end

% Inicializacao do vetor de parametros
parametro=zeros(349,1);
% Lendo parametros do arquivo 'arqsad'
for k=6:349
   parametro(k)=str2num(fscanf(fid3,'%s',1));
end
%
% Teste de consistencia para verificar se parametros estao corretos
if parametro(7) < 0.1 | parametro(7) > 8.0 % Teste no range de HS
   VF=[];VS=[];f=[];theta=[];esp_dir=[];VMTA=[];VAVH=[];VTPK1=[];VSPK1=[];VPED1=[];
   VEPK1=[];VTPK2=[];VSPK2=[];VPED2=[];VEPK2=[];VMED=[];VTZA=[];VTZS=[];VTZM=[];VZMX=[];
   HCSP=[];,HCDT=[];vel_corr=[];
   continua1=1;   
   % fclose(fid3);  % Alterado por Jose Antonio 10/09/2002
   return
end

% Caso existam apenas algumas correcoes -999.99
k=find(parametro == -999.99);parametro(k)=0.;
% Teste de consistencia para verificar se todos os parametros sao -999.99
if length(k) == 344
   VF=[];VS=[];f=[];theta=[];esp_dir=[];VMTA=[];VAVH=[];VTPK1=[];VSPK1=[];VPED1=[];
   VEPK1=[];VTPK2=[];VSPK2=[];VPED2=[];VEPK2=[];VMED=[];VTZA=[];VTZS=[];VTZM=[];VZMX=[];
   HCSP=[];,HCDT=[];vel_corr=[];
   continua1=1;   
   % fclose(fid3);  % Alterado por Jose Antonio 10/09/2002
   return
end

%
% Lendo Parametros de Dados do Radar
%
VMTA=parametro(6);
VAVH=parametro(7);
VTPK1=parametro(8);
VSPK1=parametro(9);
VPED1=parametro(10)+180.; % Rotacionando para direcao de onde vem
if VPED1 > 360.;VPED1=VPED1-360.;end;
%Direcao Media do Espectro do Pico 1(nao tem na base)=parametro(11); 
VEPK1=parametro(12);
%Altura de Onda do Pico 2=parametro(13);
VTPK2=parametro(14);
VSPK2=parametro(15);
VPED2=parametro(16)+180.; % Rotacionando para direcao de onde vem
if VPED2 > 360.;VPED2=VPED2-360.;end
%Direcao Media do Espectro do Pico 2=parametro(17);
VEPK2=parametro(18);
%Distribuição Direcional do Pico (????)=parametro(19);
VMED=parametro(20);
%Spread Direcional Total (nao tem na base)=parametro(21);
%Periodo Medio de Zero Ascendente (VTZA)=parametro(22);
VTZA=parametro(22);
%Periodo Medio (nao tem na base)=parametro(23);
HCSP=parametro(24);
HCDT=parametro(25);
%Componente E-W magnetica da Corrente de Superficie=parametro(26);
%Componente N-S magnetica da Corrente de Superficie=parametro(27);
%Desvio entre Corrente Medida e Estimada(nao tem na base)=parametro(28);
%Altura Maxima de Onda (HMax)=parametro(29);
VTZS=parametro(30);
VTZM=parametro(31); 
%Periodo de Onda Maxima de VAVH=parametro(32);
VZMX=parametro(33);
%
% A leitura dos parametros heave, pitch e roll nao esta sendo feita.
% O calculo dos demais e feito a partir destes parametros. Verificar como sera feito
% isso!
%
% Lendo Parametros do Espectro de Onda
% Capturando vetores com espectro de onda por setor
% VALIDO APENAS PARA A P-40, POR CAUSA DOS ZEROS NAS 4 PRIMEIRAS FREQUENCIAS
esp_setor1=[0 0 0 0 parametro(98:134)']';
esp_setor2=[0 0 0 0 parametro(139:175)']';
esp_setor3=[0 0 0 0 parametro(180:216)']';
esp_setor4=[0 0 0 0 parametro(221:257)']';
esp_setor5=[0 0 0 0 parametro(262:298)']';
esp_setor6=[0 0 0 0 parametro(303:339)']';

% Função de Transferência 'hf' proposta pela MIROS
% para eliminar energia nas componentes de baixa
% frequencia. Toda energia espectral inferior a
% 0.0391 Hz (periodos maiores que 25.57 seg) é
% reduzida exponencialmente para zero.
hf=[(exp([1 2 3 4 5 6 7.5])/exp(7.5))';ones(34,1)];
esp_setor1=esp_setor1.*hf;esp_setor2=esp_setor2.*hf;
esp_setor3=esp_setor3.*hf;esp_setor4=esp_setor4.*hf;
esp_setor5=esp_setor5.*hf;esp_setor6=esp_setor6.*hf;
%
% Montagem de um vetor de frequencias com 41 bandas,
% conforme indicado pelo Manual do Miros
VF=(0:1/128:0.3125);VF=VF';
% 
% Montagem do espectro nao-direcional
VS=abs(esp_setor1)+abs(esp_setor2)+ ...
   abs(esp_setor3)+abs(esp_setor4)+ ...
   abs(esp_setor5)+abs(esp_setor6);
%
% Montagem de um meshgrid frequencia-direcao
[f,theta]=meshgrid(0:1/128:0.3125,9:30:339);
%
%
% Convencao de montagem do MIROS na P-40: %%% Alterado por Dante 21/10/02
%
% Montagem da matriz com espectro direcional,
% considerando que o setor 1 tem direcao 249, e
% os outros setores giram no sentido horario
% defasados de 30 graus:
% setor 1=249 graus, setor 2=279 graus, 
% setor 3=309 graus, setor 4=339 graus
% setor 5=09 graus, setor 6=39 graus
% 
% A matriz possui direcoes como linhas e
% frequencias como colunas
esp_dir=zeros(12,41);
% ********************************************
% IMPORTANTE:
% A MATRIZ esp_dir JÁ SERA' MONTADA PELA
% CONVENCAO USUAL: DIRECAO DE ONDE A ONDA VEM.
% ELA CRESCE MONOTONICAMENTE EM INCREMENTOS DE
% 30 GRAUS:
%           LINHA  1 =  09 graus
%           LINHA  2 =  39 graus
%           LINHA  3 =  69 graus
%           LINHA  4 =  99 graus
%           LINHA  5 = 129 graus
%           LINHA  6 = 159 graus
%           LINHA  7 = 189 graus
%           LINHA  8 = 219 graus
%           LINHA  9 = 249 graus
%           LINHA 10 = 279 graus
%           LINHA 11 = 309 graus
%           LINHA 12 = 339 graus
%
% * a linha 1 deve ser aquela que parte da janela mais proxima do norte verdadeiro. % Dante 24/10/02
%
% ********************************************
% Preenchendo linha 5: 129 graus
k=find(esp_setor3 > 0);
esp_dir(5,k)=esp_setor3(k)';
% Preenchendo linha 11: 309 graus
k=find(esp_setor3 < 0);
esp_dir(11,k)=abs(esp_setor3(k))';
% Preenchendo linha 6: 159 graus
k=find(esp_setor4 > 0);
esp_dir(6,k)=esp_setor4(k)';
% Preenchendo linha 12: 339 graus
k=find(esp_setor4 < 0);
esp_dir(12,k)=abs(esp_setor4(k))';
% Preenchendo linha 7: 189 graus
k=find(esp_setor5 > 0);
esp_dir(7,k)=esp_setor5(k)';
% Preenchendo linha 1: 09 graus
k=find(esp_setor5 < 0);
esp_dir(1,k)=abs(esp_setor5(k))';
% Preenchendo linha 8: 219 graus
k=find(esp_setor6 > 0);
esp_dir(8,k)=esp_setor6(k)';
% Preenchendo linha 2:  39 graus
k=find(esp_setor6 < 0);
esp_dir(2,k)=abs(esp_setor6(k))';
% Preenchendo linha 9 : 249 graus
k=find(esp_setor1 < 0);
esp_dir(9,k)=abs(esp_setor1(k))';
% Preenchendo linha 3: 69 graus
k=find(esp_setor1 > 0);
esp_dir(3,k)=esp_setor1(k)';
% Preenchendo linha 10: 279 graus
k=find(esp_setor2 < 0);
esp_dir(10,k)=abs(esp_setor2(k))';
% Preenchendo linha 4:  99 graus
k=find(esp_setor2 > 0);
esp_dir(4,k)=esp_setor2(k)';
%
% Montando vetores e matriz com 513 pontos de frequencia 
VF513=(0:1/1024:0.5);VF513=VF513';
espdir_513=zeros(12,513);
for fk=1:12
   espdir_513(fk,1:321)=interp1(VF,esp_dir(fk,:)',VF513(1:321),'linear')';
end
VS513=sum(espdir_513(1:12,:))';
%
% Atualizar matriz esp_dir e vetores VF, VS com 513 pontos de frequencia
VF=VF513; VS=VS513; esp_dir=espdir_513;
clear VF513; clear VS513; clear espdir_513;

% Plotando espectro unidirecional
%figure(1);clf
%plot(VF,VS);hold on
%
% Plotando espectro direcional
%figure(2);clf
%surf(f,theta,esp_dir);colormap(jet);

%figure(3);clf
%surfl(f,theta,esp_dir);                             
%shading interp;                
%colormap(pink);

% Montando vetor de correntes com a mesma
% convencao do vetor de ondas.
% Exemplo: como na P-40 o setor 1 estava voltado para 249 graus,
%          se parametro(344) > 0 entao a corrente estara indo para 249,
%          se parametro(344) < 0 entao a corrente estara indo para 69 (=249-180)
vel_corr=zeros(12,1);
%
% Preenchendo linha 3 (69 graus) e linha 9 (249 graus)
if parametro(344) >= 0
  vel_corr(3)=0;vel_corr(9)=parametro(344);
else
  vel_corr(9)=0;vel_corr(3)=-parametro(344);
end
% Preenchendo linha 4 (99 graus) e linha 10 (279 graus)
if parametro(345) >= 0
  vel_corr(4)=0;vel_corr(10)=parametro(345);
else
  vel_corr(10)=0;vel_corr(4)=-parametro(345);
end
% Preenchendo linha 5 (129 graus) e linha 11 (309 graus)
if parametro(346) >= 0
  vel_corr(5)=0;vel_corr(11)=parametro(346);
else
  vel_corr(11)=0;vel_corr(5)=-parametro(346);
end
% Preenchendo linha 6 (159 graus) e linha 12 (339 graus)
if parametro(347) >= 0
  vel_corr(6)=0;vel_corr(12)=parametro(347);
else
  vel_corr(12)=0;vel_corr(6)=-parametro(347);
end
% Preenchendo linha 7 (189 graus) e linha 1 (09 graus)
if parametro(348) >= 0
  vel_corr(7)=0;vel_corr(1)=parametro(348);
else
  vel_corr(1)=0;vel_corr(7)=-parametro(348);
end
% Preenchendo linha 8 (219 graus) e linha 2 (39 graus)
if parametro(349) >= 0
  vel_corr(8)=0;vel_corr(2)=parametro(349);
else
  vel_corr(2)=0;vel_corr(8)=-parametro(349);
end

clear string1;clear k;

return