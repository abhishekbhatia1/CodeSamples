function im3 = generatePanorama(im1, im2)

%clear all
nIter = 2000;
tol = 20;
%img1 = imread('../data/incline_L.png');
%img1 = imread('../data/chickenbroth_01.jpg');
img1 = im1;
image1 = im2double(img1);
if size(image1,3)==3
    image1= rgb2gray(image1);
end
%img2 = imread('../data/incline_R.png');
%img2 = imread('../data/chickenbroth_02.jpg');
img2 = im2;
image2 = im2double(img2);
if size(image2,3)==3
    image2= rgb2gray(image2);
end
[locs1, desc1] = briefLite(image1);
[locs2, desc2] = briefLite(image2);
[matches] = briefMatch(desc1, desc2);

for i = 1:length(matches)
        p1(i,1:2) = locs1(matches(i,1),1:2);
        p2(i,1:2) = locs2(matches(i,2),1:2);
end
%H2to1 = computeH(p1',p2');
[bestH] = ransacH(matches, locs1, locs2, nIter, tol)
[panoImg] = imageStitching_noClip(img1, img2, bestH);
imshow(panoImg);
im3 = panoImg;