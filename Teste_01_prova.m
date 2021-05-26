
clear all; close all; clc

%%
%%%%%%%%%%%%%%%%%%%%%%%%
%%% Tank Conditions %%%%
%%%%%%%%%%%%%%%%%%%%%%%%

% d=0.7; %(m)
% S0=1;

% Algo diferente...
% %%% Baldock et al 1998
% d=0.9;
% S0=1;

%%% Neves et al 2012
d=0.6;
% S0=1/2;

%%
%%%%%%%%%%%%%%%%%%%%%%
%%% Incident waves %%%
%%%%%%%%%%%%%%%%%%%%%%

% H0=2; %(m)
% T=10; %(s)

% Algo diferente...
% %%% Baldock et al 1998
% H0=0.9 % Hrms
% T=1.5 % Tp (s)

%%% Neves et al 2012
T=2; %(s)
H0=0.12; %(m)

%%
%%% Wavelength (iterative)

%%% starting with d/L=0.5
L1=d/0.5;
L2=T^2*tanh(2*pi*d/L1)/pi;%%% Equação de Dispersão

cont=0;
if L1==L2
    L0=L1;
    disp(L0)
else
    while L1~=L2
        L1=L2;
        L2=T^2*tanh(2*pi*d/L1)/pi;
        cont=cont+1;
        disp(sprintf('%s%d','Iteration ',cont))
        disp(sprintf('%s%d','L1 is ',L1))
        disp(sprintf('%s%d','L2 is ',L2))
        
        if cont>500
            dif=abs(L1-L2);
            disp(sprintf('%s%d','Difference is ',dif))
            L1=L2
        end
    end
    L0=L1;
    disp(L0)
end

% break
clear L1 L2 cont

%%

IMS=pi*H0/L0;
if IMS>0.44
    disp ('Onda quebra imediatamente')
elseif IMS<0.08
    disp ('Onda não quebra')
else
    N=-11*atanh((5.5*(IMS-0.26))+23)
    xb=N*L0
end

%%
% %%% Irribarren number %%%
% 
% IN0=S0/(H0/L0)^(1/2);
% 
% if IN0<0.5
%     disp('spilling')
% elseif IN0<3.3
%     disp('plunging')
% else
%     disp('surging')
% end