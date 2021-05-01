% Mfile para carregar parametros do SIMO no
% arquivo fornecido como 'arqsai' no Mfile onda1d
%
% Jose A. LIma/ C.I. Fisch 16/07/99
%
% A variavel lm indica as posicoes dos picos espectrais
% Obs: O cabecalho (header2) do arquivo encontra-se na rotina principal ONDA1H.M.
% 28-Mar-2011

%==========================================================================
% Parametros de JONSWAP.
%==========================================================================
if length(lm) == 1
   ALFA1=alfa(1);GAMA1=gama(1);
   ALFA2=-99.99;GAMA2=-99.99;
   ALFA3=-99.99;GAMA3=-99.99;
elseif length(lm) == 2
   ALFA1=alfa(1);GAMA1=gama(1);
   ALFA2=alfa(2);GAMA2=gama(2);
   ALFA3=-99.99;GAMA3=-99.99;
elseif length(lm) == 3
   ALFA1=alfa(1);GAMA1=gama(1);
   ALFA2=alfa(2);GAMA2=gama(2);
   ALFA3=alfa(3);GAMA3=gama(3);
end

%==========================================================================
% Atribuicao de valores para alguns parametros que nao
% foram definidos no programa principal
%==========================================================================
VS(VF<1/25.0) = NaN;
VS(VF>1/2.25) = NaN;
VMED=atan2(nanmean(VS.*sin(VD.*pi./180)),nanmean(VS.*cos(VD.*pi./180)))*180/pi;%-999.99 % Direcao Media Geral (Verificar na rotina GERDIR do programa testsim3.f)
if VMED<0;VMED=VMED+360;end
% Vetor com dados para carga do SIMO
clear dados;

%==========================================================================
% Vetor com data e hora em string (opcao 1)
%==========================================================================
dados=[ID	Lat	Lon	SDVH	VAVG	VAVH	VTZD	VTZM	VTZS	VZMX	VDMX	...  % Parametros no dominio do tempo
       VMTA	VMTB	VMTC	VMTD	VMTE	VTPK	VSPK	VMED	VSPR	VPED	... % Parametros no dominio da frequencia 
       VMTA1	VMTB1	VMTC1	VMTD1	VMTE1	VCAR1	VTPK1	VSPK1	VSPR1	VPED1	ALFA1	GAMA1	... % Parametros do pico 1
       VMTA2	VMTB2	VMTC2	VMTD2	VMTE2	VCAR2	VTPK2	VSPK2	VSPR2	VPED2	ALFA2	GAMA2	... % Parametros do pico 2
       VMTA3	VMTB3	VMTC3	VMTD3	VMTE3	VCAR3	VTPK3	VSPK3	VSPR3	VPED3	ALFA3	GAMA3	... % Parametros do pico 3
       phi	s_phi	S1VSPR	S2VSPR	S1VSPR1	S1VTPK1	S2VSPR1	S2VTPK1	S1VSPR2	... % aremetros de espalhamento
       S1VTPK2	S2VSPR2	S2VTPK2	S1VSPR3	S1VTPK3	S2VSPR3	S2VTPK3]; % Paremetros de espalhamento
% Salvando como arquivo ASCII
% Formato abaixo sem parametros de espalhamento (phi n_phi s_phi n_Krogstad s_Krogstad)
%formato='%7.0f\t%10.5f\t%10.5f\t%7.4f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%7.2f\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%8.2f\t%9.4f\t%7.2f\t%10.5f\t%7.2f\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%8.2f\t%8.2f\t%9.4f\t%10.5f\t%7.2f\t%10.6f\t%6.2f\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%8.2f\t%8.2f\t%9.4f\t%10.5f\t%7.2f\t%10.6f\t%6.2f\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%8.2f\t%8.2f\t%9.4f\t%10.5f\t%7.2f\t%10.6f\t%6.2f\n';
% Formato abaixo com parametros de espalhamento (phi n_phi s_phi n_Krogstad s_Krogstad)
formato='%7.0f\t%10.5f\t%10.5f\t%7.4f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%7.2f\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%8.2f\t%9.4f\t%7.2f\t%10.5f\t%7.2f\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%8.2f\t%8.2f\t%9.4f\t%10.5f\t%7.2f\t%10.6f\t%6.2f\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%8.2f\t%8.2f\t%9.4f\t%10.5f\t%7.2f\t%10.6f\t%6.2f\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%13.6e\t%8.2f\t%8.2f\t%9.4f\t%10.5f\t%7.2f\t%10.6f\t%6.2f\t%5.4f\t%6.2f\t%8.2f\t%8.2f\t%8.2f\t%8.2f\t%8.2f\t%8.2f\t%8.2f\t%8.2f\t%8.2f\t%8.2f\t%8.2f\t%8.2f\t%8.2f\t%8.2f\n';

%==========================================================================
% Convertendo valores espúrios para NaN.
%==========================================================================
dados(dados==-99.99)=NaN; % Talvez dê problema com a longitude quando os dados forem do Oceano Pacífico.
dados(dados==-999.99)=NaN;

%==========================================================================
% Vetor com data e hora em valores numericos (opcao 2)
%==========================================================================
%dados=[ano mes dia hora min ...                    % Dados de data e hora do registro
%       SDVH VAVG VAVH VTZD VTZM VTZS VZMX VDMX ...  % Parametros no dominio do tempo
%       VMTA VMTB VMTC VMTD VMTE VTPK VSPK VMED VEPK VPED ... % Parametros no dominio da frequencia 
%       VMTA1 VMTB1 VMTC1 VMTD1 VMTE1 VCAR1 VTPK1 VSPK1 VEPK1 VPED1 ALFA1 GAMA1 ... % Parametros do pico 1
%       VMTA2 VMTB2 VMTC2 VMTD2 VMTE2 VCAR2 VTPK2 VSPK2 VEPK2 VPED2 ALFA2 GAMA2 ... % Parametros do pico 2
%       VMTA3 VMTB3 VMTC3 VMTD3 VMTE3 VCAR3 VTPK3 VSPK3 VEPK3 VPED3 ALFA3 GAMA3];   % Parametros do pico 3 
% Salvando como arquivo ASCII
%formato='%6.0f %4.0f %2.0f %2.0f %2.0f %7.4f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %7.2f %13.6e %13.6e %13.6e %13.6e %13.6e %8.2f %9.4f %7.2f %10.5f %7.2f %13.6e %13.6e %13.6e %13.6e %13.6e %8.2f %8.2f %9.4f %10.5f %7.2f %10.6f %6.2f %13.6e %13.6e %13.6e %13.6e %13.6e %8.2f %8.2f %9.4f %10.5f %7.2f %10.6f %6.2f %13.6e %13.6e %13.6e %13.6e %13.6e %8.2f %8.2f %9.4f %10.5f %7.2f %10.6f %6.2f\n';

%==========================================================================
% Imprimindo valores no arquivo de saida
%==========================================================================
fprintf(fid2,'%10s\t',[sdata]);
fprintf(fid2,'  %5s\t',[stime]);
fprintf(fid2,formato,dados(1,:));