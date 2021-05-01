function [Momentos,VSresidual]=ajuste_cauda(VS,VF,fSpico,fScava)

VDIF=diff(VS(VF>fSpico(1) & VF<fScava(2))); % diferenças de Energia em cada frequencia.

indice_do_intervalo = find(VDIF == min(VDIF)); % indices dos minimos

indice_do_intervalo = indice_do_intervalo(end);


indfSpico1 =find(fSpico(1)== VF);

ind_inflexao = indfSpico1 + indice_do_intervalo + 1;



Momentos = [m0,m1,m2,m3,m4]'; 
