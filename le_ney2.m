function [heave,etaEW,etaNS,ano,mes,dia,hora,min,sdata,stime]=le_ney2(arqdwv,DT,qualano,marlim);
%
% Funcao para leitura das series temporais de heave, 
% etaEW e etaNS (Marlim) ou heave, etaNS, etaEW (Barracuda)
% a partir dos arquivos do NEY 
%
% &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
% OBS: Por algum motivo, os arquvos do NEY encontram-se
%      com as posicoes das series etaEW e etaNS invertidas
%      para as campanhas de Marlim e Barracuda:
%         Marlim:    heave, etaEW, etaNS
%         Barracuda: heave, etaNS, etaEW
% &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
%
% Jose A LIma 15/07/2004
% Alterada a posicao de leitura do ano, mes e dia a partir do nome
% do arquivo.
%
% Leitura do arquivo 'arqdwv' com series temporais

fim = length(arqdwv);
dia = arqdwv(fim-7:fim-6);
mes = arqdwv(fim-9:fim-8);
hora= arqdwv(fim-5:fim-4);
min = arqdwv(fim-3:fim-2);
ano = num2str(qualano);
sdata=[dia,'/',mes,'/',ano];
stime=[hora,':',min];

dia = str2num(dia);
mes = str2num(mes);
hora= str2num(hora);
min = str2num(min);
ano = str2num(ano);



fid3=fopen(arqdwv,'r');
% Inicializando vetores
heave=zeros(1024,1);etaEW=zeros(1024,1);etaNS=zeros(1024,1);
for k=1:1024 % Loop para leitura das series de heave, roll, pitch e compass
   if marlim
      dd=fscanf(fid3,'%s',1);
      heave(k)=str2num(fscanf(fid3,'%s',1));
      etaEW(k)=str2num(fscanf(fid3,'%s',1));
      etaNS(k)=str2num(fscanf(fid3,'%s',1));
   else
      heave(k)=str2num(fscanf(fid3,'%s',1));
      etaNS(k)=str2num(fscanf(fid3,'%s',1));
      etaEW(k)=str2num(fscanf(fid3,'%s',1));
      dd=fscanf(fid3,'%s',1);
   end
end

clear continua;clear string1;clear k;clear fid3;clear dd;clear nod;