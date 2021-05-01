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

x = 1:50; %Para fazer os gráficos 3d??
y = 1:40;

if direcao == 0
    
    for i = 1:100
        z1 = neta(i:49+i);
        z2 = neta(i:49+i);
        z3 = neta(i:49+i);
        z4 = neta(i:49+i);
        z5 = neta(i:49+i);
        z6 = neta(i:49+i);
        z7 = neta(i:49+i);
        z8 = neta(i:49+i);
        z9 = neta(i:49+i);
        z10 = neta(i:49+i);
        z11 = neta(i:49+i);
        z12 = neta(i:49+i);
        z13 = neta(i:49+i);
        z14 = neta(i:49+i);
        z15 = neta(i:49+i);
        z16 = neta(i:49+i);
        z17 = neta(i:49+i);
        z18 = neta(i:49+i);
        z19 = neta(i:49+i);
        z20 = neta(i:49+i);
        z21 = neta(i:49+i);
        z22 = neta(i:49+i);
        z23 = neta(i:49+i);
        z24 = neta(i:49+i);
        z25 = neta(i:49+i);
        z26 = neta(i:49+i);
        z27 = neta(i:49+i);
        z28 = neta(i:49+i);
        z29 = neta(i:49+i);
        z30 = neta(i:49+i);
        z31 = neta(i:49+i);
        z32 = neta(i:49+i);
        z33 = neta(i:49+i);
        z34 = neta(i:49+i);
        z35 = neta(i:49+i);
        z36 = neta(i:49+i);
        z37 = neta(i:49+i);
        z38 = neta(i:49+i);
        z39 = neta(i:49+i);
        z40 = neta(i:49+i);
        
        tbz = [z1; z2; z3; z4; z5; z6; z7; z8; z9; z10; z11; z12; z13; z14; z15; z16; z17; z18; z19; z20; z21; z22; z23; z24; z25; z26; z27; z28; z29; z30; z31; z32; z33; z34; z34; z36; z37; z38; z39; z40];
        tbz = flipud(tbz);
        x = x';
        y = y';
        %[X,Y,Z] = meshgrid(x,y,z)
        surf(x,y,tbz)
        %ribbon(neta(1:40))
        view(10,40)
        axis([1 50 1 40 -10 3])
        M(i) = getframe        
    end
    movie(M)
end

if direcao == 30
    for i = 1:0.5:200
        z1 = neta(19.5+i:68.5+i);
        z2 = neta(19+i:68+i);
        z3 = neta(18.5+i:67.5+i);
        z4 = neta(18+i:67+i);
        z5 = neta(17.5+i:66.5+i);
        z6 = neta(17+i:66+i);
        z7 = neta(16.5+i:65.5+i);
        z8 = neta(16+i:65+i);
        z9 = neta(15.5+i:64.5+i);
        z10 = neta(15+i:64+i);
        z11 = neta(14.5+i:63.5+i);
        z12 = neta(14+i:63+i);
        z13 = neta(13.5+i:62.5+i);
        z14 = neta(13+i:62+i);
        z15 = neta(12.5+i:61.5+i);
        z16 = neta(12+i:61+i);
        z17 = neta(11.5+i:60.5+i);
        z18 = neta(11+i:60+i);
        z19 = neta(10.5+i:59.5+i);
        z20 = neta(10+i:59+i);
        z21 = neta(9.5+i:58.5+i);
        z22 = neta(9+i:58+i);
        z23 = neta(8.5+i:57.5+i);
        z24 = neta(8+i:57+i);
        z25 = neta(7.5+i:56.5+i);
        z26 = neta(7+i:56+i);
        z27 = neta(6.5+i:55.5+i);
        z28 = neta(6+i:55+i);
        z29 = neta(5.5+i:54.5+i);
        z30 = neta(5+i:54+i);
        z31 = neta(4.5+i:53.5+i);
        z32 = neta(4+i:53+i);
        z33 = neta(3.5+i:52.5+i);
        z34 = neta(3+i:52+i);
        z35 = neta(2.5+i:51.5+i);
        z36 = neta(2+i:51+i);
        z37 = neta(1.5+i:50.5+i);
        z38 = neta(1+i:50+i);
        z39 = neta(0.5+i:49.5+i);
        z40 = neta(i:49+i);
        
        tbz = [z1; z2; z3; z4; z5; z6; z7; z8; z9; z10; z11; z12; z13; z14; z15; z16; z17; z18; z19; z20; z21; z22; z23; z24; z25; z26; z27; z28; z29; z30; z31; z32; z33; z34; z34; z36; z37; z38; z39; z40];
        
        tbz = flipud(tbz);
        x = x';
        y = y';
        %[X,Y,Z] = meshgrid(x,y,z)
        surf(x,y,tbz)
        %ribbon(neta(1:40))
        view(10,40)
        axis([1 50 1 40 -10 3])
        M(i) = getframe        
    end
    movie(M)
    
end

if direcao == 45
    for i=1:100
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
        z38 = neta(2+i:51+i);
        z39 = neta(i+1:50+i);
        z40 = neta(i:49+i);
        
        figure(1)
        plot(neta(1:90))
        title('neta')
        
    end
end


tbz = [z1; z2; z3; z4; z5; z6; z7; z8; z9; z10; z11; z12; z13; z14; z15; z16; z17; z18; z19; z20; z21; z22; z23; z24; z25; z26; z27; z28; z29; z30; z31; z32; z33; z34; z34; z36; z37; z38; z39; z40];
tbz = flipud(tbz);
x = x';
y = y';
%[X,Y,Z] = meshgrid(x,y,z)
figure(2)


surf(x,y,tbz)

%ribbon(neta(1:40))
view(10,40)
axis([1 50 1 40 -10 3])

%Salva arquivo
%csvwrite('registromedio.txt',registromedio)
