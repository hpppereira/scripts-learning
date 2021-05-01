clear,clc
%Rotina de geraçao de registros de onda

%Este programa gera registros aleatorios de ondas para serem utilizados nos
%testes dos modelos de calculo do espectro direcional. o numero maximo de
%pontos gerados eh 1024.



%Variaveis utilizadas no programa

%Variaveis:
%coss
%sinn
%ttc
%tts
%ttcx
%ttcy
%netax
%ttsy
%a = amplitude
%gzero
%g
%H = profundidade local
%i = contador
%m = contador
%n = contador
%tetamean = direçao media
%cm
%tetamim = direçao minima
%pc = contado de porcentagem de execuçao
%s
%t = periodo
%tetamax = direçao maxima
%fp = frequencia de pico
%gama = constante gama
%deltateta = incremento em direçao
%km = numero de frequencia
%x = posiçao x
%dt = incremento de tempo
%kn = numero de componentes de direçao
%y = posiçao y
%eta
%oo
%fase
%sm
%tp
%ss
%cmx
%tt
%cmy
%fmin = frequencia minima
%hsig = altura  significativa
%fmax = frequencia maxima
%teta = direçao 
%deltaf = incremento em frequncia
%num = numero de dados gerados
%etax

%Dados de entrada
'Lista de dados de entrada'
h=10;
hsig = input('Escolha a altura significativa da onda: ')
tp = input('Escolha o periodo de pico da onda: ')
fmin=1/1024 ;                                
fmax=512/1024;                                   
dt=1;                                      
x=0;                                      
y=0;                                                                         
tetamean=45;                              
tetamax=60;                               
tetamin=30;                                
gama=3;                                       
smax=8;                                  
num=1024;                                 
km=100;                                   
kn=36;                                        


%Inicializaçao de variaveis
g=9.81;
fp=1/tp; 
deltaf=(fmax-fmin)/(km-1);


%Correçao angular
tetamean=corrige(tetamean);
tetamin=corrige(tetamin);
tetamax=corrige(tetamax);  

tetamin=tetamin*pi/180;
tetamean=tetamean*pi/180;
tetamax=tetamax*pi/180;

deltateta=(tetamax-tetamin)/(kn-1);

%Calculo dos senos e cossenos
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


%Espectro Simulado
    sf=fpierson(f(m), fp, gama, hsig);

%Coeficiente de Espalhamento angular
    if f(m)<=fp;
        s=smax*(f(m)/fp)^5; 
    else
        s=smax/(f(m)/fp)^2.5; 
    end

%Integral da funçao de espalhamento angular
    integ=0;
    for j=2:kn-1;
        integ=integ+cn(j)^(2*s)*deltateta;
    end
    somat=integ+((cn(1)^(2*s)+cn(kn)^(2*s))/2)*deltateta; 
    gzero=1/somat;
     
    for n=1:kn;
        
%Determinaçao da amplitude
    
        fase=rand*2*pi;
        
        gteta=gzero*cn(n)^(2*s);     
        a=sqrt(2*sf*deltaf)*sqrt(gteta*deltateta);
    
%Reduçao geometrica do ponto de analise
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
    
    pc=i*10/(num/10);
        
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

registro=[neta' netax' netay' netaxx' netayy'];

direcao = input('Escolha a direçao (0,30 ou 45 graus): ')

x = 1:50; %Quantidade de coluna (é necessario gráfico 3d)
y = 1:40; %Quantidade de linha

if direcao == 0
    z1 = neta(1:50); % Total de 50 registros de elevação
    z2 = neta(1:50); % Todas os batedores de onda (z) no mesmo 
    z3 = neta(1:50); % registro, ou seja, mesma fase de onda.
    z4 = neta(1:50);
    z5 = neta(1:50);
    z6 = neta(1:50);
    z7 = neta(1:50);
    z8 = neta(1:50);
    z9 = neta(1:50);
    z10 = neta(1:50);
    z11 = neta(1:50);
    z12 = neta(1:50);
    z13 = neta(1:50);
    z14 = neta(1:50);
    z15 = neta(1:50);
    z16 = neta(1:50);
    z17 = neta(1:50);
    z18 = neta(1:50);
    z19 = neta(1:50);
    z20 = neta(1:50);
    z21 = neta(1:50);
    z22 = neta(1:50);
    z23 = neta(1:50);
    z24 = neta(1:50);
    z25 = neta(1:50);
    z26 = neta(1:50);
    z27 = neta(1:50);
    z28 = neta(1:50);
    z29 = neta(1:50);
    z30 = neta(1:50);
    z31 = neta(1:50);
    z32 = neta(1:50);
    z33 = neta(1:50);
    z34 = neta(1:50);
    z35 = neta(1:50);
    z36 = neta(1:50);
    z37 = neta(1:50);
    z38 = neta(1:50);
    z39 = neta(1:50);
    z40 = neta(1:50);
    figure(1)
    plot(neta(1:50))
    title('neta')
end

if direcao == 30
    z1 = neta(20.5:69.5); 
    z2 = neta(20:69);
    z3 = neta(19.5:68.5);
    z4 = neta(19:68);
    z5 = neta(18.5:67.5);
    z6 = neta(18:67);
    z7 = neta(17.5:66.5);
    z8 = neta(17:66);
    z9 = neta(16.5:65.5);
    z10 = neta(16:65);
    z11 = neta(15.5:64.5);
    z12 = neta(15:64);
    z13 = neta(14.5:63.5);
    z14 = neta(14:63);
    z15 = neta(13.5:62.5);
    z16 = neta(13:62);
    z17 = neta(12.5:61.5);
    z18 = neta(12:61);
    z19 = neta(11.5:60.5);
    z20 = neta(11:60);
    z21 = neta(10.5:59.5);
    z22 = neta(10:59);
    z23 = neta(9.5:58.5);
    z24 = neta(9:58);
    z25 = neta(8.5:57.5);
    z26 = neta(8:57);
    z27 = neta(7.5:56.5);
    z28 = neta(7:56);
    z29 = neta(6.5:55.5);
    z30 = neta(6:55);
    z31 = neta(5.5:54.5);
    z32 = neta(5:54);
    z33 = neta(4.5:53.5);
    z34 = neta(4:53);
    z35 = neta(3.5:52.5);
    z36 = neta(3:52);
    z37 = neta(2.5:51.5);
    z38 = neta(2:51);
    z39 = neta(1.5:50.5);
    z40 = neta(1:50);
    figure(1)
    plot(neta(1:70))
    title('neta')

end

if direcao == 45
    z1 = neta(40:89);
    z2 = neta(39:88);
    z3 = neta(38:87);
    z4 = neta(37:86);
    z5 = neta(36:85);
    z6 = neta(35:84);
    z7 = neta(34:83);
    z8 = neta(33:82);
    z9 = neta(32:81);
    z10 = neta(31:80);
    z11 = neta(30:79);
    z12 = neta(29:78);
    z13 = neta(28:77);
    z14 = neta(27:76);
    z15 = neta(26:75);
    z16 = neta(25:74);
    z17 = neta(24:73);
    z18 = neta(23:72);
    z19 = neta(22:71);
    z20 = neta(21:70);
    z21 = neta(20:69);
    z22 = neta(19:68);
    z23 = neta(18:67);
    z24 = neta(17:66);
    z25 = neta(16:65);
    z26 = neta(15:64);
    z27 = neta(14:63);
    z28 = neta(13:62);
    z29 = neta(12:61);
    z30 = neta(11:60);
    z31 = neta(10:59);
    z32 = neta(9:58);
    z33 = neta(8:57);
    z34 = neta(7:56);
    z35 = neta(6:55);
    z36 = neta(5:54);
    z37 = neta(4:53);
    z38 = neta(3:52);
    z39 = neta(2:51);
    z40 = neta(1:50);
    figure(1)
    plot(neta(1:90))
    title('neta')
    
end


tbz = [z1; z2; z3; z4; z5; z6; z7; z8; z9; z10; z11; z12; z13; z14; z15; z16; z17; z18; z19; z20; z21; z22; z23; z24; z25; z26; z27; z28; z29; z30; z31; z32; z33; z34; z34; z36; z37; z38; z39; z40];
tbz = flipud(tbz); %Iverter a ordem do vetor
x = x';
y = y';
tbz = tbz;
%[X,Y,Z] = meshgrid(x,y,z)
figure(2)


surf(x,y,tbz)

%ribbon(neta(1:40))
view(10,40)
axis([1 50 1 40 -10 3])

%Salva arquivo
%csvwrite('registromedio.txt',registromedio)
