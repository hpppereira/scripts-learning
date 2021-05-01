clear

%-------------------------------------------------------------
%ROTINA DE GERAÇAO DE REGISTROS DE ONDA
%-------------------------------------------------------------

%-------------------------------------------------------------
% Este programa gera registros aleatorios de ondas para serem
%utilizados nos testes dos modelos de calculo do espectro dire-
%cional. O numero maximo de pontos gerados e 1024.
%-------------------------------------------------------------
%Ultima atualizaçao 23/08/04



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


%-------------------------------------------------                                 
h=100;                                       
hsig=2.5;                                    
tp=12;                                     
fmin=1/1024;                                 
fmax=512/1024;                                     
dt=1;                                      
x=0;                                      
y=0;                                                                         
tetamean=60;                              
tetamax=75;                               
tetamin=45;                                
gama=3;                                       
smax=8;                                  
num=1024;                                 
km=100;                                   
kn=36;                                        

%-------------------------------------------------
%INICIALIZACAO DE  VARIAVEIS

g=9.81;
fp=1/tp; 
deltaf=(fmax-fmin)/(km-1);

%----------------------------------------------------
%CHAMA FUNÇAO DE CORREÇAO ANGULAR (function corrige)
%----------------------------------------------------

tetamean=corrige(tetamean);
tetamin=corrige(tetamin);
tetamax=corrige(tetamax);  

tetamin=tetamin*pi/180;
tetamean=tetamean*pi/180;
tetamax=tetamax*pi/180;

deltateta=(tetamax-tetamin)/(kn-1);

%CALCULO DOS SENOS E COSSENOS

for n=1:kn;
    teta=tetamin+(n-1)*deltateta; 
    oo=tetamean-teta;
    co(n)=cos(teta);
    si(n)=sin(teta);
    cs(n)=cos(oo);
    sn(n)=sin(oo);
    cn(n)=cos(-oo/2);
end

for m=1:km;
    
    f(m)=fmin+(m-1)*deltaf+rand*deltaf; 
    coss(1,m)=cos(2*pi*f(m)*dt);     
    sinn(1,m)=sin(2*pi*f(m)*dt);  
    codt(m)=coss(1,m);   
    sndt(m)=sinn(1,m);   
    k(m)=4*pi^2*f(m)^2/g;

%-----------------------------------------------
%Espectro Simulado
%-----------------------------------------------

    sf=fpierson(f(m), fp, gama, hsig);

%COEFICIENTE DE ESPALHAMENTO

    if f(m)<=fp;
        s=smax*(f(m)/fp)^5; 
    else
        s=smax/(f(m)/fp)^2.5; 
    end

%INTEGRAL DA FUNÇAO DE ESPALHAMENTO ANGULAR

    integ=0;
    for j=2:kn-1;
        integ=integ+cn(j)^(2*s)*deltateta;
    end
    somat=integ+((cn(1)^(2*s)+cn(kn)^(2*s))/2)*deltateta; 
    gzero=1/somat;
     
    for n=1:kn;
        
    %DETERMINACAO DA AMPLITUDE
    
        fase=rand*2*pi;
        
        gteta=gzero*cn(n)^(2*s);     
        a=sqrt(2*sf*deltaf)*sqrt(gteta*deltateta);
    
    %REDUÇAO GEOMETRICA DO PONTO DE ANALISE
        
        tt=k(m)*(x*cs(n)+y*sn(n))+fase;    
        
        ttc(m,n)=a*cos(tt);
        tts(m,n)=a*sin(tt);
        
        ttcx(m,n)=ttc(m,n)*k(m)*co(n);
        ttsx(m,n)=-tts(m,n)*k(m)*co(n);
        
        ttcy(m,n)=ttc(m,n)*k(m)*si(n);
        ttsy(m,n)=-tts(m,n)*k(m)*si(n);
        
        ttcxx(m,n)=-tts(m,n)*(k(m)*co(n))^2;
        ttsxx(m,n)=-ttc(m,n)*(k(m)*co(n))^2;
        
        ttcyy(m,n)=-tts(m,n)*(k(m)*si(n))^2;
        ttsyy(m,n)=-ttc(m,n)*(k(m)*si(n))^2;
    end
end

for i=1:num;
    
    pc=i*10/(num/10)
        
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
            
            cmx=cmx+ttcx(m,n);
            smx=smx+ttsx(m,n);
            
            cmy=cmy+ttcy(m,n);
            smy=smy+ttsy(m,n);
            
            cmxx=cmxx+ttcxx(m,n);
            smxx=smxx+ttsxx(m,n);
            
            cmyy=cmyy+ttcyy(m,n);
            smyy=smyy+ttsyy(m,n);
        end

        if i==1
            
            arg=2*pi*f(m)*t; 
            eta=eta+cm*cos(arg)+sm*sin(arg);
            etax=etax+smx*cos(arg)+cmx*sin(arg);
            etay=etay+smy*cos(arg)+cmy*sin(arg);
            etaxx=etaxx+smxx*cos(arg)+cmxx*sin(arg);
            etayy=etayy+smyy*cos(arg)+cmyy*sin(arg);
            coss(2,m)=coss(1,m); 
            sinn(2,m)=sinn(1,m); 
            
        else
            
            coss(2,m)=coss(1,m)*codt(m)-sinn(1,m)*sndt(m);  
            sinn(2,m)=sinn(1,m)*codt(m)+coss(1,m)*sndt(m);   
            eta=eta+cm*coss(2,m)+sm*sinn(2,m);
            etax=etax+smx*coss(2,m)+cmx*sinn(2,m);
            etay=etay+smy*coss(2,m)+cmy*sinn(2,m);
            etaxx=etaxx+smxx*coss(2,m)+cmxx*sinn(2,m);
            etayy=etayy+smyy*coss(2,m)+cmyy*sinn(2,m);
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
%save data neta netax netay netaxx netayy

registro=[neta' netax' netay' netaxx' netayy'];

save d:\users\joao\estagiarios\eduardo\registro1.txt -ascii registro