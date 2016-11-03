function [filterResponses] = extractFilterResponses(I, filterBank)
% CV Fall 2015 - Provided Code
% Extract the filter responses given the image and filter bank
% Pleae make sure the output format is unchanged. 
% Inputs: 
%   I:                  a 3-channel RGB image with width W and height H 
%   filterBank:         a cell array of N filters
% Outputs:
%   filterResponses:    a W*H x N*3 matrix of filter responses
 
%Check if the image is greyscale, if yes, convert
if (length(size(I)) == 2)
    I = repmat(I,[1 1 3]);
end
    
%Convert input Image to Lab
doubleI = double(I);
%doubleI = I;
[L,a,b] = RGB2Lab(doubleI(:,:,1), doubleI(:,:,2), doubleI(:,:,3));
%pixelCount = zeros(size(doubleI,1)*size(doubleI,2));

%filterResponses:    a W*H x N*3 matrix of filter responses
filterResponses = zeros(size(doubleI,1), size(doubleI,2), length(filterBank)*3);



%for each filter and channel, apply the filter, and vectorize

% === fill in your implementation here  ===

k = 1;
%figure(1);
for i = 1 : size(filterBank,1)
    for j = 1 : size(I,3)
        %filterResponses(:,:,k) = imfilter(I(:,:,j),filterBank{i});
        if (j == 1)
            filterResponses(:,:,k) = imfilter(L,filterBank{i});
        elseif (j == 2)
            filterResponses(:,:,k) = imfilter(a,filterBank{i});
        else
            filterResponses(:,:,k) = imfilter(b,filterBank{i});
        end
        k = k + 1;
    end
end

% for i = 1 : size(filterBank,1)
%     subplot(4,5,i);
%     imshow(uint8(round(cat(3,filterResponses(:,:,i*3-2),filterResponses(:,:,i*3-1),filterResponses(:,:,i*3))-1)));
% end

end
