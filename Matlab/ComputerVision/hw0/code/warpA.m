function [ warp_im ] = warpA( im, A, out_size )
% warp_im=warpAbilinear(im, A, out_size)
% Warps (w,h,1) image im using affine (3,3) matrix A 
% producing (out_size(1),out_size(2)) output image warp_im
% with warped  = A*input, warped spanning 1..out_size
% Uses nearest neighbor mapping.
% INPUTS:
%   im : input image
%   A : transformation matrix 
%   out_size : size the output image should be
% OUTPUTS:
%   warp_im : result of warping im by A
warp_im = zeros(out_size(1),out_size(2));
warp_im_blah = zeros(out_size(1),out_size(2));
for i = 1:out_size(1)
    for j = 1:out_size(2)
        pt = [i,j,1]';
        ps = inv(A')*pt;
        ps(1) = round(ps(1));
        ps(2) = round(ps(2));
        if (ps(1) >= 1 && ps(1) <= out_size(1) && ps(2) >= 1 && ps(2) <= out_size(2))
            warp_im(i,j) = im(ps(1),ps(2));
        else
            warp_im(i,j) = 0;
        end
    end
end
for i = 1:out_size(1)
    for j = 1:out_size(2)
        pt = [i,j,1]';
        ps = A*pt;
        ps(1) = round(ps(1));
        ps(2) = round(ps(2));
        if (ps(1) >= 1 && ps(1) <= out_size(1) && ps(2) >= 1 && ps(2) <= out_size(2))
            warp_im_blah(i,j) = warp_im(ps(1),ps(2));
        else
            warp_im_blah(i,j) = 0;
        end
    end
end
%warp_im = warp_im_blah;