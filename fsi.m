warning off

% Listando os arquivos na pasta de arqs de dados
%     diretorio=['Z:\Reservado\03.METEO-OCEANOGRAFIA\Disponibilização\Analise_de_dados\Dados\Onda_FSI_ADCP\PCE'];
%     diretorio=['../dados/pch2/'];
%    diretorio=['./pch2_j/'];
      diretorio=['./temp/'];
%     diretorio=['../dados/p34/'];
    arqs_dados=dir([diretorio '*.fsi']);

% Cabecalho e rabo dos arquivos brutos de dados:    
    cabeca=26; % cabecalho;
    rabo=6;
    
% Verificando o número de arquivos (=num de linhas de arqs_dados)
    [l,c]=size(arqs_dados);  

% Gerando um arquivo de saida de dados
arqsai=input('Entre com nome do arquivo de saida .dat (nome com extensao):','s'); 
fid2=fopen(arqsai,'w'); header='%  DATA     Dir       Ucor     Vcor     mare'; fprintf(fid2,'%s\n',header);

% Parametros de entrada para a rotina de calculo de ondas
%     ngl=32;     % Graus de liberdade
    hlocal=100;  % Profundidade local
    DT=1; dt=DT; % Intervalo de amostragem
    
% Barra de espera:
    h=waitbar(0,'Aguarde...');

% Loop variando os arquivos na pasta com os dados
for k=1:l
    % Bara de espera
    waitbar(k/l,h);
    
    % Lendo os arquivos de dados com a rotina readtext
    [a,b]= readtext([diretorio arqs_dados(k).name], '[,\t]');
    arqdad=arqs_dados(k).name;
    for m=cabeca:(length(a)-rabo)
        dado=char(a(m));
        dados(m-cabeca+1,:)=str2num(dado(10:end));
    end
    
    % Matriz de dados
    press=dados(:,4);
    u=dados(:,end); %u
    v=dados(:,end-1); %v
    w=dados(:,3); %end-11
    p=(press-1012.5)/100;
%      p=press;
    pr=p(1:1024);
    uu=u(1:1024);
    vv=v(1:1024);
    ww=w(1:1024);
    
    daatpuv1;
    %daat2010oceanop;
    
%     [i1 i2]=max(matr1);
%     [i11 i22]=max(i1);
%     %[i11 i22]=min(i2);
%     dire=i22*4;

% u=detrend(u);
% v=detrend(v);
% w=detrend(w);
% p=detrend(p);
    cota=-15;


    ano=str2num(arqdad(1,end-19:end-16)); mes=str2num(arqdad(1,end-14:end-13)); dia=str2num(arqdad(1,end-11:end-10));
    hora=str2num(arqdad(1,end-8:end-7));minu=str2num(arqdad(1,end-5:end-4));
    n =datenum(ano,mes,dia,hora,minu,0);

%     return
 %--------------------
% [VCAR,VTPK,VPED,f,esp]=proc_fsi_ver0(press,u,v,w);
% for pot=4:6;
%     janseg=2^pot;
%     [dirp,f,zxx,Spp,Sxz,imax,Tp,VCAR]=corrcruz_uggo22(cota,p,u,v,w,dt,janseg);   VTPK=Tp; VPED=dirp; 
%     eval(['dire' num2str(pot) '(k)=dirp;']);
% end
%   janseg=256; [dirp,f,zxx,Spp,Sxz,imax,Tp,VCAR]=corrcruz_uggo2(cota,p,u,v,w,dt,janseg);   VTPK=Tp; VPED=dirp; 
%  [f,Spp,Suu,Spv,imax,tpp]=corrcruz_uggo21(w,v,dt,256);

% [VF, VS, VTPK, VCAR, VPED, VEPK, VSPK, VD, SPRD, ESP, el, HCSP, HCDT, SDCS, SDCD, SLEV, VCSP, sigma1, sigma2,...
%     [VMTA,VMTB,VMTC,VMTD,VMTE]=trat_puv_spr_barra2(p,u,v,w,DT,ngl,h,hlocal);

% [VTPK, VCAR, VPED]=puv_modified(press,u,v,w,DT,ngl,hlocal,cota);

%      [VS,VD, VF, VTPK, VCAR, VPED]=puv_modified2(press,u,v,DT,ngl,h,hlocal);

%     [VF, VS, VTPK, VCAR, VPED, VEPK, VSPK, VD, SPRD, ESP, el, HCSP, HCDT, SDCS, ...
%         SDCD, SLEV, VCSP, sigma1, sigma2,VMTA,VMTB,VMTC,VMTD,VMTE]=puv(press,u,v,w,DT,ngl,h,hlocal);
%     [VCAR,VTPK,VPED] = waveparam(p,u,v,w,1,100,-15,-15,[.05 .3],128,50);
%                         %  p,u,v,w,dt,hl,dpp,dpv,frcoff,wnp,ovlp
%     
% VPED=; VCAR=Hs; VTPK=T;


% figure(20), hold on, plot(n,VCAR,'o')
% figure(21), hold on, plot(n,VTPK,'*k')
% figure(22), hold on, plot(n,VPED,'*k')


% figure(5), hold on, plot(f,esp)

% figure(20),hold on, plot(n,VCAR,'og')                     
% figure(21),hold on, plot(n,VTPK,'og') 
% figure(22),hold on, plot(n,VPED,'og') 

    Ucor=mean(u);
    Vcor=mean(v);
    mare=mean(p);
    
%     hs =VCAR;% 4*sqrt(VMTA');

    clear dados dado;
% mare=t;

%     dad=  [n  hs   VTPK  VPED Ucor Vcor mare];
%    
%     % Salvando como arquivo ASCII
%     formato='%8.2f %6.2f %6.2f %8.2f %8.2f %8.2f %8.2f\n';
%     fprintf(fid2,formato,dad');

% % %     dad=  [n  direc Ucor Vcor mare];
% % %    
% % %     % Salvando como arquivo ASCII
% % %     formato='%8.2f  %8.2f %8.2f %8.2f %8.2f   %8.2f %8.2f %8.2f\n';
% % %     fprintf(fid2,formato,dad');

% %     u=u-mean(u);v=v-mean(v);
% %     [th,R]=cart2pol(u,v);th=th*180/pi;
% %     vect=[th R];
% %     vect1=sortrows(vect,1);
% % %     [U,V]=pol2cart(teta,vect1(:,2));
% % %     x=1:length(U);y=zeros(1,length(U));
% % %     figure,quiver(x,y,U,V)
% %     vetor(find(vect(:,1)<0),1) = 180 + vect(find(vect(:,1)<0),1);
% %     figure(1),hist(vetor(:,1),18*2)
% %     pause(.5)
end

fclose all;
close(h)
clear DT Ucor Vcor a ano arqdad arqs_dados b c cabeca cota dia diretorio dt
clear hora k l m mare mes minu n press rabo h hlocal


