% Onda1g.m - Programa Onda1 - Versao G
%
% ######################################################################
%   Programa Especifico para Processamento de Dados de Onda Direcionais  
%     ou não direcionais conforme definido no parâmetro pdir
% 
% ######################################################################
%
% Mfile elaborado pelo Prof. Carlos E. Parente para processamento
% no dominio do tempo e da frequencia de series temporais de 
% registros de mar. Adaptado posteriormente por Jose Antonio M. Lima
% para particularizar as analises no dominio do tempo e da frequencia
% com metodologia padronizada do SIMO.
%
% Autores: C.E. Parente (COPPE/UFRJ)- 30/03/99
%          J.A. Lima    (PETROBRAS/CENPES)
% Adaptado com a ajuda de: C.I. Fisch 
% +++++++++++++++++++++++++++++++++++++
% Alteracoes introduzidas na versao C:    J.A. Lima 20/04/99
%   - Inclusao do teste de direcao para baixas frequencias no
%     3o. criterio de selecao de picos
%   - Salvando direcoes associadas a ondas induividuais
%   - Incluido opcoes para diversos tipos de entrada:
%      opt=1 heave,etaEW,etaNS (formato de Marlim)   
%      opt=2 heave,etaNS,etaEW  (formato de Barracuda)
%      opt=3 heave,roll,pitch,compass (formato da P-18 Seatex)
%   - Funcao com rotacao de (x,y,z) da boia para Norte Magnetico
%   - Lendo funcao de transferencia de heave da boia Seatex
% ++++++++++++++++++++++++++++++++++++
% Alteracoes introduzidas na versao D:   J.A. Lima/ C.I. Fisch 16/07/99
%   - Leitura de nome do arquivo com listas de todos arquivos *.dwv
%   - Leitura de cada um dos arquivos *.dwv para identificacao
%     das series temporais de heave, roll, pitch e compass
%   - Processamento das series temporais dos arquivos *.dwv
%   - Armazenamento dos parametros gerados para o SIMO em apenas
%     um arquivo (que possua os parametros de cada uma das series *.dwv)
% ++++++++++++++++++++++++++++++++++++
% Alteracoes introduzidas na versao E:   C.I. Fisch/ J.A. Lima 21/07/99
%   - Modularizacao do programa em blocos para leitura de dados (le_series),
%     calculo de parametros no dominio do tempo (trat_tempo), da frequencia
%     (trat_freq), direcionais (trat_dir), selecao de picos (sele_pico),
%     calculo dos momentos espectrais (momentos), montagem do vetor com direcao
%     das ondas individuais e direcao de onda maxima (vetor_dir) e impressao
%     de resultados (carrega_simo).
% ++++++++++++++++++++++++++++++++++++++
% Alteracoes introduzidas na versao F:   J.A. Lima/ C.I. Fisch  12/08/99
%   - Adaptacao do codigo para processar dados direcionais ou nao-
%     direcionais de ondas (variavel pdir) e qual a boia utilizada
%     (dboia), inclusao das rotinas le_pearl (ler dados de ondas
%     do Pearl Marine) e corrseries (aplica funcao de transferencia
%     nos dados da P-18). Inclusao de 4o. criterio na sele_pico.m
%   - Adaptacao da rotina de leitura dos dados da boia de Marlim e Barracuda
%     (le_consub)      Caroline 20/08/99
%   - Foi desativada a rotina "le_ney.m", pois os dados de series temporais
%     de Marlim e Barracuda serão lidos diretamente dos dados nbrutos da CONSUB
% ++++++++++++++++++++++++++++++++++++++
% Alteracoes introduzidas na versao G:   Eric / J.A. Lima 12/08/2004
%   - Foi montada rotina "le_Waverider.m" para ler os arquivos "mmddhhmi.raw" com as
%     series brutas geradas pelo ondografo Datawell Waverider MK-II. Esta
%     rotina remove tambem os spikes das series temporais.
%   - Foi criada a opçao dboia=2 no "onda1g.m" para boia Waverider
%   - Foi alterada a rotina "trat_dir.m" como forma de incluir a opçao de
%     calculo da direçao para a boia Waverider: r1=pi/2 + amgle(r1)
%  - Inclusao na rotina "trat_dir.m" do calculo do Spreading por:
%        Krogstad, H.E. et al, 1998, Directional Distributions in Wave
%        Spectrum, Proc. WAVES97, Nov. 3-7 1997, 1, ASCE, 883-895.
%
% OBS: O SIMO usa nomenclatura para parametros de ondas conforme
%      UNESCO/GF3
%
% Series temporais de Entrada:
%  heave é uma série de 1024 pontos de elevação
%  etaEW é uma série de 1024 pontos de inclinação leste
%  etaNS é uma série de 1024 pontos de inclinação norte
%
% Pela convencao do SIMO:
%  heave=VWSE
%  etaEW=ROLL (PITCH LESTE-OESTE do SIMO))
%  etaNS=PITCH (PITCH NORTE-SUL do SIMO)
%  DONV = declinacao magnetica:
%    Positiva para declinacoes Leste (E)
%    Negativa para declinacoes Oeste (W)
clear;
% Identificacao do arquivo que possue a lista dos arquivos *.txt
[arqdad,pafdad]=uigetfile('*.txt','Entre com nome do arquivo com lista dos arquivos');
if ~isstr(arqdad); return; end;
fid1=fopen([pafdad,arqdad],'r');

% Identificacao do arquivo de saida com parametros para SIMO
[arqsai,pafsai]=uiputfile([pafdad,'*.out'],'Entre com nome do arquivo de saida com parametros para SIMO');
if ~isstr(arqsai); return; end;
fid2=fopen([pafsai,arqsai],'a');

prompt={'Os dados são direcionais (entre com o valor 1) ou não-direcionais (entre com o valor 0):',...
        'Boia Triaxys (digite 4), Boia do Merenda no ES (digite 3), Waverider (digite 2),da P-18 (digite 1) ou a do SEGEN/CONSUB (digite 0), deixe em branco caso seja nao-direcional:',...
        'O fundo de escala de heave eh 20 m (digite 1) ou 10 m (digite 0) (Deixe em branco caso nao seja P-18):',...
        'Entre com a taxa de amostragem (em segundos) das series temporais (Ex. Waverider: 0.7818 s):',...
        'Entre com a latitude da coleta (em graus decimais, negativo para Hemisferio Sul):',...
        'Entre com a longitude da coleta (em graus decimais, negativo para Hemisferio Oeste):',...
        'Qual o ano dos dados? ',...
        'O dado eh da plataforma Pat-3 (0) ou Pearl Marine(1)?(Deixe em branco caso nao seja nenhuma das duas.)',...
        'Numero de graus de liberdade para a analise espectral.',...
        'Declinaçao Magnetica:(Oeste = Negativo, Leste = Positivo)'};
%def={'1',' ',' ',     ' ',       ' ',       ' ',   ' ',' ',  ' '}; %Padroes para qualquer dado de boia.
def={'1','4',' ','0.78','-19.9514','-39.5388','2006',' ','32','-23'}; %Padroes para a boia Waverider de PECEM.
dlgTitle=['Paramentros para Analise Espectral do arquivo ', pafdad,arqdad];
lineNo=1;
answer=inputdlg(prompt,dlgTitle,lineNo,def);

% Parâmetro para identificar se os dados são direcionais ou não direcionais 
%     pdir=0: variavel logica booleana que indica falso (representa ondas nao-direcionais)
%     pdir=1: variavel logica booleana que indica verdadeiro (representa ondas direcionais)
pdir =str2num(char(answer(1)));

% Tipo de boia utilizado na mediçao.
dboia=str2num(char(answer(2)));

% Seleciona o fundo de escala de heave da boia da P-18.
fundh=str2num(char(answer(3)));

% Taxa de amostragem (no tempo) das medicoes.
DT=str2num(char(answer(4)));

% Latitude (em graus decimais, negativo para Hemisferio Sul).
Lat=str2num(char(answer(5)));

% Longitude (em graus decimais, negativo para Hemisferio Oeste).
Lon=str2num(char(answer(6)));

% Ano da Mediçao.
qualano =str2num(char(answer(7)));

% Pat-3 ou Pearl Marine.
t=str2num(char(answer(8)));

% Numero de graus de liberdade
mgl=str2num(char(answer(9)));

% Declinaçao Magnetica
DONV=str2num(char(answer(10)));

% Formato de saida para data e hora em string (opcao 1) no arquivo de saida de parametros arqsai
header2='%     DATA    HH    SDVH   VAVG   VAVH   VTZD   VTZM   VTZS   VZMX    VDMX          VMTA          VMTB          VMTC          VMTD          VMTE     VTPK      VSPK    VMED       VEPK    VPED         VMTA1         VMTB1         VMTC1         VMTD1         VMTE1    VCAR1    VTPK1     VSPK1      VEPK1   VPED1      ALFA1  GAMA1         VMTA2         VMTB2         VMTC2         VMTD2         VMTE2    VCAR2    VTPK2     VSPK2      VEPK2   VPED2      ALFA2  GAMA2         VMTA3         VMTB3         VMTC3         VMTD3         VMTE3    VCAR3    VTPK3     VSPK3      VEPK3   VPED3      ALFA3  GAMA3';
fprintf(fid2,'%s\n',header2);clear header2;
% Formato de saida para data e hora numerica (opcao 2) 
%header2='    AA   MM DD HH MI    SDVH   VAVG   VAVH   VTZD   VTZM   VTZS   VZMX    VDMX          VMTA          VMTB          VMTC          VMTD          VMTE     VTPK      VSPK    VMED       VEPK    VPED         VMTA1         VMTB1         VMTC1         VMTD1         VMTE1    VCAR1    VTPK1     VSPK1      VEPK1   VPED1      ALFA1  GAMA1         VMTA2         VMTB2         VMTC2         VMTD2         VMTE2    VCAR2    VTPK2     VSPK2      VEPK2   VPED2      ALFA2  GAMA2         VMTA3         VMTB3         VMTC3         VMTD3         VMTE3    VCAR3    VTPK3     VSPK3      VEPK3   VPED3      ALFA3  GAMA3';

% Carregando funcao de transferencia de heave da boia Seatex
%if pdir
%   if dboia
%      load wavescan_hf.mat
%   end
%end

% Criaçao da estrutura de diretorios de saida!!
pastas_de_saida= {'esp','ind','figs','tsr'};

for ij =1:size(pastas_de_saida,2);
    if exist([pafsai,pastas_de_saida{ij}])==0;
        [sucesso,mensagem,idmensagem]=mkdir(pafsai,pastas_de_saida{ij});
    end
end

% Leitura do primeiro registro do arquivo 'arqdad'
arqdwv=fscanf(fid1,'%s',1); % Original
% arqdwv1=fscanf(fid1,'%s',1);
% arqdwv2=fscanf(fid1,'%s',1);
% arqdwv=[arqdwv1,' ',arqdwv2];
fig=0;fg=0;

% Inicio do LOOP PRINCIPAL para leitura de todos os arquivos com dados de onda do arquivo arqdad
while ~isempty(arqdwv) % Teste para identificar se ainda existe algum arquivo 
   
   if pdir == 1
     
         %  IMPORTANTE: Os dados brutos de Roll, Pitch e Compass
         %               precisam estar obrigatoriamente em GRAUS
         if dboia == 1
            % #### Leitura das series temporais do arquivo arqdwv ###
            % Rotina para ler dados de arquivos *.dwv da P-18
             [heave,roll,pitch,compas,ano,mes,dia,hora,min,sdata,stime] = le_p18(arqdwv,fundh);
%              arqdado=load(arqdwv);
%              roll=arqdado(:,1);
%              heave=arqdado(:,2);
%              pitch=arqdado(:,3);
%              compas=arqdado(:,4);
%              ano=1999;mes=08;dia=19;hora=13;min=00;
%              sdata='19/08/1999';stime='13:00'
             
             % Rotina para gerar etaEW e etaNS para boia Seatex
             [etaEW etaNS]=rota_boia(roll,pitch,compas);
         elseif dboia == 3
            % Leitura dos arquivos Onda_#####.dat da bóia do Espirito Santo
            % Esses dados já estão corrigidos com a declinação magnética!!
            % Desconsidera-se a função de transferência da bóia para esses
            % dados do ES, portanto não entra em corrseries
             DONV=0;
             [heave,roll,pitch,compas,ano,mes,dia,hora,min,sdata,stime] = le_boiaES(arqdwv);
             % Rotina para gerar etaEW e etaNS para boia do ES
             [etaEW etaNS]=rota_boia(roll,pitch,compas);
         end
         % As tres linhas abaixo foram usadas apenas para teste: 
         %figure(99);plot(heave);hold on;grid on;zoom on
         %figure(100);plot(etaEW);hold on;grid on;zoom on
         %figure(101);plot(etaNS);hold on;grid on;zoom on
         % Rotina para aplicar funcoes de transferencia nos
         % dados da boia Seatex
         if dboia == 1
         %    [heave,etaEW,etaNS]=corrseries(heave,etaEW,etaNS,transhf,transhm,DT);
         end
         % As onze linhas abaixo foram usadas apenas para teste: 
         %figure(99);plot(heave,'r');hold on;grid on;zoom on
         %figure(100);plot(etaEW,'r');hold on;grid on;zoom on
         %figure(101);plot(etaNS,'r');hold on;grid on;zoom on
         %load ondatr150808.mat;
         %figure(99);plot(A(:,dir /b/o/n/s j:\media\externo\cenpes\onda1g\Onda > j:\home\ricardo\onda1g\listagem.txt1));
         %figure(100);plot(A(:,2));
         %figure(101);plot(A(:,3));
         %heave=A(:,1);
         %etaEW=A(:,2);
         %etaNS=A(:,3);
         %ano=1999;mes=08;dia=15;hora=08;min=0;
    if dboia == 0
         % Rotina para ler dados de arquivos *.dat da boia de Marlim/Barracuda
         %  IMPORTANTE: Os dados brutos da boia da CONSUB (em CD) possuem a
         %              ordem: heave (m), etaEW e ETANS (adimensionais)         
         % [heave,etaEW,etaNS,ano,mes,dia,hora,min,sdata,stime]=le_consub(arqdwv,DT);
         % A rotina abaixo foi desativada
         marlim=1; % boia de Marlim (1991-1993)
         % marlim=0; % boia de Barracuda (1994-1995)
         [heave,etaEW,etaNS,ano,mes,dia,hora,min,sdata,stime]=le_ney2(arqdwv,DT,qualano,marlim);
         % As linhas abaixo foram usadas apenas para teste de espectro tri-modal
         %load 1992051316.dat;
         %heave=X1992051316(:,2);
         %etaEW=X1992051316(:,3);
         %etaNS=X1992051316(:,4);
         %ano=1992;mes=05;dia=13;hora=16;min=0;
    end

    if dboia == 2
         % Rotina para ler dados de arquivos da boia WAVERIDER da UFSC
         %  IMPORTANTE: Os dados brutos da boia WAVERIDER estao em
         %              ordem: heave (m), dEW e dNS (adimensionais)
         % A rotina abaixo foi desativada
         %marlim=1; % boia de Marlim (1991-1993)
         % marlim=0; % boia de Barracuda (1994-1995)
         %[heave,etaEW,etaNS,ano,mes,dia,hora,min,sdata,stime]=le_Waverider(arqdwv,DT,marlim);        
         [heave,etaEW,etaNS,ano,mes,dia,hora,min,sdata,stime,fig]=le_Waverider(arqdwv,DT,qualano,fig); 
         
    end
    if dboia == 4
         % Leitura da boia Triaxys. Arquivos sao referentes a elevacao e deslocamentos x e y (em metros)
         % DONV=0;
         [heave,etaEW,etaNS,ano,mes,dia,hora,min,sdata,stime]=le_boiaBS(arqdwv); 
    end


   else
     
      if t==0
          [heave,ano,mes,dia,hora,min,sdata,stime]=le_pat3(arqdwv,DT);
      else    
      % #### Leitura das series temporais dos arquivos do Pearl Marine
          [heave,ano,mes,dia,hora,min,sdata,stime]=le_pearl(arqdwv,DT);
      end
   end
   
   % Nome para ser usado nos arquivos de espectros, ondas individuais e figuras
   nomefig=[sdata([7:10 4:5 1:2]),stime([1:2 4:5])];
   
   % Montando serie temporal com instantes de tempo
   tempo=(DT:DT:length(heave)*DT)';
  
   % Salvando os valores das series temporais
   if pdir
      series=[tempo heave etaEW etaNS];
      header41='%      Data  Horai           Lat           Lon  Freqs';
      formato41='%13.5f %13.5f %6.2f\n';
      header42='%Tempo   Heave       etaEW       etaNS';
      formato42='%6.1f %7.3f %11.6f %11.6f\n';
   else
      header41='%      Data  Horai           Lat           Lon  Freqs';
      formato41='%13.5f %13.5f %6.2f\n';
      series=[tempo heave];
      header42='%Tempo   Heave';
      formato42='%6.1f %7.3f\n';
   end
   varplic='tes''te';
   plic=varplic(4);
   kponto=find(arqdwv == '.');
   auxh=round(hora+min/60);
   if auxh < 10
      nhora='00';nhora(2:2)=num2str(auxh,1);
   else
      nhora=num2str(auxh,2);
   end
   %eval(['arqtsr=',plic,sdata(7:10),sdata(4:5),sdata(1:2),nhora,'.tsr',plic,';']);
   %fid4=fopen(arqtsr,'w');
   fid4=fopen([pafsai,'tsr\W',nomefig,'.tsr'],'w');
   fprintf(fid4,'%s\n',header41);clear header41;
   fprintf(fid4,'%1s','%');
   fprintf(fid4,'%10s  ',sdata);
   fprintf(fid4,'%5s ',stime);
   fprintf(fid4,formato41,[Lat Lon 1/DT]);
   fprintf(fid4,'%s\n',header42);clear header42;
   for j=1:length(series(:,1));
       fprintf(fid4,formato42,series(j,:));
   end
   fclose(fid4);clear formato42;clear arqtsr;clear formato41;
   
   
   % Retirando trend das series
   % retirando a tendencia!!
   heave=detrend(heave);
   if pdir
      etaEW=detrend(etaEW);
      etaNS=detrend(etaNS);
   end

   pi2=2*pi;
   
   % ### Analise no dominio do tempo ###
   [VH,VHC,VT,SDVH,VAVG,VAVH,VTZD,VTZM,VTZS,VZMX] = trat_tempo(heave,DT);
   
   % ### Analise no dominio da frequencia ###
   [VF,VS,VS0,VTPK,kVTPK,VSPK,VMTA,VMTB,VMTC,VMTD,VMTE,NDT,noverlap,w,nfft]=trat_freq(heave,DT,mgl,pi2);
   
   % ### Analise direcional ###
   if pdir
      % A rotina trat_dir foi montada para series cujos etaEW e
      % etaNS possuem como referencia o eixo Leste (com rumo das
      % ondas crescendo no sentido antihorario). E' o caso da boia
      % da Coastal Climate-CONSUB, usada em Marlim e Barracuda
      % [VD,VPED,VNUM,VESP,VEPK] = trat_dir(VF,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK);
      % A rotina trat_dirp18 foi montada para series cujos etaEW e
      % etaNS possuem como referencia o eixo Norte (com rumo das
      % ondas crescendo no sentido horario). E' o caso da boia
      % da Seatex, usada na P-18.
      
      if dboia == 0  
        % [VD,VPED,VNUM,VESP,VEPK] = trat_dir(VF,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK,dboia); 
        [VD,VPED,VNUM,VESP,VEPK] = trat_dir_atual(VF,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK,nfft,dboia);
      end
      
      if dboia == 1  
         % Processa direcionalmente dados da boia Seatex da P-18 (1) e
         % tambem a boia do ES (Merenda)
         [VD,VPED,VNUM,VESP,VEPK] = trat_dir_atual(VF,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK,nfft,dboia);       
      end
      if dboia ==3
         % Processa direcionalmente dados da boia Seatex da P-18 (1) e
         % tambem a boia do ES (Merenda)
         [VD,VPED,VNUM,VESP,VEPK] = trat_dir_atual(VF,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK,nfft,dboia);  
      end
      if dboia==2       
         % Processa direcionalmente dados da boia de Marlim/Barracuda
         [VD,VPED,VNUM,VESP,VEPK] = trat_dir_atual(VF,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK,nfft,dboia);
      end
      if dboia == 4
         % Processa direcionalmente dados da boia Triaxys
         [VD,VPED,VNUM,VESP,VEPK] = trat_dir_atual(VF,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK,nfft,dboia);
      end
      
   else
      VD=zeros(length(VF),1);VESP=zeros(length(VF),1);VNUM=zeros(length(VF),1);
      VPED=999.99;VEPK=999.99;
   end
   
   % ### Selecao dos picos espectrais ###
   % IMPORTANTE: Os picos sao fornecidos em ordem decrecente, ou seja, 
   %             Spico(1) armazena o maior pico espectral, Spico(2) o
   %             segundo maior pico espectral, e Spico(3) o terceiro pico.
   %             O vetor Scava possui a ordenada do minimo espectral que
   %             antecede o Spico correspondente.
   [Spico,fSpico,dSpico,Scava,fScava,dScava] = sele_pico(VS,DT,VD,VF,VSPK,mgl,heave,pdir,nfft);
   
   % ### Cálculo dos momentos espectrais para espectros multi-modais ###
   [VMTA1,VMTB1,VMTC1,VMTD1,VMTE1,VCAR1,VTPK1,VSPK1,VEPK,VEPK1,VPED1,VMTA2,VMTB2,VMTC2,VMTD2,VMTE2,VCAR2,VTPK2,VSPK2,VEPK2,VPED2,VMTA3,VMTB3,VMTC3,VMTD3,VMTE3,VCAR3,VTPK3,VSPK3,VEPK3,VPED3] = momentos(fScava,Spico,fSpico,dSpico,VF,VS,NDT,VMTA,VMTB,VMTC,VMTD,VMTE,VTPK,VSPK,VEPK,VPED,VESP,pdir);
   
   % Plotando espectros e pontos para ajuste ao espectro de Jonswap
   plot_treshold  = 0.5; % Limite inferior  de Hs para plotar o Espectro!!
   if pdir
      if 4*sqrt(VMTA) > plot_treshold   
         fig=fig+1;figure(fig);%clf ;% Original
         subplot(2,1,1);plot(VF,VS,'linewidth',3);hold on;grid on
         %title(['Espectro da serie ',arqdwv,' - Azul(medido) e Vermelho(modelo JONSWAP)'])
         %axis([0.03 0.4 0 max(VS)+0.5]) % restringe a plotagem para as frequencias que fazem sentido
         axis tight
         plot(fSpico,Spico,'r+');plot(fScava,Scava,'ro')
         %title([ arqdwv,'- Hs = ', num2str(4*sqrt(VMTA)) ]),
         title([ sdata,' ',stime,' - Hs = ', num2str(4*sqrt(VMTA)) ]),
         %subplot(2,1,2);plot(VF,(unwrap(VD*pi/180)*57.3)+360);
         subplot(2,1,2);plot(VF,VD);grid on;
         %axis([0.03 0.4 0 max(VD)+2]) % restringe a plotagem às frequencias que fazem sentido
         xlabel('Freq');%return
     	end 
   else
      mfg=mod(fg,9);
      if mfg == 0;
         fig=fig+1;figure(fig);clf;hold on
      end
      fg=fg+1;subplot(3,3,mfg+1);
      plot(VF,VS,'linewidth',3);hold on
      %title(['Espectro da serie ',arqdwv,' - Azul(medido) e Vermelho(modelo JONSWAP)'])
      title([arqdwv(max(find(arqdwv=='\'))+1:length(arqdwv)-4),'-Hs=',num2str(4*sqrt(VMTA))]);
      %title([arqdwv,'-Hs=',num2str(4*sqrt(VMTA))])
      plot(fSpico,Spico,'r+');plot(fScava,Scava,'m.');
      text(fSpico(1)+10*(1/(nfft*DT)),Spico(1),['Tp=',num2str(VTPK)]);
   end
   %
   % Salvando dados espectrais de onda em arquivo proprio
   if pdir
      header51='%      Data  Horai           Lat           Lon  Freqs';
      formato51='%13.5f %13.5f %6.2f\n';  %'%9.5f %10.5f %5.2f\n';
      espec=[VF VS VD VNUM VESP];
      header52='%      VF         VS       VD      VNUM       VESP';
      formato52='%10.7f %10.4f %8.2f %9.5f %10.4f\n';
   else
      header51='%      Data  Horai           Lat           Lon  Freqs';
      formato51='%13.5f %13.5f %6.2f\n'; %'%9.5f %10.5f %5.2f\n';
      espec=[VF VS];
      header52='%    Freq   Sp_Heave';
      formato52='%10.7f %10.4f\n';
   end
   %eval(['arqesp=',plic,sdata(7:10),sdata(4:5),sdata(1:2),nhora,'.esp',plic,';']);
   %fid5=fopen(arqesp,'w'); Futuramente pode ser apagado
   fid5=fopen([pafsai,'esp\SP',nomefig,'.esp'],'w');
   fprintf(fid5,'%s\n',header51);clear header51;
   fprintf(fid5,'%1s','%');
   fprintf(fid5,'%10s  ',sdata);
   fprintf(fid5,'%5s ',stime);
   fprintf(fid5,formato51,[Lat Lon 1/DT]);
   fprintf(fid5,'%s\n',header52);clear header52;
   for j=1:length(espec(:,1));
      fprintf(fid5,formato52,espec(j,:));
   end
   fclose(fid5);clear formato52;clear arqesp;
   clear formato51;
   
   % ### Monta vetor com direcoes de ondas individuais e direcao da onda maxima ###
   if pdir
      [VDMX,VID]=vetor_dir(VH,VT,Spico,dSpico,fScava,VTZM);
   else
      VDMX=999.99;
   end

   % Salvando os valores de ondas individuais em arquivo proprio
   if pdir
      header61='%      Data  Horai           Lat           Lon  Freqs';
      formato61='%13.5f %13.5f %6.2f\n'; %'%9.5f %10.5f %5.2f\n';      
      h_indiv=[VH VT VID VHC];
      header62='%   VH     VT     VID    VHC';
      formato62='%6.2f %6.2f %7.2f %6.2f\n';
   else
      header61='%      Data  Horai           Lat           Lon  Freqs';
      formato61='%13.5f %13.5f %6.2f\n'; %'%9.5f %10.5f %5.2f\n';      
      h_indiv=[VH VT VHC'];
      header62='% Hind   Tind Crista';
      formato62='%6.2f %6.2f %6.2f\n';
   end
   %eval(['arqind=',plic,sdata(7:10),sdata(4:5),sdata(1:2),nhora,'.ind',plic,';']);
   %fid6=fopen(arqind,'w');
   fid6=fopen([pafsai,'ind\W',nomefig,'.ind'],'w');
   fprintf(fid6,'%s\n',header61);clear header61;
   fprintf(fid6,'%1s','%');
   fprintf(fid6,'%10s  ',sdata);
   fprintf(fid6,'%5s ',stime);
   fprintf(fid6,formato61,[Lat Lon 1/DT]);   
   fprintf(fid6,'%s\n',header62);clear header62;
   for j=1:length(h_indiv(:,1));
     fprintf(fid6,formato62,h_indiv(j,:));
   end
   fclose(fid6);clear formato62;clear arqind;clear formato61
   clear h_indiv
   % ###  Ajuste de um modelo empirico de JONSWAP aos diferentes mares  ###
   %      representados pelos picos Spico do espectro VS. 
   [alfa,gama,Hsmod,lm,epj1,epj2,epj3]=modelo_jonsw2(fSpico,Spico,fScava,Scava,VS,VF,DT,VMTA1,VMTA2,VMTA3,nfft,pdir,fig);
   %Vetor_parametro_Alfa=alfa
   %Vetor_parametro_Gama=gama
   
   % Plota o ajuste espectral de JONSWAP sobre o grafico com espectros
   epjT=epj1+epj2+epj3;
   if pdir
      if 4*sqrt(VMTA) > plot_treshold  
         figure(fig);subplot(2,1,1);plot(VF,epjT,'r')
      end   
   else
      figure(fig);subplot(3,3,mfg+1);plot(VF,epjT,'r')
   end
      
   % ### Salva dados no arquivo 'arqsai' com parametros do SIMO ###
   carrega_SIMO
   
   % salva e fecha a figura fig
   if pdir
      if 4*sqrt(VMTA) > 0
         eval(['print -djpeg90 ',['SP',nomefig],'.jpg']);
         %close(fig)
      end
  elseif isempty(arqdwv); % Eric, 11/04/2006.
       eval(['print -djpeg90 ',[pafsai,'figs\SP',nomefig],'.jpg']);
      %close(fig)
   end
   
   % Fechamento das figuras para aliviar o processamento do MATLAB!! Eric, 11/04/2006.
   if mod(fig,10) == 0 & fig > 10; % Isso aqui vai funcionar a partir da figura 20, Eric, 11/04/2006.
       close(fig-19:fig-10);
   end
      
   % Limpando variaveis de trabalho
   clear alfa ano arqdwv auxf ans
   clear c* e* g* i* j* k* l* n* r* s* v* w*
   clear dados dia dScava dSpico 
   clear fScava fSpico fid4 fid5 fid6 formato
   clear hora tempo mes pitch heave
   clear pi2 plic
   clear A* G* H* M* N* O* P* S* V*
   %
   % Leitura do proximo registro do arquivo 'arqdad'
   arqdwv=fscanf(fid1,'%s',1);
   % fclose(fid1);fclose(fid2);return % Linha apenas para debug. Comentar.
end
% Final do LOOP PRINCIPAL

disp([' Foram criados os seguintes diretorios:']);
disp(['     ',pafsai,pastas_de_saida{1},'  (Espectros)']);
disp(['     ',pafsai,pastas_de_saida{2},'  (Ondas Individuais)']);
disp(['     ',pafsai,pastas_de_saida{3},' (Figuras)']);
disp(['     ',pafsai,pastas_de_saida{4},'  (Series Temporais)']);

fclose(fid1);
fclose(fid2);
