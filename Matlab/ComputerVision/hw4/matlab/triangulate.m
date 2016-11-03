function [ P, error ] = triangulate( M1, p1, M2, p2 )
% triangulate:
%       M1 - 3x4 Camera Matrix 1
%       p1 - Nx2 set of points
%       M2 - 3x4 Camera Matrix 2
%       p2 - Nx2 set of points

% Q2.4 - Todo:
%       Implement a triangulation algorithm to compute the 3d locations
%       See Szeliski Chapter 7 for ideas
%
for i = 1:size(p1,1)
    A(1,:) = (- M1(1,:) + M1(3,:)*p1(i,1));
    A(2,:) = (- M1(2,:) + M1(3,:)*p1(i,2));
    A(3,:) = (- M2(1,:) + M2(3,:)*p2(i,1));
    A(4,:) = (- M2(2,:) + M2(3,:)*p2(i,2));
    [~,~,V] = svd(A);
    X = V(:,size(V,2))';
    P(i,1) = X(1,1)/X(1,4);
    P(i,2) = X(1,2)/X(1,4);
    P(i,3) = X(1,3)/X(1,4);
end
b = ones(size(P,1),1);
P_hm = horzcat(P,b);
points1_hm = (M1*P_hm')';
points2_hm = (M2*P_hm')';
points1_fn(:,1) = points1_hm(:,1)./points1_hm(:,3);
points1_fn(:,2) = points1_hm(:,2)./points1_hm(:,3);
points2_fn(:,1) = points2_hm(:,1)./points2_hm(:,3);
points2_fn(:,2) = points2_hm(:,2)./points2_hm(:,3);
error_1 = sum((p1-points1_fn).^2);
error_2 = sum((p2-points2_fn).^2);
error = sum(error_1 + error_2);
end