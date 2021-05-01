%passar acel z para dsp z utilizando a funcao
%iomega.m

load acz_gx3.txt

datain = acz_gx3(1,:) - mean(acz_gx3(1,:));
dt = 1;
datain_type = 3; %aceleration
dataout_type = 1; %displacement

dataout =  iomega(datain*1000, dt, datain_type, dataout_type);

plot(dataout)