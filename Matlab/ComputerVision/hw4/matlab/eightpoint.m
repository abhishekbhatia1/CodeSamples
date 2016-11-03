function [ F ] = eightpoint( pts1, pts2, M )
%   pts1 - Nx2 matrix of (x,y) coordinates
%   pts2 - Nx2 matrix of (x,y) coordinates
%   M    - max (imwidth, imheight)
% max_im = M;
% clear M;
% M = [2/max_im 0 -1; 0 2/max_im -1; 0 0 1];
pts1_old = pts1;
pts2_old = pts2;
a = ones(size(pts1,1),1);
pts1 = horzcat(pts1,a);
pts2 = horzcat(pts2,a);
p1 = (M*pts1')';
p2 = (M*pts2')';
A = zeros(size(p1,1),9);
A(1:end,1) = p1(:,1).*p2(:,1);
A(1:end,2) = p1(:,2).*p2(:,1);
A(1:end,3) = p2(:,1);
A(1:end,4) = p1(:,1).*p2(:,2);
A(1:end,5) = p1(:,2).*p2(:,2);
A(1:end,6) = p2(:,2);
A(1:end,7) = p1(:,1);
A(1:end,8) = p1(:,2);
A(1:end,9) = 1;
[~,S,V] = svd(A);
C = size(S,2);
F = reshape(V(:,C),[3 3])';
[U_F,S_F,V_F] = svd(F);
S_F(size(S_F,1),size(S_F,2)) = 0;
F = U_F*S_F*V_F;
F = M'*F*M;
F = refineF(F,pts1_old,pts2_old);
pts1 = pts1_old;
pts2 = pts2_old;
%save('q2_1.mat','F','M','pts1','pts2');
end