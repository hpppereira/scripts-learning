

%**************************************************************************
% Rotina daatsiiodocnovo para uso da DAAT com series
% de heave, pitch + roll dda bóia SIDOC de Arraial do Cabo
%******************************************************

%arquivos iniciais - uma direçaõ e um espectro para cada  faixa (4) de
%frequencia; energ: Hs "de aceleração", energia em 4 faixas + 4 maiores
%periodos de pico
%Os arquivos são para um mes de 31 dias, com medições a cada hora

diresio=zeros(744,4);%direção
espesio=zeros(744,4);%espectros
energsio=zeros(9,744);%Hs(?)+4 energias(uma por faixa)+4 maiores picos
picpic=zeros(744,1);
angulo=zeros(90,744);%compa15=zeros(744,4);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%carregar os dados de um mes: vento e onda
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
load wind.txt
load pitch_corr.txt
load heave.txt
load roll_corr.txt
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
zco=heave;
zdd=pitch_corr;
zdc=roll_corr;
clear heave pitch_corr roll_corr
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%dados iniciais
df=1/128;dt=1;
%vetor de frequencias
f=df:df:0.5;
w4=(2*pi*f').^4;
fa=1/dt;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%preparo de wavelets com 3 ciclos correspondentes a periodos de ordem
%6 até 64 - correspondem a uma analise de 128 pontos com dt=1 segundo 
%- são 59 wavelets.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

t1=1./f';t2=round(3*t1);
t2=t2(6:64);
wavecos=zeros(64,59);wavesen=wavecos;
%wavelets do tipo morlet com janela de hanning
%as wavelets são calculadas apenas uma vez para toda o mes

for i=1:59,
    out2=linspace(-3.14,3.14,t2(i));
    gau=hanning(t2(i));
    out1 =gau'.* cos(3*out2);
    out3 =gau'.* sin(3*out2);
    wavecos((1:t2(i))',i)=out1';
    wavesen((1:t2(i))',i)=out3';
end;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% tabela de senos e cosenos para a analise de máxima entropia
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
load lyg2.mat;
a26=[a23(311:360) a23 a23(1:50)];
a27=[a24(311:360) a24 a24(1:50)];
a30=[(311:360) (1:360) (1:50)];
grad1=0.0175;grad2=180/pi;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%CÁLCULO DA DAAT
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for kkl=1:744,
    ww55=zeros(9,1);%para o energ
    co=zco(:,kkl);co=co-mean(co);
    dd=zdd(:,kkl);dd=dd-mean(dd);
    dc=zdc(:,kkl);dc=dc-mean(dc);
    %caso não exista uma das séries
    if sum(abs(co))*sum(abs(dd))*sum(abs(dc))>0,
        %usando pwelch
        [qq1 F]=pwelch(co,hanning(128),64,128,fa);
        qq1=qq1(2:65,1);
        qq1(1:5)=0;
        
        %faixas em segundos
        %2     3    4
        %4,12  6    8
        %8.5   9.8  11.6
        %12.8  16   21.3
        
        %faixas de periodos (sugestao do Rogerio) 
        %2.10 (64)     3.05 (44)    4.07 (33)
        %4.07 (33)     5.59 (24)    7.07 (19)
        %7.07 (19)     8.40 (16)    10.34(13) 
        %10.34(13)     11.20(12)    13.44(10)
        %13.44(10)     16.80(8)     22.40(6)
        
        %faixas em segundos
        %2     3    4
        %4,12  6    8
        %8.5   9.8  11.6
        %12.8  16   21.3
        
        
        %onda significativa 
        ww55(1)=4*sqrt(sum(qq1)*df);
        %energias nas 4 faixas para a normalizaçaõ das faixas 1,2,3 e 4
        ww55(2)=sum(qq1(6:10));
        ww55(3)=sum(qq1(11:15));
        ww55(4)=sum(qq1(16:31));
        ww55(5)=sum(qq1(32:end));
        ww55=round(ww55*100)/100;
        %caso queira alisar mais o espectro
        qq2=smooth(qq1,4);
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
        %cálculo dos picos
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        g2=diff(qq2);g2=sign(g2);g2=diff(g2);g2=[0;g2];
        g2=find(g2==-2);
        
        %escolhendo os 4 maiores
        [g4 g5]=sort(qq2(g2));
        g5=flipud(g5);
        g5=g2(g5);
        g20=g5;
        g5=[g5;0;0;0;0];g5=g5(1:4);
        
        picos1=[0;13;21;42];
        g=find(g20<11);isempty(g);
        if ans==0,picos1(1)=g20(g(1));g20(g)=80; 
        end;
        g=find(g20<16);isempty(g);
        if ans==0,picos1(2)=g20(g(1));g20(g)=80; 
        end;
        g=find(g20<32);isempty(g);
        if ans==0,picos1(3)=g20(g(1));g20(g)=80; 
        end;
        
        g=find(g5>0);g6=g5(g);
        g5=128./g5(g);
        ww55(5+g)=round(g5*10)/10;
        %w55(6:5+length(g5))=g5;
        %os 4 maiores picos (se maiores do que zero)
        %foram colocados em ww55, de forma sequencial.
        %if kkl==15,sf11,end                
        %kkl é a ordem do registro
        energsio(1:9,kkl)=ww55;
        if picos1(1)>0,if qq1(picos1(1))<0.1*sum(qq1),
                picos1(1)=0;end;end
        picpic(kkl)=picos1(1);
        %picos1(1)=8;
       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
        %calculo das direções por faixa; a wavelet corresponde
        %ao pico na faixa (se houver) ou ao centro da faixa,
        %sempre em picos1
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        for iwq=1:4,
            s=picos1(iwq);
            if s>0,
            %if iwq==1,if s<11,
                
            s=s-5;
                s1=wavecos(:,s);g=find(s1)>0;
                out1=wavecos(g,s);
                out3=wavesen(g,s);
                m=length(g);
                m1=1024-m;
                %parâmetros para cálculo de tet2 e sp2
                m3=m1;m1=m1-1;m3=m1;
                m4=2*dt/(m*.375);
                m2=m-1;
                mq=round(m/2);
                
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                %calcula tet2 e sp2 a partir das 3 series:
                %heave, pitch e roll 
                
                % eta=acos(fase);
                % pitch=-akcos(teta)sen(fase);
                % roll= -aksen(teta)sen(fase);
                % espectros cruzados:
                % heave-pitch=imag(a2w2kcos(teta));
                % heave-roll =imag(a2w2ksen(teta));
                % teta=artg(heave-roll/heave-pitch);
                
                %out1 é a wavelet coseno e out3 a wavelet seno
                
                %aplica wavelets para as 3 series
                a1=filter((out1-j*out3)',1,co);
                a2=filter((out1-j*out3)',1,dd);
                a3=filter((out1-j*out3)',1,dc);
                
                
                %series após a convoluução
                a1=a1(m:1024);
                a2=a2(m:1024);
                a3=a3(m:1024);
                
                z41=a1;z42=a2;z43=a3;
                
                %espectros brutos e cruzados
                a4=m4*(z41.*conj(z41));
                a8=m4*-imag(z41.*conj(z43));
                a9=m4*-imag(z41.*conj(z42));
                a51=zeros(976,1);
                
                a20=m4*(z42.*conj(z42));
                a21=m4*(z43.*conj(z43));
                
                %soma dos dois espectros:a2k2; a7=sqrt(a4w4k2);
                a34=a20+a21;
                a7=sqrt(a4.*a34);
                %espectro cruzado dos dois slopes
                a12=m4*real(z42.*conj(z43));
                                
                %cálculo da direção principal
                %%a partir de Kuik (sen(teta)/cos(teta))
                c0=a8+j*a9;
                c1=c0./a7;
                %direção principal
                c0=angle(c0)*360/(2*pi);
                c0=ceil(c0);
                c00=find(c0<=0);c0(c00)=c0(c00)+360;
                c000=270-c0-23;g=find(c000<=0);c000(g)=c000(g)+360;
                
                %cálculo da direção principal por maxima entropia (Bill O'Reilly)
                %maxima entropia
                
                c2=(a20-a21+j*2*a12)./a34;
                p1=(c1-c2.*conj(c1))./(1-(abs(c1)).^2);
                p2=c2-c1.*p1;
                
                tet2=zeros(1,m3+2);
                
                %in order to avoid the ambiguity caused by 2teta the main
                %direction calculated by Fourier (c0) techniques is used
                %as a reference; the mem value is calculated in an interval
                %of 100 degrees around this value;
                
                %cálculation for each segment
                for kl=1:m3+2,
                    p3=ceil(c0(kl));d=(p3:p3+100);
                    
                    z1=1-p1(kl)*a26(d)-p2(kl)*a27(d);
                    z1=z1.*conj(z1);z1=z1';
                    %mínimum of denominator is sufficient to
                    %determine the maximum
                    
                    p5=find(z1==min(z1));p5=p5(1);
                    p7=a30(p3+p5-1);
                    %main direction (mem) for each segment
                    tet2(1,kl)=grad1*p7;
                    
                end;
                
                %spectrum for each segment
                sp2=a4';
                %angulo(kkl,iwq)=mean(c0);
                
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                %CÁLCULO DA DIREÇAO PRINCIPAL A PARTIR DE tet2 e sp2
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                %[b a]=butter(3,0.15);
%                 xz=zeros(90,1);
%                 for i=1:length(tet2),
%                     
%                     z=tet2(i)*180/pi;g=ceil(z/4);
%                     if g>90,g=g-90;end
%                     xz(g)=xz(g)+sp2(i);
%                 end
%                 g1=smooth(xz,6);
%                 %g1=filtfilt(b,a,g1);
%                 g2=find(g1==max(g1));
%                 g2=g2*4;
%                 g2=270-g2-23;
%                 if g2<0,g2=g2+360;end
%                 diresio(kkl,iwq)=g2;
                
                teste7    
                %if s==2,sf11,end;
                espesio(kkl,iwq)=energsio(iwq+1,kkl);
                end;
            end;
    end;
end;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%FILTRAGEM DOS DADOS DE DIREÇÂO
ddirsiodoc=zeros(744,4);tv=1:744;
for i=1:4,
    ddirsiodoc(:,i)=smooth(tv,diresio(:,i),'lowess',6);
    ddirsiodoc(:,i)=smooth(ddirsiodoc(:,i),6);
end;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%FILTRAGEM DO VENTO
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ventosiodoc1=smooth(wind(1:744,2)-23);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%CASO DESEJE UMA FILTRAGEM MELHOR: filtraventosiodoc.m