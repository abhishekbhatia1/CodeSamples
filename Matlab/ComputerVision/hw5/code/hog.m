function ohist = hog(I)
%
% compute orientation histograms over 8x8 blocks of pixels
% orientations are binned into 9 possible bins
%
% I : grayscale image of dimension HxW
% ohist : orinetation histograms for each block. ohist is of dimension (H/8)x(W/8)x9
% TODO

% normalize the histogram so that sum over orientation bins is 1 for each block
%   NOTE: Don't divide by 0! If there are no edges in a block (ie. this counts sums to 0 for the block) then just leave all the values 0. 
% TODO
im = im2double(I);
[mag,ori] = mygradient(I);
for i = 1:size(ori,1)
    for j = 1:size(ori,2)
        if (ori(i,j) < -pi/2)
            ori(i,j) = ori(i,j) + pi;
        elseif(ori(i,j) > pi/2)
            ori(i,j) = ori(i,j) - pi;
        end
    end
end
n_or = 9;
th = 0.1*max(mag(:));
ohist = zeros(ceil(size(I,1)/8),ceil(size(I,2)/8),n_or);
for i = 1:n_or
    bin_left = -pi/2 + (i-1)* pi/9;
    bin_right = bin_left + pi/9;
    binary_I = mag > th & ori >= bin_left & ori < bin_right;
    spatial_blocks = im2col(binary_I,[8 8],'distinct');
    ohist(:,:,i) = reshape(sum(spatial_blocks),[size(ohist,1),size(ohist,2)]);
end
for i = 1:size(ohist,1)
    for j = 1:size(ohist,2)
        if (sum(ohist(i,j,:)) > 0)
            ohist(i,j,:) = ohist(i,j,:)./sum(ohist(i,j,:));
        end
    end
end
end



