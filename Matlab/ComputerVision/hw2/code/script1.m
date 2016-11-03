clear all
im = imread('../data/model_chickenbroth.jpg');
im = im2double(im);
if size(im,3)==3
    im= rgb2gray(im);
end
levels = [-1, 0, 1, 2, 3, 4];
k = sqrt(2);
sigma0 = 1;
th_contrast = 0.03;
th_r = 12;

[locsDoG, GaussianPyramid] = DoGdetector(im, sigma0, k, levels,th_contrast, th_r);

imshow(im);
hold on;
scatter(locsDoG(:,1),locsDoG(:,2),'*','g');
% hold on;

% im1 = im2double(im);
% if size(im1,3)==3
%     im1= rgb2gray(im1);
% end
% 
% [locsDoG1, GaussianPyramid1] = DoGdetector(im1, sigma0, k, levels,th_contrast, th_r);

%imshow(im);
%hold on;
%scatter(locsDoG1(:,1),locsDoG1(:,2),'*','r');
%sum(locsDoG-locsDoG1)