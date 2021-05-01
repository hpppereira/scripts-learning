function [heave,ano,mes,dia,hora,min,sdata,stime]=le_pearl(arqdwv,DT);
%
% Funcao para leitura das series temporais de heave 
%     no caso de dados não direcionais
%
% C.I. Fisch / J.A. LIma 04/08/99
%
% Leitura do arquivo 'arqdwv' com series temporais
fid3=fopen(arqdwv,'r');
continua=1;
while continua
   string1=fscanf(fid3,'%s',1);
   if length(string1) == 1
      if string1 == 'A'
         string1=fscanf(fid3,'%s',1);
         data=str2num(string1);
         dia=str2num(string1(1:2));
         mes=str2num(string1(4:5));
         if length(string1) == 8
            ano=1900+str2num(string1(7:8));
         else
            ano=str2num(string1(7:10));
         end
         continua=1;
      else
         if string1 == 'B'
            string1=fscanf(fid3,'%s',1);
            hora=str2num(string1(1:2));
            min=str2num(string1(4:5));
            continua=1;
         else 
           if string1 == 'C' % Teste para identificar posicao de inicio da serie
              continua=0;
           end   
        end
      end  
   end
end
nlinhas=2401;
heave=zeros(nlinhas,1);
for k=1:nlinhas % Loop para leitura das series de heave
    instante=fscanf(fid3,'%s',1);
    heave(k)=str2num(fscanf(fid3,'%s',1));
end
%
% Teste para remocao de spikes
heave=detrend(heave);
desvp=std(heave);
k=find(abs(heave)>abs(10*desvp));
if ~isempty(k)
   j=1;
   while j <= length(k)
      figure(10);clf
      plot(heave);hold on
      plot(k(j),heave(k(j)),'ro')
      % Observe que o desvio padrao das elevacoes e' aproximadamente igual a sqrt(m0),
      % deste modo Hs=4*sqrt(m0)=4*std(heave)
      Hs=4*desvp;
      Zmax=(1/sqrt(8))*Hs*sqrt(log(length(heave)*DT/5));
      title(['serie ',arqdwv,' - Hs: ',num2str(Hs),' - Maximo estatistico:',num2str(Zmax),' - Spike: ',num2str(heave(k(j)))])
      plot([1 length(heave)],[10*desvp 10*desvp],'k--')
      plot([1 length(heave)],[-10*desvp -10*desvp],'k--')
      zoom on
      opt=input('Deseja corrigir o spike indicado em vermelho [s ou n]:','s');
      if opt == 's'
         heave(k(j))=(heave(k(j)-1)+heave(k(j)+1))/2;
         if abs(heave(k(j))) > abs(10*desvp)
            heave(k(j))=sign(heave)*desvp;
         end
      end
      plot(k(j),heave(k(j)),'mo');
      j=j+1;
   end
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

clear continua;clear string1;clear k;clear fid3;