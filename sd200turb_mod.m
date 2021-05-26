% Rotina para redução de dados obtidos com o SD200 para extração de informações
% à cada 0.5 m
%
% Sintaxe
%				SAIDA = TRATASD200(ENTRADA)
%
% ENTRADA: matriz de 4 colunas [serie salinidade temperatura profundidade]
% SAIDA: matriz de 4 colunas [serie profunidade salinidade temperatura]

%dados=load('C:\Users\Henrique\Documents\MATLAB\CTD\dados_ctd_mod.txt');

% Serie / Meas / Sal. / TºC / Turb (FTU) / Dens / Prof / Dia / Mes / Ano / Hora / Min / Seg
%   1       2      3      4      5           6      7     8     9     10    11    12     14


%dados=dados(find(dados(:,7)>0),:);

%load c:\porto\p2002\grafico\p200206\po170602.dat
function saida=sd200turb_mod(dados)
%dados=mv;

serie=dados(:,1);
sal=dados(:,3);
temp=dados(:,4);
prof=-dados(:,7);
ano=dados(:,10);
mes=dados(:,9);
dia=dados(:,8);
hora=dados(:,11);
minuto=dados(:,12);
turb=dados(:,5);

saida=[0 0 0 0 0 0 0 0 0 0];
series=max(dados(:,1)); %quantidade total de series
j=1;
k=1;
for i=1:series %vai variar todas as series
   while serie(k) == i %enquanto estiver na primeira serie
      if k == length(serie)
         break %quando chegar até o ultimo dado, vai parar
      end
      pt(j)=prof(k);
      st(j)=sal(k);
      tb(j)=turb(k);
        tt(j)=temp(k);
     	k=k+1;
      j=j+1;
   end
   saisal=kungfu3(pt,st,0.5); %Pega só dados de descida
   saitemp=kungfu3(pt,tt,0.5);
   saiturb=kungfu3(pt,tb,0.5);
   
   for l=1:length(saisal(:,1))
      pegadata(l,:)=[ano(k-1) mes(k-1) dia(k-1) hora(k-1) minuto(k-1)];
   end
      
   sai=[saisal saitemp(:,2) saiturb(:,2) pegadata];
   seriesai=linspace(i,i,length(sai(:,1)))';
   sai=[seriesai sai];
   saida=[saida; sai];
   clear pt st tt pegadata
   j=1;
end

saida2=[0 0 0 0 0 0 0 0 0 0];
for i=1:length(saida)
   if saida(i,2) < 0 
      saida2(j,:) = saida(i,:);
      j=j+1;
   end
end
saida=saida2;
%save c:\carla\mare5.dat saida -ascii
%save c:\porto\p2002\grafico\p200206\saida.dat saida -ascii

%opcional para extrair dados de 1 em 1 metro, sem ser rodando como function
%j=1;
%for i=1:length(saida(:,1))
 %  if saida(i,2) ~= round(saida(i,2))
  %    pega(j,:) = saida(i,:);
   %   j=j+1;
   %end
   %end
%clear saida
%saida=pega;
   