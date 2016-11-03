layerNum = 3;
k_words = 300;

load('../dat/traintest.mat','train_imagenames','mapping','train_labels');
load('dictionary.mat','filterBank','dictionary');
source = '../dat/';

l = length(train_imagenames)
%train_features = zeros(k_words*(4^layerNum - 1)/3,l);
for i = 1:l
    image = train_imagenames{i};
    image = strrep(image,'.jpg','');
    image = strcat(image,'.mat')
    load([source, image]);
    train_features(:,i) = getImageFeaturesSPM(layerNum, wordMap, k_words);
end
save('vision.mat','filterBank','dictionary','train_features','train_labels');