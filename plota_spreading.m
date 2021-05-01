ccc

a=load('saidaOnda1h_BS_axys13e15.txt');



% figure;plot(a(:,33),a(:,68),'*');title('VTPK1 X S2_VEPK1');xlabel('VTPK1');ylabel('S2_VEPK1');grid on;
% 
% figure;plot(a(:,33),a(:,69),'*');title('VTPK1 X S2_VTPK1');xlabel('VTPK1');ylabel('S2_VTPK1');grid on;
% 
% figure;plot(a(:,32),a(:,68),'*');title('VCAR1 X S2_VEPK1');xlabel('VCAR1');ylabel('S2_VEPK1');grid on;
% 
% figure;plot(a(:,32),a(:,69),'*');title('VCAR1 X S2_VTPK1');xlabel('VCAR1');ylabel('S2_VTPK1');grid on;

% Carregando dados do arquivo de ondas da BS
vcar1=a(:,32);
vtpk1=a(:,33);
vped1=a(:,36);
s1=a(:,68); % coluna com s1_VTPK1
%s1=a(:,67); % coluna com s1_VEPK1
s2=a(:,70); % coluna com s2_VTPK1
%s2=a(:,69); % coluna com s2_VEPK1
s=(s1+s2)/2;

return

int_vcar1=(0.5:1:8.5)';
nt=length(int_vcar1);
s_media_vcar1=ones(nt,1)*NaN;s_mediana_vcar1=ones(nt,1)*NaN;s_per70_vcar1=ones(nt,1)*NaN;
for j=1:nt
    k=find(vcar1 > int_vcar1(j)-0.5 & vcar1 <= int_vcar1(j)+0.5);
    if ~isempty(k)
        s_media_vcar1(j)=mean(s(k));
        s_mediana_vcar1(j)=median(s(k));
        s_per70_vcar1(j)=percentile(s(k),0.7);
    end
end

% Eliminando o ultimo valor (=NaN) para poder calcular os coeficientes com polyfit
int_vcar1=int_vcar1(1:8);s_media_vcar1=s_media_vcar1(1:8);s_mediana_vcar1=s_mediana_vcar1(1:8);s_per70_vcar1=s_per70_vcar1(1:8);
aux=[int_vcar1 s_media_vcar1 s_mediana_vcar1 s_per70_vcar1];
fid=fopen('vcar1_s.dat','w');
for j=1:length(int_vcar1);
    fprintf(fid,'%5.2f %5.2f %5.2f %5.2f\n',aux(j,:));
end
fclose(fid)
% save vcar1_s.dat -ascii aux


% [P,S] = polyfit(int_vcar1,s_media_vcar1,2); P
% ajuste_s_media_vcar1=(int_vcar1.^2).*P(1)+int_vcar1.*P(2)+P(3);
% figure;plot(int_vcar1,s_media_vcar1,'ko');grid on;xlabel('Hs1 (m)');ylabel('spreading s');title('MEDIA s x HS1')
% hold on;plot(int_vcar1,ajuste_s_media_vcar1,'r')
% 
% 
% [P,S] = polyfit(int_vcar1,s_mediana_vcar1,2); P
% ajuste_s_mediana_vcar1=(int_vcar1.^2).*P(1)+int_vcar1.*P(2)+P(3);
% figure;plot(int_vcar1,s_mediana_vcar1,'ko');grid on;xlabel('Hs1 (m)');ylabel('spreading s');title('MEDIANA s x HS1')
% hold on;plot(int_vcar1,ajuste_s_mediana_vcar1,'r')
% 
% 
% [P,S] = polyfit(int_vcar1,s_per70_vcar1,2); P
% ajuste_s_per70_vcar1=(int_vcar1.^2).*P(1)+int_vcar1.*P(2)+P(3);
% figure;plot(int_vcar1,s_per70_vcar1,'m*');grid on;xlabel('Hs1 (m)');ylabel('spreading s');title('per70 s x HS1')
% hold on;plot(int_vcar1,ajuste_s_per70_vcar1,'r')




% Calculando media e mediana de VTPK1
int_vtpk1=(4.5:1:16.5)';
nt=length(int_vtpk1);
s_media_vtpk1=ones(nt,1)*NaN;s_mediana_vtpk1=ones(nt,1)*NaN;s_per70_vtpk1=ones(nt,1)*NaN;
for j=1:nt
    k=find(vtpk1 > int_vtpk1(j)-0.5 & vtpk1 <= int_vtpk1(j)+0.5);
    if ~isempty(k)
        s_media_vtpk1(j)=mean(s(k));
        s_mediana_vtpk1(j)=median(s(k));
        s_per70_vtpk1(j)=percentile(s(k),0.7);
    end
end

%int_vtpk1=int_vtpk1(3:9);s_media_vtpk1=s_media_vtpk1(3:9)';s_mediana_vtpk1=s_mediana_vtpk1(3:9)';s_per70_vtpk1=s_per70_vtpk1(3:9);
aux=[int_vtpk1 s_media_vtpk1 s_mediana_vtpk1 s_per70_vtpk1];
fid=fopen('vtpk1_s.dat','w');
for j=1:length(int_vtpk1);
    fprintf(fid,'%5.2f %5.2f %5.2f %5.2f\n',aux(j,:));
end
fclose(fid)

% save vtpk1_s.dat -ascii aux


% [P,S] = polyfit(int_vtpk1,s_media_vtpk1,2); P
% ajuste_s_media_vtpk1=(int_vtpk1.^2).*P(1)+int_vtpk1.*P(2)+P(3);
% figure;plot(int_vtpk1,s_media_vtpk1,'r+');grid on;xlabel('Tp1 (m)');ylabel('spreading s');title('MEDIA s x TP1')
% hold on;plot(int_vtpk1,ajuste_s_media_vtpk1,'r')
% 
% 
% [P,S] = polyfit(int_vtpk1,s_mediana_vtpk1,2); P
% ajuste_s_mediana_vtpk1=(int_vtpk1.^2).*P(1)+int_vtpk1.*P(2)+P(3);
% figure;plot(int_vtpk1,s_mediana_vtpk1,'ko');grid on;xlabel('Tp1 (m)');ylabel('spreading s');title('MEDIANA s x TP1')
% hold on;plot(int_vtpk1,ajuste_s_mediana_vtpk1,'r')
% 
% 
% [P,S] = polyfit(int_vtpk1,s_per70_vtpk1,2); P
% ajuste_s_per70_vtpk1=(int_vtpk1.^2).*P(1)+int_vtpk1.*P(2)+P(3);
% figure;plot(int_vtpk1,s_per70_vtpk1,'m*');grid on;xlabel('Tp1 (m)');ylabel('spreading s');title('per70 s x TP1')
% hold on;plot(int_vtpk1,ajuste_s_per70_vtpk1,'r')

% Selecionando os intervalos simultaneos de VCAR1, VTPK1 e s_VTPK1
nx=length(int_vcar1);ny=length(int_vtpk1);
s_media_vcar1_vtpk1=ones(nx,ny)*NaN;s_mediana_vcar1_vtpk1=ones(nx,ny)*NaN;s_per70_vcar1_vtpk1=ones(nx,ny)*NaN;
for jx=1:length(int_vcar1)
    for jy=1:length(int_vtpk1)
        k=find(vcar1 > int_vcar1(jx)-0.5 & vcar1 <= int_vcar1(jx)+0.5 & vtpk1 > int_vtpk1(jy)-0.5 & vtpk1 <= int_vtpk1(jy)+0.5 );
        if ~isempty(k)
            s_media_vcar1_vtpk1(jx,jy)=mean(s(k));
            s_mediana_vcar1_vtpk1(jx,jy)=median(s(k));
            s_per70_vcar1_vtpk1(jx,jy)=percentile(s(k),0.7);
        end
    end
end
%
fid=fopen('s_vcar1_vtpk.dat','w');
for jx=1:length(int_vcar1)
    for jy=1:length(int_vtpk1)
        aux=[int_vcar1(jx) int_vtpk1(jy) s_media_vcar1_vtpk1(jx,jy) s_mediana_vcar1_vtpk1(jx,jy) s_per70_vcar1_vtpk1(jx,jy)];
        fprintf(fid,'%5.2f %6.2f %6.2f %6.2f %6.2f\n',aux);
    end
end
fclose(fid);


x=a(:,33);y=a(:,32);z=a(:,69);
figure;plot3(x,y,z,'*');xlabel('VTPK1');ylabel('VCAR1');zlabel('s_VTPK1');grid on
%[x, y] = meshgrid(x,y);
%figure;surf(x,y,z);

% Montando funcao 
