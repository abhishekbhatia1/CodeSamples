function [ E ] = essentialMatrix( F, K1, K2 )
% essentialMatrix:
%    F - Fundamental Matrix
%    K1 - Camera Matrix 1
%    K2 - Camera Matrix 2

% Q2.3 - Todo:
%       Compute the essential matrix 
%
%       Write the computed essential matrix in your writeup

% [U,S,V] = svd(K2'*F*K1);
% S_new = S;
% S_new(1,1) = (S(1,1) + S(2,2))/2;
% S_new(2,2) = (S(1,1) + S(2,2))/2;
% S_new(3,3) = 0;
% E = U*S_new*V;
E = K2'*F*K1;
end