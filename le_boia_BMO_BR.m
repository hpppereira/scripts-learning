function [heave,roll,pitch,compas,ano,mes,dia,hora,min,sdata,stime] = le_boia_BMO_BR(arqdwv,dt)
%
% Funcao para leitura das series temporais de heave, pitch, roll
% geradas pela BMO BR 
%
% Ricardo Campos 11/05/2011
% Leitura do arquivo 'arqdwv' com series temporais
% Heave, Pitch, Roll e Compass
% Considera o Compass = YAW da bóia


%%
% Abre arquivo com leitura de series temporais
fid=fopen(arqdwv,'r');
% Pula 2 linhas com comentarios do cabeçalho 
fgetl(fid);fgetl(fid);

% Data 
linha=fgetl(fid);
datatexto=[linha(7:10),'-',linha([4:5]),'-',linha(1:2),' ',linha(12:19)];
tempo = datenum(datatexto);
sdata=datestr(tempo,24);
stime=datestr(tempo,15);
[ano mes dia hora min] = datevec(tempo);


% flag para ler 20 min ou 40 min. 
f=20;
% f=40;

if f==20
    
     roll(1)=str2num(linha(432:441));  % ROLL
     pitch(1)=str2num(linha(443:452)); % PITCH
     heave(1)=str2num(linha(465:474));
     yaw(1)=str2num(linha(454:463));
%    roll(1)=str2num(linha(267:276)); % Ax
%    pitch(1)=str2num(linha(278:287)); % Ay   
%    roll(1)=str2num(linha(300:309));  % GiroX
%    pitch(1)=str2num(linha(311:320));  % GiroY
    

    for i=1:(1200-1)
        linha=fgetl(fid);
         roll(i+1)=str2num(linha(432:441));  % ROLL
         pitch(i+1)=str2num(linha(443:452));  % PITCH
         heave(i+1)=str2num(linha(465:474));
         yaw(i+1)=str2num(linha(454:463));         
%         roll(1+1)=str2num(linha(267:276)); % Ax
%         pitch(1+1)=str2num(linha(278:287));  % Ay
%         roll(1+1)=str2num(linha(300:309));  % GiroX
%         pitch(1+1)=str2num(linha(311:320)); % GiroY
        

    end
    
elseif f==40
    
    roll(1)=str2num(linha(432:441));
    pitch(1)=str2num(linha(443:452));
    heave(1)=str2num(linha(465:474));
    yaw(1)=str2num(linha(454:463));
    for i=1:(2399-1)
        linha=fgetl(fid);
        roll(i+1)=str2num(linha(432:441));
        pitch(i+1)=str2num(linha(443:452));
        heave(i+1)=str2num(linha(465:474));
        yaw(i+1)=str2num(linha(454:463));
    end
    
end

fclose(fid);

heave=detrend(heave);
roll=detrend(roll);
pitch=detrend(pitch);
a=find(yaw<0);yaw(a)=360+yaw(a);clear a;
a=find(yaw>360);yaw(a)=360-yaw(a);clear a;
compas=yaw';


% Transformando series em vetores coluna
[lin col]=size(heave);if lin == 1;heave=heave';end
[lin col]=size(pitch);if lin == 1;pitch=pitch';end
[lin col]=size(roll);if lin == 1;roll=roll';end
[lin col]=size(compas);if lin == 1;compas=compas';end

% figure;
% subplot(4,1,1);plot(heave,'k');hold on;
% subplot(4,1,2);plot(pitch,'k');hold on;
% subplot(4,1,3);plot(roll,'k');hold on;
% subplot(4,1,4);plot(compas,'k');hold on;

% Filtro passa-alta -----------------------
Thpass=10.; % Thpass=25.;
heave = highpass_filter(heave,dt,Thpass);
roll = highpass_filter(roll,dt,Thpass);
pitch = highpass_filter(pitch,dt,Thpass); %inverter o pitch (ou heave e roll)
% -----------------------------------------


% Filtragem do compas - Medias moveis 5 pontos ---------------------
ucompas=cos(compas.*(pi/180));
vcompas=sin(compas.*(pi/180));

nucompas(1:2,1)=ucompas(1:2,1);
nucompas((length(ucompas)-1):length(ucompas),1)=ucompas((length(ucompas)-1):length(ucompas),1);
for i=3:length(nucompas)-2
 nucompas(i,1)=(ucompas(i-2)+ucompas(i-1)+ucompas(i)+ucompas(i+1)+ucompas(i+2))./5;
end

nvcompas(1:2,1)=vcompas(1:2,1);
nvcompas((length(vcompas)-1):length(vcompas),1)=vcompas((length(vcompas)-1):length(vcompas),1);
for i=3:length(nvcompas)-2
 nvcompas(i,1)=(vcompas(i-2)+vcompas(i-1)+vcompas(i)+vcompas(i+1)+vcompas(i+2))./5;
end

compas=atan2(nvcompas,nucompas).*(180/pi);
compas(compas<0)=compas(compas<0)+360;
% ---------



% subplot(4,1,1);plot(heave,'r-.');
% subplot(4,1,2);plot(pitch,'r-.');
% subplot(4,1,3);plot(roll,'r-.');
% subplot(4,1,4);plot(compas,'r-.');
%

return





