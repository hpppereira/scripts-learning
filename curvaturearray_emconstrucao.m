function[aa]=curvaturearray(eta,etax,etay,etaxx,etayy,deltat,donv)

%calcula espectro direcional para ondografo de curvatura
%DADOS DE ENTRADA  
%                 eta = vetor de deslocamento vertical(potencia de 2)
%                 etax, etay = inclinacao da superficie
%                 etaxx, etayy = curvatura da superficie
%                 deltat = intervalo de amostragem
%                 donv = direçao que o eixo de origem (x) faz com o Norte
%                 Verdadeiro medido no sentido horario

%DADOS DE SAIDA
%MATRIZ CONTENDO: COLUNA 1 = frequencia
%                        2 = auto espectro de eta
%                        3 = direcao principal
%                        4 = espalhamento angular 

%SUBRROTINAS CHAMADAS

%                  cortheta.m
%                  espec.m (alisa.m)
%                  espec2.m (alisa.m)


% Inicializaçao de constantes

reg=length(eta);
reg2=fix(reg/2);

%Calculo dos espectros

espeta = espec(eta,deltat);
coeta = espeta(:,2); 

espetax = espec(etax,deltat);
coetax = espetax(:,2); 

espetay = espec(etay,deltat);
coetay = espetay(:,2); 

espetaxx = espec(etaxx,deltat);
coetaxx = espetaxx(:,2);

espetayy = espec(etayy,deltat);
coetayy = espetayy(:,2);

espetaetax = espec2(eta,etax,deltat);
qdetaetax = espetaetax(:,5); 

espetaxetay = espec2(etax,etay,deltat);
coetaxetay = espetaxetay(:,4);

espetaetay = espec2(eta,etay,deltat);
qdetaetay = espetaetay(:,5); 

espetaetaxx = espec2(eta,etaxx,deltat);
coetaetaxx = espetaetaxx(:,4);

espetaetayy = espec2(eta,etayy,deltat);
coetaetayy = espetaetayy(:,4);

espetaxetaxx = espec2(etax,etaxx,deltat);
qdetaxetaxx = espetaxetaxx(:,5); 

espetaxetayy = espec2(etax,etayy,deltat);
qdetaxetayy = espetaxetayy(:,5); 

espetaetax = espec2(eta,etax,deltat);
qdetaetax = espetaetax(:,5); 

espetayetaxx = espec2(etay,etaxx,deltat);
qdetayetaxx = espetayetaxx(:,5); 

espetayetayy = espec2(etay,etayy,deltat);
qdetayetayy = espetayetayy(:,5); 

k=sqrt((coetax+coetay)./coeta);

%Calcula direcao principal

for i=1:reg2;
    
    if coeta(i)>0.001;

        %Coeficientes de primeira ordem
        
        a1(1)= 1/pi*qdetaetax(i)/(coeta(i)*k(i));
        a1(2)=-4/(3*pi)*qdetaxetaxx(i)/(coeta(i)*k(i)^3);
        a1(3)=-4/pi*qdetaxetayy(i)/(coeta(i)*k(i)^3);
   
        b1(1) =1/pi*qdetaetay(i)/(coeta(i)*k(i));  
        b1(2)=-4/(3*pi)*qdetayetaxx(i)/(coeta(i)*k(i)^3);
        b1(3)=-4/pi*qdetayetayy(i)/(coeta(i)*k(i)^3);

        %coeficientes de segunda ordem
        
        a2(1)=-2/pi*((coetaetaxx(i)/(coeta(i)*k(i)^2))-1/2);
        a2(2)=2/pi*((coetaetayy(i)/(coeta(i)*k(i)^2))-pi);
        a2(3)=2/pi*((coetay(i)/(coeta(i)*k(i)^2))+1/2);
        a2(4)=2/pi*((coetaxx(i)/(coeta(i)*k(i)^4))-3/8);
        a2(5)=-2/pi*((coetayy(i)/(coeta(i)*k(i)^4))-3/8);
        a2(6)=2/pi*((coetax(i)/(coeta(i)*k(i)^2))-1/2);
        
        b2(1)=2/pi*(coetaxetay(i)/(coeta(i)*k(i)^2));
              
        %coeficientes medios
        
        am1=mean(a1);
        bm1=mean(b1);
        am2=mean(a2);
        bm2=mean(b2);
        
        %Theta utilizando os coeficientes de primeira ordem      
        
        theta(i,1)=cortheta(a1(1),b1(1),donv);
        theta1(i,1)=cortheta2(a1(2),b1(2),donv);
        theta1(i,2)=cortheta2(a1(3),b1(3),donv);
        
        thetam(i,1)=cortheta2(am1,bm1,donv);

        %Theta utilizando os coeficientes de segunda ordem
        
        theta2(i,1)=cortheta(a2(1),b2(1),donv);
        theta2(i,2)=cortheta2(a2(2),b2(1),donv);
        
        thetam(i,2)=cortheta2(am2,bm2,donv);
        
        thetaux=atan(b1(1)/a1(1));
        auxc(i)=coeta(i)*cos(thetaux);
        auxs(i)=coeta(i)*sin(thetaux);

        % Calculo do parametro de espalhamento
        
        s(i)=pi*sqrt(a1(1)*a1(1)+b1(1)*b1(1));
        s(i)=s(i)/(1-s(i));
        
    end
end

aa= [espeta(:,1) coeta theta theta1 theta2 thetam s];

   