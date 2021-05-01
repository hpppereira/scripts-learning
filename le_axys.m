function [heave,etaEW,etaNS,ano,mes,dia,hora,min,sdata,stime] = le_axys(arqdwv)
%
% Funcao para leitura das series temporais de heave, etaNS, etaEW
% geradas pela boia Axys na Bacia de Santos
%
% Eric Oliveira e Ricardo Campos 15/05/2009
% Leitura do arquivo 'arqdwv' com series temporais

% Abre arquivo com leitura de series temporais
fid=fopen(arqdwv,'r');
% Pula 3 linhas com comentarios do cabecalho (no arquivo *.HNE)
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

% % [lixo,heave,etaNS,etaEW]=textread(arqdwv,'%f%f%f%f','headerlines',11);
% % etaNS(etaNS==0)=0.00001;
% % etaEW(etaEW==0)=0.00001;
% % etaNS=heave./etaNS;
% % etaEW=heave./etaEW;
% 
% [lixo,heave,dspNS,dspEW]=textread(arqdwv,'%f%f%f%f','headerlines',11);
% 
% difdspNS=diff(dspNS);difdspNS(difdspNS==0)=0.01;
% etaNS=diff(heave)./difdspNS;
% etaNS(end+1)=etaNS(end);
% 
% difdspEW=diff(dspEW);difdspEW(difdspEW==0)=0.01;
% etaEW=diff(heave)./difdspEW;
% etaEW(end+1)=etaEW(end);
% 
% % Caso não dê exatamente as mesmas direções, tente fazer:
% %    etaNS=-heave/etaNS;
% %    etaEW=-heave/etaEW;
% % Ou
% %    heave=-heave;  
% %    etaNS=-etaNS;
% %    auxlixo = etaNS;
% %    etaNS=etaEW;
% %    etaEW=auxlixo;