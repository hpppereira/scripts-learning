function [Spico,fSpico,dSpico,Scava,fScava,dScava] = sele_pico(VS,DT,VD,VF,VSPK,ngl,heave,pdir,nfft,VAVH,hsmin);
% [Spico,fSpico,dSpico,Scava,fScava,dScava] = sele_pico(VS,DT,VD,VF,VSPK,ngl,heave,pdir,nfft,VAVH,hsmin)
% Funcao para selecao de picos espectrais.
%    Entrada:
%         VS = Espectro Omni-direcional (1-D).
%         DT = resolução temporal da série temporal (1/delta f).
%         VD = Espectro de Direção 1-D.
%         VF = Vetor de frequência (Hz).
%         VSPK = Valor de energia do pico do espectro (m2/Hz).
%         ngl = núm. de graus de liberdade.
%         heave = série de elevação de superfície do mar.
%         pdir = chaveamento direcinal (sim ou não).
%         nfft = número de pontos a serem utilizados no espectro.
%         VAVH = Altura H1/3 (domínio do tempo).
%         hsmin = Limite de altura.
%  Saida:
%         Spico = Energia dos picos do espectro (1 x 3 - até trimodal).
%         fSpico = frequência de cada pico.
%         dSpico = direção de cada pico.
%         Scava = Energia dos cavas do espectro (1 x 3 - até trimodal).
%         fScava = frequência de cada cava.
%         dScava = direção de cada cava.

% J.A. Lima 21/07/99
%
% IMPORTANTE: Os picos sao fornecidos em ordem decrecente, ou seja,
%             Spico(1) armazena o maior pico espectral, Spico(2) o
%             segundo menor pico espectral, e Spico(3) o terceiro pico.
%
% -------------------------------------------------------------------------
%       Modulo para Identificacao de Picos Significativos do Espectro
%            para Ajuste de Parametros do Espectro de Jonswap
%           (Criterios de selecao desenvolvidos por Jose Antonio)
%
d=diff(VS);d=sign(d);d=diff(d);d=[0;d];
d=find(d==-2);
% Identificacao de maximos estatisticamente independentes
% Obs:
% Depois do alizamento com ngl graus de liberdade, o espectro possui valores
% estatisticamente independentes espacados de (ngl/2) pontos com relacao ao
% espectro com banda de frequencia original de DF=1/(length(heave)*DT).
% Deste modo, em frequencia, os dados estatisticamente independentes estao
% separados de DFI=(ngl/2)*DF;
%
% 1o. criterio: Identifica picos estatisticamente independentes. Sera'
%               adotado um espacamento em frequencia de DFI=(ngl*DF)
DFI=ngl*(1/(nfft*DT));Spico=[];fSpico=[];dSpico=[];
j=1;
Spico(1)=VS(d(1));fSpico(1)=VF(d(1));
if pdir
  dSpico(1)=VD(d(1));
else
  dSpico(1)=999.99;
end
for k=1:length(d)-1
  if (VF(d(k+1))-fSpico(j)) < DFI
    [Spico(j) h]=max([Spico(j) VS(d(k+1))]);
    if h == 2
      fSpico(j)=VF(d(k+1));
      if pdir
        dSpico(j)=VD(d(k+1));
      else
        dSpico(j)=999.99;
      end
    end
  else
    j=j+1;
    Spico(j)=VS(d(k+1));
    fSpico(j)=VF(d(k+1));
    if pdir
      dSpico(j)=VD(d(k+1));
    else
      dSpico(j)=999.99;
    end
  end
end
[m n]=size(Spico);
if m==1 & n~=1
  Spico=Spico';fSpico=fSpico';dSpico=dSpico'; % Converte para vetores coluna
end

if VAVH < hsmin;
  [Spico,posicao]=max(Spico);
  fSpico=fSpico(posicao);
  dSpico=dSpico(posicao);
  Scava=0.;fScava=0.;dScava=0.;
  %Scava =Scava(posicao);
  %fScava=fScava(posicao);
  %dScava=dScava(posicao);
else
  
  %criterio=1
  %Periodos_e_Ordenadas_de_Pico=[1./fSpico Spico]
  
  %
  % 2o. criterio: Despreza picos cuja amplitude (ou ordenada de pico no
  %               espectro) seja inferior a 15% da energia associada ao
  %               maior pico espectral para periodos inferiores 10 seg
  %               e inferiores a 5% para periodos superiores a 10 seg.
  %    Referencia: Soares, C.G. e Nolasco,1992,"Spectral Modeling of Sea
  %                States with Multiple Wave Systems", Journal Offshore
  %                Mechanics and Arctic Engineering,114,278-284.
  %
  %         Obs:  Despreza picos inferiores a 4 segundos por serem
  %               dificeis de serem resolvidos adequadamente por boias,
  %               picos superiores a 22 segundos por não serem
  %               representativos de swell que alcança nossa costa.
  %
  auxS=Spico;auxf=fSpico;auxd=dSpico;
  Spico=[];fSpico=[];dSpico=[];
  j=0;
  for k=1:length(auxS)
    % Para periodos entre 2 (antes era 4, mudou com o GoM) seg e 10 seg, adotar limite de 0.15*VSPK
    %if (auxf(k) <= 1./4.) & (auxf(k) >= 1./10.) % Comentado por EOR e RMC )04-Mar-2011
    if (auxf(k) <= 1./2.) & (auxf(k) >= 1./10.)%Alterado por EOR e RMC )04-Mar-2011
      if auxS(k) > 0.15*VSPK
        j=j+1;
        Spico(j)=auxS(k);
        fSpico(j)=auxf(k);
        dSpico(j)=auxd(k);
      end
      %elseif (auxf(k) < 1./10.) & (auxf(k) > 1./22.)
    elseif (auxf(k) < 1./10.) & (auxf(k) > 1./42.); % Eric Oliveira Ribeiro. 25/09/2007!!
      % Para periodos entre 10 seg e 22 seg, adotar limite de 0.05*VSPK
      if auxS(k) > 0.05*VSPK
        j=j+1;
        Spico(j)=auxS(k);
        fSpico(j)=auxf(k);
        dSpico(j)=auxd(k);
      end
    end
  end
  [m n]=size(Spico);
  if m==1 & n~=1
    Spico=Spico';fSpico=fSpico';dSpico=dSpico'; % Converte para vetores coluna
  end
  %criterio=2
  %Periodos_e_Ordenadas_de_Pico=[1./fSpico Spico]
  
  %
  % 3o. criterio: Seleciona picos em alta frequencia (periodos menores que
  %               8 segundos que estejam na mesma direção +/- 30 graus) usando
  %               criterio da direcao. Utiliza tambem o criterio de direcao
  %               para selecionar picos superiores a 10 segundos. O limite
  %               de teste e' 10 segundos para dados direcionais e
  %               12 segundos para dados nao-direcionais.
  %        Obs:   Ate' este ponto do programa, os vetores fSpico e
  %               Spico ainda estao ordenados por ordem crescente de
  %               frequencia, ou seja fSpico(1)<fSpico(2)<fSpico(3).
  if pdir
    % ## Para dados direcionais de ondas: ##
    % Periodos inferiores a 8 segundos:
    fLim=1/8.;
    klim=find(fSpico >= fLim);
    if isempty(klim) ~= 1 & length(klim) > 1
      auxS=Spico;auxf=fSpico;auxd=dSpico;
      Spico=[];fSpico=[];dSpico=[];
      SpL=max(auxS(klim)); % Maximo pico para frequencias superiores a fLim
      fpL=auxf(find(auxS==SpL)); % Frequencia associada a SpL
      dpL=auxd(find(auxS==SpL)); % Direcao associada a SpL
      j=0;
      for k=1:length(auxS)
        % Frequencias menores que fLim ou igual a fpL
        if auxf(k) < fLim | auxf(k) == fpL
          j=j+1;
          Spico(j)=auxS(k);
          fSpico(j)=auxf(k);
          dSpico(j)=auxd(k);
        else
          % Frequencias maiores ou iguais a fLim
          if dpL > 30. & dpL < 330.
            % Direcao principal fora das proximidades do Norte Verd.
            Lid=dpL-30; % Limite inferior do intervalo de direcao
            Lsd=dpL+30; % Limite superior do intervalo de direcao
            if auxd(k) >= Lid & auxd(k) < Lsd
              flag=0;
            else
              j=j+1;
              Spico(j)=auxS(k);
              fSpico(j)=auxf(k);
              dSpico(j)=auxd(k);
            end
          else
            % Direcao principal nas proximidades do Norte Verdadeiro
            Lid=dpL-30;if Lid < 0; Lid=Lid+360; end
            Lsd=dpL+30;if Lsd > 360; Lsd=Lsd-360; end
            if auxd(k) >= Lid | auxd(k) < Lsd
              flag=0;
            else
              j=j+1;
              Spico(j)=auxS(k);
              fSpico(j)=auxf(k);
              dSpico(j)=auxd(k);
            end
          end
        end
      end
    end
    % Periodos superiores a 10 segundos:
    fLim=1/10.;
    klim=find(fSpico <= fLim);
    if isempty(klim) ~= 1 & length(klim) > 1
      auxS=Spico;auxf=fSpico;auxd=dSpico;
      Spico=[];fSpico=[];dSpico=[];
      SpL=max(auxS(klim)); % Maximo pico para frequencias inferiores a fLim
      fpL=auxf(find(auxS==SpL)); % Frequencia associada a SpL
      dpL=auxd(find(auxS==SpL)); % Direcao associada a SpL
      j=0;
      for k=1:length(auxS)
        % Frequencias maiores que fLim ou igual a fpL
        if auxf(k) > fLim | auxf(k) == fpL
          j=j+1;
          Spico(j)=auxS(k);
          fSpico(j)=auxf(k);
          dSpico(j)=auxd(k);
        else
          % Frequencias menores ou iguais a fLim
          if dpL > 30. & dpL < 330.
            % Direcao principal fora das proximidades do Norte Verd.
            Lid=dpL-30; % Limite inferior do intervalo de direcao
            Lsd=dpL+30; % Limite superior do intervalo de direcao
            if auxd(k) >= Lid & auxd(k) < Lsd
              flag=0;
            else
              j=j+1;
              Spico(j)=auxS(k);
              fSpico(j)=auxf(k);
              dSpico(j)=auxd(k);
            end
          else
            % Direcao principal nas proximidades do Norte Verdadeiro
            Alerta='O arquivo abaixo possui periodos de picos maiores que 10 seg e proximos do NV:'
            %arqin
            Lid=dpL-30;if Lid < 0; Lid=Lid+360; end
            Lsd=dpL+30;if Lsd > 360; Lsd=Lsd-360; end
            if auxd(k) >= Lid | auxd(k) < Lsd
              flag=0;
            else
              j=j+1;
              Spico(j)=auxS(k);
              fSpico(j)=auxf(k);
              dSpico(j)=auxd(k);
            end
          end
        end
      end
    end
    [m n]=size(Spico);
    if m==1 & n~=1
      Spico=Spico';fSpico=fSpico';dSpico=dSpico'; % Converte para vetores coluna
    end
  else
    % ## Para dados não-direcionais de ondas: ##
    % Selecionar apenas um pico para periodos inferiores a 8 segundos:
    fLim=1/8;
    klim=find(fSpico >= fLim);
    kinf=find(fSpico < fLim);
    if isempty(klim) ~= 1 & length(klim) > 1
      auxS=Spico';auxf=fSpico';
      Spico=[];fSpico=[];
      [SpL kmax]=max(auxS(klim));   % Maximo pico para frequencias superiores a fLim
      Spico=[ auxS(kinf) auxS(klim(kmax))];
      fSpico=[ auxf(kinf) auxf(klim(kmax))];
      dSpico=999.99*ones(1,length(Spico));
      [m n]=size(Spico);
      if m==1 & n~=1
        Spico=Spico';fSpico=fSpico';dSpico=dSpico'; % Converte para vetores coluna
      end
    end
    % Selecionar apenas um pico para periodos superiores a 12 segundos (longo swell de apenas 1 direcao):
    fLim=1/12;
    klim=find(fSpico < fLim);
    ksup=find(fSpico >= fLim);
    if isempty(klim) ~= 1 & length(klim) > 1
      auxS=Spico';auxf=fSpico';
      Spico=[];fSpico=[];
      [SpL kmax]=max(auxS(klim));   % Maximo pico para frequencias inferiores a fLim
      Spico=[ auxS(ksup) auxS(klim(kmax))];
      fSpico=[ auxf(ksup) auxf(klim(kmax))];
      dSpico=999.99*ones(1,length(Spico));
      [m n]=size(Spico);
      if m==1 & n~=1
        Spico=Spico';fSpico=fSpico';dSpico=dSpico'; % Converte para vetores coluna
      end
    end
  end
  %criterio=3
  %Periodos_e_Ordenadas_de_Pico=[1./fSpico Spico]
  
  % Ordenacao em ordem decrescente e Selecao dos maiores
  % tres picos do espectro. Identifica os minimos entre
  % picos: Scava(i)=vetor com ponto minimo no espectro
  % entre o pico de ordem i e o pico que o antecede.
  npico=length(Spico);
  % Ordena os picos
  if npico == 2 | npico == 3
    [S n]=sort(Spico);fSpico=fSpico(n);dSpico=dSpico(n);
    Spico=flipud(S);fSpico=flipud(fSpico);dSpico=flipud(dSpico);
  elseif npico > 3
    [S n]=sort(Spico);fSpico=fSpico(n);dSpico=dSpico(n);
    Spico=flipud(S);fSpico=flipud(fSpico);dSpico=flipud(dSpico);
    % Seleciona apenas os tres maiores picos
    Spico=Spico(1:3);fSpico=fSpico(1:3);dSpico=dSpico(1:3);
    npico=3;
  end
  % Identifica cavas entre picos espectrais
  Scava=[];fScava=[];dScava=[];
  if npico == 1
    Scava(1)=0.;fScava(1)=0.;dScava(1)=0.;
  else
    [auxf k]=sort(fSpico);
    Scava(k(1))=0;fScava(k(1))=0.;dScava(k(1))=0.;
    for n=2:npico
      ni=find(VF==auxf(n-1));ns=find(VF==auxf(n));
      [Scava(k(n)) km]=min(VS(ni:ns));
      fScava(k(n))=VF(ni+km-1);
      if pdir
        dScava(k(n))=VD(ni+km-1);
      else
        dScava(k(n))=999.99;
      end
    end
  end
  Scava=Scava';fScava=fScava';dScava=dScava';
  %ordenacao='Decrescente_por_pico'
  %Periodos_e_Ordenadas_de_Pico=[1./fSpico Spico]
  
  %
  % 4o. criterio: Calcula a relacao entre os picos espectrais
  % e cavas espectrais adjacentes. Caso a relacao Spico/Scava
  % seja superior a 1.10, o pico e'considerado significativo,
  % caso contrario, o pico e'desprezado.
  SPP=[];
  if length(Spico) > 1
    k=[];
    % Ordenando os vetores com valores de pico em
    % ordem crescente de frequencia
    [auxfp k]=sort(fSpico);auxfp=auxfp';
    auxS=Spico(k)';
    auxdS=dSpico(k)';
    auxfc=fScava(k)';
    auxC=[Scava(k)' VS(length(VS))];
    auxdC=dScava(k)';
    % Calculando o vetor lm com posicao do pico no eixo de
    % frequencias VF (abcissa)
    lm=auxfp*(nfft*DT)+1;
    % Calculando o vetor lc com posicao da cava espectral no
    % eixo de frequencias VF (abcissa)
    lc=[auxfc 1/(2*DT)]*(nfft*DT)+1;
    % Teste para verificar se o pico e' significativo
    jp=0;
    for j=1:length(k)
      if auxC(j) ~= 0
        AA=auxS(j)/auxC(j);
      else
        AA=auxS(j)/(0.01*VSPK);
      end
      if auxC(j+1) ~= 0
        AB=auxS(j)/auxC(j+1);
      else
        AB=auxS(j)/(0.01*VSPK);
      end
      if pdir == 1
        % Dados direcionais: e' usada menor relacao (crista/cava=1.04)
        % if ( AA >= 1.04 & AB >= 1.04) % Valores originais do criterio 4
        if ( AA >= 1.25 & AB >= 1.25) % Valores atualizados do criterio 4 por Eric/Jose Antonio em 20/12/2005
          jp=jp+1;
          SPP(jp)=auxS(j);
          fPP(jp)=auxfp(j);
          dPP(jp)=auxdS(j);
          SCC(jp)=auxC(j);
          fCC(jp)=auxfc(j);
          dCC(jp)=auxdC(j);
        end
      else
        % Dados não-direcionais: e' usada maior relacao (crista/cava=1.10)
        % if ( AA >= 1.10 & AB >= 1.10) % Valores originais do criterio 4
        if ( AA >= 1.25 & AB >= 1.25) % Valores atualizados do criterio 4 por Eric/Jose Antonio em 20/12/2005
          jp=jp+1;
          SPP(jp)=auxS(j);
          fPP(jp)=auxfp(j);
          dPP(jp)=auxdS(j);
          SCC(jp)=auxC(j);
          fCC(jp)=auxfc(j);
          dCC(jp)=auxdC(j);
        end
      end
    end
    if isempty(SPP)
      Spico=Spico(1);fSpico=fSpico(1);dSpico=dSpico(1);
      Scava=Scava(1);fScava=fScava(1);dScava=dScava(1);
    else
      [Sl l]=sort(SPP);Spico=fliplr(Sl);kl=fliplr(l);
      fSpico=fPP(kl);dSpico=dPP(kl);
      Scava=SCC(kl);fScava=fCC(kl);dScava=dCC(kl);
      [m n]=size(Spico);
      if m==1 & n~=1
        Spico=Spico';fSpico=fSpico';dSpico=dSpico'; % Converte para vetores coluna
        Scava=Scava';fScava=fScava';dScava=dScava';
      end
    end
  end
end
%criterio=4
%Periodos_e_Ordenadas_de_Pico=[1./fSpico Spico dSpico 1./fScava Scava dScava]
