function [arctang]=arctang(b,a)
%Calcula o arco-tangente de b/a de 0 a 2 pi

%Variaveis de entrada

%b,a...........quadespectros

%Variaveis Internas

%arct..........recebe o valor do arco tangente
%arctang.......recebe arct corrigido para 0 a 2 pi

arct=atan(abs(b)/abs(a));
if a>0 & b>0
    arctang=2*pi-arct;
end
if a>0 & b<0
    arctang=pi+arct;
end
if a<0 & b<0
    arctang=pi-arct;
end
if a<0 & b>0
    arctang=pi+arct;
end

