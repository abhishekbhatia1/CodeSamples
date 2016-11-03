function mask = SubtractDominantMotion(image1, image2)
It = image1;
It1 = image2;
M = LucasKanadeAffine(It,It1);
TF = affine2d(M');
It = im2double(It);
It1 = im2double(It1);
WIt = imwarp(It,TF,'OutputView',imref2d(size(It)));
error = abs(It1 - WIt);
bw = im2bw(error,.4);
st = strel('disk',5);
mask = imdilate(bw,st);
end
