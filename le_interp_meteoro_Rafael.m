tic
% Listando os arquivos na pasta de arqs de dados
diretorio='./'; %./dados/pch2
% diretorio='../../PVI/';
arqs_dados = dir([diretorio 'METEOS_YOUNG_PIER_*.txt']);
% Verificando o número de arquivos (=num de linhas de arqs_dados)
[l,c]=size(arqs_dados);  

% Barra de espera inicializacao
%h=waitbar(0,'Aguarde...');

cabeca=19; % cabecalho;
rabo=0;

Vint=[];Vdir=[];
Ur=[];Temp=[];Patm=[];
vData=[];n=[];
clear dado*
for k=1:l
    % Evolucao da barra de espera:
%     waitbar(k/l,h);
    
    [a,b]= readtext([diretorio arqs_dados(k).name], '[,\t]');
    arqdad=arqs_dados(k).name;
    for m=cabeca:(length(a)-rabo)
        dado=char(a(m));
        dados(m-cabeca+1,:)=str2num(dado(20:end));
       ano=str2num(dado(1:4)); mes=str2num(dado(6:7));
       dia=str2num(dado(9:10));
       hora=str2num(dado(12:13));minu=0;
       n(m-cabeca+1,:) =datenum(ano,mes,dia,hora,minu,0);
    end
    
    vData=[vData;n];
    Vint=[Vint;dados(:,1)];
    Vdir=[Vdir;dados(:,2)];
    Ur(k,:)=[Ur;dados(:,9)];
    Temp(k,:)=[Temp;dados(:,8)];
    Patm(k,:)=[Patm;dados(:,6)];
    
end
c = datevec(vData);

fclose all;
% close(h)

figure(11),hold on,plot(vData,Vint,'b'),grid on
datetick('x',20,'keepticks')
toc





clear a ano arqdad arqs* b c diret* dia h dado cabeca ans minu m l k hora rabo n mes dados