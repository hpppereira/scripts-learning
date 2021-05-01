% Calcula parametros de onda no dominio da frequencia
%
% Elaborado por Henrique P. P. Pereira (henriqueppp@peno.coppe.ufrj.br)
%
% Ultima modificacao: 01/11/2012
%
% Dados de entrada: dt - intervalo de amostragem
%                   h - profundidade
%                   eta - vetor de elevacao
%                   etax - vetor de deslocamento em x
%                   etay - vetor de deslocamento em y
%
% Dados de saida: f - vetor de frequencias
%                 an - auto-espectro de eta
%                 anx - auto-espectro de etax
%                 any - auto-espectro de etay
%                 a1, b1 - coeficientes de fourier de 1 ordem
%                 diraz - vetor de direcao azimutal em graus
%                 dirm - vetor de direcao media
%                 dirtp - direcao associado a frequencia de pico
%                 fp - frequencia de pico
%                 tp - periodo de pico
%                 hm0 - altura significativa
%
% Subrotinas chamadas: spec
%                      spec2
%                      numeronda
%


function [f,an,anx,any,a1,b1,diraz,dirm,dirtp,fp,tp,hm0]=onda_freq(dt,h,eta,etax,etay,gl)


%% Calculo do espectro pela funcao spectrum (subrotina spec e spec2)

%graus de liberdade
% gl=2;

%calculo do espectro
[aan]=spec(eta,dt,gl);
[aannx]=spec2(eta,etax,dt,gl);
[aanny]=spec2(eta,etay,dt,gl);

f=aan(:,1);

%% Calculo do numero de onda 'k' (subrotina numeronda) verificar com parente
[k]=numeronda(h,f,length(f))'; 

%% Calcula os quad-espectros necessarios para o calculo de a1 e b1
qnnx=aannx(:,5); %quad-espectro de eta e etax
qnny=aanny(:,5); %quad-espectro de eta e etay
an=aan(:,2) ;%auto-espectro de eta
anx=aannx(:,3); %auto-espectro de etax
any=aanny(:,3); %auto-espectro de etay

%% Calculo da direcao da onda

% Calculo de a1 e b1 em radianos
for i=1:length(f)
    
    a1(i,1)=qnnx(i,1)/(k(i,1)*pi*an(i,1)); % qual usar, com ou sem o autoespectro?
    
    b1(i,1)=qnny(i,1)/(k(i,1)*pi*an(i,1));
            
end

% Calcula o angulo em radianos (forma correto neste caso) utilizando funcao 'angle'
%dirr=angle(a1+b1.*j);

% Calcula da direcao pelo arcotangente em radianos
dirr=atan(b1./a1);

% Passa de rad. para grau (trigonometrico)
dirt=dirr.*(180/pi);

%corrige erro de nan que esta dando  de nan no ultimo elemento
dirt(end) = dirt(end - 1);

diraz = dirt;
% Passa de trigonometrico para azimute
diraz = trig_para_azim(dirt);

%diraz=270-dirt;

% Muda de onde a onda vai para onde a onda vem (confirmar com parente)
%diraz=diraz-180;

% Condicao para valores maior que 360 e menores que 0
for i=1:length(diraz)
    
    if diraz(i)>360;
        
        diraz(i)=diraz(i)-360;
        
    elseif diraz(i)<0
        
        diraz(i)=diraz(i)+360;
        
    end
end
  
% Correcao da declinacao magnetica
%nao foi feita mais a direcao esta certa. 
%provavelmente a bussola da boia ja deve corrigir

%% Calcula parametros de onda

% Periodo de pico no espectro de eta
fp=aan(find(aan(:,2)==max(aan(:,2))),1);
tp=1/fp;

% Altura Hm0 calculado pela espectro de eta

% Delta de frequencia
df=f(2)-f(1);

% Momento espectral de ordem zero
m0=0;

for i=1:length(an)
    
    m0=m0+(an(i,1)*df);
    
end

% Calculo da alt sig, utilizando momento espectral de ordem zero
hm0=4.01*sqrt(m0);

% Cria matriz para [f diraz] para o calculo da direco de pico
fdir=[f,diraz];

% Direcao associada ao periodo de pico
dirtp=fdir(find(fdir(:,1)==fp),2);

% Direcao media
dirm=mean(diraz);

% Acha o numero de onda associado a frequencia de pico

% Cria matriz para [f k] para o calculo do numero de onda associado a frequencia de pico
fk=[f,k];

%numero de onda associado a frequencia de pico
kfp=fk(find(fk(:,1)==fp),2);