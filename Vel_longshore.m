clear all, close all, clc
%% REFRA��O - EMPINAMENTO - QUEBRA DE ONDA - VELOCIDADE LONGSHORE

set(0,'DefaultAxesFontSize',14);  % para que o tamanho das fontes sejam 14

%==================== dados de ondas ======================================


load praia01.txt
Hs = praia01(:,6);
Tp = praia01(:,7);
Dp = praia01(:,8);
Dir = Dp-25-(90);               %deixa todos os �ngulos em fun��o de 90


% Hs = 1       % Altura  
% T = 15       % Per�odo
% Dir = 45     % Dire��o
% d = 10       % Profundidade 
  
g= 9.8;

%%  Comprimento de onda 
% Lo=1.56*(T^2); % m 
%        
% omega=2*pi/T;
% 
% L= fzero(@(L) omega ^2 - g * 2 * pi / L * tanh( (2 * pi) / L * d), Lo)
% 
% k=2*pi/L

   
d = [1:0.1:8]; 
    

for j = 1:384 %% comprimento da serie +++++++++++++
    
    

    %variando o tempo
    for i = 1:length(d)  %variando as profundidades

        
        Lo(i,j) = 1.56 * (Tp(j).^2); % m 
        
        omega(i,j) = 2 * pi/ Tp(j);
        
        L = fzero(@(L) omega(i,j).^2 -g * 2 * pi / L * tanh( (2*pi) / L * d(i)),Lo(i,j));
        
        Lmat(i,j) = L; %ultimo L calculado pela iteracao
        
        k(i,j) = 2 * pi / Lmat(i,j); 

        

%% C�lculo do Coeficiente de SHOALING Ks

        Cgo(i,j) = 0.5 * 1.56 * Tp(j); %(tanh(k*d))           % velocidade de grupo �gua profunda

        Cg (i,j) = (1/2)*(1 + (4 * pi * d(i)/Lmat(i,j)) / (sinh(4 * pi * d(i) /Lmat(i,j)))) ...
            * ((g * Tp(j) / 2 /pi) * tanh (2* pi * d(i) / Lmat(i,j))); % velocidade de grupo �gua RASA

        Ks(i,j) = sqrt(Cgo(i,j) / Cg(i,j));     % SHOALING
  
 

%% C�lculo do Coeficiente de REFRA��O

        Co(i,j) = 1.56 * Tp(j) *(tanh(k(i,j) * d(i)));     %Velocidade de Fase i

        C1(i,j) = Lmat(i,j) / Tp(j);                         % Velocidade de Fase ii


        % MUDAR ou n�o: Tetha0 � Dir (em Radianos) 

        Tetha_o = degtorad(Dir);                 % Dire��o em RADIANOS
        
        sin_Dir(j) = sin (Tetha_o(j));
        sin_tetha(i,j) = C1(i,j) *  sin_Dir(j) / Co(i,j) ;
        
        
        Kr(i,j) =  ((1 - (sin_Dir(j))^2) / (1 - (sin_tetha(i,j))^2))^0.25;  % COEFICIENTE DE REFRA��O

% C�lculo do Empinamento + Shoaling = H modificado

        H_shoaling(i,j) = Hs(j) *  Ks(i,j) * Kr(i,j)  ;               % Hb da onda

        Tetha_final(i,j) = asin (sin_tetha(i,j))  ;           % �ngulo no PONTO DE d ap�s a Refra��o

        %Tetha_final_deg(i,j) = radtodeg (Tetha_final(i,j)) ;  % Diferen�a de dire��o das ondas entre as profundidades 
        Dif_de_angulo(i,j) = Dir(j) - Tetha_final(i,j) ;     % Diferen�a de dire��o das ondas entre as profundidades 

%% Determinar a profundidade de quebra e Hb pela declividade
% Indice de quebra de onda KOMAR e GAUGHAN (1973)

        Ind_Hb (j) = 0.56 *(H_shoaling(i,j) / Lo(i,j))^(-0.2);     % Indice de quebra.... o coeficiente 0.56 foi encontrado por dados de laborat�rio

        Hb(j) = Ind_Hb(j) * H_shoaling(i,j) ;                   % Altura de QUEBRA DE ONDA

% pela fun��o de inclina��o da praia
% o ponto de dados aos 8m tem ~ 1200 da praia.
% assim a inclina��o �:

        beta = 0.6/100;                              % inclina��o da PRAIA

        a(j) = 43.8 * (1 - exp(-19*tan(beta))) ;        % constante

        b(j) = 1.56 / (1+ exp(-19.5*tan(beta))) ;         % constante

        y_b(j) = b(j) - a(j) * Hb(j) / (g * Tp(j).^2)   ;     % INDICE DE QUEBRA DA ONDA NA PRAIA
        
        d_b(j) = Hb(j) / y_b(j);                     % Profundidade de QUEBRA DE ONDA

% Obs.: The initial value selected for the refraction coefficient would now
% be checked to determine if it is correct for the actual breaker location. 
% If necessary, a corrected refraction coefficient should be used to recompute breaker height and depth.

% Cf         %values in the range 0.005 to 0.01, but is dependent on bottom roughness

        d90 = 1.56;
        Chezy(i,j) = 18 * log (12 * d (i) / 3 * d90);
        Fric(i,j)  = 8 * g / (Chezy(i,j)^2);
        F_c(i,j) = 0.24 * ((log ( 12 * d(i) / 3 * d90))^-2);
        C_fric(i,j) = F_c(i,j);


        %RAD_Tetha_final = degtorad(Tetha_final);
        
        V_LC(i,j) = ((5 * pi) / 16) * tan(beta) / C_fric(i,j) *  y_b(j) * sqrt(g*d(i)) * sin(Tetha_final(i,j)) * cos(Tetha_final(i,j));
    end
end



figure (1)
subplot(311)
plot(Dp(1:j),'o')
legend ('direcao')
ylabel ('Graus')
axis([0 length(Dp) 0 200])
subplot(312)
plot(Hs(1:j),'o')
legend ('Altura')
ylabel ('Altura')
axis([0 length(Hs) 0 2.5])
subplot(313)
imagesc(1:length(d_b),linspace(1,8,i),V_LC(1:71,1:384));figure(gcf);
%contourf(VX)
hold on
plot(d_b)

ylabel ('Velocidades na largura da zona de surf')
xlabel ('Tempo (hs)')
legend ('velocidades','largura da zona de surf')

%% largura da zona de surf

L_SZ = d_b .* 60;   % inclina��oo da praia 60....calibrar
%outside = max(d)*120;

figure(2)
subplot(311)
plot(Dp(1:j),'o')
legend ('direcao')
ylabel ('Graus')
axis([0 length(Dp) 0 200])
subplot(312)
plot(Hs(1:j),'o')
legend ('Altura')
ylabel ('Altura')
axis([0 length(Hs) 0 2.5])
subplot(313)
%imagesc(1:length(d_b),linspace(0,max(d)*140),V_LC(1:71,1:384));figure(gcf);
imagesc(1:length(d_b),linspace(0,max(d)*140),V_LC(1:71,1:384));figure(gcf);

legend ('velocidades')
hold on
plot(L_SZ)
legend('largura da zona de surf')
ylabel ('Distancia 8m ate 0m')


for z = 1:j
    
    n = find(d >= L_SZ(j));
    
%     aux(z) = n; %verificacao
    
    V_LC(n,z) = NaN;
    
end
    
    
%plot(V_LCnan)
    
    


