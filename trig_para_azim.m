function [diraz]=trig_para_azim(dirt)
%Programa que muda dire��o que est�o no padr�o
%do arco trigonom�trico (90�=norte) para dire��o em azimute (0�=norte)

%Dados de entrada: dire��o em trigonom�trico
%Dados de sa�da: Dire��o corrigida para azimute

for i=1:length(dirt)
    if dirt(i,1)>=0 && dirt(i,1)<=90
        diraz(i,1)=90-dirt(i);
    elseif dirt(i,1)>90 && dirt(i,1)<=180
        diraz(i,1)=90+(360-dirt(i,1));
    elseif dirt(i,1)>180 && dirt(i,1)<=270
        diraz(i,1)=180+(270-dirt(i,1));
    elseif dirt(i,1)>270 && dirgrau1(i,1)<=360 || dirt(i,1)<0 && dirt(i,1)>=-90
        diraz(i,1)=(270+(180-dirt(i,1)))-360;
    end
end
