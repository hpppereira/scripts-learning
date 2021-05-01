function [heave,roll,pitch,compas,ano,mes,dia,hora,min,sdata,stime] = le_wavescan(arqdwv)
%
% Funcao para leitura das series temporais de heave, roll, pitch
% e compas da boia Wavescan no Golfo do Mexico. 
%
% Foi unificada à funcao rota-boia pois as series sao de 2048 (2HZ)
% e a funcao rota-boia somente trabalha com series de 1024
%
% Ricardo Campos 04/02/2011
% Leitura do arquivo 'arqdwv' com series temporais

fid=fopen(arqdwv,'r');
fgetl(fid);
linha=fgetl(fid);
linha = linha(find(linha~='T')); % Eric 01/Abr/2011.

dia=linha(10:11);
mes=linha(8:9);
ano=linha(4:7);
hora=linha(12:13);
min=linha(14:15);

sdata=[dia,'/',mes,'/',ano];
stime=[hora,':',min];

dia = str2num(dia);
mes = str2num(mes);
hora= str2num(hora);
min = str2num(min);
ano = str2num(ano);

fclose(fid)


[heave pitch roll compas]=textread(arqdwv,'%f%f%f%f','headerlines',3);
% roll =asin(roll)*180/pi;
% pitch=asin(pitch)*180/pi;
heave=-heave;

