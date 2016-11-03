function [ x2, y2 ] = epipolarCorrespondence( im1, im2, F, x1, y1 )
% epipolarCorrespondence:
%       im1 - Image 1
%       im2 - Image 2
%       F - Fundamental Matrix between im1 and im2
%       x1 - x coord in image 1
%       y1 - y coord in image 1

% Q2.6 - Todo:
%           Implement a method to compute (x2_v,y2_v) given (x1,y1)
%           Use F to only scan along the epipolar line
%           Experiment with different window sizes or weighting schemes
%           Save F, pts1, and pts2 used to generate view to q2_6.mat
%
%           Explain your methods and optimization in your writeup
H = fspecial('gaussian',[45 45],1);
patchWidth = 22;
startx = x1-patchWidth;
endx = x1+patchWidth;
starty = y1-patchWidth;
endy = y1+patchWidth;
im1_patch = im1(starty:endy, startx:endx);
im1_patch = imfilter(im1_patch,H);
x_hm = [x1;y1;1];
L = x_hm' * F;
y2_v = [y1-19:1:y1+19];
x2_v = round(- L(2)/L(1) * y2_v - L(3)/L(1));
error_min = inf;
for i = 1:length(x2_v)
    startx = x2_v(i)-patchWidth;
    endx = x2_v(i)+patchWidth;
    starty = y2_v(i)-patchWidth;
    endy = y2_v(i)+patchWidth;
    im2_patch = im2(starty:endy, startx:endx);
    im2_patch = imfilter(im2_patch,H);
    error = sum(sum((im2_patch-im1_patch).^2));
    if (error < error_min)
        error_min = error;
        i_min = i;
    end
end
x2 = x2_v(i_min);
y2 = y2_v(i_min);
end