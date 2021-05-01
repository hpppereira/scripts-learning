function [heave,roll,pitch,compas,ano,mes,dia,hora,min,sdata,stime] = le_p18(arqdwv,fundh)
%
% Funcao para leitura das series temporais de heave, roll, pitch
% e compas geradas pela boia SEATEX da plataforma P-18, e 
% transferidas pelo SISMO atraves de arquivos *.dwv.
%
% C.I. Fisch / J.A. LIma 21/07/99
%
% Leitura do arquivo 'arqdwv' com series temporais
fid3=fopen(arqdwv,'r');
string1=fscanf(fid3,'%s',1);
continua=1;
while continua
   if length(string1) == 6
      if string1 == 'Dados:' % Teste para identificar posicao de inicio da serie
         continua=0;
      else
         string1=fscanf(fid3,'%s',1);
      end
   else
     string1=fscanf(fid3,'%s',1);
   end
end
for k=1:7 % Pula os caracteres de Heave ate Compass
   string1=fscanf(fid3,'%s',1);
end
heave=zeros(1024,1);roll=zeros(1024,1);pitch=zeros(1024,1);compas=zeros(1024,1);
for k=1:1024 % Loop para leitura das series de heave, roll, pitch e compass
   dd=fscanf(fid3,'%s',1);
   nod=fscanf(fid3,'%s',1);
   heave(k)=str2num(fscanf(fid3,'%s',1));
   roll(k)=str2num(fscanf(fid3,'%s',1));
   pitch(k)=str2num(fscanf(fid3,'%s',1));
   compas(k)=str2num(fscanf(fid3,'%s',1));
end
plot(heave);
% Ajusta o fundo de escala de heave (se fundo escala=20 m, entao multiplica heave por dois) 
if fundh
   heave=heave*2;
end
% Data e hora fornecida no arquivo de dados (valores numericos)
ano=str2num(arqdwv(1:4));
mes=str2num(arqdwv(5:6));
dia=str2num(arqdwv(7:8));
hora=str2num(arqdwv(9:10));
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
clear continua;clear string1;clear nod;clear k;clear dd;clear fid3;
