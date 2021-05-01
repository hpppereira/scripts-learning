%grafico da evolucao espectral

function evol_espec(f,bb)

ad=['jan';'fev';'mar';'abr';'mai';'jun';'jul';'ago';'set';'out';'nov';'dez'];

%limita o tempo da evolucao
% bb=bb(:,1:100);

[lin,col]=size(bb); %Cria valor 'lin' e 'col' com a dimens�o da matriz 'bb'
x=linspace(1,col,col); x=x./24;
y=f;


% x=linspace(1,col,col); %Cria vetor com 36 elementos (os 36 registros)
% y=interp1(1:32,f,1:512); 

%% Plot evolucao espectral
% Figura mesh

%y=linspace(0,max(aa(:,1)),length(aa)); %Cria vetor de 1024 elementos, com os valores de frequencia

fig_mesh=figure;
mesh(x,y,bb),view(90,30)
title('Evolucao Espectral')
xlabel('Tempo (h)')
ylabel('Frequ�ncia (Hz)')
zlabel('Energia')
colorbar
axis tight

%% Figura contour
% x=linspace(1,col,col); %Cria vetor com 36 elementos (os 36 registros)

fig_cont=figure;
contour(x,y,bb)
title('Evolucao Espectral')
xlabel('Tempo (h)')
ylabel('Frequ�ncia (Hz)')
colorbar
axis tight

%salva figuras

nome=(['evspmesh_' ad(5,:),'.jpg']);
saveas(fig_mesh,nome)
nome=(['evspcont_' ad(5,:),'.jpg']);
saveas(fig_cont,nome)

