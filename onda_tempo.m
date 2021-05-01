% Calcula parametros de onda no dominio do tempo
%
% Elaborado por Henrique P. P. Pereira (henriqueppp@peno.coppe.ufrj.br)
%
% Ultima modificacao: 01/11/2012
%
% Dados de entrada: t - vetor de tempo  
%                   eta - vetor de elevacao
%                   h - profundidade
%[Hs,H10,Hmed,Hmin,Hmax,Tmed,Tmin,Tmax,THmax,Lmed,Lmax,Lmin,Cmed]
% Dados de saida: Hs - altura significativa
%                 H10 - altura de 1/10 das maiores
%                 Hmed - altura media
%                 Hmin - altura minima
%                 Hmax - altura maxima
%                 Tmed - periodo medio
%                 Tmin - periodo minimo
%                 Tmax - altura maxima
%                 THmax - periodo associado a altura maxima
%                 Lmed - comprimento de onda medio
%                 Lmin - comprimento de onda minimo
%                 Cmed -  celeridade media
%
% Subrotinas chamadas: regressao


function [Hs,H10,Hmed,Hmin,Hmax,Tmed,Tmin,Tmax,THmax,Lmed,Lmax,Lmin,Cmed]=onda_tempo(t,eta,h)

% Nivel medio
nm=mean(eta);

% Contador de zero ascendente
contza=0;

% Acha os indicies anteriores que cruza o zero ascendente
for i=1:length(eta)-1     
    
    
    if eta(i)<nm && eta(i+1)>nm %Condicao de zero ascendente       
        
        contza=contza+1; %conta zero ascendente
        
        x=[t(i) t(i+1)]; %Cria vetor x(1x2) para fazer o calculo da regressao linear 
        
        y=[eta(i) eta(i+1)]; %Cria vetor y(1x2) para fazer o calculo da regressao linear
        
        [b,a]=regressao(x,y); %chama subrotina de regressao linear
        
        xnm(i,1)=(nm-b)/a; % Acha valor de x(tempo) para elevacao=nm
        
     end
end

% Cria vetor com os indices de onde cruza o zero ascendente
ind_nm=find(xnm); 

% Quantidade de ondas no registro
contonda=contza-1; 

% Acha altura de cada onda
for i=1:length(ind_nm)-1
    
    elmin(i,1)=min(eta(ind_nm(i,1):ind_nm(i+1,1))); %Acha elevacao minima entre 2 zeros ascendentes
    
    elmax(i,1)=max(eta(ind_nm(i,1):ind_nm(i+1,1))); %Acha elevacao maxima entre 2 zeros ascendentes
    
    H(i,1)=elmax(i,1)-elmin(i,1); %Acha altura (el max - el min)
    
end

% Cria vetor com o tempo para cada zero ascendente (eta=nm)
for i=1:length(ind_nm)
    
    t_nm(i,1)=xnm(ind_nm(i,1),1);  %criar vetor com tempo onde nm=0;
    
end

% Acha o periodo de zero ascendente (Tza) de cada onda
for i=1:length(ind_nm)-1
  
    Tza(i,1)=t_nm(i+1)-t_nm(i);

end

% Calcula a altura significativa (H 1/3)
Hss=sort(H,'descend'); %se usar 'ascedent' utiliza-se hs=flipud(hs);
div=round(length(Hss)/3);
Hs=mean(Hss(1:div));

% Calcula a altura 1/10 (H 1/10)
H10=sort(H,'descend'); % hs=flipud(hs);
div=round(length(H10)/10);
H10=mean(H10(1:div));

% Altura maxima
Hmax=max(H); 

% Altura minima
Hmin=(min(H)); 

% Altura media
Hmed=mean(H); 

% Periodo maximo
Tmax=max(Tza); 

% Periodo minimo
Tmin=min(Tza); 

% Periodo medio
Tmed=mean(Tza); 

% Periodo associado a altura maxima

% Cria matriz para [H Tza] para o calculo do periodo associado a altua maxima
HTza=[H,Tza];

% Periodo de zero ascendente associado a altura maxima
THmax=HTza(find(HTza(:,1)==max(HTza(:,1))),2);
THmax=THmax(1);

% Comprimento de onda em aguas profundas (Lo=1.56T^2 (m))
Lo=1.56*(Tza.^2);

% Comprimento de cada onda em aguas rasas (L=2*pi/k), calculo do k pela itera��o (relacao de dispersao)??

%Iteracao para o calculo de L (Perguntar para o Parente, talvez esteja subestimando o L)

L=Lo;
for j=1:length(L)
        
    for i=1:100
  
        L(j)=Lo(j)*tanh((2*pi)/L(j)*h);
   
    end

    L(j+1)=L(j);
    
end
L=L(1:length(Lo));

% Comprimento de onda maximo em aguas profundas
Lomax=max(Lo);

% Comprimento de onda minimo em aguas profundas
Lomin=min(Lo);

% Comprimento de onda m�ximo em aguas intermediarias
Lmax=max(L);

% Comprimento de onda minimo em aguas intermediarias
Lmin=min(L);

% Comprimento medio em aguas profundas
Lomed=mean(Lo);

% Comprimento medio em aguas intermediarias
Lmed=mean(L);

% Celeridade em aguas profundas Co=1.56*T (m/s)
Co=1.56.*Tza; 

% Celeridade em aguas intermediarias (C=L/T)
C=L./Tza;

% Celeridade media em aguas profundas
Comed=mean(Co);

% Celeridade media em aguas intermediarias
Cmed=mean(C);

% Numero de onda em aguas profundas
kot=2*pi./Lo;

% Numero de onda em aguas intermediarias
kt=2*pi./L;

% Numero de onda medio em aguas profundas
kotmed=mean(kot);

% Numero de onda em medio aguas intermediarias
ktmed=mean(kt);

% Frequencia
ft=1./Tza; 

% Frequencia media
ftmed=mean(ft);

% Frequenca angular (w=2*pi*f)
w=2*pi.*ft; 

%frequencia angular media
wmed=mean(w);