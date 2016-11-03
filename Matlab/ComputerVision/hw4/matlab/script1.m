clear all
%load('../data/some_corresp.mat');
load('../data/some_corresp_noisy.mat');
im1 = imread('../data/im1.png');
im2 = imread('../data/im2.png');
im1 = im2double(im1);
im2 = im2double(im2);
M = [2/size(im1,2) 0 -1; 0 2/size(im2,1) -1; 0 0 1];
%M = max(size(im1,1), size(im1,2));
%[F] = eightpoint( pts1, pts2, M );
%load('../data/intrinsics.mat');
% load('../data/manual_corresp.mat')
%p = randi(length(pts1),7,1);
% for j = 1:length(pts1)
%      P1(j,1:2) = pts1((j),1:2);
%      P2(j,1:2) = pts2((j),1:2);
% end
% [F] = sevenpoint( P1, P2, M );
[F] = ransacF( pts1, pts2, M )
% displayEpipolarF(im1, im2, F);
for i = 1:size(F,3)
    displayEpipolarF(im1, im2, F(:,:,i));
end
% [E] = essentialMatrix( F, K1, K2 );
% M1 = K1*[1,0,0,0;0,1,0,0;0,0,1,0];
% [M2s] = camera2(E);
% for i = 1:size(M2s,3)
%     M2 = K2*M2s(:,:,i);
%     [P(:,:,i), error(i)] = triangulate( M1, pts1, M2, pts2 );
% end