%programa para fazer a distribuicao
%conjunta utilizando a suborinta
% distribuicaoconjunta.m

clear,clc,close all

dados = load('/home/hp/Dropbox/siodoc/dados/proc/janis_data.dat');

hs = dados(:,28);
tp = dados(:,58);
dp = dados(:,54);

tp(tp>22) = NaN;

distribuicaoconjunta