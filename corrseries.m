function[heave1,etaEW1,etaNS1]=corrseries(heave,etaEW,etaNS,transhf,transhm,DT);
% Funcao para correcao das series brutas de heave,
% etaEW e etaNS da boia WAVESCAN com as funcoes de
% transferencia fornecidas pela SEATEX
% Dados de saida: heave1 = serie de heave corrigida
%                 etaEW1 = serie de etaEW corrigida
%                 etaNS1 = serie de etaNS corrigida
%
% Autor:
% Carlos Eduardo Parente Ribeiro 
% 13/08/99
%
% Carregando a funcao de transferencia de heave
% para a boia WAVESCAN
f1=( 1/(length(heave)*DT):1/(length(heave)*DT):1/(2*DT) );
beta=f1/0.43;
q1=1-beta.^2;q2=2*beta*0.1;
transrm=1./sqrt(q1.^2+q2.^2);transrm=transrm';
transrf=angle(q1+j*q2);transrf=transrf';
% Função de transferencia trans2 enviada pela OCEANOR
%    IMPORTANTE: A função a seguir apresentou alguns
%    problemas no que diz respeito ao calculo de
%    Spreading. O Prof. Parente sugere provisoriamente
%    uma correção adaptativa.
trans2=(q1'+j*q2'); 

% Correção adaptativa fixa de fase: angfase=25 graus
%    OBS: Substitui provisoriamente a função acima
angfase=25;
zte=ones(512,1)*angfase*2*pi/360;
trans2=cos(zte)+j*sin(zte);

%corrigindo a série de heave
%a função foi carregada copm o bóia6.mat
h1=fft(heave);

trans1=transhm.*(cos(transhf)+j*sin(transhf));
gh1=h1(2:512).*trans1(1:511);
gh1=[h1(1);gh1;h1(257);flipud(conj(gh1))];
heave1=real(ifft(gh1));%volta para o tempo

%corrigindo a série de roll
r1=fft(etaEW);

gr1=r1(2:512).*trans2(1:511);
gr1=[r1(1);gr1;r1(257);flipud(conj(gr1))];
etaEW1=real(ifft(gr1));%volta para o tempo

%corrigindo a série de  pitch
p1=fft(etaNS);
gp1=p1(2:512).*trans2(1:511);
gp1=[p1(1);gp1;p1(257);flipud(conj(gp1))];
etaNS1=real(ifft(gp1));%volta para o tempo