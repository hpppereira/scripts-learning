clear, clc, close all
%Discrete wavelet transform (Haar Wavelet) using Matlab

%import the image
lena = imread('../dados/IMG_0075.JPG');

%display the image
%image(lena);

%perform single wavelet decomposition
[ca,ch,cv,cd] = dwt2(lena,'haar');

%construct aproximation and coefficients
a = upcoef2('a',ca,'haar',1);
h = upcoef2('h',ch,'haar',1);
v = upcoef2('v',cv,'haar',1);
d = upcoef2('d',cd,'haar',1);

%perform multilevel wavelet decomposition
[c,s] = wavedec2(lena,1,'haar');

%extract the coefficients
[ch,cv,cd] = detcoef2('all',c,s,1);

%reconstruct the decomposed values
h = wrcoef2('h',c,s,'haar',1);
v = wrcoef2('v',c,s,'haar',1);
d = wrcoef2('d',c,s,'haar',1);

%reconstruct the image from multilevel decomposition
x0 = waverec2(c,s,'haar');

%compress the image
[thr,sorh,keepapp] = ddencmp('cmp','wv',lena);


[lenacomp,cxc,lxc,perf0,perf12] = wdencmp('gbl',c,s,'haar',1,thr,sorh,keepapp);


figure
subplot(1,2,1); image(lena); axis square
subplot(1,2,2); image(lena); axis square







