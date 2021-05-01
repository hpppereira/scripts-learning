clear, clc, close all
%wavelet coursera

%wavelet package - matlab
%image processing

%open panel of matlab wavelet package
%wavemenu

A = imread('../dados/IMG_0075.JPG','jpg');

%corta a imagem
A = A(1:600,1:800,:);

%black and white image
Abw = rgb2gray(A);

[a,b] = size(Abw);

Abw = double(Abw(a:-1:1,:)); %convert from uint8 to double

size(A) %three dimension
size(Abw) %one dimension

%add some noise
Abwn = Abw + 100* randn(600,800);


figure
image(A)

figure
imshow(A)

figure
imshow(Abw)

figure
pcolor(Abw), shading interp, colormap(hot)

figure
pcolor(Abwn), shading interp, colormap(hot)

Abwt = fft2(Abw); %fourier transform

figure
pcolor( log(abs(fftshift(Abwt))) ), shading interp, colormap(hot)

figure()
pcolor( (abs(fftshift(Abwt))) ), shading interp, colormap(hot)


%plot spectra with noise
Abwtn = fft2(Abwn); %fourier transform

figure
pcolor( log(abs(fftshift(Abwtn))) ), shading interp, colormap(hot)



