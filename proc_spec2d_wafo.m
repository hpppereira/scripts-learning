clear, clc, close all

% Simula espectro 1D

% Hm0 = 5;
% Tp = 10;
% wc = 33/Tp;
% w = linspace(0, wc, 257);
% D = 0.036 - 0.0056 * Tp/sqrt(Hm0);
% gamma = exp(3.484*(1-0.1975*D*Tp^4/(Hm0^2)));
% sa = 0.07;
% sb = 0.09;
% A = -1;
% plotflag = 0;
% S = jonswap(w,[Hm0 Tp gamma sa sb A],plotflag);

% Espalhamento angular

% Nt = 360; % number of angles
% th0 = pi; % primary direction of waves
% type = 'cos2s';
% data = [15, 15, 0.52, 5, -2.5, 0, 1, inf];
% w = S.w;
% def = 1;
% D = spreading(Nt, type, th0, data, w, def);

% Calcula espectro direcional

% SD = mkdspec(S, D, 0);

% Nang = 360; % numero de angulos
% Nx = 3;
% Ny = 3;
% Nt = 2^14;
% dx = 10;
% dy = 10;
% dt = 0.5;
% plotflag = 0;
% use_waitbar = 0;
% h = inf;
% NFFT = Nt / 24;

% F = seasim(SD, Nx, Ny, Nt, dx, dy, dt, 1, plotflag, use_waitbar); 

% Gera espectro 2D da serie temporal

% Z  = permute(F.Z, [3 1 2]);
% [X,Y] = meshgrid(F.x,F.y);
% W = Z(:,:);
% W1 = [F.t, W(:,1:3:end)];
% pos = [[20, 0, 0]; [10, 0, 0]; [0, 0, 0]];
% types = [1, 1, 1]';
% bfs = [1, 0, 0]';

% [Se, D, Sw, Fcof] = dat2dspec(W1, [pos, types, bfs]);

% figure
% plotspec(SD), hold all
% plotspec(Se,'r-.'), hold off
% shg

pathname = '/home/hp/Dropbox/doutorado/dados/HNE_rio_grande_200912/';
W1 = dlmread([pathname, '20091213200000.HNE'], '', 11, 0);
W2 = dlmread([pathname, '20091220070000.HNE'], '', 11, 0);

W(:,1) = W1(:,1);
W(:,2:4) = W1(:,2:4) + W2(:,2:4)

% W = load('registro_090_geraonda.txt');

pos = [[0, 0, 0]; [0, 0, 0]; [0, 0, 0]];
types = [1, 4, 5]';
bfs = [1, 0, 0]';

[Se, D, Sw, Fcof] = dat2dspec(W, [pos, types, bfs]);

figure
% plotspec(SD), hold all
plotspec(Se,'b-')
shg

save onda_wafo.txt -ascii W