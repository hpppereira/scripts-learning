%
% *************  EXTREME ANALYSIS ROUTINE  **********************
% --------- Technique: Peaks Over Threshold (POT) ---------------------
%
% Author:     Ricardo Martins Campos      e-mail:  riwave@gmail.com
% July 2009 - version 1.0
% Guidance and collaboration: Carlos Eduardo Parente Ribeiro (COPPE/UFRJ) -
% Brazil
%                             Felipe Leite (COPPE/UFRJ) - Brazil
%                             Eric Oliveira Ribeiro (CENPES/PETROBRAS) - Brazil
%                             Luis Manoel Paiva Nunes (CENPES/PETROBRAS) - Brazil
%                             Marcelo Andrioni (CENPES/PETROBRAS) - Brazil
%                             Slim Gana (SAROST) - Tunisia
% ______________________________________________________________________
%
% The input file must be formated with just one column containing the
% values of the variable of interest, without header. Do not use comma (,)!
%
% *********************************************************************
%


clear all, clear global, close all, fclose all, clc


disp('======================================================================================');
disp('Extreme analysis (univariate) routine using the Peaks Over Threshold (POT) techique');
disp('======================================================================================');
disp('Author:     Ricardo Martins Campos      e-mail:  riwave@gmail.com');
disp('Guidance and collaboration: Carlos Eduardo Parente, Felipe Leite, Eric Oliveira, Luis Manoel, Marcelo Andrioni and Slim Gana');
disp('-------------------------------------------------------------------------------------');
disp('The input file must be formated with just one column containing the values of the variable of interest, without header.');



[arqdad,pafdad]=uigetfile('*.txt','Select the input file name for the extreme analysis');
if ~isstr(arqdad); return; end;
h=load([pafdad,arqdad],'r');

[arqsai,pafsai]=uiputfile([pafdad,'*.txt'],'Choose an output file name for saving the return values');
if ~isstr(arqsai); return; end;

clear pafdad arqdad;

nddadosserie =num2str(length(h));
disp(' ');
disp(['Data length (number of points): ',nddadosserie]);


prompt={'Number of months available',...
    'Measurement interval in hours (time between measurements)'};

def={'',''};
dlgTitle=['Extreme analysis. First step.'];
lineNo=1;
answer=inputdlg(prompt,dlgTitle,lineNo,def);

nmeses=str2num(char(answer(1)));
intmed=str2num(char(answer(2)));

% calcuting the sugested time window to ensure the statistical independence
[B,A] = butter(3,1/(length(h)/30)); suave = filtfilt(B,A,h); resi = h-suave;
clear B A suave
np=round(length(resi)/30);
t=autocorr(resi,np,1);
v=1+round(length(resi)/500); % minimos de autocorr locais de 20 horas
i=v+1;
teste=1;
while teste~=0
    n=t(i-v:i-1);m=t(i+1:i+v);
    if t(i)< 0.3
        if t(i-1)>t(i) & t(i+1)>t(i)
            if min(m)>t(i) & min(n)>t(i)
                jts=i*intmed;
                teste=0;
            end
        end
    end
    i=i+1;
end

jts=num2str(jts);

clear np teste v i t n m resi


binsize=num2str((max(h)-min(h))/20);

prompt={'Variable name (for exemple: Wave height, Wind speed, Surface temperature etc)',...
    'Unit (for exemple: m, m/s, C etc)',...
    'Time window (in hours) - required time (minimum) between the extremes to ensure the statistical independence',...
    'Minimum value for the analysis of extreme events',...
    'Bin size of the histogram'};

def={'Wave height','m',jts,'0.0',binsize};
dlgTitle=['Extreme analysis. First step.'];
lineNo=1;
answer=inputdlg(prompt,dlgTitle,lineNo,def);

nomev=char(answer(1));
unidade=char(answer(2));
jt=str2num(char(answer(3)));
vmin=str2num(char(answer(4)));
inthist=str2num(char(answer(5)));

% --------------------------------------------------
% Selecting the statistically independent events
% --------------------------------------------------
jt=jt/2; jt=round(jt/intmed);
cont=0;

for i=(jt+1):(length(h)-jt)
    aux=0;
    if h(i)>vmin
        for j=(i-jt):(i-1)
            if h(j)>h(i)
                aux=0;
            else
                aux=aux+1;
            end
        end
        for j=(i+1):(i+jt)
            if h(j)>h(i)
                aux=0;
            else
                aux=aux+1;
            end
        end
    end
    if aux == (jt*2)
        cont=cont+1;
        hs(cont)=h(i);
    end
end

clear cont aux bjt jts h i j pp sp nddadosserie vmin

% titulo='testando'; fecha=1;
% [varargout vari] = pot_gpd(hs,nmeses,titulo,fecha)

% ____ Starting the analysis - first graphs [proposed by (EMBRECHTS et al., 1997)] ___

% --- Plotting the events ---------

y=sort(hs);
tam=length(y);
na=num2str(y(1));
nb=num2str(y(end));

figure(1)

subplot(2,2,1:2);colormap copper;bar(hs,0.05,'stacked')
hold on;plot(hs,'ko');axis tight
% iid= statistically independent and identically distributed
title('Events iid selected')
neixo=([nomev,' (',unidade,')']);
xlabel('Selected events'), ylabel(neixo)


% ---- Initial Histogram -------
subplot(2,2,3); hb=[y(1):inthist:max(hs)];
% getting the values of the histogram
[hisa,hb]=hist(hs,hb);bar(hb,100*hisa/max(size(hs)),'k');hold on
title('Histogram of the selected iid events');xlabel(neixo);ylabel('Ocurrence (%)')


% ---- Events in ascending order ---------
subplot(2,2,4); plot(y,'ko'); axis tight; grid on
eixoy=([nomev,' (',unidade,')']);
title('Distribution of the selected events'), xlabel('Selected peaks'), ylabel(eixoy)


% ---- Number of events versus threshold ----

u=linspace(min(y),max(y),tam)';
for i=1:tam;
    mql = find(y>u(i));
    m(i,1) = mean(y(mql));
    nal(i,1) = length(mql);
end

figure (2); subplot(2,2,[1 2]); plot(u,nal,'k'); hold on; plot(u,nal,'k.');
grid on;  axis tight;
eixox=(['Threshold (',unidade,')']);
title('Distribution of peaks over threshold versus threshold'), xlabel(eixox), ylabel('Number of peaks over threshold')
hold on

% ---- Percentage of events versus threshold ----

pnal=(nal/tam)*100;
subplot(2,2,[3 4]);  plot(u,pnal,'k');  hold on;  plot(u,pnal,'k.')
grid on; axis tight;  title('Percentage distribution of peaks over threshold versus threshold'),
xlabel(eixox), ylabel('% of peaks over threshold')
% red lines.
plot(u([1 end]),[25 25],'r','linewidth',0.01); clear linha;
plot(u([1 end]),[3 3],'r','linewidth',0.01); clear linha;
% blue lines (BELITSKY & MOREIRA, 2007).
plot(u([1 end]),[15 15],'b--','linewidth',0.005); clear linha;
plot(u([1 end]),[10 10],'b--','linewidth',0.005); clear linha;


% ---- Choosing the threshold ---------
% ---- MEAN EXCESS PLOT -----------

figure(3), set(gcf,'color',[1 1 0.8]), plot(u,m-u,'k'), axis tight
eixox=(['Threshold (',unidade,')']);
eixoy=(['Mean of excess over threshold minus threshold (',unidade,')']);
title('Mean Excess Plot','fontsize',13,'color','k','fontweight','bold','FontName','Arial'), xlabel(eixox), ylabel(eixoy)
colordef white

%-----------------------------------------------
% GPD fit using wgpdfit function

for i=1:tam

    c=y(y>u(i))-u(i);
    % Using the Moment Methods. Based on Hosking&Wallis(1987)
    % Revised by Ricardo Campos (08/07/2009). Same as WAFO.
    teste= nal(i); % General number of peaks over threshold
    if teste>3
        nu(i,1)= teste; % Number os peaks over threshold used.
        csi(i,1)=(1/2)*(((mean(c)^2)/(std(c)^2))-1);
        beta(i,1)=(1/2)*mean(c)*((mean(c)^2/(std(c)^2))+1);
        if (csi(i,1)<=-0.25),
            cov=ones(2)*NaN;
            warning([' The estimate of shape (' num2str(csi(i,1)) ') is not within the range where the Moment estimator is valid (csi>-0.25).'])
        else
            Vshape = (1+2*csi(i,1))^2*(1+csi(i,1)+6*csi(i,1)^2);
            Covari = beta(i,1)*(1+2*csi(i,1))*(1+4*csi(i,1)+12*csi(i,1)^2);
            Vscale = 2*beta(i,1)^2*(1+6*csi(i,1)+12*csi(i,1)^2);
            cov_f = (1+csi(i,1))^2/(1+2*csi(i,1))/(1+3*csi(i,1))/(1+4*csi(i,1))/length(c);
            cov=cov_f*[Vshape Covari; Covari, Vscale];
            covac(i,1)=cov(1,1); covab(i,1)=cov(2,2);
        end

    end

end

eita=length(covac);
v=u(1:eita);

% --- Variance of the shape parameter (calculated by the estimators) varying the threshold ----

figure(4)
subplot(2,2,[1 2]);
plot(v,covac,'k','linewidth',1)
eixoyv=(['Variance ( (',unidade,')^2 )']);
title('Variance of the shape parameter versus threshold'), xlabel(eixox), ylabel(eixoyv)
legend('MOM'); grid on;
if max(covac)<0.7
    axis tight
else
    axis([min(v) max(v) 0 0.7])
end


% ______________________________________________________________________

clc

% -------------------------------------------------------------------------
% ---- Calculating the shape parameter with confidence interval (c.i.) ----

varcsi=covac;

intconfiq=csi-(1.96.*( sqrt(varcsi) ./ sqrt(nu) ));
intconfsq=csi+(1.96.*( sqrt(varcsi) ./ sqrt(nu) )); 

subplot(2,2,[3 4]);
plot(v,csi,'k','linewidth',1.5);hold on; grid on
plot(v,intconfiq,'k--','linewidth',0.2)
plot(v,intconfsq,'k--','linewidth',0.2); axis tight
title('Shape parameter (with c.i.) versus threshold'), xlabel(eixox), ylabel('Shape parameter')


% --- Calculating the extremes (the return values) versus threshold -------
anos = [nmeses/12 5 50 100];
proba = 1-( 1 ./( (anos*12*tam)/nmeses ) )';

for  ii = 1:length(proba);
    % HOSKING&WALLIS(1987) eq.7
    eer(:,ii) = v+(beta./csi).*[1-((1-proba(ii)).^(csi))];
end

% The figure show the return values based on diferent formulations. Remove the % inside the last loop
% figure;plot(v,heer(:,4),'k');hold on;plot(v,weer(:,4),'r:');plot(v,eeer(:,4),'b')

figure(5);
plot(v,eer(:,1),'k','linewidth',[1.5]); hold on;
plot(v,eer(:,2),'m:','linewidth',[0.5]);
plot(v,eer(:,3),'g--','linewidth',[0.5]);
plot(v,eer(:,4),'b','linewidth',[0.5]);
grid on; axis([min(v) max(v) 0 3*max(y)]);
eixoy=(['Return value - ',nomev,' (',unidade,')']);
title('Extreme values for static return periods versus threshold'), xlabel(eixox), ylabel(eixoy)
legend([num2str(nmeses),' months'],'5 years', '50 years','100 years');
hold on; plot([min(v) max(v)],[max(y) max(y)],'y','linewidth',[1.5]);



% -------------------------------------------------------------------------
% ----- Correlation Coefficient and Root Mean Square versus Threshold -----

for i=1:length(v)

    c = y(y>v(i))-v(i); nu = length(c);

    csi=(1/2)*(((mean(c)^2)/var(c))-1);
    beta=(1/2)*mean(c)*(((mean(c)^2)/var(c))+1);

    proba=linspace(0,1-1/tam,length(c));
    % HOSKING&WALLIS(1987) eq.7
    x = (beta./csi).*[1-((1-proba).^(csi))];

    corre=corrcoef(c,x);corrc(i)=corre(1,2);

    emq(i)=0;
    for j=1:length(c)
        emq(i)=emq(i)+sqrt((c(j)-x(j))^2);
    end
    emq(i)=emq(i)/length(c);

end

figure(6);
subplot(2,2,[1 2])
plot(v,emq,'k','linewidth',[1.5]);
if max(emq)>mean(y)
    axis([min(v) max(v) min(emq) mean(y)]);
else
    axis tight;
end
grid on; eixoy2=(['Root Mean Square (',unidade,')']);
title('Root Mean Square (Empirical and GPD) versus Threshold'), xlabel(eixox),ylabel(eixoy2)

subplot(2,2,[3 4])
plot(v,corrc,'k','linewidth',[1.5]);
if min(corrc)<0.5
    axis([min(v) max(v) 0.5 max(corrc)]);
else
    axis tight;
end
grid on;
title('Correlation coefficient (Empirical and GPD) versus Threshold'), xlabel(eixox), ylabel('Correlation Coefficient');

% --------------------------------------------------------------------
% --------------------------------------------------------------------

clc
disp(['Highest value: ',nb]);
disp('======================================================================================');
disp('Analyse the graphs, think about the best threshold to fit the GPD and PRESS ENTER');
disp('======================================================================================');

pause

prompt={'Choose a threshold'};
def={''};
dlgTitle=['The choose of the threshold to fit the GPD. Third step.'];
lineNo=1;
answer=inputdlg(prompt,dlgTitle,lineNo,def);
th=str2num(char(answer(1)));


c = y(y>th)-th; nu = length(c);

csi=(1/2)*(((mean(c)^2)/var(c))-1);
beta=(1/2)*mean(c)*(((mean(c)^2)/var(c))+1);
if (csi<=-0.25)
    cov=ones(2)*NaN;
    warning([' The estimate of shape (' num2str(csi) ') is not within the range where the Moment estimator is valid (csi>-0.25).'])
else
    Vshape = (1+2*csi)^2*(1+csi+6*csi^2);
    Covari = beta*(1+2*csi)*(1+4*csi+12*csi^2);
    Vscale = 2*beta^2*(1+6*csi+12*csi^2);
    cov_f = (1+csi)^2/(1+2*csi)/(1+3*csi)/(1+4*csi)/length(c);
    cov=cov_f*[Vshape Covari; Covari, Vscale];
    covac=cov(1,1); covab=cov(2,2);
end


% HOSKING&WALLIS(1987) eq.7
proba=linspace(0,1-1/tam,length(c));
x = (beta./csi).*[1-((1-proba).^(csi))];

figure(7)


subplot(2,2,[1 2])
plot(c+th,x+th,'ko'); hold on;
g=linspace((min([min(c+th) min(x+th)])-(min(c+th)/10)),(max([max(c+th) max(x+th)])+(max(c+th)/10)),length(c));
plot(g,g,'k')
axis([(min([min(c+th) min(x+th)])-(min(c+th)/10)) (max([max(c+th) max(x+th)])+(max(c+th)/10)) (min([min(c+th) min(x+th)])-(min(c+th)/10)) (max([max(c+th) max(x+th)])+(max(c+th)/10))]);

eixoy2=(['Mean values of order statistics (',unidade,') - GPD']);
eixox2=(['Ordered peak (',unidade,') - Empirical function']);
title('GPD fitted to the tail exceedances - Estatistical Model versus Empirical'), xlabel(eixox2),
ylabel(eixoy2)

subplot(2,2,[3 4])
plot(c+th,'ko');hold on;plot(x+th,'r*');
axis([0 (length(c)+1) (min([min(c+th) min(x+th)])-(min(c+th)/10)) (max([max(c+th) max(x+th)])+(max(c+th)/10))]);
title('GPD fitted to the tail exceedances - Estatistical Model versus Empirical'), xlabel('Peaks over threshold'),
ylabel(eixoy2), legend('Empirical Values','GPD');

coeficiente=corrcoef(c,x);
ncoef=num2str(coeficiente(2,1));
disp(['Correlation coefficient: ',ncoef]);
disp(' ');

% ------------------------------------------------
% ------------------------------------------------


disp('======================================================================================');
disp('Analyse the fit, think about the theshold chosen and PRESS ENTER');
disp('======================================================================================');

pause

prompt={'Is the threshold acceptable (do you want to keep the value) ?',...
    'Do you want to calculate the return values with CONFIDENCE INTERVAL (indicated) ?'};

def={'yes','yes'};
dlgTitle=['Return values estimation. Final step.'];
lineNo=1;
answer=inputdlg(prompt,dlgTitle,lineNo,def);

avlim=answer{1};
avic=answer{2};

if strcmpi(avlim,'no')

    disp('__________________________________________________________________________');
    disp('Restart the analysis looking for a threshold that favors the linearity of');
    disp('the values over it in the MEAN EXCESS PLOT graphics (figure 6)');
    disp('.');
    disp('Read the following references in the guide:');
    disp('(EMBRECHTS et al., 1997)');
    disp('(COLES, S., 2007)');
    disp('(CAMPOS, 2009)');
    disp('(BELITSKY e MOREIRA, 2007)');
    disp('(MENDES, 2004)');
    disp('(FERREIRA e GUEDES SOARES, 1998)');
    disp('(CARDOSO JUNIOR, 2004)');
    disp('(SILVA, 2008)');

else

    close all;
    clear nint;

    % ---------------------------------------------------------------------------

    prompt={'Maximum return period (in years) for the vector of return values (extremes)',...
        'Any other specific return period? Type the period (in hours). Enter 0 (zero) if you do not want to'};

    def={'100','1000'};
    dlgTitle=['Additional return period. Final step.'];
    lineNo=1;
    answer=inputdlg(prompt,dlgTitle,lineNo,def);

    tvr=char(answer(1));
    tvr=str2num(tvr);

    nano=char(answer(2));
    oano=str2num(nano);

    % ---------------------------------------------------------

    if strcmpi(avic,'yes')

        prompt={'Enter with the number of iterations (ideal: 100000).'};
        def={'100000'};
        dlgTitle=['The calculation of the confidence interval (c.i.). Final step.'];
        lineNo=1;
        answer=inputdlg(prompt,dlgTitle,lineNo,def);
        nint=str2num(char(answer(1)));

        if nint<10000
            disp(' ');
            disp('The number of iterations chosen will not generate a realistic confidence interval');
            disp('A good estimate of the confidence interval requires a number of iterations equal to or greater than 10000');
            disp(' ');
        end

        if tvr>=100 & nint>=100000
            if nint<1000 & tvr<1000000
                disp(' ');
                disp('Please wait. It may take some minutes.');
                disp(' ');
            end
        end
        if tvr>=1000 & nint>=1000000
            disp(' ');
            disp('Please wait. It may take several hours.');
            disp(' ');
        end

        x=linspace(0,1,nint+2);
        qsim=norminv(x,csi,sqrt(covac)); qsim=qsim(2:end-1);
        bsim=norminv(x,beta,sqrt(covab)); bsim=bsim(2:end-1);
        clear x

        barra3 = waitbar(0,'Please wait.');

        for i=1:tvr


            N=(i*12*tam)/nmeses;
            p=1-1/N;

            % HOSKING&WALLIS(1987) eq.7
                xr(i) = th+(beta./csi).*[1-((1-p).^(csi))];
                vxr(i)=var(th+(bsim./qsim).*[1-((1-p).^(qsim))]);
           
            eintconfsxr(i)=xr(i)+(1.96*( std(c) / sqrt(N) ));
            eintconfixr(i)=xr(i)-(1.96*( std(c) / sqrt(N) ));


            intconfsxr(i)=xr(i)+(1.96*( sqrt(vxr(i)) / sqrt(tam) ));
            intconfixr(i)=xr(i)-(1.96*( sqrt(vxr(i)) / sqrt(tam) ));


            ni=num2str(i);
            disp(['Return value and confidence interval for ',ni,' years']);
            waitbar(i/tvr,barra3)

        end

        close(barra3)

        disp('.');

        an=linspace(1,tvr,tvr);
        figure(8)
        set(gcf,'color',[0.9 0.95 0.97])
        plot(an,xr,'k','linewidth',[1.5])
        hold on
        plot(an,intconfsxr,'k--','linewidth',[0.5])
        plot(an,intconfixr,'k--','linewidth',[0.5])
        plot(an,eintconfsxr,'k:','linewidth',[0.5])
        plot(an,eintconfixr,'k:','linewidth',[0.5])
        eixoy3=(['Return Values - ',nomev,' Extremes (',unidade,')']);
        title('Return value (extremes) versus return period','fontsize',11,'color','k','fontweight','bold','FontName','Arial'), xlabel('Years'), ylabel(eixoy3)


        sai=fopen([pafsai,arqsai],'w');
        fprintf(sai,'%10.5f\n',xr);
        fclose(sai);
        clear sai;

        sai=fopen([pafsai,'rv_variance.txt'],'w');
        fprintf(sai,'%10.5f\n',vxr);
        fclose(sai);
        clear sai;

        sai=fopen([pafsai,'upperconfint_extremes.txt'],'w');
        fprintf(sai,'%10.5f\n',intconfsxr);
        fclose(sai);
        clear sai;

        sai=fopen([pafsai,'lowerconfint_extremes.txt'],'w');
        fprintf(sai,'%10.5f\n',intconfixr);
        fclose(sai);
        clear sai;



        if oano==0

            disp('======================================================================================');
            disp('********   END OF ANALYSIS  *********');
            disp('Extremes (return values) from 1 to 100 years saved in return_values.txt');
            disp('Variance of the estimative in rv_variance.txt');
            disp('Upper confidence interval in upperconfint_extremes.txt');
            disp('Lower confidence interval in lowerconfint_extremes.txt');
            disp('======================================================================================');

        else

            N=(oano*12*tam)/nmeses;
            p=1-1/N;

            % HOSKING&WALLIS(1987) eq.7
            xroano = th+(beta./csi).*[1-((1-p).^(csi))];

            nxroano=num2str(xroano);
            noano=num2str(oano);
            disp(['Extreme (highest) ',nomev,' for ',noano,' years (return value) = ',nxroano,' ',unidade]);
            disp('.');

            nomesaida=(['specific_return_value',nano,'.txt']);
            sai=fopen([pafsai,nomesaida],'w');
            fprintf(sai,'%10.5f\n',xroano);
            fclose(sai); clear nomesaida

            disp('======================================================================================');
            disp('********   END OF ANALYSIS   *********');
            disp('Extremes (return values) from 1 to 100 years saved in return_values.txt');
            disp(['Extreme (return value) for ',noano,' years saved in specific_return_value',nano,'.txt']);
            disp('Variance of the estimative in rv_variance.txt');
            disp('Upper confidence interval in upperconfint_extremes.txt');
            disp('Lower confidence interval in lowerconfint_extremes.txt');
            disp('======================================================================================');

        end

    else


        for i=1:tvr

            N=(i*12*tam)/nmeses;
            p=1-1/N;

            % HOSKING&WALLIS(1987) eq.7
            xr(i) = th+(beta./csi).*[1-((1-p).^(csi))];

        end

        an=linspace(1,tvr,tvr);

        set(gcf,'color',[0.70 0.80 0.97])
        plot(an,xr,'k','linewidth',[1.5])
        eixoy3=(['Return Values - ',nomev,' Extremes (',unidade,')']);
        title('Return value (extremes) versus return period','fontsize',11,'color','k','fontweight','bold','FontName','Arial'), xlabel('Years'), ylabel(eixoy3)

        sai=fopen([pafsai,arqsai],'w');
        fprintf(sai,'%10.5f\n',xr);
        fclose(sai);

        if oano==0

            disp('======================================================================================');
            disp('********   END OF ANALYSIS   *********');
            disp('Extremes (return values) from 1 to 100 years saved in return_values.txt');
            disp('======================================================================================');

        else

            N=(oano*12*tam)/nmeses; p=1-1/N;

            % HOSKING&WALLIS(1987) eq.7
            xroano = th+(beta./csi).*[1-((1-p).^(csi))];

            nxroano=num2str(xroano); noano=num2str(oano);
            disp(['Extreme (highest) ',nomev,' for ',noano,' years (return value) = ',nxroano,' ',unidade]);
            disp('.');

            nomesaida=(['return_value',nano,'.txt']);
            sai=fopen([pafsai,nomesaida],'w');
            fprintf(sai,'%10.5f\n',xroano);
            fclose(sai);clear nomesaida

            disp('======================================================================================');
            disp('********  END OF ANALYSIS   *********');
            disp('Extremes (return values) from 1 to 100 years saved in return_values.txt');
            disp(['Extreme (return value) for ',noano,' years saved in specific_return_value',nano,'.txt']);
            disp('======================================================================================');


        end


    end

end

disp('.')
disp('Thank you for using extremesPOT.m');
disp('Please, send your questions, suggestions and opinion to:  riwave@gmail.com');
disp('Ricardo Martins Campos');
