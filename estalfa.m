% ROTINA ESTALFA

% rotina ESTALFA
% segundo passo para ajuste => estimativa de alfa
% alfa varia de 0.0001 a 0.01 e f de 1.37*fph a fmax

% o segundo passo e' obter o valor de alfa para (k e gama)=1
% e fp obtido do espectro medido. O valor de alfa (=alfa2) e' escolhido
% de maneira que o erro medio quadratico seja o menor para
% a faixa de altas freqs (acima de 1.37*fph). Gama e k nao
% influenciam esta faixa de altas freqs logo podem ser setados em 1

% in:   - freq de pico fp
%       - vetor de freq f
%       - espectro medido strab
%       - decaimento a

% out:  - melhor ajuste de alfa => alfa3


n=0;g=9.81;

      for alfa=0.0001:0.0001:0.1,

      n=n+1;

% calculo dos limites de integracao inferior e 
% superior (linf e lsup)
linf=1.37*fp;
lsup=2.00*fp;

if lsup>.5
lsup=.5;
end

inf=find(f>=linf);inf=inf(1);
sup=find(f>=lsup);sup=sup(1);
%sup=length(f);

% espectro de Pierson-Moskowitz (Spm) (ou seja gama e k=1)

i=fp./f;b=i.^4;c=-1.25*b;d=exp(c);
e=d*2*pi*alfa*g^2;h=(2*f*pi).^(a);
Spm=e.*h;

% calculo do erro minimo quadratico entre o espectro
% medido (strab) e o espectro de P-M (Spm) para f entre 1.37*fp
% e f max

soma=0;
                 for cont=inf:1:sup,
  Sr=(strab(cont)-Spm(cont))^2;
  soma=soma+Sr;
                 end

emq(n)=soma;
alf(n)=alfa;
      

                      end  % loop de alfa
      
% valor de alfa que gera o menor erro quadratico para (k e gama)=1
pos=find(emq==min(emq));

alfa3=alf(pos);

clear alfa i c b e d h alf soma Sr Spm cont inf sup emq pos linf
