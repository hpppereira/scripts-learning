 function [heave,etaEW,etaNS,ano,mes,dia,hora,min,sdata,stime,fig] = le_Waverider(arqdwv,DT,qualano,fig,fid1,bnome_arq_log); 
%
% Rotina montada pelo Eric Ribeiro para leitura das series brutas
% do Waverider MK-II (IEAPM e UFSC) - 11/08/2004
%
% Retorna os valores do arquivo de HEAVE, etaNS(=deslocamento NS),
% etaEW(=deslocamento EW), e vetores com data e hora.
%

testel=0;
while testel==0
    try
        dlmread(arqdwv); testel=1;
    catch
        arq_selecionado = ['Arquivo com problema de leitura!  ',arqdwv];
        display(arq_selecionado)
        alog = fopen(bnome_arq_log,'w+');
        fprintf(alog,'%s\n',arq_selecionado);
        fclose(alog);
        
        arqdwv=fscanf(fid1,'%s',1);
        if isempty(arqdwv); testel=1; return ;end
    end    
end





testel=0;
while testel==0
    if length(dlmread(arqdwv))==0
        testel=0; 
        arq_selecionado = ['Arquivo Vazio! ',arqdwv];
        display(arq_selecionado)
        alog = fopen(bnome_arq_log,'w+');
        fprintf(alog,'%s\n',arq_selecionado);
        fclose(alog);       
        
        arqdwv=fscanf(fid1,'%s',1);if isempty(arqdwv); return ;end        
        testell=0;
        while testell==0
            try
                dlmread(arqdwv); testell=1;
            catch             
                arq_selecionado = ['Arquivo com problema de leitura!  ',arqdwv];
                display(arq_selecionado)
                alog = fopen(bnome_arq_log,'w+');
                fprintf(alog,'%s\n',arq_selecionado);
                fclose(alog);
                           
                arqdwv=fscanf(fid1,'%s',1);if isempty(arqdwv); return ;end
            end
        end
        
    else
        testel=1;
    end
end

        

fim = length(arqdwv);
dia = arqdwv(fim- 9:fim- 8);
mes = arqdwv(fim-11:fim-10);
hora= arqdwv(fim- 7:fim- 6);
min = arqdwv(fim- 5:fim- 4);
ano = num2str(qualano);
sdata=[dia,'/',mes,'/',ano];
stime=[hora,':',min];

dia = str2num(dia);
mes = str2num(mes);
hora= str2num(hora);
min = str2num(min);
ano = str2num(ano);

m = csvread([arqdwv]);

% Leitura das colunas com series brutas
flag  = m(:,1); % Flag de qualidade do registro.
heave = m(:,2)./100; % Heave  % ESTAMOS TRABALHANDO EM METROS
etaNS = m(:,3)./100; % Pitch  % ESTAMOS TRABALHANDO EM METROS
etaEW = -m(:,4)./100; % Roll  % ESTAMOS TRABALHANDO EM METROS

%=========================================================================
% Retira de Spikes superiores a 5 vezes o Desvio padrao (STD)!!
%=========================================================================
% Calcula primeira estimativa de medias e desvio-padrao
diffabs = abs(diff(heave));  % Incremento sucessivos da serie temporal
[freq,bin]=hist(diffabs,10); % HItograma dos incrementos
[valmax, imax] = max(freq);  % Seleçao do incremento modal
diffmodal = bin(imax); % 
kin = find (diffabs < 3.*diffmodal);
mhe = mean(heave(kin)); men = mean(etaNS(kin)); mew = mean(etaEW(kin));
she = std(heave(kin)); sen = std(etaNS(kin)); sew = std(etaEW(kin));

% Corrige heave
k = find(abs(heave) >= 5*she+mhe);
heave(k) = mhe; etaNS(k) = men; etaEW(k) = mew; 
mhe = mean(heave); she = std(heave);

% Corrige etaNS
k = find(abs(etaNS) >= 5*sen+men);
heave(k) = mhe; etaNS(k) = men; etaEW(k) = mew; 
mhe = mean(heave); she = std(heave);
men = mean(etaNS); sen = std(etaNS);

% Corrige etaEW
k = find(abs(etaEW) >= 5*sew+mew);
heave(k) = mhe; etaNS(k) = men; etaEW(k) = mew; 

%=========================================================================
% Metodo Alternativo: NAO FUNCIONOU BEM COM AS SERIES DO WAVERIDER
% Retira os Spikes superiores ao incremtento modal metodo "Median Filter"
%=========================================================================
% diffabs = abs(diff(heave)); % Incremento sucessivos da serie temporal
% [freq,bin]=hist(diffabs,10); % HItograma dos incrementos
% [valmax, imax] = max(freq); % Seleçao do incremento modal
% diffmodal = bin(imax); % 
% kex = find (diffabs > 3.*diffmodal);
% kin = find (diffabs < 3.*diffmodal);
% mhe = mean(heave(kin)); men = mean(etaNS(kin)); mew = mean(etaEW(kin));
% heave(kex+1) = mhe; etaNS(kex+1) = men; etaEW(kex+1) = mew;

% diffabs = abs(diff(etaNS)); % Incremento sucessivos da serie temporal
% [freq,bin]=hist(diffabs,10); % HItograma dos incrementos
% [valmax, imax] = max(freq); % Seleçao do incremento modal
% diffmodal = bin(imax); % 
% kex = find (diffabs > 3.*diffmodal);
% kin = find (diffabs < 3.*diffmodal);
% mhe = mean(heave(kin)); men = mean(etaNS(kin)); mew = mean(etaEW(kin));
% heave(kex+1) = mhe; etaNS(kex+1) = men; etaEW(kex+1) = mew;
% 
% diffabs = abs(diff(etaEW)); % Incremento sucessivos da serie temporal
% [freq,bin]=hist(diffabs,10); % HItograma dos incrementos
% [valmax, imax] = max(freq); % Seleçao do incremento modal
% diffmodal = bin(imax); % 
% kex = find (diffabs > 3.*diffmodal);
% kin = find (diffabs < 3.*diffmodal);
% mhe = mean(heave(kin)); men = mean(etaNS(kin)); mew = mean(etaEW(kin));
% heave(kex+1) = mhe; etaNS(kex+1) = men; etaEW(kex+1) = mew;


%=========================================================================
% Plotagem das serie de Heave Pitch and Roll SOH PARA TESTE!!
%=========================================================================
% fig=fig+1;
% figure(fig)
% subplot(3,1,1),plot(heave,'r'),title(['heave - ver | Norte - verde | Leste -azul']);subplot(3,1,2),plot(etaNS,'g'),subplot(3,1,3),plot(etaEW,'b')
% h = warndlg('Series Corrigidas','Series Corrigidas');
% waitfor(h);