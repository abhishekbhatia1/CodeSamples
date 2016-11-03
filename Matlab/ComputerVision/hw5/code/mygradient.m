function [mag,ori] = mygradient(I)
%
% compute image gradient magnitude and orientation at each pixel
%
im = im2double(I);
%[mag,ori] = imgradient(im);
[Hx Hy] = gradient(im);
% h = [-1 1];
% Hx = double(imfilter(I, h, 'replicate'));
% Hy = double(imfilter(I, h', 'replicate'));

mag = zeros(size(I));
ori = zeros(size(I));

mag = sqrt(Hx.^2 + Hy.^2);
ori = atan2(Hy,Hx);