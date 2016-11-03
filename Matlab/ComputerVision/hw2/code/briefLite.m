function [locs, desc] = briefLite(im)

levels = [-1, 0, 1, 2, 3, 4];
k = sqrt(2);
sigma0 = 1;
th_contrast = 0.03;
th_r = 12;
patchWidth = 9;
nbits = 256;

%[compareX, compareY] = makeTestPattern(patchWidth, nbits);
load('testPattern.mat');
[locsDoG, GaussianPyramid] = DoGdetector(im, sigma0, k, levels,th_contrast, th_r);
size(locsDoG);
%im = imread('../data/model_chickenbroth.jpg');
[locs,desc] = computeBrief(im, GaussianPyramid, locsDoG, k, levels, compareX, compareY);