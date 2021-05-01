function [heave,etaEW,etaNS,ano,mes,dia,hora,min,sdata,stime]=le_consub(arqdwv,DT);
%
% Funcao para leitura das series temporais de heave, 
% etaEW e etaNS (Marlim) ou heave, etaNS, etaEW (Barracuda)
% a partir dos arquivos '*.dat' da CONSUB
%
% &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
% OBS: Os arquivos com series brutas "txddmmaa.dat" encontram-se
%      no CD-PROCAP, elaborado pelo SEGEN/DENPRO. Nestes arquivos
%      as series temporais estão na seguinte ordem:
%             T1         T2        T3
%           heave      etaEW      etaNS
% &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
%
% C.I. Fisch 20/08/99
%
% Leitura do arquivo 'arqdwv' com series temporais
fid3=fopen(arqdwv,'r');
string1=fscanf(fid3,'%s',1);
continua=1;
while continua
string1=fscanf(fid3,'%s',1);
   if length(string1) == 5
      if string1 == 'DATA:'
         string1=fscanf(fid3,'%s',1);
         data=str2num(string1);
         dia=str2num(string1(1:2));
         mes=str2num(string1(4:5));
         ano=1900+str2num(string1(7:8));
         continua=1;
      elseif string1 == 'HORA:'
            string1=fscanf(fid3,'%s',1);
            hora=str2num(string1(1:2));
            min=00;
            continua=1;
      end
   elseif length(string1) == 8      
          if string1 == 'hh:mm:ss' % Teste para identificar posicao de inicio da serie
             continua=0;
          end   
   end
end
heave=zeros(1024,1);etaEW=zeros(1024,1);etaNS=zeros(1024,1);
for k=1:1024 % Loop para leitura das series de heave, roll, pitch e compass
   dd=fscanf(fid3,'%s',1);
   nod=fscanf(fid3,'%s',1);
   heave(k)=str2num(fscanf(fid3,'%s',1));
   etaEW(k)=str2num(fscanf(fid3,'%s',1));
   etaNS(k)=str2num(fscanf(fid3,'%s',1));
end
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