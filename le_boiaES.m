function [heave,roll,pitch,compas,ano,mes,dia,hora,min,sdata,stime] = le_boiaES(arqdwv)
%
% Funcao para leitura das series temporais de heave, roll, pitch
% e compas geradas pela boia do Espirito Santo, desenvolvida pelo Rafael Merenda. 
%
% Eric Oliveira e Ricardo Campos 15/04/2009
% Leitura do arquivo 'arqdwv' com series temporais

fid=fopen(arqdwv,'r');
fgetl(fid);
fgetl(fid);
linha=fgetl(fid);
sdata=linha(9:18);
stime=linha(32:36);

dia=str2num(linha(9:10));
mes=str2num(linha(12:13));
ano=str2num(linha(15:18));
hora=str2num(linha(32:33));
min=str2num(linha(35:36));

fclose(fid)

[heave roll pitch compas]=textread(arqdwv,'%f%f%f%f','headerlines',13);
% heave=heave(1:1024);
% roll=-roll(1:1024);
% % pitch=-pitch(1:1024); % Funcionava assim com o referencial da trat_dir_p18
% pitch=pitch(1:1024); 
% compas=compas(1:1024);
roll=-roll;


