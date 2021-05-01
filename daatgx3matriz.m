%CODE daatgx3matriz.m to select the segments for
%the directional spectrum composition
%usado para a faixa 1 do 3DM-GX3
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Prepared by C.E. Parente
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Preparing ensembles of mq segments advancing one sample
fr3=[];fr4=[];
%fr3 ia a matrix with the segments whose direction
%stability will be investigated
%fr4 is a spectrum matrix
mq=round(m/2);

for ip=1:mq,
    fr3=[fr3;tet2(ip:m1-(mq-ip))];
    fr4=[fr4;sp2(ip:m1-(mq-ip))];
end;

%using the mean and the standard circular deviation
%to select the segments with a given stability

fr2a=mean(cos(fr3));fr2b=mean(sin(fr3));
r=sqrt(fr2a.^2+fr2b.^2);
%circular deviation
fr9=sqrt(2*(1-r));

%espectro medio por coluna
fr45=mean(fr4);
%sera preparada uma matriz: linhas=desvio
%padrao circular - fr9; 
%colunas - direçao/6 (0 a 60 graus)
%os elementos sao a energia para cada cruzamento

fr2=angle(fr2a+j*fr2b);
g=find(fr2<0);fr2(g)=fr2(g)+2*pi;
g=size(fr2);g=g(2);
fr2=fr2*180/pi;
matr=zeros(10,60);matr1=matr;

%direçao/6
qp=90-fr2-22;
gg=find(qp<=0);qp(gg)=qp(gg)+360;
gg=find(qp>360);qp(gg)=qp(gg)-360;
qp=ceil(qp/6);

%desvio padrao *100 - desvios padrões entre
%menores do que 10;
fr10=round(fr9*100);

%preparando a matriz

for kk=1:length(qp),
    a1=fr10(kk);
    a2=qp(kk);
    
    if a1*a2>0,
        if a1<10,
            matr(a1,a2)=matr(a1,a2)+fr45(kk);
            matr1(a1,a2)=matr1(a1,a2)+1;
        end;
    end;
end;
%calculando as medias de direção e espectro para a maior 
%concentração de energia

g=find(matr1==0);matr1(g)=1;
matr=matr./matr1;
s=contourc(matr);
d=isempty(s);if d==0,
    g=size(s);g=g(2);
    g5=s(2,1);g6=1;
    while g6<g,g7=g6;g6=g6+g5+1;
        if g6<g,g5=s(2,g6);
        end;
    end
    e=mean(s(1,g7+1:end))*6;
    %seleção de valores na faixa 1 de direção e energia;alguns
    %criterios subjetivos
    if s(1,g7)>0.005,if e>140,if e<270,
                dire(kkl,iwq)=e;
                %essa escala para a faixa 1 é arbitrária até se reseolver
                %o problema do ruido nessa faixa
                espe(kkl,1)=s(1,g7);
            end;
        end;
    end;
end;