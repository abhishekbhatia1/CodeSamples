function tl_detect_script

load('template_images_pos.mat');
load('template_images_neg.mat');
ndet = 2;
%Itest= im2double(rgb2gray(imread('../data/test_blah.jpg')));
Itest= im2double(rgb2gray(imread('../data/test/multiple2.jpg')));

template = tl_pos(template_images_pos);
[x,y,score] = detect(Itest,template,ndet);
draw_detection(ndet,x,y,1);


template = tl_pos_neg(template_images_pos, template_images_neg);
[x,y,score] = detect(Itest,template,ndet);
draw_detection(ndet,x,y,2);

lambda = 0.35;
template = tl_lda(template_images_pos, template_images_neg, lambda);
[x,y,score] = detect(Itest,template,ndet);
draw_detection(ndet,x,y,3);

det_res = multiscale_detect(Itest, template, ndet);
x(:) = det_res(:,1);
y(:) = det_res(:,2);
draw_detection(ndet,x,y,4);

end

function draw_detection(ndet,x,y,idx)
% please complete this function to show the detection results
%Itest= im2double(rgb2gray(imread('../data/test_blah.jpg')));
Itest= im2double(rgb2gray(imread('../data/test/multiple2.jpg')));

%display top ndet detections
figure(idx); clf; imshow(Itest);
for i = 1:ndet
  % draw a rectangle.  use color to encode confidence of detection
  %  top scoring are green, fading to red
  hold on; 
  h = rectangle('Position',[x(i)-64 y(i)-64 128 128],'EdgeColor',[(i/ndet) ((ndet-i)/ndet)  0],'LineWidth',3,'Curvature',[0.3 0.3]); 
  hold off;
end
end