%cria gráficos de onda processados no dominio do tempo e frequencia

function grafonda(tt,sai_onda)

%salva os parametros de onda em uma matriz
%       linha = 1   2   3    4    5    6    7    8     9    10   11   12   13  14 15   16  17
%sai_onda(:,n)=[Hs H10 Hmed Hmin Hmax Tmed Tmin Tmax THmax Lmed Lmax Lmin Cmed fp tp dirtp hm0]';

ad=['jan';'fev';'mar';'abr';'mai';'jun';'jul';'ago';'set';'out';'nov';'dez'];

fig=figure;
subplot(3,1,1)
plot(tt,sai_onda(17,:)), axis tight, title(['Altura Significativa - ' ad(5,:)]), xlabel('Dias'), ylabel('metros')
subplot(3,1,2)
plot(tt,sai_onda(15,:)), axis tight, title('Perdiodo de pico'), xlabel('Dias'), ylabel('segundos')
subplot(3,1,3)
plot(tt,sai_onda(16,:)), axis tight, title('Direção do periodo de pico'), xlabel('Dias'), ylabel('graus')

%salva figura

nome=(['onda_' ad(5,:),'.jpg']);
saveas(fig,nome)
