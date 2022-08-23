%teste1.m para detectar grupos de ondas
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%começa com arquivos fr3 de 100 linhas por 1282 colunas para
%detectar estabilidade de direção (diferença entre valor máximo e mínimo)
%menoor do que 13 graus


z1=[];z2=[];
for i=100:-1:34,
    fr3=[];fr4=[];mq=i;
    for ip=1:mq,
        fr3=[fr3;tet2(ip:ip+1382-mq-ip+(ip-1))];
        fr4=[fr4;co1(ip:ip+1382-mq-ip+(ip-1))];
        
    end;
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%se já foi escolhido um dos valores de z1, a coluna correspondente
%em fr3 é manipulada (valor zero na primeira linha e valor 1000 na
%segunda até as várias colunas subsequentes (determinadas por z2)    
    if length(z1)>0,
         for k=1:length(z1),
             fr3(1,z1(k):z1(k)+mq-1)=0;
             fr3(2,z1(k)+1:z1(k)+mq-1)=1000;
             
         end;
     end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%escolha de uma coluna vendo as diferenças entre valor máximo e mínimo
    x1=max(fr3);x2=min(fr3);
    x=x1-x2;
    [q1 q2]=find(x<=13);
    if length(q2>0),
        z1=[z1;q2(1)];
        z2=[z2;mq];
        
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%ligeira filtragem na sériede heave (co1)
[b,a]=butter(6,0.2);
co2=filtfilt(b,a,co1);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%eliminação das colunas com duplicidade
z3=[];z4=[];k=0;z3=[];z4=[];s4=1;
while length(z1)>0,k=k+1;
    s1=z1(1);s2=z2(1);
    s3=abs(z1-s1);
    s4=find(s3<=s2);
    z1(s4)=[];z2(s4)=[];
    z3=[z3;s1];z4=[z4;s2];
    
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%plotagem dos grupos
figure(3);clf;hold on
for k=1:length(z3),
    x=mean(tet2(z3(k):z3(k)+z4(k)-1));
    v=[0 1382 180 240];axis(v);
    plot(z3(k):z3(k)+z4(k)-1,3*co2(z3(k):z3(k)+z4(k)-1)+x,'color',[1 0 0]);
end
axis(v);
grid
s1=[0;1382];s2=[215;215];line(s1,s2,'color','k');
xlabel('amostras(n) - tempo=n*0.7813')
ylabel ('direção em graus')
title('grupos para o registro 515')
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%







