

clear all; close all;

% Nome do arquivo de LOG.
bnome_arq_log = [mfilename,'_',datestr(now,30)];

[arqdad,pafdad]=uigetfile('*.txt','Nome do arquivo com a lista dos arquivos heave/pitch/roll, heave/etaNS/etaEW ou heave.');
if ~isstr(arqdad); return; end;
fid1=fopen([pafdad,arqdad],'r');

[arqsai,pafsai]=uiputfile([pafdad,'*.out'],'Nome do arquivo de saida.out com os parametros para carga.');
if ~isstr(arqsai); return; end;
fid2=fopen([pafsai,arqsai],'a');

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

def={'1','2','','0.7818','999999','-27.70483','-48.13650','2002','','32','-17.45','1e3','0.30','2'}; % Waverider SC.

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


end
