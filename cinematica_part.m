%Cinemática da Particula - Ondas do mar
%Calculo apenas para águas rasas ou profundas
clear,clc
format 
x=(1:1024)'; %Eixo x
t=1; %Intervalo de amostragem
g=9.81; %Ac. gravidade
z=0;

aguas=input('Digite ´1´ para ondas se propagando em águas rasas, ´2´ intermedárias e ´3´ profundas: ');

if aguas==1
    
    disp('A onda está se propagando em águas rasas');
    
    %Altura da onda
    H=input('Entre com a altura de onda (H): ');
        
    %Amplitude da onda (a)
    a=H/2;
    
    %Periodo da onda
    T=input('Entre com o período de onda (T): ');
    
    %Profundidade em que a onda está se propagando
    h=input(['Entre com a profundidade do local (menor que ',num2str(1.56*T^2/20),' m): ']);
    
    %Cota para o movimento da particula
    z=input(['Digite a cota (z) entre 0 e ',num2str(-h),' para o gráfico do movimento da partícula: ']);
    
    %Comprimento de ondas em águas profundas (Lo)
    Lo=1.56*T^2;
    
    %Numero de onda em águas profundas (ko)
    ko=2*pi/Lo;
    
    %Celeridade em águas profundas (Co)
    Co=1.56*T;
    
    %Comprimento de onda em águas rasas
    %L=Lo*tanh(ko*h);
    L=sqrt(g*h)*T; %outras formulas
    %L2=g*T^2*tanh(2*pi*h/Lo)/2*pi; %outras formulas
    %L3=T*sqrt(g*h);
    
    
    %Numero de onda em águas rasas
    k=2*pi/L;
    %k1=2*pi/L1; %outras formulas
    
    %Frequencia angular
    fa=2*pi/T; %não varia (apenas em função do periodo que é cte)
    
    %Celeridade da onda em águas rasas
    C=L/T;
    %C1=Lo*tanh(k*h)/T; %outras formulas
    
    %Esbeltez da onda em aguas rasas
    esbr=H/L;
    
    %Esbeltez da onda em aguas profundas
    esbf=H/Lo;
    
    

    for i=1:length(x)
    
        %Deslocamento da superfície (eta) (utilizando o 'k' de águas rasas)
        eta(i,1)=H/2*cos((k*x(i,1))-(fa*t));
        
        %Potencial de velocidade (utilizando o 'k' de águas rasas)
        potvel(i,1)=(-(H/2)*g*cosh(k)*(h+z)*sinh(k*x(i,1)-fa*t))/(2*fa*cosh(k*h)); 
        
        %Relação de dispersão (utilizando o 'k' de águas rasas??)
        reldisp=g*ko*tanh(ko*h); 
        %reldisp1=g*k1*tanh(k1*h); %outras formulas
        
        %Potencial de vel introduzindo a relação de dispersão (utilizando o 'k' e o 'C' de águas rasas)
        potveldisp(i,1)=(-(H/2)*C*cosh(k)*(h+z)*sin(k*x(i,1)-fa*t))/(2*sinh(k*h));
        
        %Velocidade horizontal 
        u(i,1)=(H*fa*cosh(k)*(h+z)*cos(k*x(i,1)-fa*t))/(2*sinh(k*h));
        
        %Velocidade horizontal introduzindo a relação de dispersão
        udisp(i,1)=(H*g*k*cosh(k)*(h+z)*cos(k*x(i,1)-fa*t))/(2*fa*cosh(k*h));
        
        %Aceleração horizontal 
        acelh(i,1)=(H*g*k*cosh(k)*(h+z)*sin(k*x(i,1)-fa*t))/(2*cosh(k*h));
        
        %Velocidade vertical introduzindo a relação de dispersão
        wdisp(i,1)=(H*g*k*sinh(k)*(h+z)*sin(k*x(i,1)-fa*t))/(2*fa*cosh(k*h));
    
    
        %Aceleração vertical
        acelv(i,1)=(H*g*k*sinh(k)*(h+z)*cos(k*x(i,1)-fa*t))/(2*cosh(k*h));
        
        %Maior semi-eixo (A) (horizontal)
        A=((H*T)/(4*pi))*sqrt(g/h);
        %A1=(H*cosh(k)*(h+z))/(2*sinh(k*h));
        
        %Menor semi-eixo (B) (vertical)
        B=(H/2)*(1+(z/h));
        
        %Deslocamento horizontal
        desh(i,1)=-A*sin(ko*x(i,1)-fa*t);
        
        %Deslocamento horizontal usando a relação de dispersão
        deshd(i,1)=(-H*cosh(ko)*(h+z)*sin(ko*x(i,1)-fa*t))/(2*sinh(k*h));
                
        %Deslocamento vertical
        desv(i,1)=B*cos(ko*x(i,1)-fa*t);
        
        %Deslocamento vertical usando a relação de dispersão
        desvd(i,1)=(-H*sinh(k)*(h+z)*cos(ko*x(i,1)-fa*t))/(2*sinh(k*h));
        
    end
    
end
% plot(desh,desv);
% figure
% plot(deshd,desvd,'r')

if aguas==2
    
    disp('A onda está se propagando em águas intermediárias');
    
    %Altura da onda
    H=input('Entre com a altura de onda (H): ');
    
    %Amplitude da onda (a)
    a=H/2;
    
    %Periodo da onda
    T=input('Entre com o período de onda (T): ');
    
    %Profundidade em que a onda está se propagando
    h=input(['Entre com a profundidade do local (maior que ',num2str(1.56*T^2/20),'m e menor que ',num2str(1.56*T^2/2),'m): ']);
    
    

end
    
if aguas==3
    
    disp('A onda está se propagando em águas profundas');
    
    %Altura da onda
    H=input('Entre com a altura de onda (H): ');
        
    %Amplitude da onda (a)
    a=H/2;
    
    %Periodo da onda
    T=input('Entre com o período de onda (T): ');
    
    %Profundidade em que a onda está se propagando
    h=input(['Entre com a profundidade do local (maior que ',num2str(1.56*T^2/2),' m): ']);
    
    %Comprimento de ondas em águas profundas (Lo)
    Lo=1.56*T^2;
    L=Lo;
    
    %Numero de onda em águas profundas (ko)
    ko=2*pi/Lo;
    k=ko;
    
    %Celeridade em águas profundas (Co)
    Co=1.56*T;
    C=Co;
        
    %Frequencia angular
    fa=2*pi/T;
    
    for i=1:length(x)

    
        %Deslocamento da superfície (eta)
        eta(i,1)=H/2*cos((k*x(i,1))-(fa*t));
        
        %Potencial de velocidade
        potvel(i,1)=(-(H/2)*g*cosh(k)*(h+z)*sinh(k*x(i,1)-fa*t))/(2*fa*cosh(k*h)); 
        
        %Relação de dispersão
        reldisp=g*k*tanh(k*h); 
        
        %Potencial de vel introduzindo a relação de dispersão
        potveldisp(i,1)=(-(H/2)*C*cosh(k)*(h+z)*sin(k*x(i,1)-fa*t))/(2*sinh(k*h));
        
        %Velocidade horizontal 
        u(i,1)=(H*fa*cosh(k)*(h+z)*cos(k*x(i,1)-fa*t))/(2*sinh(k*h));
        
        %Velocidade horizontal introduzindo a relação de dispersão
        udisp(i,1)=(H*g*k*cosh(k)*(h+z)*cos(k*x(i,1)-fa*t))/(2*fa*cosh(k*h));
        
        %Aceleração horizontal 
        acelh(i,1)=(H*g*k*cosh(k)*(h+z)*sin(k*x(i,1)-fa*t))/(2*cosh(k*h));
        
        %Velocidade vertical introduzindo a relação de dispersão
        wdisp(i,1)=(H*g*k*sinh(k)*(h+z)*sin(k*x(i,1)-fa*t))/(2*fa*cosh(k*h));
    
    
        %Aceleração vertical
        acelv(i,1)=(H*g*k*sinh(k)*(h+z)*cos(k*x(i,1)-fa*t))/(2*cosh(k*h));
        
        %Maior semi-eixo (A) (horizontal)
        A=(H/2)*exp(k*z);
           
        
        %Menor semi-eixo (B) (vertical)
        B=A;
        
        %Deslocamento horizontal
        desh(i,1)=-A*sin((k*x(i,1))-(fa*t));
        
        %Deslocamento vertical
        desv(i,1)=B*cos((k*x(i,1))-(fa*t));

    end
end

    
    
    
    
    
    
   