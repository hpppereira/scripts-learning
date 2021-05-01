function [n]=converte_s_n(s);
% Função para calcular o spreading parameter N como dado de entrada o
% parameter S%
% Obs: Utilizada formulha em função de PHI da norma ISO
%
% Autores: Jose Antonio/Andre Mendes/Guisela/Ricardo 03/Nov/2011
%

% Funcao que correlaciona o "s" com o "n"
aux=0.5.*(1+s.*(s-1)./((s+1).*(s+2)));
n=(2.*aux-1)./(1-aux);

return


