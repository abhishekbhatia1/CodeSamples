function [h] = getImageFeaturesSPM(layerNum, wordMap, dictionarySize)

height = size(wordMap,1);
width = size(wordMap,2);

fun = @(block_struct)getImageFeatures(block_struct.data,dictionarySize);
for i = 1:layerNum
    h_new = height - rem(height,2^(i-1));
    w_new = width - rem(width,2^(i-1));
    wordMap = wordMap(1:h_new,1:w_new);
    histo{i} = blockproc(wordMap,[h_new/2^(i-1) w_new/2^(i-1)],fun);
    histo{i} = reshape(histo{i},[numel(histo{i}),1]);    
end
if (layerNum > 1)
    h = vertcat((1/4).*histo{1},(1/4).*histo{2},(1/2).*histo{3});
else
    h = histo{1};
end
h = h/sum(h);