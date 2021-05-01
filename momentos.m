function [VMTA1,VMTB1,VMTC1,VMTD1,VMTE1,VCAR1,VTPK1,VSPK1,VEPK,VEPK1,VPED1,VMTA2,VMTB2,VMTC2,VMTD2,VMTE2,VCAR2,VTPK2,VSPK2,VEPK2,VPED2,VMTA3,VMTB3,VMTC3,VMTD3,VMTE3,VCAR3,VTPK3,VSPK3,VEPK3,VPED3] = momentos(fScava,Spico,fSpico,dSpico,VF,VS,NDT,VMTA,VMTB,VMTC,VMTD,VMTE,VTPK,VSPK,VEPK,VPED,VESP,pdir);
%
% Funcao para calculo dos momentos espectrais 
%
% J.A. LIma 21/07/99
%
% -------------------------------------------------------------------------
% OBS: Os vetores de entrada Spico,fSpico,dSpico,Scava,fScava,dScava foram
% calculadas na totina "sele_pico":
% Os picos sao fornecidos em ordem decrecente, ou seja,
% Spico(1) armazena o maior pico espectral, Spico(2) o
% segundo maior pico espectral, e Spico(3) o terceiro pico.
% O vetor Scava possui a ordenada do minimo espectral que
% antecede o Spico correspondente.
%========================================================================
%
% Calculo dos momentos espectrais por bandas de periodos de pico
for k=1:length(fScava)
   if length(fScava) == 1
      VMTA1=VMTA;VMTB1=VMTB;VMTC1=VMTC;VMTD1=VMTD;VMTE1=VMTE;
      VCAR1=4*sqrt(VMTA1);
      VTPK1=VTPK;VSPK1=VSPK;
      if pdir
         VPED1=VPED;VEPK1=VEPK;
      else
         VPED1=-999.99;VEPK1=-999.99;
      end
      VMTA2=-999.99;VMTB2=-999.99;VMTC2=-999.99;VMTD2=-999.99;VMTE2=-999.99;VCAR2=-999.99;
      VTPK2=-999.99;VSPK2=-999.99;VEPK2=-999.99;VPED2=-999.99;
      VMTA3=-999.99;VMTB3=-999.99;VMTC3=-999.99;VMTD3=-999.99;VMTE3=-999.99;VCAR3=-999.99;
      VTPK3=-999.99;VSPK3=-999.99;VEPK3=-999.99;VPED3=-999.99;
   elseif length(fScava) == 2
      % Colocando as frequencias dos cavados espectrais em ordem crescente 
      [auxf nf]=sort(fScava);
      k0=find(VF == fScava(nf(1)));k1=find(VF == fScava(nf(2)));kc=length(VF);
      mo0=[sum(VS(k0:k1).*(1/NDT)) (VMTA-sum(VS(k0:k1).*(1/NDT)))];
      mo1=[sum(VF(k0:k1).*VS(k0:k1))/NDT sum(VF(k1:kc).*VS(k1:kc))/NDT];
      mo2=[sum(VF(k0:k1).^2.*VS(k0:k1))/NDT sum(VF(k1:kc).^2.*VS(k1:kc))/NDT];
      mo3=[sum(VF(k0:k1).^3.*VS(k0:k1))/NDT sum(VF(k1:kc).^3.*VS(k1:kc))/NDT];
      mo4=[sum(VF(k0:k1).^4.*VS(k0:k1))/NDT sum(VF(k1:kc).^4.*VS(k1:kc))/NDT];
      picos=Spico(nf);
      [auxS nk]=sort(picos);
      VMTA1=mo0(nk(2));VMTB1=mo1(nk(2));VMTC1=mo2(nk(2));VMTD1=mo3(nk(2));VMTE1=mo4(nk(2));VCAR1=4*sqrt(VMTA1);
      VTPK1=VTPK;VSPK1=auxS(2);
      VMTA2=mo0(nk(1));VMTB2=mo1(nk(1));VMTC2=mo2(nk(1));VMTD2=mo3(nk(1));VMTE2=mo4(nk(1));VCAR2=4*sqrt(VMTA2);
      VTPK2=1./fSpico(2);VSPK2=auxS(1);
      if pdir
         VPED1=VPED;VPED2=dSpico(2); % Direcao dominante nos picos 1 e 2
         % Espalhamento medio da cada região de pico
         % Opção 1: selecionando o desvio padrao circular VESP exatamento nos picos 
         VEPK1=VESP(find(VS == auxS(2))); VEPK2=VESP(find(VS == auxS(1)));
         % Opção 2: utilizar uma media ponderada pelo espectro (proposta paper Forristall&Ewans)
         % df=VF(3)-VF(2);
         % E1=VS(k1:kc).*df/VMTA1; % Calculo do espectro omni-direcional normalizado pela area espectral
         % VEPK1=sum(VESP(k1:kc).*E1); % Conforme seção "Circular rms spreading"
         % E2=VS(k0:k1).*df/VMTA2; % Calculo do espectro omni-direcional normalizado pela area espectral
         % VEPK2=sum(VESP(k0:k1).*E2); % Conforme seção "Circular rms spreading"       
      else
         VPED1=-999.99;VEPK1=-999.99;
         VPED2=-999.99;VEPK2=-999.99;
      end
      VMTA3=-999.99;VMTB3=-999.99;VMTC3=-999.99;VMTD3=-999.99;VMTE3=-999.99;VCAR3=-999.99;
      VTPK3=-999.99;VSPK3=-999.99;VEPK3=-999.99;VPED3=-999.99;
   elseif length(fScava) == 3
      [auxf nf]=sort(fScava);
      k0=find(VF == fScava(nf(1)));k1=find(VF == fScava(nf(2)));k2=find(VF == fScava(nf(3)));kc=length(VF);
      mo0=[sum(VS(k0:k1).*(1/NDT)) sum(VS(k1:k2).*(1/NDT)) (VMTA-(sum(VS(k0:k1).*(1/NDT))+sum(VS(k1:k2).*(1/NDT))))];
      mo1=[sum(VF(k0:k1).*VS(k0:k1))/NDT sum(VF(k1:k2).*VS(k1:k2))/NDT sum(VF(k2:kc).*VS(k2:kc))/NDT ];
      mo2=[sum(VF(k0:k1).^2.*VS(k0:k1))/NDT sum(VF(k1:k2).^2.*VS(k1:k2))/NDT sum(VF(k2:kc).^2.*VS(k2:kc))/NDT];
      mo3=[sum(VF(k0:k1).^3.*VS(k0:k1))/NDT sum(VF(k1:k2).^3.*VS(k1:k2))/NDT sum(VF(k2:kc).^3.*VS(k2:kc))/NDT];
      mo4=[sum(VF(k0:k1).^4.*VS(k0:k1))/NDT sum(VF(k1:k2).^4.*VS(k1:k2))/NDT sum(VF(k2:kc).^4.*VS(k2:kc))/NDT];
      picos=Spico(nf);
      [auxS nk]=sort(picos);
      VMTA1=mo0(nk(3));VMTB1=mo1(nk(3));VMTC1=mo2(nk(3));VMTD1=mo3(nk(3));VMTE1=mo4(nk(3));VCAR1=4*sqrt(VMTA1);
      VTPK1=1./fSpico(1);VSPK1=auxS(3);
      if pdir
         VEPK1=VEPK;VPED1=VPED;
         VEPK2=VESP(find(VS == auxS(2)));VPED2=dSpico(2);
         VEPK3=VESP(find(VS == auxS(1)));VPED3=dSpico(3);
      else
         VEPK1=-999.99;VPED1=-999.99;
         VEPK2=-999.99;VPED2=-999.99;
         VEPK3=-999.99;VPED3=-999.99; 
      end
      VMTA2=mo0(nk(2));VMTB2=mo1(nk(2));VMTC2=mo2(nk(2));VMTD2=mo3(nk(2));VMTE2=mo4(nk(2));VCAR2=4*sqrt(VMTA2);
      VTPK2=1./fSpico(2);VSPK2=auxS(2);
      VMTA3=mo0(nk(1));VMTB3=mo1(nk(1));VMTC3=mo2(nk(1));VMTD3=mo3(nk(1));VMTE3=mo4(nk(1));VCAR3=4*sqrt(VMTA3);
      VTPK3=1./fSpico(3);VSPK3=auxS(1);
   end
end