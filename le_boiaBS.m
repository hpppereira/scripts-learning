function [heave,etaEW,etaNS,ano,mes,dia,hora,min,sdata,stime] = le_boiaBS(arqdwv)
%
% Funcao para leitura das series temporais de heave, etaNS, etaEW
% geradas pela boia Triaxys (13) na Bacia de Santos
%
% Eric Oliveira e Ricardo Campos 15/05/2009
% Leitura do arquivo 'arqdwv' com series temporais

% Abre arquivo com leitura de series temporais
fid=fopen(arqdwv,'r');
% Pula 3 linhas com comentarios do cabeçalho (no arquivo *.HNE)
fgetl(fid);fgetl(fid);fgetl(fid);
% Leitura da linha com data
linha=fgetl(fid);
datatexto=[linha(17:18) ,'-',linha([13:15]),'-',linha(8:11),linha(19:end),':00'];
tempo = datenum(datatexto);

sdata=datestr(tempo,24);
stime=datestr(tempo,15);

[ano mes dia hora min] = datevec(tempo);

fclose(fid);

[lixo,heave,etaNS,etaEW]=textread(arqdwv,'%f%f%f%f','headerlines',11);
   


%    heave=-heave;  
%    etaNS=-etaNS;
%    auxlixo = etaNS;
%    etaNS=etaEW;
%    etaEW=auxlixo;
   
% if max(etaNS) > 2.0 && max(etaNS) <= 12.0 
%   etaNS=etaNS/10;
% end
% 
% if max(etaEW) > 2.0 && max(etaEW) <= 12.0 
%   etaEW=etaEW/10;
% end
% 
% 
% if max(etaNS) > 12.0
%   etaNS=etaNS/100;
% end
% 
% if max(etaEW) > 12.0
%   etaEW=etaEW/100;
% end