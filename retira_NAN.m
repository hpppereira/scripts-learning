[arqi,pafi] = uigetfile('*.out','Arquivo de saida do ONDA1H');
if ~isstr(arqi); return; end
fid = fopen([pafi,arqi],'r');
cabecalho = fgetl(fid);
cont=0;
linha = fgetl(fid);
while linha ~=-1
    cont = cont+1;
    datahora(cont,:) = linha(1:18);
    valores(cont,:) = str2num(linha(19:end));
    linha=fgetl(fid);
end
fclose(fid);

% Abrindo como arquivo ASCII
formato='%7.4f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %7.2f %13.6e %13.6e %13.6e %13.6e %13.6e %8.2f %9.4f %7.2f %10.5f %7.2f %13.6e %13.6e %13.6e %13.6e %13.6e %8.2f %8.2f %9.4f %10.5f %7.2f %10.6f %6.2f %13.6e %13.6e %13.6e %13.6e %13.6e %8.2f %8.2f %9.4f %10.5f %7.2f %10.6f %6.2f %13.6e %13.6e %13.6e %13.6e %13.6e %8.2f %8.2f %9.4f %10.5f %7.2f %10.6f %6.2f\n';
   
valores(valores > 900) =  NaN;

saida = fopen([pafi,arqi(1:length(arqi)-4),'.fim'],'w');
fprintf(saida,'%s\n',cabecalho);
for i =1 :cont;
    fprintf(saida,'%s  ',datahora(i,:)');
    fprintf(saida,[formato],valores(i,:)');
end
fclose(saida);
