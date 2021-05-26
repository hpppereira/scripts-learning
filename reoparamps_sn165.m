%programa transformar REO em MPS
%para os dados dos perfis verticais do projeto do porto 2006
%
% equacao obtida indiretamente a partir da equacao do CTD sn 368 velho
%
%abril de 2006
%****CTD NOVO***


function sai = reoparamps_sn165(entra)


for i=1:length(entra)
    if entra(i) < 5;
        entra(i) = 5;
    end
end

sai = -2.9282 + 0.6777*entra;
