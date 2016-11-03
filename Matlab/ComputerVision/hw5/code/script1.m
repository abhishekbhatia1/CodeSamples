clear all
I = rgb2gray(imread('../data/test4.jpg'));
%[mag,ori]  = mygradient(I);
%[mag,ori] = imgradient(I);
ohist = hog(I);
V = hogdraw(ohist, 15);
imagesc(V);
% figure
% subplot(1,2,1); 
% imagesc(mag);
% subplot(1,2,2);
% imagesc(ori);
%[x,y,score] = detection(I,template,ndet)