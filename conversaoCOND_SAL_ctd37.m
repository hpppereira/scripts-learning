load C:\Users\LUCIA\Documents\julio\BACKUPPENDRIVE23032014\Julio\CampanhaBg\dados.txt

ctd=teste;
clear teste

dados_temp_ctd=ctd(:,1)/10;
dados_condu_ctd=ctd(:,2)/100;
dados_pressao_ctd=ctd(:,3);
clear ctd

%%% CONVERSÃO DA CONDUTIVIDADE EM SALINIDADE %%%
C=dados_condu_ctd*1000/100; % convertendo para mS/cm
R=1/sw_c3515*C; % rotina do pacote sea-water (sw_c3515 e sw_salt)
S=sw_salt(R,dados_temp_ctd,dados_pressao_ctd);
dados_sal_ctd=S;
dados_dens_ctd=sw_dens(dados_sal_ctd,dados_temp_ctd,dados_pressao_ctd);
clear C R S
