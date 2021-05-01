function [urot,vrot]=rotaxis_boia(u,v,theta)
%   function [urot,vrot]=rotaxis(u,v,theta)
%   M-file to plot an ellipse. It uses the rotation matrix:
%   | xrot |  =  | cos(theta)    sin(theta)  |   *   | x |
%   | yrot |     |-sin(theta)    cos(theta)  |       | y |
%
%   PS: The angle theta is the angle between the original cartesian
%       coordinate axes (u,v) and the rotated axes (urot,vrot) in
%       the trigonometric (or anticlockwise) sense.
%
%   Reference: Gere,J.M. and W. Weaver Jr.,Analysis of Framed
%              Structures, D.Van Nostrand Co., pp.250-251, 1965.
%
%   Jose A. Lima - 02/06/95

% Somente corrige os valores com o angulo em graus do
% compas. 
% Para converter de roll/pitch para etaEW/etaNS deve usar a funcao rota_boia 
% Entretanto utiliza-se o artificio de que o processamento com a série do
% angulo em graus ou sin(angulo) fornece o mesmo resultado. Na pratica
% (baseado em testes) é melhor usar a rotaxis_boia ao inves da rota_boia!
% Ricardo Campos 04/04/2012
urot= cos(pi*theta/180) .* u + sin(pi*theta/180) .* v; 
vrot= -sin(pi*theta/180) .* u + cos(pi*theta/180) .* v;
