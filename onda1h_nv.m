
% Onda1h.m - Programa Onda1 - Versao H

%
% ######################################################################
%   Programa Especifico para Processamento de Dados de Onda Direcionais  
%     ou nao direcionais conforme definido no Parametreo pdir
% ######################################################################
%
% Autores: J.A. Lima    (PETROBRAS/CENPES) 
%          C.E. Parente (COPPE/UFRJ)- 30/03/99 (colaborou com o onda1b.m)
%          versão 1H: Ricardo Campos, J.A. Lima & Eric Oliveira
%
% Adaptado com a ajuda de: C.I. Fisch, Eric Oliveira, Ricardo Campos e
% Andre Mendes
%
% Series temporais de Entrada:
%  heave eh uma serie de 1024 (ou mais) pontos de elevacao
%  roll ou etaEW eh uma serie de 1024 (ou mais) pontos de inclinacao/deslocamento leste
%  pitch ou etaNS eh uma seerie de 1024 (ou mais) pontos de inclinacao/deslocamento norte
%
% Possibilidade de entrar com os coeficientes de Fourier a1,b1,a2,b2 no
% caso das boias Axys e Wavescan.
%
% DONV = declinacao magnetica:
%  Positiva para declinacoes Leste (E)
%  Negativa para declinacoes Oeste (W)

%% Alteracoes Principais
%>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
% 03/04/2012 - ( Ricardo Campos ).
% 18/03/2011 - ( Ricardo Campos / Eric O. Ribeiro).
%>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
%%

clear all; close all;

% Nome do arquivo de LOG.
bnome_arq_log = [mfilename,'_',datestr(now,30)];

%========================================================================
% Identificacao do arquivo que possui a lista dos arquivos *.txt
%========================================================================
% Arquivo com o nome dos arquivos de tempo contendo heave/pitch/roll
% heave/etaNS/etaEW ou apenas heave (nesse caso deve forncecer obrigatoriamente a1,b1,a2,b2 posteriormente)

[arqdad,pafdad]=uigetfile('*.txt','Nome do arquivo com a lista dos arquivos heave/pitch/roll, heave/etaNS/etaEW ou heave.');
if ~isstr(arqdad); return; end;
fid1=fopen([pafdad,arqdad],'r');

%========================================================================
% Identificacao do arquivo de saida
%========================================================================
[arqsai,pafsai]=uiputfile([pafdad,'*.out'],'Nome do arquivo de saida.out com os parametros para carga.');
if ~isstr(arqsai); return; end;
fid2=fopen([pafsai,arqsai],'a');

%========================================================================
% Argumentos de entrada.
%========================================================================
prompt={'Os dados sao direcionais (entre com o valor 1) ou nao-direcionais (entre com o valor 0).',...
        'BMO-BR (7), Wavescan-Brasil (6), Wavescan-GOM (5),Axys (4), Boia_ES_Merenda (3), Waverider (2), P-18 (1) ou a do SEGEN/CONSUB (0), deixe em branco caso seja nao-direcional.',...
        'O fundo de escala de heave 20 m (digite 1) ou 10 m (digite 0) (em branco caso nao seja P-18).',...
        'Entre com a taxa de amostragem (em segundos) das series temporais (Ex. Waverider: 0.7818 s).',...
        'Entre com o ID (6 digitos).',...
        'Entre com a latitude da coleta (em graus decimais, negativo para Hemisferio Sul).',...
        'Entre com a longitude da coleta (em graus decimais, negativo para Oeste).',...
        'Qual o ano dos dados ? (Axys e Wavescan leem direto do arquivo de entrada)',...
        'O dado eh da plataforma Pat-3 (0) ou Pearl Marine(1)?(Deixe em branco caso nao seja nenhuma das duas).',...
        'Numero de graus de liberdade para a analise espectral.',...
        'Declinacao Magnetica:(Oeste = Negativo, Leste = Positivo).',...
        'Entre com a profundiade local em (m).',...
        'Altura Significativa minima para analise direcional 2D (EMEM) e para identificar mais de um pico espectral.',...
        'Tratamento direcional 1D (digite 1). Tratamento direcional 1D e 2D com Metodo de Maxima Entropia (digite 2)'};
%def={'1',' ',' ','1','999999',' ',' ',' ',' ','32','-23','1e3','0.30','2'}; %Padroes gerais.
%def={'1','2','','0.7818','999999','-27.70483','-48.13650','2001','','32','-17.45','1e3','0.30','2'}; % Waverider SC.
%def={'1','2','','0.7818','999999','-23.01667','-42.05000','1998','','32','-21.633','1e3','0.30','2'}; % Waverider Arraial.
%def={'1','3',' ','1','999999','-19.95','-39.53','2006',' ','32','-23','1e3','0.30','2'}; % boia do ES (Merenda).
def={'1','4',' ','0.7813571','999999','-31.56667','-49.86667','',' ','32','-15.866667','1e3','0.30','2'}; % boia Axys MARINHA RS
%def={'1','4',' ','0.7813571','999999','-23.0570','-44.2343','',' ','32','-21.83','1e3','0.10','2'}; % boia Mini-Triaxys Terminal Angra
%def={'1','4',' ','0.7813571','999999','-24.389','-43.95','',' ','32','-21.72','1e3','0.30','2'}; % boia Axys BS
%def={'1','4',' ','0.7813571','999999','-23.1283','-40.9200','',' ','32','-23.02','1e3','0.30','2'}; % boia Axys BC
%def={'1','4',' ','0.7813571','999999','-11.3188','-37.116','',' ','32','-23.15','1e3','0.30','2'}; % boia Axys SEAL
%def={'1','4',' ','0.7813571','999999','-3.130','-38.516','',' ','32','-21.12','1e3','0.30','2'}; % boia Axys RNCE
%def={'1','5',' ','0.5','999999','26.7','-90.45','2009',' ','32','0.5','1e3','0.30','2'}; % boia Wavescan-GOM.
%def={'1','6',' ','0.5','999999','','','','','32','0.5','1e3','0.30','2'}; % boia Wavescan-Brasil.
%def={'1','7',' ','1','999999','-23.057','-44.2343','2011',' ','32','-21.83','1e3','0.10','2'}; %Padroes para a boia BMO_BR
dlgTitle=['Paramentros para Analise Espectral do arquivo ', pafdad,arqdad];
lineNo=1;
answer=inputdlg(prompt,dlgTitle,lineNo,def);

% Parametreo para identificar se os dados sao direcionais ou nao direcionais 
%     pdir=0: variavel logica booleana que indica falso (representa ondas nao-direcionais)
%     pdir=1: variavel logica booleana que indica verdadeiro (representa ondas direcionais)
pdir =str2num(char(answer(1)));

% Tipo de boia utilizada na medicao.
dboia=str2num(char(answer(2)));

% Seleciona o fundo de escala de heave da boia da P-18.
fundh=str2num(char(answer(3)));

% Taxa de amostragem (no tempo) das medicoes, em segundos.
DT=str2num(char(answer(4)));

% Latitude (em graus decimais, negativo para Hemisferio Sul).
ID=str2num(char(answer(5)));

% Latitude (em graus decimais, negativo para Hemisferio Sul).
Lat=str2num(char(answer(6)));

% Longitude (em graus decimais, negativo para Hemisferio Oeste).
Lon=str2num(char(answer(7)));

% Ano da Medicao (Axys e Wavescan leem direto do arquivo de entrada).
qualano =str2num(char(answer(8)));

% Pat-3 ou Pearl Marine.
% Chaveamento para leitura especifica de PAT-3 e Pearl Marine
t=str2num(char(answer(9)));

% Numero de graus de liberdade
mgl=str2num(char(answer(10)));

% Declinacao Magnetica
DONV=str2num(char(answer(11)));

% Profundiade local em metros.
prof=str2num(char(answer(12)));

% Hs minimo. Evita problemas na trat_dir_emem e sele_pico.
hsminimo=str2num(char(answer(13)));

% Flag para decidir entre tratamento direcional 1D (trat_dir_fft...), mais
% rapido, ou tratamento direcional 1D E 2D (trat_dir_EMEM) mais demorado.
decidespec=str2num(char(answer(14)));


%===============================================================================================
% Formato de saida para data e hora em string (opcao 1) no arquivo de saida de parametros arqsai
% Para uma olhada rapida dos mnemonicos, olhe o fim deste programa.
%===============================================================================================
header2={'%DATA';'HORA';'ID';'LAT';'LON';'SDVH';'VAVG';'VAVH';'VTZD';'VTZM';'VTZS';'VZMX';'VDMX';'VMTA';'VMTB';'VMTC';'VMTD';'VMTE';'VTPK';'VSPK';'VMED';'VSPR';'VPED';'VMTA1';'VMTB1';'VMTC1';'VMTD1';'VMTE1';'VCAR1';'VTPK1';'VSPK1';'VSPR1';'VPED1';'ALFA1';'GAMA1';'VMTA2';'VMTB2';'VMTC2';'VMTD2';'VMTE2';'VCAR2';'VTPK2';'VSPK2';'VSPR2';'VPED2';'ALFA2';'GAMA2';'VMTA3';'VMTB3';'VMTC3';'VMTD3';'VMTE3';'VCAR3';'VTPK3';'VSPK3';'VSPR3';'VPED3';'ALFA3';'GAMA3';'PHI';'S_PHI';'S1VSPR';'S2VSPR';'S1VSPR1';'S1VTPK1';'S2VSPR1';'S2VTPK1';'S1VSPR2';'S1VTPK2';'S2VSPR2';'S2VTPK2';'S1VSPR3';'S1VTPK3';'S2VSPR3';'S2VTPK3'};
% Formato de saida:             '%7.0f\t      %10.5f\t      %10.5f\t     7.4f\t   %6.2f\t   %6.2f\t   %6.2f\t    %6.2f\t  %6.2f\t   %6.2f\t     %7.2f\t        %13.6e\t         %13.6e\t          %13.6e\t        %13.6e\t          %13.6e\t    %8.2f\t      %9.4f\t    %7.2f\t       %10.5f\t   %7.2f\t         %13.6e\t         %13.6e\t         %13.6e\t         %13.6e\t         %13.6e\t     %8.2f\t     %8.2f\t      %9.4f\t      %10.5f\t    %7.2f\t      %10.6f\t    %6.2f\t        %13.6e\t         %13.6e\t         %13.6e\t         %13.6e\t         %13.6e\t     %8.2f\t     %8.2f\t      %9.4f\t      %10.5f\t    %7.2f\t      %10.6f\t   %6.2f\t         %13.6e\t         %13.6e\t         %13.6e\t         %13.6e\t         %13.6e\t     %8.2f\t     %8.2f\t      %9.4f\t     %10.5f\t    %7.2f\t       %10.6f\t   %6.2f\t %5.4f\t   %6.2f\t     %8.2f\t     %8.2f\t     %8.2f\t     %8.2f\t     %8.2f\t     %8.2f\t     %8.2f\t     %8.2f\t     %8.2f\t     %8.2f\t     %8.2f\n';

for iji = 1:length(header2)-1;
    fprintf(fid2,'%s\t',header2{iji});
end
fprintf(fid2,'%s\t\n',header2{iji+1});clear header2;

% Criacao da estrutura de diretorios de saida
pastas_de_saida= {'esp','ind','figs','tsr'};

for ij =1:size(pastas_de_saida,2);
    if exist([pafsai,pastas_de_saida{ij}])==0;
        [sucesso,mensagem,idmensagem]=mkdir(pafsai,pastas_de_saida{ij});
    end
end


%================================================================================
% Possibilidade de utilizar os coeficientes de Fourier a1,b1,a2,b2
% fornecidos pela boia ao inves de calcular com o onda1h (trat_dir_fft_ndbc9601).
% Possivel somente para boias Axys e Wavescan.
% Ricardo Campos 04/04/2012.
%================================================================================
cfourier = menu('Deseja utilizar os coeficientes de Fourier a1,b1,a2,b2 para a analise direcional (Somente para Axys e Wavescan!) ?','Nao','Sim');
cfourier = cfourier - 1; % 0=Nao  1=Sim

if cfourier==1;
    
    % A Axys fornece um arquivo com os coef de Fourier para cada tempo com
    % final .FOURIER . Sao 77 frequencias de 0.090 a 0.470 Hz e passo 0.005
    % (=(0.09:0.005:0.47))
    
    % A Wavescan fornece um arquivo *dirspec* com os coef de Fourier de todos os
    % tempos . Sao 47 frequencias de 0.04 a 0.50 e passo 0.01
    % (=(0.04:0.01:0.50))
    
    [arqdad2,pafdad2]=uigetfile('*.txt','Nome do arquivo com a lista do(s) arquivo(s) contendo os coef de Fourier.');
    if ~isstr(arqdad2); return; end;
        fid3=fopen([pafdad2,arqdad2],'r');
    
end


% Leitura do primeiro registro do arquivo 'arqdad'
arqdwv=fscanf(fid1,'%s',1); % Original
fig=0;fg=0;

%================================================================================================
% Inicio do LOOP PRINCIPAL para leitura de todos os arquivos com dados de onda do arquivo arqdad
%================================================================================================
while ~isempty(arqdwv) % Teste para identificar se ainda existe algum arquivo
  
  if pdir == 1
    
      
    if dboia == 0
      % Rotina para ler dados de arquivos *.dat da boia de Marlim/Barracuda
      %  IMPORTANTE: Os dados brutos da boia da CONSUB (em CD) possuem a
      %              ordem: heave (m), etaEW e etaNS (adimensionais)
      marlim=1; % boia de Marlim (1991-1993)
      % marlim=0; % boia de Barracuda (1994-1995)
      [heave,etaEW,etaNS,ano,mes,dia,hora,min,sdata,stime]=le_ney2(arqdwv,DT,qualano,marlim);
    end
      
    if dboia == 1
      % Rotina para ler dados de arquivos *.dwv da P-18
      [heave,roll,pitch,compas,ano,mes,dia,hora,min,sdata,stime] = le_p18(arqdwv,fundh);
      % converte de roll e pitch para etaEW e etaNS corrigindo o compas.
      % [etaEW etaNS]=rota_boia(roll,pitch,compas);
      [etaEW etaNS]=rotaxis_boia(roll,pitch,compas);
      % [heave,etaEW,etaNS]=corrseries(heave,etaEW,etaNS,transhf,transhm,DT);
    end
    
    if dboia == 2
      % Rotina para ler dados de arquivos da boia WAVERIDER
      %  IMPORTANTE: Os dados brutos da boia WAVERIDER estao em
      %              ordem: heave (m), dEW e dNS (adimensionais)
      testezero=0;
      while testezero==0
          
          [heave,etaEW,etaNS,ano,mes,dia,hora,min,sdata,stime,fig]=le_Waverider(arqdwv,DT,qualano,fig,fid1,bnome_arq_log);         
          if isempty(arqdwv)
              arq_selecionado = ['Acabou a lista de arquivos '];
              display(arq_selecionado)
              return             
          end
          
          if length(find(abs(heave)<0.0001))>512 || length(find(abs(etaEW)<0.0001))>512 || length(find(abs(etaNS)<0.0001))>512
              testezero=0;
              arq_selecionado = ['Arquivo .RAW com problemas (valores zerados): ',arqdwv];
              display(arq_selecionado)
              alog = fopen(bnome_arq_log,'w+');
              fprintf(alog,'%s\n',arq_selecionado);
              fclose(alog);
              % Leitura do proximo registro do arquivo 'arqdad'
              arqdwv=fscanf(fid1,'%s',1);
          elseif length(heave)<1024 || length(etaEW)<1024 || length(etaNS)<1024
              testezero=0;
              arq_selecionado = ['Arquivo .RAW com problemas (serie curta/dados faltantes): ',arqdwv];
              display(arq_selecionado)
              alog = fopen(bnome_arq_log,'w+');
              fprintf(alog,'%s\n',arq_selecionado);
              fclose(alog);
              % Leitura do proximo registro do arquivo 'arqdad'
              arqdwv=fscanf(fid1,'%s',1);
              
          elseif length(find(abs(heave)>15))>60 || length(find(abs(etaEW)>15))>60 || length(find(abs(etaNS)>15))>60
              testezero=0;
              arq_selecionado = ['Arquivo .RAW com problemas (valores espurios): ',arqdwv];
              display(arq_selecionado)
              alog = fopen(bnome_arq_log,'w+');
              fprintf(alog,'%s\n',arq_selecionado);
              fclose(alog);
              % Leitura do proximo registro do arquivo 'arqdad'
              arqdwv=fscanf(fid1,'%s',1);
              
              
          elseif length(find(abs(heave)>0.0001))>512 && length(find(abs(etaEW)>0.0001))>512 && length(find(abs(etaNS)>0.0001))>512  && length(heave)>1024 && length(etaEW)>1024 && length(etaNS)>1024
              testezero=1;
          end
      end
      
      
      
    end 
    
    if dboia == 3
      % Leitura dos arquivos Onda_#####.dat da boia do Espirito Santo
      % Esses dados ja estao corrigidos com a declinacao magnetica!!
      % Desconsidera-se a funcao de transferencia da boia para esses
      % dados do ES, portanto nao entra em corrseries
      DONV=0; % Declinacao magnetica ja corrigida, DONV deve ser zero!
      [heave,roll,pitch,compas,ano,mes,dia,hora,min,sdata,stime] = le_boiaES(arqdwv);
      % converte de roll e pitch para etaEW e etaNS corrigindo o compas.
      % [etaEW etaNS]=rota_boia(roll,pitch,compas);   
      [etaEW etaNS]=rotaxis_boia(roll,pitch,compas);
    end
       
    
    if dboia == 4 
      % Leitura da boia Axys. Arquivos sao referentes a elevacao (heave) e deslocamentos (dispEW e dispNS)
      testezero=0;
      while testezero==0
      [heave,etaEW,etaNS,ano,mes,dia,hora,min,sdata,stime]=le_axys(arqdwv);
            if length(find(abs(heave)<0.0001))>512 || length(find(abs(etaEW)<0.0001))>512 || length(find(abs(etaNS)<0.0001))>512
                testezero=0;
                arq_selecionado = ['Arquivo .HNE com problemas (valores zerados): ',arqdwv];
                display(arq_selecionado)                                
                alog = fopen(bnome_arq_log,'w+');
                fprintf(alog,'%s\n',arq_selecionado);
                fclose(alog);
                % Leitura do proximo registro do arquivo 'arqdad'
                arqdwv=fscanf(fid1,'%s',1);
            elseif length(heave)<1024 || length(etaEW)<1024 || length(etaNS)<1024               
                testezero=0;
                arq_selecionado = ['Arquivo .HNE com problemas (serie curta/dados faltantes): ',arqdwv];
                display(arq_selecionado)                                
                alog = fopen(bnome_arq_log,'w+');
                fprintf(alog,'%s\n',arq_selecionado);
                fclose(alog);
                % Leitura do proximo registro do arquivo 'arqdad'
                arqdwv=fscanf(fid1,'%s',1);                
            elseif length(find(abs(heave)>0.0001))>512 && length(find(abs(etaEW)>0.0001))>512 && length(find(abs(etaNS)>0.0001))>512  && length(heave)>1024 && length(etaEW)>1024 && length(etaNS)>1024
                testezero=1;
            end
      end
    end
    
    if dboia == 5
      % Leitura dos dados da boia Wavescan. 

       
      testezero=0;
      while testezero==0
       [heave,roll,pitch,compas,ano,mes,dia,hora,min,sdata,stime] = le_wavescan(arqdwv);
            if length(find(abs(heave)<0.0001))>512 || length(find(abs(roll)<0.0001))>512 || length(find(abs(pitch)<0.0001))>512
                testezero=0;
                arq_selecionado = ['Arquivo .WSC com problemas (valores zerados): ',arqdwv];
                display(arq_selecionado)                                
                alog = fopen(bnome_arq_log,'w+');
                fprintf(alog,'%s\n',arq_selecionado);
                fclose(alog);
                % Leitura do proximo registro do arquivo 'arqdad'
                arqdwv=fscanf(fid1,'%s',1);
            elseif length(heave)<1024 || length(roll)<1024 || length(pitch)<1024               
                testezero=0;
                arq_selecionado = ['Arquivo .WSC com problemas (serie curta/dados faltantes): ',arqdwv];
                display(arq_selecionado)                                
                alog = fopen(bnome_arq_log,'w+');
                fprintf(alog,'%s\n',arq_selecionado);
                fclose(alog);
                % Leitura do proximo registro do arquivo 'arqdad'
                arqdwv=fscanf(fid1,'%s',1);                
            elseif length(find(abs(heave)>0.0001))>512 && length(find(abs(roll)>0.0001))>512 && length(find(abs(pitch)>0.0001))>512  && length(heave)>1024 && length(roll)>1024 && length(pitch)>1024
                testezero=1;
            end
      end

      [etaEW etaNS]=rotaxis_boia(roll,pitch,compas);       

    end
    
    
    
    % Wavescan Brasil :  Shel_BS4  BC-10
    
    
    if dboia == 7
        % Leitura dos dados da boia BMO-BR 
        [heave,roll,pitch,compas,ano,mes,dia,hora,min,sdata,stime] = le_boia_BMO_BR(arqdwv,DT);
        % converte de roll e pitch para etaEW e etaNS corrigindo o campas.
        %[etaEW etaNS]=rota_boia(roll,pitch,compas);
        [etaEW etaNS]=rotaxis_boia(roll,pitch,compas);        
    end
    
    
    
  else
    
    if t==0; % Chaveamento para leitura especifica de PAT-3 e Pearl Marine
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
    header41='%	Data	Horai	Lat	Lon	Freqs';
    formato41='%13.5f\t%13.5f\t%6.2f\n';
    header42='%Tempo	Heave	etaEW	etaNS';
    formato42='%6.1f\t%7.3f\t%11.6f\t%11.6f\n';
  else
    header41='%	Data	Horai	Lat	Lon	Freqs';
    formato41='%13.5f\t%13.5f\t%6.2f\n';
    series=[tempo heave];
    header42='%Tempo	Heave';
    formato42='%6.1f\t%7.3f\n';
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
  
  %========================================================================
  % Retirando a tendencia
  %========================================================================
  heave=detrend(heave);
  if pdir
    etaEW=detrend(etaEW);
    etaNS=detrend(etaNS);
  end
  
  pi2=2*pi;
  
  %========================================================================
  % ### Analise no dominio do tempo ###
  %========================================================================
  [VH,VHC,VT,SDVH,VAVG,VAVH,VTZD,VTZM,VTZS,VZMX] = trat_tempo(heave,DT);
  
  % ### Analise no dominio da frequencia ###
  [VF,VS,VS0,VTPK,kVTPK,VSPK,VMTA,VMTB,VMTC,VMTD,VMTE,NDT,noverlap,w,nfft]=trat_freq(heave,DT,mgl,pi2);
  
  %========================================================================
  % ### Analise direcional ### 
  %========================================================================
   if pdir
    
    % Calculando o espectro direcional 2D pela rotina WAFO (metodo de
    % maxima entropia EMEM)
    if decidespec==2
      if VAVH >= hsminimo  % Hs minimo para aplicar o EMEM. Ricardo 11/02/2011
        [VF2D, VDIR2D, VESP2D] = trat_dir_EMEM(DT,heave,etaEW,etaNS,DONV);
      else
        VF2D=-999;VDIR2D=-999;VESP2D=-999;
      end
    end
    % Calculando a direcao pelo Metodo de Longuet-Higgins:
    % As duas rotinas abaixo sao antigas e apresentaram piores resultados nos testes direcionais:
    %[VD,VPED,VNUM,VESP,VSPR] = trat_dir(VF,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK,dboia);
    %[VD,VPED,VNUM,VESP,VSPR,A1,B1,A2,B2,Rcheck] = trat_dir_fft(VF,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK,nfft,dboia,prof);
    
    % As duas rotinas abaixo foram testadas direcionalmente e apresentaram otimos resultados (principalmente a ndbc). 
    % Ja foram referenciadas para o referencial da trat_dir_EMEM (nao mudar nenhum sinal!).
    % Rotina baseada no calculo desenvolvido pelo manual NDBC:
    [VD,VPED,VNUM,VESP,VSPR,A1,B1,A2,B2,s1,s2,Rcheck,phi,s_phi,S1VSPR,S2VSPR] = trat_dir_fft_ndbc9601(VF,VS,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK,nfft,dboia,mgl,prof);
    
    % Calculo da direcao pelo artigo do Tucker (1989), ocean enginnering vol. 16, pp.173-192. :
    %[VD,VPED,VNUM,VESP,VSPR,A1,B1,A2,B2,s1,s2,Rcheck,phi,s_phi,S1VSPR,S2VSPR] = trat_dir_fft_tucker1989(VF,VS,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK,nfft,dboia,mgl,prof); % Funcao igual ao artigo do Tucker 1989.
      
  else
    VD=zeros(length(VF),1);VESP=zeros(length(VF),1);VNUM=zeros(length(VF),1);
    VPED=-999.99;VSPR=-999.99;
   end 
  
  %========================================================================
  % ### Selecao dos picos espectrais ###
  % IMPORTANTE: Os picos sao fornecidos em ordem decrecente, ou seja,
  %             Spico(1) armazena o maior pico espectral, Spico(2) o
  %             segundo maior pico espectral, e Spico(3) o terceiro pico.
  %             O vetor Scava possui a ordenada do minimo espectral que
  %             antecede o Spico correspondente.
  %========================================================================
  [Spico,fSpico,dSpico,Scava,fScava,dScava] = sele_pico(VS,DT,VD,VF,VSPK,mgl,heave,pdir,nfft,VAVH,hsminimo);
  
  
  %========================================================================
  % ### Calculo dos momentos espectrais para espectros multi-modais ###
  %========================================================================
  [VMTA1,VMTB1,VMTC1,VMTD1,VMTE1,VCAR1,VTPK1,VSPK1,VSPR1,S1VSPR1,S1VTPK1,S2VSPR1,S2VTPK1,VPED1,VMTA2,VMTB2,VMTC2,VMTD2,VMTE2,VCAR2,VTPK2,VSPK2,VSPR2,S1VSPR2,S1VTPK2,S2VSPR2,S2VTPK2,VPED2,VMTA3,VMTB3,VMTC3,VMTD3,VMTE3,VCAR3,VTPK3,VSPK3,VSPR3,S1VSPR3,S1VTPK3,S2VSPR3,S2VTPK3,VPED3] = momentos_rev2(fScava,Spico,fSpico,dSpico,VF,VS,NDT,VMTA,VMTB,VMTC,VMTD,VMTE,VTPK,VSPK,VSPR,S1VSPR,S2VSPR,VPED,VESP,s1,s2,pdir);
  
  %========================================================================
  % Plotando espectros e pontos para ajuste ao espectro de Jonswap
  %========================================================================
  % plot_treshold  = 0.1; % Limite inferior de Hs para plotar o Espectro
  if pdir
    if 4*sqrt(VMTA) > hsminimo
      fig=fig+1;figure(fig);%clf ;% Original
      subplot(2,1,1);plot(VF,VS,'linewidth',3);hold on;grid on
      %title(['Espectro da serie ',arqdwv,' - Azul(medido) e Vermelho(modelo JONSWAP)'])
      %axis([0.03 0.4 0 max(VS)+0.5]) % restringe a plotagem para as frequencias que fazem sentido
      axis tight
      plot(fSpico,Spico,'r+');plot(fScava,Scava,'ro')
      %title([ arqdwv,'- Hs = ', num2str(4*sqrt(VMTA)) ]),
      title([ sdata,' ',stime,' - Hs = ', num2str(4.01*sqrt(VMTA),'%5.2f'),'m Tp = ',num2str(VTPK,'%5.2f'),'s Dirp = ', num2str(VPED,'%3.0f'),'º']),
      ylabel('Energia (m2/Hz)');
      subplot(2,1,2);plot(VF,VD);grid on;
      %axis([0.03 0.4 0 max(VD)+2]) % restringe a plotagem as frequencias que fazem sentido
      xlabel('Frequencia (Hz)');
      ylabel('Direcao (º)');
    end
  else
    mfg=mod(fg,9);
    if mfg == 0;
      fig=fig+1;figure(fig);clf;hold on
    end
    fg=fg+1;subplot(3,3,mfg+1);
    plot(VF,VS,'linewidth',3);hold on
    %title(['Espectro da serie ',arqdwv,' - Azul(medido) e Vermelho(modelo JONSWAP)'])
    title([arqdwv(max(find(arqdwv=='\'))+1:length(arqdwv)-4),' - Hs = ', num2str(4*sqrt(VMTA),'%5.2f'),'m Tp = ',num2str(VTPK,'%5.2f'),'s Dirp = ', num2str(VPED,'%3.0f'),'º']);
    %title([arqdwv,'-Hs=',num2str(4*sqrt(VMTA))])
    plot(fSpico,Spico,'r+');plot(fScava,Scava,'m.');
    text(fSpico(1)+10*(1/(nfft*DT)),Spico(1),['Tp=',num2str(VTPK)]);
  end
  
  %========================================================================
  % Salvando dados espectrais de onda em arquivo proprio
  %========================================================================
  if pdir
    header51='%	Data    Hora	Lat	Lon	Freqs';
    formato51='%13.5f\t%13.5f\t%6.2f\n';
    espec=[VF VS VD VNUM VESP A1 B1 A2 B2 Rcheck];
    header52='%	VF	VS	VD	VNUM	VESP	A1	B1	A2	B2	Rcheck';
    formato52='%10.7f\t%10.4f\t%8.2f\t%9.5f\t%10.4f\t%9.5f\t%9.5f\t%9.5f\t%9.5f\t%9.5f\n';
  else
    header51='%	Data	Hora	Lat	Lon	Freqs';
    formato51='%13.5f\t%13.5f\t%6.2f\n';
    espec=[VF VS]; 
    header52='%	Freq	Sp_Heave';
    formato52='%10.7f\t%10.4f\n';
  end
  
  % escrita do espectro 1D
  fid5=fopen([pafsai,'esp\SP',nomefig,'.esp'],'w');
  fprintf(fid5,'%s\n',header51);
  fprintf(fid5,'%1s','%');
  fprintf(fid5,'%10s  ',sdata);
  fprintf(fid5,'%5s	',stime);
  fprintf(fid5,formato51,[Lat Lon 1/DT]);
  fprintf(fid5,'%s\n',header52);clear header52;
  for j=1:length(espec(:,1)); 
    fprintf(fid5,formato52,espec(j,:));
  end
  fclose(fid5);clear formato52;clear arqesp;
  if VAVH>hsminimo && decidespec>1
    % escrita do espectro 2D resultado da trat_dir_EMEM
    fid5=fopen([pafsai,'esp\SP',nomefig,'.esp2D'],'w');
    fprintf(fid5,'%s\n','% Resultados de Espectro Direcional do Programa onda1h.m');
    fprintf(fid5,'%s\n','% Foi utilizada a rotina dat2dspec do pacote WAFO com metodo EMEM (NFFT=256 Nt=65)');
    fprintf(fid5,'%s\n',header51);clear header51;
    fprintf(fid5,'%1s','%');
    fprintf(fid5,'%10s\t',sdata);
    fprintf(fid5,'%5s\t',stime);
    fprintf(fid5,formato51,[Lat Lon 1/DT]);clear formato51;
    fprintf(fid5,'%s\n','%	');
    fprintf(fid5,'%s\n','% Primeira linha da matriz abaixo indica direcao e a primeira coluna indica frequencia(Hz)');
    fprintf(fid5,'    NaN  ');
    [r1 r2]=size(VESP2D);
    aux(:,1)=VF2D(:,1);
    aux(:,2:(r2+1))=VESP2D;
    formatoaux='%12.2f\t';
    fprintf(fid5,formatoaux,VDIR2D);
    fprintf(fid5,'%s\n','');
    dlmwrite([pafsai,'esp\SP',nomefig,'.esp2D'],aux,'-append','delimiter',' ','precision','%12.5e\t')
    fclose(fid5);clear aux r1 r2
  end
  
  %========================================================================
  % ### Monta vetor com direcoes de ondas individuais e direcao da onda maxima ###
  %========================================================================
  if pdir
    [VDMX,VID]=vetor_dir(VH,VT,Spico,dSpico,fScava,VTZM);
  else
    VDMX=-999.99;
  end
  
  %========================================================================
  % Salvando os valores de ondas individuais em arquivo proprio
  %========================================================================
  if pdir
    header61='%	Data	Horai	Lat	Lon	Freqs';
    formato61='%13.5f\t%13.5f\t%6.2f\n'; %'%9.5f %10.5f %5.2f\n';
    h_indiv=[VH	VT	VID	VHC];
    header62='%	VH	VT	VID	VHC';
    formato62='%6.2f\t%6.2f\t%7.2f\t%6.2f\n';
  else
    header61='%	Data	Horai	Lat	Lon	Freqs';
    formato61='%13.5f\t%13.5f\t%6.2f\n'; %'%9.5f %10.5f %5.2f\n';
    h_indiv=[VH	VT	VHC'];
    header62='%	Hind	Tind	Crista';
    formato62='%6.2f\t%6.2f\t%6.2f\n';
  end
  
  fid6=fopen([pafsai,'ind\W',nomefig,'.ind'],'w');
  fprintf(fid6,'%s\n',header61);clear header61;
  fprintf(fid6,'%1s','%');
  fprintf(fid6,'%10s\t',sdata);
  fprintf(fid6,'%5s\t',stime);
  fprintf(fid6,formato61,[Lat Lon 1/DT]);
  fprintf(fid6,'%s\n',header62);clear header62;
  for j=1:length(h_indiv(:,1));
    fprintf(fid6,formato62,h_indiv(j,:));
  end
  fclose(fid6);clear formato62;clear arqind;clear formato61
  clear h_indiv

  %========================================================================
  % ###  Ajuste de um modelo empirico de JONSWAP aos diferentes mares  ###
  %      representados pelos picos Spico do espectro VS.
  %========================================================================
  [alfa,gama,Hsmod,lm,epj1,epj2,epj3]=modelo_jonsw2(fSpico,Spico,fScava,Scava,VS,VF,DT,VMTA1,VMTA2,VMTA3,nfft,pdir,fig);
  
  % Plota o ajuste espectral de JONSWAP sobre o grafico com espectros
  epjT=epj1+epj2+epj3;
  if pdir
 %   if 4*sqrt(VMTA) > plot_treshold
    if 4*sqrt(VMTA) > hsminimo
      figure(fig);subplot(2,1,1);plot(VF,epjT,'r')
    end
  else
    figure(fig);subplot(3,3,mfg+1);plot(VF,epjT,'r')
  end
  
  %========================================================================
  % ### Salva dados no arquivo 'arqsai' com parametros do SIMO ###
  %========================================================================
  carrega_SIMO_onda1h
     
%     formato00='%8.3f %8.3f %8.3f %8.3f\n';
%     header00= '%           dp_ndbc_dirp8 dp_ndbc_dirp1 dp_fft_dirp8 dp_fft1_dirp1';
%     fid00=fopen(['confere_dir',nomefig,'.txt'],'w'); 
%     fprintf(fid00,'%s\n',header00); clear header00;
%     fprintf(fid00,'%1s','%');
%     fprintf(fid00,'%10s  ',sdata);
%     fprintf(fid00,'%5s ',stime);
%     fprintf(fid00,formato00,[dp_ndbc_dirp8 dp_ndbc_dirp1 dp_fft_dirp8 dp_fft1_dirp1]);
%     fclose(fid00);clear formato00;clear header00;
  
    
  %========================================================================
  % salva e fecha a figura fig. Gera e salva a figura do espectro 2D.
  %========================================================================
  if pdir
    if 4*sqrt(VMTA) > 0
      % salva figura espectro 1D
      % eval(['print -djpeg90 ',['SP',nomefig],'.jpg']);
      print(gcf,'-djpeg',['figs\SP',nomefig,'.jpg']);
      if decidespec==2
        if VAVH>hsminimo
          % Gera e salva figura espectro 2D
          fig=fig+1;
          figure(fig)
          VDIR2D(1,length(VDIR2D)+1)=VDIR2D(1);
          pVESP2D=VESP2D;
          [r1 r2]=size(VESP2D);
          VESP2D(:,r2+1)=VESP2D(:,1);
          % Plotando espectro direcional calculado pelo WAFO
          for j=1:length(VDIR2D);for k=1:length(VF2D);xx(k,j)=VF2D(k)*cos(VDIR2D(j)*pi/180);end;end
          for j=1:length(VDIR2D);for k=1:length(VF2D);yy(k,j)=VF2D(k)*sin(VDIR2D(j)*pi/180);end;end
          % Calculando limite superior para plotar frequencia do espectro 2D na
          % primeira casa decimal
          %supf=ceil(max(VF2D)*10 )/10;
          supf=.4; % Truncando em 2.5 segs ou 0.4 Hz!!
          ourpolar2(pi/2,supf,[],[0.05 supf .05]);%,'w.','w',0.1,supf);
          hold on
          %pcolor(xx',yy',VESP2D);shading flat;colormap(colormap_light_bottom);
          pcolor(xx(find(VF2D<=.4),:),yy(find(VF2D<=.4),:),VESP2D(find(VF2D<=.4),:));shading flat;colormap(colormap_light_bottom);
          %contour(xx',yy',VESP2D,'k')
          contour(xx(find(VF2D<=.4),:),yy(find(VF2D<=.4),:),VESP2D(find(VF2D<=.4),:),'k')
          %axis([-0.34 0.34 -0.34 0.34])
          title([sdata,' ',stime,' Espectro 2D - rotina dat2dspec do WAFO - Extended Maximum Entropy Method'],'fontsize',9)
          colorbar
          % eval(['print -djpeg90 ',['SP',nomefig,'_2D'],'.jpg']);
          print('-djpeg',['figs\SP',nomefig,'_2D.jpg']);
        end
      end
    end
  elseif isempty(arqdwv); % Eric, 11/04/2006.
    % eval(['print -djpeg90 ',[pafsai,'figs\SP',nomefig],'.jpg']);
    print('-djpeg',['figs\SP',nomefig,'.jpg']);
  end
  
  %========================================================================
  % Fechamento das figuras para aliviar o processamento do MATLAB!! Eric, 11/04/2006.
  %    if mod(fig,10) == 0 & fig > 10; % Isso aqui vai funcionar a partir da figura 20, Eric, 11/04/2006.
  %        close(fig-19:fig-10);
  %    end
  % Fechamento das figuras para aliviar o processamento do MATLAB!! Ricardo, 22/12/2010.
  %========================================================================
  if fig > 10; % Isso aqui vai funcionar a partir da figura 20, para processar series muito longas.
    close all
  end
  
  
  %========================================================================
  % Limpando variaveis de trabalho
  %========================================================================
  clear alfa ano arqdwv auxf ans
  clear c* e* g* i* j* k* l* n* r* s* v* w*
  clear dados dia dScava dSpico
  clear fScava fSpico fid4 fid5 fid6 formato
  clear hora tempo mes pitch heave
  clear pi2 plic
  clear A* G* H* M* N* O* P* S* V*
  
  %========================================================================
  % Leitura do proximo registro do arquivo 'arqdad'
  %========================================================================
  arqdwv=fscanf(fid1,'%s',1);
  % fclose(fid1);fclose(fid2);return % Linha apenas para debug. Comentar.
  
end
% Final do LOOP PRINCIPAL

disp([' Foram criados os seguintes diretorios:']);
disp(['     ',pafsai,pastas_de_saida{1},'  (Espectros)']);
disp(['     ',pafsai,pastas_de_saida{2},'  (Ondas Individuais)']);
disp(['     ',pafsai,pastas_de_saida{3},'  (Figuras)']);
disp(['     ',pafsai,pastas_de_saida{4},'  (Series Temporais)']);

fclose(fid1);
fclose(fid2);








% Mnemonicos do arquivo saida.out para carregar na base:
% SDVH  Desvio Padrao das Alturas de Zero Descendente
% VAVG  Altura Media
% VAVH  Altura Significativa
% VTZD  Periodo Medio de Zero Descendente
% VTZM  Periodo de Altura Maxima 
% VTZS  Periodo Significativo
% VZMX  Altura Maxima
% VDMX  Direcao da Onda Maxima
% VMTA  Momento Espectral de Ordem 0
% VMTB  Momento Espectral de Ordem 1
% VMTC  Momento Espectral de Ordem 2
% VMTD  Momento Espectral de Ordem 3   
% VMTE  Momento Espectral de Ordem 4
% VTPK  Periodo de Pico Espectral     
% VSPK  Ordenada de Pico Espectral 
% VMED  Direcao Media de Propagacao
% VSPR  Parametreo Espalhamento
% VPED  Direcao Espectral
% 
% VMTA1 Momento Espectral de Ordem 0 do Pico 1 (Mais Energetico) 
% VMTB1 Momento Espectral de Ordem 1 do Pico 1 (Mais Energetico)
% VMTC1 Momento Espectral de Ordem 2 do Pico 1 (Mais Energetico)
% VMTD1 Momento Espectral de Ordem 3 do Pico 1 (Mais Energetico)
% VMTE1 Momento Espectral de Ordem 4 do Pico 1 (Mais Energetico)
% VCAR1 Altura Significativa do Pico 1 (Mais Energetico)
% VTPK1 Periodo de Pico Espectral do Pico 1 (Mais Energetico)
% VSPK1 Ordenada de Pico Espectral do Pico 1 (Mais Energetico)
% VSPR1 Parametreo Espalhamento do Pico 1 (Mais Energetico)
% VPED1 Direcao do Pico 1 (Mais Energetico)      
% ALFA1 Parametreo de JONSWAP do Pico 1 (Mais Energetico)
% GAMA1 Parametreo  de JONSWAP do Pico 1 (Mais Energetico)
% 
% VMTA2  Momento Espectral de Ordem 0 do Pico 2. O segundo mais Energetico.       
% VMTB2  Momento Espectral de Ordem 1 do Pico 2. O segundo mais Energetico.      
% VMTC2  Momento Espectral de Ordem 2 do Pico 2. O segundo mais Energetico.      
% VMTD2  Momento Espectral de Ordem 3 do Pico 2. O segundo mais Energetico.     
% VMTE2  Momento Espectral de Ordem 4 do Pico 2. O segundo mais Energetico.
% VCAR2  Altura Significativa do Pico 2. O segundo mais Energetico.
% VTPK2  Periodo de Pico Espectral do Pico 2. O segundo mais Energetico.
% VSPK2  Ordenada de Pico Espectral do Pico 2. O segundo mais Energetico.
% VSPR2  Parametreo Espalhamento do Pico 2. O segundo mais Energetico. 
% VPED2  Direcao do Pico 2. O segundo mais Energetico.
% ALFA2  Parametreo de JONSWAP do Pico 2. O segundo mais Energetico.
% GAMA2  Parametreo  de JONSWAP do Pico 2. O segundo mais Energetico.
% 
% VMTA3  Momento Espectral de Ordem 0 do Pico 3. O menos Energetico.
% VMTB3  Momento Espectral de Ordem 1 do Pico 3. O menos Energetico.
% VMTC3  Momento Espectral de Ordem 2 do Pico 3. O menos Energetico.
% VMTD3  Momento Espectral de Ordem 3 do Pico 3. O menos Energetico.        
% VMTE3  Momento Espectral de Ordem 4 do Pico 3. O menos Energetico. 
% VCAR3  Altura Significativa do Pico 3. O menos Energetico.
% VTPK3  Periodo de Pico Espectral do Pico 3. O menos Energetico.  
% VSPK3  Ordenada de Pico Espectral do Pico 3. O menos Energetico.   
% VSPR3  Parametreo Espalhamento do Pico 3. O menos Energetico.
% VPED3  Direcao do Pico 3. O menos Energetico.   
% ALFA3  Parametreo de JONSWAP do Pico 3. O menos Energetico.
% GAMA3  Parametreo  de JONSWAP do Pico 3. O menos Energetico.

