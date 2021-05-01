% Exemplo de calculo de spreading do tutorial do WAFO
% S1=torsethaugen([],[6 8],1);
% D1 = spreading(101,'cos',pi/2,[15],[],0);
% D12 = spreading(101,'cos',0,[15],S1.w,1);
% SD1 = mkdspec(S1,D1);
% SD12 = mkdspec(S1,D12);
% figure;wspecplot(SD1,1), hold on, wspecplot(SD12,1); hold off
%
% Lendo espectro direcional do onda1h.m
dado=load('SP200806161800.esp2D');
%[freq,dir]=meshgrid(dado(2:end,1),dado(1,2:end));
freq=dado(2:end,1);dir=dado(1,2:end);
espec2D=dado(2:end,2:end);
figure;surf(dir,freq,espec2D);%shading flat;
title('espectro 2D do EMEM');ylabel('Freq (Hz)');xlabel('Dir(graus)');zlabel('Densidade (m2/Hz/rad)')
hs=4*sqrt( sum( sum(espec2D,2)*(dir(2)-dir(1))*pi/180)*(freq(2)-freq(1)));
disp(['Hs do espectro EMEM 2D =',num2str(hs)])

% Plotanod espectros omni-direcionais
espec=sum(espec2D,2)*(dir(2)-dir(1))*pi/180;
fig=figure;plot(freq,espec);grid on;hold on
title('Espectro Omnidirecional');xlabel('Freq (Hz)');
% Lendo espectro omni-direcional do onda1h (calculado pela FFT)
dado1=load('SP200806161800.esp');
figure(fig);plot(dado1(:,1),dado1(:,2),'r');
legend('espectro pela EMEM','espectro pela FFT')

% Testando espectro direcional calculado por rotinas do WAFO usando o
% espectro de JONSWAP e o parametro de edspalhamento s2
w=2*pi*freq;
hs1=7.59;tp1=13.42;vspk1=99.4431;vepk1=29.54932;vped1=205.69;alfa1=0.007608;gama1=1.70;
s2_vepk1=round(24.26);s2_vtpk1=round(36);
figure;S1=jonswap(w,[hs1 tp1 gama1],1);
daux=dir*pi/180;k=find(daux>pi);daux(k)=daux(k)-2*pi;
daux=[-pi sort(daux)];
%D1 = spreading(dir(1,:),'cos',vped1*pi/180,[24.26],[],0);
D1 = spreading(daux,'cos',vped1*pi/180,[s2_vtpk1],[],0);
SD1 = mkdspec(S1,D1);
figure;wspecplot(SD1,1);

% Plotando espectro calculado pelo WAFO na mesma escala do EMEM
thetaSD1= SD1.theta(2:end); thetaSD1(thetaSD1<0)=thetaSD1(thetaSD1<0)+2*pi;
[lixo kd]=sort(thetaSD1);
dirSD1=thetaSD1(kd)*180/pi; % Direção em graus
freqSD1=SD1.w/(2*pi); % Frequencia em Hertz
auxesp=SD1.S(kd,:);
auxespHz=(auxesp*2*pi)'; % Convertendo espectro para m2/Hz
hs=4*sqrt( sum( sum(auxespHz,2)*5.63*pi/180)*0.031/2/pi);
disp(['Hs do espectro JONSWAP s2 =',num2str(hs)])
figure;surf(dirSD1,freqSD1,auxespHz);
title('espectro pelo WAFO (JONSWAP e s2)');ylabel('Freq (Hz)');xlabel('Dir(graus)');zlabel('Densidade (m2/Hz/rad)')
%
% Montando espectro a partir da função EMEM e do s2
c2= gamma(s2_vtpk1+1)/(2*sqrt(pi)*gamma(s2_vtpk1+0.5)); % *(1/(2*pi));
espec2Ds=[];
% for j=1:length(freq)
%     for k=1:length(dir)
%         diffang=(dir(k)-vped1)*pi/180
%         espec2Ds(j,k)=espec(j)* (c2*cos(diffang/2).^(2*s2_vtpk1)); %/((dir(2)-dir(1))*pi/180);
%     end
% end

diffang=(dir-vped1)*pi/180;
for j=1:length(freq)
        espec2Ds(j,:)=espec(j)* (c2*cos(diffang/2).^(2*s2_vtpk1)); %/((dir(2)-dir(1))*pi/180);
end
figure;
surf(dir,freq,espec2Ds);
title('espectro pelo EMEM e s2');ylabel('Freq (Hz)');xlabel('Dir(graus)');zlabel('Densidade (m2/Hz/rad)')
hs=4*sqrt( sum( sum(espec2Ds,2)*(dir(2)-dir(1))*pi/180)*(freq(2)-freq(1)));
disp(['Hs do espectro EMEM e s2 =',num2str(hs)])
%
% Plotando espectro direcional na frequencia de pico
m=max(max(espec2D));[iff id]=find(espec2D == m);
figure;plot(dir,espec2D(iff,:),'m');grid on;hold on;
plot([0 360],[m/2 m/2],'m')
m=max(max(auxespHz));[iff id]=find(auxespHz == m);
plot(dirSD1,auxespHz(iff,:));
xlabel('Dir (graus)');ylabel('Densidade (m2/Hz/rad)')
plot([0 360],[m/2 m/2])
m=max(max(espec2Ds));[iff id]=find(espec2Ds == m);
plot(dir,espec2Ds(iff,:),'k');
plot([0 360],[m/2 m/2],'k')
legend('Espectro do EMEM 2D','3dB','Espectro JONSWAP com s2 pelo WAFO','3dB','Espectro do EMEM e s2','3dB')
