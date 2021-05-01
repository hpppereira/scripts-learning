%% Tutorial para wavelet toolbox to Matlab
%site http://cas.ensmp.fr/~chaplais/Wavelet_Matlab/GetSignal/GetSignal.html
%dado para exemplo: PieceRegSig.mat

clear all, clc, close all

load('../dados/PieceRegSig.mat');

sig.s = sig;

% "d" to store the time (represented as an integer index) at which the signal starts
sig.d = 0;

fieldnames(sig)