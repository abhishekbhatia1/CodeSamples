% %batchToVisualWords(2)
% filterBank = createFilterBank();
% load('dictionary.mat','filterBank','dictionary');
% [wordMap] = getVisualWords(imread('../dat/airport/sun_ahigtnhmsjrkayvw.jpg'), filterBank, dictionary);
% [image] = imread('../dat/airport/sun_ahigtnhmsjrkayvw.jpg');
% %[h] = getImageFeaturesSPM(3, wordMap, 200);
% [h] = getImageFeaturesSPM_new(3, wordMap, 200);
% %[h] = getImageFeatures(wordMap, 200);
load('../dat/traintest.mat'); 
l = length(test_imagenames);
source = '../dat/';
conf = zeros(8,8);
for i = 1:l
    image = test_imagenames{i};
    image = strcat('../dat/',image);
    %image = strrep(image,'.jpg','');
    %image = strcat(image,'.mat')
    %load([source, image]);
    %imagesc(wordMap);
    %[tl,~] = guessImage(image);
    gi = guessImage(image);
    if (strcmp(gi,mapping{1}))
        tl = 1;
    elseif (strcmp(gi,mapping{2}))
        tl = 2;
    elseif (strcmp(gi,mapping{3}))
        tl = 3;
    elseif (strcmp(gi,mapping{4}))
        tl = 4;
    elseif (strcmp(gi,mapping{5}))
        tl = 5;
    elseif (strcmp(gi,mapping{6}))
        tl = 6;
    elseif (strcmp(gi,mapping{7}))
        tl = 7;
    else
        tl = 8;
    end
    al = test_labels(i);
    conf(al,tl) = conf(al,tl) + 1;
end
trace(conf)/sum(conf(:))*100