clear all
for i = 0:36
    im1 = imread('../data/model_chickenbroth.jpg');
    im1 = im2double(im1);
    if size(im1,3)==3
        im1= rgb2gray(im1);
    end
    im2 = imread('../data/model_chickenbroth.jpg');
    im2 = imrotate(im2,i*10);
    im2 = im2double(im2);
    if size(im2,3)==3
        im2= rgb2gray(im2);
    end
    [locs1, desc1] = briefLite(im1);
    [locs2, desc2] = briefLite(im2);
    [matches] = briefMatch(desc1, desc2);
    barc(i+1,1) = i*10;
    barc(i+1,2) = length(matches);
    %bar(i*10,length(matches));
    %hold on;
end
bar(barc(:,1),barc(:,2));