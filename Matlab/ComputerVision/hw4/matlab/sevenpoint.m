function [ F ] = sevenpoint( pts1, pts2, M )
% sevenpoint:
%   pts1 - Nx2 matrix of (x,y) coordinates
%   pts2 - Nx2 matrix of (x,y) coordinates
%   M    - max (imwidth, imheight)

% Q2.2 - Todo:
%     Implement the eightpoint algorithm
%     Generate a matrix F from some '../data/some_corresp.mat'
%     Save recovered F (either 1 or 3 in cell), M, pts1, pts2 to q2_2.mat

%     Write recovered F and display the output of displayEpipolarF in your writeup
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
C = size(V,2);
F1 = reshape(V(:,C),[3 3])';
F2 = reshape(V(:,C-1),[3 3])';
syms alph
alph = roots(sym2poly(det(alph *F1 + (1 - alph) * F2)));
for i = 1:length(alph)
    F_i = alph(i) * F1 + (1-alph(i)) * F2;
    F_i = M'*F_i*M;
    F(:,:,i) = refineF(F_i,pts1_old,pts2_old);
end
pts1 = pts1_old;
pts2 = pts2_old;
%save('q2_2.mat','F','M','pts1','pts2');
end