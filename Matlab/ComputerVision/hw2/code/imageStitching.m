function [panoImg] = imageStitching(img1, img2, H2to1)

warp_im = warpH(img2, H2to1, size(img1));

mask1 = zeros(size(img1,1), size(img1,2));
mask1(1,:) = 1; mask1(end,:) = 1; mask1(:,1) = 1; mask1(:,end) = 1;
mask1 = bwdist(mask1, 'city');
mask1 = mask1/max(mask1(:));
mask1_new(:,:,1) = mask1;
mask1_new(:,:,2) = mask1;
mask1_new(:,:,3) = mask1;

mask2 = zeros(size(warp_im,1), size(warp_im,2));
mask2(1,:) = 1; mask2(end,:) = 1; mask2(:,1) = 1; mask2(:,end) = 1;
mask2 = bwdist(mask2, 'city');
mask2 = mask2/max(mask2(:));
mask2_new(:,:,1) = mask2;
mask2_new(:,:,2) = mask2;
mask2_new(:,:,3) = mask2;

warp_mask2 = warpH(mask2_new, H2to1, size(img1));

img1 = im2double(img1);
mask1_im = mask1_new.*img1;
% mask1_im(:,:,1) = mask1.*img1(:,:,1);
% mask1_im(:,:,2) = mask1.*img1(:,:,2);
% mask1_im(:,:,3) = mask1.*img1(:,:,3);
warp_im = im2double(warp_im);
%mask2_im = mask2_new.*warp_im;
mask2_im = warp_mask2.*warp_im;
% mask2_im(:,:,1) = mask2.*warp_im(:,:,1);
% mask2_im(:,:,2) = mask2.*warp_im(:,:,2);
% mask2_im(:,:,3) = mask2.*warp_im(:,:,3);

%panoImg = imadd(mask1_im, mask2_im)/imadd(mask1_new, mask2_new);
panoImg = imadd(mask1_im, mask2_im)./imadd(mask1_new, warp_mask2);
%panoImg = max(mask1_im,mask2_im);
%panoImg = warp_im;