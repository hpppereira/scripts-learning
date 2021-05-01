function [heave,etaEW,etaNS,ano,mes,dia,sdata,stime]=le_ney(arqdwv,DT,marlim);
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
% C.I. Fisch 20/08/99
%
% Leitura do arquivo 'arqdwv' com series temporais
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
% Data e hora fornecida no arquivo de dados (valores numericos)
ano=1900+str2num(arqdwv(1:2));
mes=str2num(arqdwv(3:4));
dia=str2num(arqdwv(5:6));
hora=str2num(arqdwv(7:8));
min=0;
% Montando strings para data e hora
if mes < 10
   smes='00';smes(2:2)=num2str(mes);
else
   smes=num2str(mes);
end
if dia < 10
   sdia='00';sdia(2:2)=num2str(dia);
else
   sdia=num2str(dia);
end
sdata='00/00/0000';sdata(1:2)=sdia;sdata(4:5)=smes;sdata(7:10)=num2str(ano);
if min < 10
   smin='00';smin(2:2)=num2str(min);
else
   smin=num2str(min);
end
if hora < 10
   shora='00';shora(2:2)=num2str(hora);
else
   shora=num2str(hora);
end
stime='00:00';stime(1:2)=shora;stime(4:5)=smin;
%
clear continua;clear string1;clear k;clear fid3;clear dd;clear nod;