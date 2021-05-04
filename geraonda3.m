clear,clc

%%% Variveis de sada %%%
%neta - elevao
%netax - inclinao em x
%netay - inclinao em y
%netaxx - curvatura em x
%netayy - curvatura em y
%velx - velocidade horizontal em x
%vely - velocidade horizontal em y
%velz - velocidade vertical superficial (Dneta/Dt)
%velzz - velocidade vertical (Equao integral - papaer RAPPORT)
%velzzz - velocidade vertical (Dpot.vel/Dz)
%dt - intervalo de amostragem

%-------------------------------------------------------------
%ROTINA DE GERAAO DE REGISTROS DE ONDA
%-------------------------------------------------------------
                
                    %%%%%%%%%%%%%%%
%%% Adaptado para calcular as velocidade orbitais Vx e Vy e Vz %%%

%-------------------------------------------------------------
% Este programa gera registros aleatorios de ondas para serem
%utilizados nos testes dos modelos de calculo do espectro dire-
%cional. O numero maximo de pontos gerados e 1024.
%-------------------------------------------------------------
%Ultima atualizaao 23/08/04



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
%TETAMEAN.....DIREAO MEDIA
%CM...........
%TETAMIN......DIREAO MINIMA
%PC...........CONTADOR DE % DE EXECUAO
%S............
%T............PERIODO
%TETAMAX......DIREAO MAXIMA
%FP...........FREQUENCIA DE PICO
%GAMA.........CONSTANTE GAMA
%DELTATETA....INCREMENTO EM DIREAO
%KM...........NUMERO DE FREQUENCIA
%X............POSIAO X
%DT...........INCREMENTO DE TEMPO
%PI...........PI
%KN...........NUMERO DE COMPONENTES DE DIREAO
%Y............POSIAO Y
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
%TETA.........DIREAO
%DELTAF.......INCREMENTO EM FREQUENCIA
%NUM..........NUMERO DE DADOS GERADOS
%ETAX........


%-------------------------------------------------                                 
h=200;                                       
hsig=2.5;                       
tp=12;                   
fmin=1/1024;                                 
fmax=512/1024;                                     
dt=1;                                      
x=0;                                      
y=0;                                                                         
tetamean=180;                        
tetamax=tetamean+15; 
tetamin=tetamean-15; 
gama=3;                                       
smax=8;                                  
num=1024;                                 
km=100;                                   
kn=36;                                        
z=0; %henrique (valores de cota negativos)
d=1025; %(1.025 = g/cm^3) (1025 = kg/m^3)

%-------------------------------------------------
%INICIALIZACAO DE  VARIAVEIS

g=9.81;
fp=1/tp; 
deltaf=(fmax-fmin)/(km-1); %incremento de frequencia

%----------------------------------------------------
%CHAMA FUNAO DE CORREAO ANGULAR (function corrige)
%----------------------------------------------------

tetamean=corrige(tetamean);
tetamin=corrige(tetamin);
tetamax=corrige(tetamax);  

tetamin=tetamin*pi/180;
tetamean=tetamean*pi/180;
tetamax=tetamax*pi/180;

deltateta=(tetamax-tetamin)/(kn-1); %Incremento de direo

%CALCULO DOS SENOS E COSSENOS

for n=1:kn; %Variando a direo (36 vezes)
    teta=tetamin+(n-1)*deltateta;  %Calcula varias direes, de 45  75
    oo=tetamean-teta; %Calcula a direo em relao a direo mdia
    co(n)=cos(teta); %cosseno da direo
    si(n)=sin(teta); %seno da direo
    cs(n)=cos(oo); %cosseno da direo menos a media
    sn(n)=sin(oo); %seno da direo menos a media
    cn(n)=cos(-oo/2); %cosseno da direo menos a media /2
    
%     dir_teta(n,1)=teta; %henrique
%     dir_oo(n,1)=oo; %henrique
%     dir_teta(n,2)=teta*180/pi; %henrique
%     dir_oo(n,2)=oo*180/pi; %henrique
end

for m=1:km; %Variando a frequencia
    
    f(m)=fmin+(m-1)*deltaf+rand*deltaf; %Calacula a frequencia (aleatria)
    coss(1,m)=cos(2*pi*f(m)*dt);     %Cosseno da parte final da formula do eta (sem a fase)
    sinn(1,m)=sin(2*pi*f(m)*dt);     %Seno da parte final da formula da inclinao (sem a fase)
    codt(m)=coss(1,m);   %Coloca os valores de coss em codt (cria um vetor codt com os valores de cos 2pift)
    sndt(m)=sinn(1,m);   %Coloca os valores de sinn em sndt
    k(m)=4*pi^2*f(m)^2/g;            %Calcula os valores de k (numero de onda)
    periodo(m)=1/f(m); %henrique
%-----------------------------------------------
%Espectro Simulado
%-----------------------------------------------

    sf=fpierson(f(m), fp, gama, hsig); %um valor de 'sf' para cada frequencia

%COEFICIENTE DE ESPALHAMENTO

    if f(m)<=fp;
        s=smax*(f(m)/fp)^5; 
    else
        s=smax/(f(m)/fp)^2.5; 
    end

%INTEGRAL DA FUNAO DE ESPALHAMENTO ANGULAR

    integ=0;
    for j=2:kn-1;
        integ=integ+cn(j)^(2*s)*deltateta; %faz um somatrio (integral)
    end
    somat=integ+((cn(1)^(2*s)+cn(kn)^(2*s))/2)*deltateta; 
    gzero=1/somat;
     
    for n=1:kn; %variar a direo
        
    %DETERMINACAO DA AMPLITUDE
    
        fase=rand*2*pi; %determinao da fase aleatria (funo rand) para cada componente de direo
        
        gteta=gzero*cn(n)^(2*s);     
        a=sqrt(2*sf*deltaf)*sqrt(gteta*deltateta); %Oq faz o gteta? o 2 no precisa estar fora?
    
    %REDUAO GEOMETRICA DO PONTO DE ANALISE
        
        tt=k(m)*(x*cs(n)+y*sn(n))+fase;     %Parte das frmulas integrais dentro do colchetes [] (sem o 2*pi*f*t)
        
        ttc(m,n)=a*cos(tt);     %"Cm" tese joao (Parte da esquerda das frmulas inegrais (cos --> eta e etaxx (elevao e curvatura))
        tts(m,n)=a*sin(tt);     %"Sm" tese joao (sin --> etax (inclinao)
        
        ttcx(m,n)=ttc(m,n)*k(m)*co(n); %"Sm' em x" - tese joao (Parte da direita entre colchetes da formula da inclinao (+) com o cosseno(ttc) * co(n)
        ttsx(m,n)=-tts(m,n)*k(m)*co(n); %"Cm' em x" -  teste joao (Parte da direita entre colchetes da formula da inclinao (-) com o seno(tts) * co(n)
        
        ttcy(m,n)=ttc(m,n)*k(m)*si(n); %"Sm' em y" - tese joao (Parte da direita entre colchetes da formula da inclinao (+) com o cosseno(ttc) * si(n)
        ttsy(m,n)=-tts(m,n)*k(m)*si(n); %"Cm' em y" - tese joao (Parte da direita entre colchetes da formula da inclinao (+) com o cosseno(ttc) * si(n)
        
        ttcxx(m,n)=-tts(m,n)*(k(m)*co(n))^2;    %"Sm'' em x" - tese joao (Parte da direita entre colchetes da formula da curvatura (-) com o cosseno(ttc) * co(n)^2
        ttsxx(m,n)=-ttc(m,n)*(k(m)*co(n))^2;    %"Cm'' em x" - tese joao (Parte da direita entre colchetes da formula da curvatura (-) com o seno(tts) * co(n)^2
        
        ttcyy(m,n)=-tts(m,n)*(k(m)*si(n))^2;    %"Sm'' em y" - tese joao (Parte da direita entre colchetes da formula da elevao (-) com o seno(tts) * si(n)^2
        ttsyy(m,n)=-ttc(m,n)*(k(m)*si(n))^2;    %"Cm'' em y" - tese joao (Parte da direita entre colchetes da formula da curvatura (-) com o cosseno(ttc) * si(n)^2
        
        ttcvx(m,n)=-ttc(m,n)*(2*pi*f(m)*cosh(k(m)*(h+z))*co(n))/sinh(k(m)*h); %Henrique - Calculo de Vx positivo pq deriva o cosseno e fica seno
        ttsvx(m,n)=-tts(m,n)*(2*pi*f(m)*cosh(k(m)*(h+z))*co(n))/sinh(k(m)*h); %henrique - positivo pq deriva o cosseno e fica seno
        
        ttcvy(m,n)=-ttc(m,n)*(2*pi*f(m)*cosh(k(m)*(h+z))*si(n))/sinh(k(m)*h); %Henrique - Calculo de vy positivo pq deriva o cosseno e fica seno
        ttsvy(m,n)=-tts(m,n)*(2*pi*f(m)*cosh(k(m)*(h+z))*si(n))/sinh(k(m)*h); %henrique - positivo pq deriva o cosseno e fica seno
        
        ttcvz(m,n)=+tts(m,n)*2*pi*f(m); %henrique - frmula derivando o eta no tempo - negativo pq quero saber o cosseno, que  menos seno
        ttsvz(m,n)=-ttc(m,n)*2*pi*f(m); %henrique - positivo pq quero saber o cosseno, que a derivada de seno  cosseno
        
        ttcvzz(m,n)=+tts(m,n)*(2*pi*f(m)*sinh(k(m)*(h+z))/sinh(k(m)*h)); %henrique - velocidade vertical (deriva eta em t) - negativo pq quero saber o cosseno, que  menos seno
        ttsvzz(m,n)=-tts(m,n)*(2*pi*f(m)*sinh(k(m)*(h+z))/sinh(k(m)*h)); %henrique - formula paper rapport - positivo pq quero saber o cosseno, que a derivada de seno  cosseno 
        
        ttcvzzz(m,n)=tts(m,n)*(g/(2*pi*f(m)))*(sinh(k(m)*(h+z))/cosh(k(m)*h))*k(m); %henrique - vel z derivando o pot. de vel em z - negativo pq quero saber o cosseno, que  menos seno
        ttsvzzz(m,n)=-ttc(m,n)*(g/(2*pi*f(m)))*(sinh(k(m)*(h+z))/cosh(k(m)*h))*k(m); %henrique - vel z derivando o pot. de vel em z - positivo pq quero saber o cosseno, que a derivada de seno  cosseno 
        
        ttcp(m,n)=ttc(m,n)*(d*g*cosh(k(m)*(h+z))/sinh(k(m)*h)); %henrique - presso
        ttsp(m,n)=tts(m,n)*(d*g*cosh(k(m)*(h+z))/sinh(k(m)*h)); %henrique

    end
end

for i=1:num; %Variando a quantidade de registros (1024)
    
    pc=i*10/(num/10) %Calcula o periodo de corte
        
    eta=0;
    etax=0;
    etay=0;
    etaxx=0;
    etayy=0;
    vx=0; %henrique
    vy=0; %henrique
    vz=0; %henrique
    vzz=0; %henrique
    vzzz=0; %henrique
    p=0; %henrique
    
    t=i*dt; %Criar valor de tempo, passando de 1 em 1

    for m=1:km; %Variando a frequencia
        
        cm=0; %para cada novo valor de f, vai ser zerado o cm, sm....
        sm=0;
        cmx=0;
        smx=0;
        cmy=0;
        smy=0;
        cmxx=0;
        smxx=0;
        cmyy=0;
        smyy=0;
        cvx=0; %henrique - vel x cosseno
        svx=0; %henrique - vel x seno
        cvy=0; %henrique - vel y cosseno
        svy=0; %henrique - vel y seno
        cvz=0; %henrique - vel z cosseno
        svz=0; %henrique - vel z seno
        cvzz=0; %henrique - vel zz cosseno
        svzz=0; %henrique - vel zz seno
        cvzzz=0; %henrique - vel zzz cosseno
        svzzz=0; %henrique - vel zzz seno
        cp=0; %henrique - pressao cosseno
        sp=0; %henrique - pressao seno
        
        for n=1:kn; %Variando a direo
            
            cm=cm+ttc(m,n); %somatrio dos senos em cada frequencia
            sm=sm+tts(m,n); %elevao - seno
            
            cmx=cmx+ttcx(m,n); %inclinao em x
            smx=smx+ttsx(m,n);
            
            cmy=cmy+ttcy(m,n); %inclinao em y
            smy=smy+ttsy(m,n);
            
            cmxx=cmxx+ttcxx(m,n); %curvatura em x
            smxx=smxx+ttsxx(m,n);
            
            cmyy=cmyy+ttcyy(m,n); %curvatura em y
            smyy=smyy+ttsyy(m,n);
            
            cvx=cvx+ttcvx(m,n); %henrique - Vx
            svx=svx+ttsvx(m,n); %henrique
            
            cvy=cvy+ttcvy(m,n); %henrique - Vy
            svy=svy+ttsvy(m,n); %henrique
            
            cvz=cvz+ttcvz(m,n); %henrique - Vz - derivando o eta
            svz=svz+ttsvz(m,n); %henrique        
            
            cvzz=cvzz+ttcvzz(m,n); %henrique - Vz - formula rapport
            svzz=svzz+ttsvzz(m,n); %henrique
            
            cvzzz=cvzzz+ttcvzzz(m,n); %henrique - Vz derivando o pot de vel em z
            svzzz=svzzz+ttsvzzz(m,n); %henrique
            
            cp=cp+ttcp(m,n); %henrique - Presso
            sp=sp+ttsp(m,n); %henrique
        end

        if i==1 %quando o registro for 1 (vai calcular s uma vez) -> no precisa variar em direo , s em frequencia
            
            arg=2*pi*f(m)*t; 
            eta=eta+cm*cos(arg)+sm*sin(arg); %cm = somatrio dos cossenos e sm somatrio dos senos
            etax=etax+smx*cos(arg)+cmx*sin(arg);
            etay=etay+smy*cos(arg)+cmy*sin(arg);
            etaxx=etaxx+smxx*cos(arg)+cmxx*sin(arg);
            etayy=etayy+smyy*cos(arg)+cmyy*sin(arg);
            vx=vx+cvx*cos(arg)+svx*sin(arg); %henrique - vel x
            vy=vy+cvy*cos(arg)+svy*sin(arg); %henrique - vel y
            vz=vz+cvz*cos(arg)+svz*sin(arg); %henrique  - vel z derivando o eta no tempo
            vzz=vzz+cvzz*cos(arg)+svzz*sin(arg); %henrique - vel z formula rapport
            vzzz=vzzz+cvzzz*cos(arg)+svzzz*sin(arg); %henrique - vel z derivando o pot. de vel em z
            p=p+cp*cos(arg)+sp*sin(arg); %henrique - pressao
            
            coss(2,m)=coss(1,m);  %coss(1,m) = cos(2*pi(f(m)*dt)
            sinn(2,m)=sinn(1,m);  %sinn(1,m) = sin(2*pi(f(m)*dt)
            
        else
            
            coss(2,m)=coss(1,m)*codt(m)-sinn(1,m)*sndt(m);  
            sinn(2,m)=sinn(1,m)*codt(m)+coss(1,m)*sndt(m);   
            eta=eta+cm*coss(2,m)+sm*sinn(2,m);
            etax=etax+smx*coss(2,m)+cmx*sinn(2,m);
            etay=etay+smy*coss(2,m)+cmy*sinn(2,m);
            etaxx=etaxx+smxx*coss(2,m)+cmxx*sinn(2,m);
            etayy=etayy+smyy*coss(2,m)+cmyy*sinn(2,m);
            vx=vx+cvx*coss(2,m)+svx*sinn(2,m); %henrique - vel x
            vy=vy+cvy*coss(2,m)+svy*sinn(2,m); %henrique - vel y
            vz=vz+cvz*coss(2,m)+svz*sinn(2,m); %henrique - derivando o eta no tempo
            vzz=vzz+cvzz*coss(2,m)+svzz*sinn(2,m); %henrique - vel z
            vzzz=vzzz+cvzzz*coss(2,m)+svzzz*sinn(2,m); %henrique - vel z derivando o pot. de vel em z
            p=p+cp*coss(2,m)+sp*sinn(2,m); %henrique - pressao

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
    velx(i)=vx; %henrique
    vely(i)=vy; %henrique
    velz(i)=vz; %henrique
    velzz(i)=vzz; %henrique
    velzzz(i)=vzzz; %henrique
    pr(i)=p; %henrique
end 

%% Salvar registros

registro180=[neta',velx',vely',velzzz'];
%registro150=[neta',netax',netay',netaxx',netayy',velx',vely',velzzz',pr'];

%Para salvar: registro.txt -> nome do arquivo a ser salvo / -ascii registro -> nome da variavel a salvar

save registro180.txt -ascii registro180


