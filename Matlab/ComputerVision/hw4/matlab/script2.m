% Q2.5 - Todo:
%       1. Load point correspondences
%       2. Obtain the correct M2
%       4. Save the correct M2, p1, p2, R and P to q2_5.mat
clear all
load('../data/some_corresp.mat');
im1 = imread('../data/im1.png');
im2 = imread('../data/im2.png');
M = [2/size(im1,2) 0 -1; 0 2/size(im2,1) -1; 0 0 1];
[F] = eightpoint( pts1, pts2, M );
load('../data/intrinsics.mat');
[E] = essentialMatrix( F, K1, K2 );
M1 = K1*[1,0,0,0;0,1,0,0;0,0,1,0];
[M2s] = camera2(E);
for i = 1:size(M2s,3)
    M2_ind = K2*M2s(:,:,i);
    [P, error] = triangulate( M1, pts1, M2_ind, pts2 );
    if (P(:,3)> 0)
        M2 = M2_ind;
    end
end
for i = 1:1
%     x1 = pts1(i,1);
%     y1 = pts1(i,2);
    x1 = 124;
    y1 = 217;
    [ x2, y2 ] = epipolarCorrespondence( im1, im2, F, x1, y1 )
end