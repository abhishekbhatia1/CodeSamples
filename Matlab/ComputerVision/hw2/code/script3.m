clear all
img1 = imread('../data/incline_L.png');
%img1 = imread('../data/chickenbroth_01.jpg');
im1 = im2double(img1);
if size(im1,3)==3
    im1= rgb2gray(im1);
end
img2 = imread('../data/incline_R.png');
%img2 = imread('../data/chickenbroth_02.jpg');
im2 = im2double(img2);
if size(im2,3)==3
    im2= rgb2gray(im2);
end
[locs1, desc1] = briefLite(im1);
[locs2, desc2] = briefLite(im2);
[matches] = briefMatch(desc1, desc2);

for i = 1:length(matches)
        p1(i,1:2) = locs1(matches(i,1),1:2);
        p2(i,1:2) = locs2(matches(i,2),1:2);
end
H2to1 = computeH(p1',p2');
%[panoImg] = imageStitching_noClip(img1, img2, H2to1);
[panoImg] = imageStitching(img1, img2, H2to1);
imshow(panoImg);
%save('q5 1.mat','H2to1');