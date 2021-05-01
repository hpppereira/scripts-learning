% PP slopearray.m %

load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000100_Convertido.gin.mat')
w1a=WAVE1A(3477:4500);
w2a=WAVE2A(3477:4500);
w3a=WAVE3A(3477:4500);
w4a=WAVE4A(3477:4500);
w5a=WAVE5A(3477:4500);

L=1000; %1 metro = 1000 mm. - Para ficar na mesma unidade que a elevação
deltat=tempo(2)-tempo(1);
donv=270;
% Achar inclinação etax e etay dos sensores externos
for i=1:length(w1a)
    etax(i)=(w1a(i)-w2a(i))/L;
    etay(i)=(w4a(i)-w1a(i))/L;
end
etax=etax';
etay=etay';
eta=w1a;


% % Achar Curvatura
% for i=1:length(w1a)
%     etaxx(i)=2*((w1a(i)-2*w5a(i)+w3a(i))/(L*sqrt(2)/2));
%     etayy(i)=2*((w4a(i)-2*w5a(i)+w2a(i))/(L*sqrt(2)/2));
% end
% etaxx=etaxx';
% etayy=etayy';

% % Achar inclinação etax_int e etay_int dos sensores internos
% for i=1:length(w1a)
%     netax_int(i)=(w1a(i)-w5a(i))/(L*sqrt(2)*2);
%     netay_int(i)=(w2a(i)-w5a(i))/(L*sqrt(2)*2);
% end
% netax=netax';
% netay=netay';

[aa]=slopearray(eta,etax,etay,deltat,donv);