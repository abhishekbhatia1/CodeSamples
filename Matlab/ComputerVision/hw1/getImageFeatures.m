function [h] = getImageFeatures(wordMap, dictionarySize)

h = zeros(dictionarySize,1);

I = reshape(wordMap,size(wordMap,1)*size(wordMap,2),1);
h = hist(I,dictionarySize);
%h = h/sum(h);
h = h';