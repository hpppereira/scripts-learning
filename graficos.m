%cria gráficos de onda processados no dominio do tempo e frequencia

function grafonda(tt,sai_onda)

%salva os parametros de onda em uma matriz
%      linha = 1   2   3     4    5    6   7 8
%matonda(:,n)=[hs,h10,hmax,thmax,tmed,hm0,tp,dp]';


ad=['jan';'fev';'mar';'abr';'mai';'jun';'jul';'ago';'set';'out';'nov';'dez'];

fig=figure;
subplot(3,1,1)
plot(tt,sai_onda(6,:)), axis tight, title(['Altura Significativa - ' ad(5,:)]), xlabel('Dias'), ylabel('metros')
subplot(3,1,2)
plot(tt,sai_onda(7,:)), axis tight, title('Perdiodo de pico'), xlabel('Dias'), ylabel('segundos')
subplot(3,1,3)
plot(tt,sai_onda(8,:)), axis tight, title('Direção do periodo de pico'), xlabel('Dias'), ylabel('graus')

%salva figura

nome=(['onda_' ad(5,:),'.jpg']);
saveas(fig,nome)
