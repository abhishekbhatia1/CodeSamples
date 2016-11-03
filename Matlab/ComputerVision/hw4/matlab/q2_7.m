clear all
load('../data/templeCoords.mat');
load('q2_6.mat');
load('q2_5.mat');
im1 = imread('../data/im1.png');
im2 = imread('../data/im2.png');
im1 = im2double(im1);
im2 = im2double(im2);
load('../data/intrinsics.mat');
[E] = essentialMatrix( F, K1, K2 );
M1 = K1*[1,0,0,0;0,1,0,0;0,0,1,0];
[M2s] = camera2(E);
for i = 1:length(x1)
    [x2(i,1),y2(i,1)] = epipolarCorrespondence( im1, im2, F, x1(i), y1(i) );
end
pts1_new(:,1) = x1(:,1);
pts1_new(:,2) = y1(:,1);
pts2_new(:,1) = x2(:,1);
pts2_new(:,2) = y2(:,1);
for i = 1:size(M2s,3)
    M2_ind = K2*M2s(:,:,i);
    [P, error] = triangulate( M1, pts1, M2_ind, pts2 );
    if (P(:,3)> 0)
        M2 = M2_ind;
        break;
    end
end
[P, error] = triangulate( M1, pts1_new, M2, pts2_new );
save('q2_7.mat','F','M1','M2');
scatter3(P(:,1),P(:,2),P(:,3));
%scatter(P(:,1),P(:,2));
% figure;
% subplot(1,2,1);
% imshow(im1);
% hold on
% scatter(x1,y1);
% subplot(1,2,2);
% imshow(im1);
% hold on
% scatter(x2,y2);
% hold off;