
% Estatisticas do mes e dia atual

c = datevec(vData);
c1 = datevec(now);

rmes=2;
rdia=3;
rhora=4;

% Que mes eh esse? R:c1(rmes) 
% Acha todos os dados de meses = a este mes:
imes=find(c(:,rmes)==c1(rmes));


% que horas sao? R:


% vetor com temperaturas deste mes:
tempMes=Temp(imes);

% dias com dados deste mes:
dataMes=vData(imes);
c2 = datevec(dataMes);

% Que dia eh hoje? R:c1(rdia) 
% Acha todos os dias = hoje
idia=find(c2(:,rdia)==c1(rdia));

% Dias desde o inicio do mes ate hoje:
idiasMes=find(c2(:,rdia)<=c1(rdia));

% media deste mes:
nanmean(tempMes)
nanmax(tempMes)

% media deste dia:
nanmean(tempMes(idia))
nanmax(tempMes(idia))

% media desde o inicio do mes ate hj:
nanmean(tempMes(idiasMes))
nanmax(tempMes(idiasMes))

L=length(tempMes);

% Hoje: (ultimas 24 horas)
nanmean(tempMes((L-c1(rhora)):end))



