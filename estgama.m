% ROTINA ESTGAMA

% espectro de Pierson-Moskowitz (Spm) (ou seja gama e k=1)

% O terceiro passo e' estimar um valor de gama ^M
% E' usada a relacao gama=strab(fp)/Sp-m(fp)^M

% in:   - freq de pico fp
%       - vetor de freq f^M
%       - espectro medido strab^M
%       - melhor ajuste de alfa^M

% out:  - melhor ajuste de gama => gama2 ^M


i=fp./f;b=i.^4;c=-1.25*b;d=exp(c);
e=d*alfa*g^2*(2*pi)^(-4);h=(f).^(-5);
Spm=e.*h;

% freq de pico espectral (fp) do espec medido
pos=find(f==fp);

% ordenada de pico espectral (opm) do espec de P-M
opm=max(Spm);

% freq de pico espectral (fpm) do espec de P-M
posfpm=find(Spm==opm);
fpm=f(posfpm);

gama2=strab(pos)/Spm(posfpm);

clear i c b e d h pos posfpm opm Spm fpm fp op
