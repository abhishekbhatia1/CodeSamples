function [wordMap] = getVisualWords(image, filterBank, dictionary)

I = image;
% if (length(size(I)) == 2)
%     wordMap = zeros(size(I,1),size(I,2));
% else
%     wordMap = zeros(size(I,1),size(I,2));
% end

filterResponses = extractFilterResponses(I, filterBank);
filterResponses_new = reshape(filterResponses,size(filterResponses,1)*size(filterResponses,2),size(filterResponses,3));
euc_dist = pdist2(filterResponses_new,dictionary');
[M,I] = min(euc_dist');
size_fr = size(filterResponses);
wordMap = reshape(I',size_fr(1:2));



