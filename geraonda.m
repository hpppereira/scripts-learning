%-------------------------------------------------------------
%ROTINA DE GERAÇAO DE REGISTROS DE ONDA
%-------------------------------------------------------------

%-------------------------------------------------------------
% Este programa gera registros aleatorios de ondas para serem
%utilizados nos testes dos modelos de calculo do espectro dire-
%cional. O numero maximo de pontos gerados e 1024.
%-------------------------------------------------------------

% Elaborado por Eduardo Vitarelli e Joao Luiz Baptista de Carvalho

%---------Variaveis utilizadas no programa--------------------

%COSS.........
%SINN.........
%TTC..........
%TTS..........
%TTCX.........
%TTSX.........
%TTCY.........
%NETAX........
%TTSY.........
%A............AMPLITUDE
%SAI$.........ARQUIVO DE SAIDA
%GZERO........
%G............
%H............PROFUNDIDADE LOCAL
%I............CONTADOR
%ENT$.........ARQUIVO ED SAIDA
%M............CONTADOR
%N............CONTADOR
%TETAMEAN.....DIREÇAO MEDIA
%CM...........
%TETAMIN......DIREÇAO MINIMA
%PC...........CONTADOR DE % DE EXECUÇAO
%S............
%T............PERIODO
%TETAMAX......DIREÇAO MAXIMA
%FP...........FREQUENCIA DE PICO
%GAMA.........CONSTANTE GAMA
%DELTATETA....INCREMENTO EM DIREÇAO
%KM...........NUMERO DE FREQUENCIA
%X............POSIÇAO X
%DT...........INCREMENTO DE TEMPO
%PI...........PI
%KN...........NUMERO DE COMPONENTES DE DIREÇAO
%Y............POSIÇAO Y
%ETA..........
%OO...........
%FASE.........FASE
%SM...........
%TP...........PERIODO DE PICO
%SS...........
%CMX..........
%TT...........
%CMY..........
%FMIN.........FREQUENCIA MINIMA
%HSIG.........ALTURA SIGNIFICATIVA
%FMAX.........FREQUENCIA MAXIMA
%TETA.........DIREÇAO
%DELTAF.......INCREMENTO EM FREQUENCIA
%NUM..........NUMERO DE DADOS GERADOS
%ETAX........


%INICIALIZACAO DE  VARIAVEIS
%------------------------------------------------     
clear

h=100;                                       
hsig=10;                                    
tp=10;                                        
fmin=0.05;                                    
fmax=0.15;                                    
dt=1;                                      
x=0;                                      
y=0;                                                                         
tetamin=60;   
tetamean=90;                              
tetamax=120;                               
                             
gama=3;                                       
smax=50;                                  
num=1024;                                 
km=100;                                   
kn=36;                                        
%-------------------------------------------------

g=9.81;
fp=1./tp;
deltaf=(fmax-fmin)/(km-1);

%----------------------------------------------------
%CHAMA FUNÇAO DE CORREÇAO ANGULAR (function corrige)
%----------------------------------------------------

tetamin=corrige(tetamin);
tetamean=corrige(tetamean);
tetamax=corrige(tetamax);  

tetamin=tetamin*pi/180;
tetamean=tetamean*pi/180;
tetamax=tetamax*pi/180;
deltateta=(tetamax-tetamin)/(kn-1);

%CALCULO DOS SENOS E COSSENOS
%-----------------------------------------------

for n=1:kn;
    teta=tetamin+(n-1)*deltateta;
    oo=tetamean-teta;
    co(n)=cos(teta);
    si(n)=sin(teta);
    cs(n)=cos(oo);
    sn(n)=sin(oo);
    cn(n)=cos(-oo/2);
end

%Calculo dos espectros
%-----------------------------------------------
ran=rand(1,1);

for m=1:km;
    
    f(m)=fmin+(m-1)*deltaf+ran*deltaf;
    
    coss(1,m)=cos(2*pi*f(m)*dt);     
    sinn(1,m)=sin(2*pi*f(m)*dt);  
    codt(m)=coss(1,m);   
    sndt(m)=sinn(1,m);   
    k(m)=4.*pi^2*f(m)^2/g;

%FUNCTION FPIERSON
%-----------------------------------------------

    sf=fpierson(f(m), fp, gama, hsig);

%COEFICIENTE DE ESPALHAMENTO
%-----------------------------------------------

    if f(m)<=fp;
        s=smax.*(f(m)./fp).^5; 
    else
        s=smax./(f(m)/fp)^2.5; 
    end

%INTEGRAL DA FUNÇAO DE ESPALHAMENTO ANGULAR
%-----------------------------------------------

    integ=0;
    for j=2:kn-1;
        integ=integ+cn(j)^(2.*s)*deltateta;
    end
    somat=integ+((cn(1)^(2.*s)+cn(kn)^(2.*s))/2)*deltateta; 
    gzero=1./somat;

    random=rand(1,1);
    
    for n=1:kn;
    
    %DETERMINACAO DA AMPLITUDE
    
        fase=rand*2.*pi;
        gteta=gzero.*cn(n)^(2.*s);      
        a=sqrt(2.*sf.*deltaf)*sqrt(gteta*deltateta);
    
    %REDUÇAO GEOMETRICA DO PONTO DE ANALISE
        
        tt=k(m)*(x*cs(n)+y*sn(n))+fase;    
        
        ttc(m,n)=a*cos(tt);
        tts(m,n)=a*sin(tt);
        
        ttsx(m,n)=ttc(m,n)*k(m)*co(n);
        ttcx(m,n)=-tts(m,n)*k(m)*co(n);
        
        ttsy(m,n)=ttc(m,n)*k(m)*si(n);
        ttcy(m,n)=-tts(m,n)*k(m)*si(n);
        
        ttsxx(m,n)=-tts(m,n)*(k(m)*co(n))^2;
        ttcxx(m,n)=-ttc(m,n)*(k(m)*co(n))^2;
        
        ttsyy(m,n)=-tts(m,n)*(k(m)*si(n))^2;
        ttcyy(m,n)=-ttc(m,n)*(k(m)*si(n))^2;
    end
end

for i=1:num;
    
    pc=i*10./(num/10)
    
    eta=0;
    etax=0;
    etay=0;
    etaxx=0;
    etayy=0;
    
    t=i*dt;

    for m=1:km;
        
        cm=0;
        sm=0;
        cmx=0;
        smx=0;
        cmy=0;
        smy=0;
        cmxx=0;
        smxx=0;
        cmyy=0;
        smyy=0;
        
        for n=1:kn;
            cm=cm+ttc(m,n);
            sm=sm+tts(m,n);
            
            smx=smx+ttcx(m,n);
            cmx=cmx+ttsx(m,n);
            
            smy=smy+ttcy(m,n);
            cmy=cmy+ttsy(m,n);
            
            smxx=smxx+ttcxx(m,n);
            cmxx=cmxx+ttsxx(m,n);
            
            smyy=smyy+ttcyy(m,n);
            cmyy=cmyy+ttsyy(m,n);
        end

        if i==1

            eta=eta+cm*cos(2.*pi*f(m)*t)+sm*sin(2.*pi*f(m)*t);
            etax=etax+cmx*cos(2.*pi*f(m)*t)+smx*sin(2.*pi*f(m)*t);
            etay=etay+cmy*cos(2.*pi*f(m)*t)+smy*sin(2.*pi*f(m)*t);
            etaxx=etaxx+cmxx*cos(2.*pi*f(m)*t)+smxx*sin(2.*pi*f(m)*t);
            etayy=etayy+cmyy*cos(2.*pi*f(m)*t)+smyy*sin(2.*pi*f(m)*t);
            coss(2,m)=coss(1,m); 
            sinn(2,m)=sinn(1,m); 
            
        else
            
            coss(2,m)=coss(1,m)*codt(m)-sinn(1,m)*sndt(m);  
            sinn(2,m)=sinn(1,m)*codt(m)+coss(1,m)*sndt(m);   
            eta=eta+cm*coss(2,m)+sm*sinn(2,m);
            etax=etax+cmx*coss(2,m)+smx*sinn(2,m);
            etay=etay+cmy*coss(2,m)+smy*sinn(2,m);
            etaxx=etaxx+cmxx*coss(2,m)+smxx*sinn(2,m);
            etayy=etayy+cmyy*coss(2,m)+smyy*sinn(2,m);
        end
        
    end
    
    for m=1:km;
        coss(1,m)=coss(2,m); 
        sinn(1,m)=sinn(2,m); 
    end
    
    neta(i)=eta;
    netax(i)=etax;
    netay(i)=etay;
    netaxx(i)=etaxx;
    netayy(i)=etayy;
end