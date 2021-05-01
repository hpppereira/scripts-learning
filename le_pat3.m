function [heave,ano,mes,dia,hora,minu,sdata,stime]=le_pat3(arqdwv,DT);
%
%[HEAVE,ANO,MES,DIA,SDATA,STIME]=LE_PEARL(ARQDWV,DT) retorna os valore de
% elevaçao da superficie do mar e data hora do arquivo ARQDWV.
% onde :
% ARQDWV = arquivo com os dados de onda nao direcional (so heave),
% DT = intervalo amostral em segundos,
% HEAVE = elevaçao da superficie do mar,
% ANO = numeral indicando o ano,
% MES = numeral indicando o mes,
% DIA = numeral indicando o dia,
% SDATA = string de texto contendo a data
% STIME = string de texto contendo a hora
%
% Veja tambem: (See also) ONDA1G

% Copyright 2006-2006 The EricWorks, Inc.
% $Revision: 1.00 $ $ Date 2006/04/06 12:42:52 $
%
% Leitura do arquivo 'arqdwv' com series temporais
if strcmp(upper(arqdwv(length(arqdwv)-3:length(arqdwv))),'.DAT');
    [heave] = textread(arqdwv,'%f','headerlines',7);
    [dia,mes,ano] = textread(arqdwv,'%2c%*c%2c%*c%4c',1,'headerlines',3);
    [hora,minu,segu] = textread(arqdwv,'%2c%*c%2c%*c%2c',1,'headerlines',5);
    
elseif strcmp(upper(arqdwv(length(arqdwv)-3:length(arqdwv))),'.SER')| strcmp(upper(arqdwv(length(arqdwv)-3:length(arqdwv))),'.CNP');
    [heave] = textread(arqdwv,'%*s%f','headerlines',5);
    [dia,mes,ano] = textread(arqdwv,'%2c%*c%2c%*c%4c',1,'headerlines',1);
    [hora,minu,segu] = textread(arqdwv,'%2c%*c%2c%*c%2c',1,'headerlines',3);
end

dia = str2num(dia);
mes = str2num(mes);
ano = str2num(ano);
hora = str2num(hora);
minu = str2num(minu);
segu = str2num(segu);
tempo = datenum(ano,mes,dia,hora,minu,segu);
sdata = datestr(tempo,24);
stime = datestr(tempo,15);

