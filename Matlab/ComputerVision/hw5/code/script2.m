clear all
%%

%select_patches();
load('template_images_pos.mat');
load('template_images_neg.mat');
%template = tl_pos(template_images_pos);
%template = tl_pos_neg(template_images_pos, template_images_neg);
lambda = 0.35;
template = tl_lda(template_images_pos, template_images_neg, lambda);
Itest= im2double(rgb2gray(imread('../data/test/multiple2.jpg')));


% find top 5 detections in Itest
ndet = 2;
%[x,y,score,CC] = detect(Itest,template,ndet);
x = zeros(ndet,1);
y = zeros(ndet,1);
scale = zeros(ndet,1);
det_res = multiscale_detect(Itest, template, ndet);
x(:) = det_res(:,1);
y(:) = det_res(:,2);
scale(:) = det_res(:,3);

%display top ndet detections
figure; clf; imshow(Itest);
for i = 1:ndet
  % draw a rectangle.  use color to encode confidence of detection
  %  top scoring are green, fading to red
  scale(i)
  hold on; 
  h = rectangle('Position',[x(i)-64/scale(i) y(i)-64/scale(i) 128/scale(i) 128/scale(i)],'EdgeColor',[(i/ndet) ((ndet-i)/ndet)  0],'LineWidth',3,'Curvature',[0.3 0.3]); 
  hold off;
end
