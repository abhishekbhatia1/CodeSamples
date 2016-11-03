clear all;
load(fullfile('..','data','carseq.mat'));
rect(1,:) = [60,117,146,152];
figure(1);
hold on;

%for i=1:length(frames)-1
for i=1:size(frames,3)-1
    It=frames(:,:,i);
    It1=frames(:,:,i+1);
    It_new = insertShape(It,'rectangle',[rect(i,1),rect(i,2),rect(i,3)-rect(i,1),rect(i,4)-rect(i,2)], ...
         'Color','yellow','LineWidth',2);
    imshow(It_new);
    [u,v] = LucasKanade(It,It1,rect(i,:));
    rect(i+1,:)=  rect(i,:) + round([u,v,u,v]);
end

% count = 1;
% for i = 1:size(frames,3)-1
%     It=frames(:,:,i);
%     It1=frames(:,:,i+1);
%     It_new = insertShape(It,'rectangle',[rect(i,1),rect(i,2),rect(i,3)-rect(i,1),rect(i,4)-rect(i,2)], ...
%          'Color','yellow','LineWidth',2);
%     if (i == 1 || i == 100 || i == 200 || i == 300 || i == 400)
%         subplot(1,5,count);
%         imshow(It_new);
%         count = count + 1;
%     end
%     [u,v] = LucasKanade(It,It1,rect(i,:));
%     rect(i+1,:)=  rect(i,:) + round([u,v,u,v]);
% end

rects = rect;
save('../results/carseqrects.mat', 'rects'); 
hold off;