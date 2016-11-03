% Extra credit.  You can leave this untouched if you're not doing the EC.
clear all;
load(fullfile('..','data','carseq.mat'));
rect1(1,:) = [60,117,146,152];
rect2(1,:) = [60,117,146,152];
rect_new(1,:) = [60,117,146,152];
figure(1);
hold on;
It=frames(:,:,1);
    
for i=1:length(frames)-1
    It1=frames(:,:,i+1);
    [u,v] = LucasKanade(It,It1,rect_new);
    rect1(i+1,:)=  rect_new + round([u,v,u,v]);
    if (norm([u,v]) > 5)
        It = frames(:,:,i+1);
        rect_new = rect_new + round([u,v,u,v]);
    end
    It_new = insertShape(It1,'rectangle',[rect1(i+1,1),rect1(i+1,2),rect1(i+1,3)-rect1(i+1,1),rect1(i+1,4)-rect1(i+1,2)], ...
         'Color','yellow','LineWidth',2);
    [u,v] = LucasKanade(frames(:,:,i),frames(:,:,i+1),rect2(i,:));
    rect2(i+1,:)=  rect2(i,:) + round([u,v,u,v]);
    It_new = insertShape(It_new,'rectangle',[rect2(i+1,1),rect2(i+1,2),rect2(i+1,3)-rect2(i+1,1),rect2(i+1,4)-rect2(i+1,2)], ...
         'Color','green','LineWidth',2);
    imshow(It_new);
end

% count = 1;
% for i=1:length(frames)-1
%     It1=frames(:,:,i+1);
%     [u,v] = LucasKanade(It,It1,rect_new);
%     rect1(i+1,:)=  rect_new + round([u,v,u,v]);
%     if (norm([u,v]) > 5)
%         It = frames(:,:,i+1);
%         rect_new = rect_new + round([u,v,u,v]);
%     end
%     It_new = insertShape(It1,'rectangle',[rect1(i+1,1),rect1(i+1,2),rect1(i+1,3)-rect1(i+1,1),rect1(i+1,4)-rect1(i+1,2)], ...
%          'Color','yellow','LineWidth',2);
%     [u,v] = LucasKanade(frames(:,:,i),frames(:,:,i+1),rect2(i,:));
%     rect2(i+1,:)=  rect2(i,:) + round([u,v,u,v]);
%     It_new = insertShape(It_new,'rectangle',[rect2(i+1,1),rect2(i+1,2),rect2(i+1,3)-rect2(i+1,1),rect2(i+1,4)-rect2(i+1,2)], ...
%          'Color','green','LineWidth',2);
%     if (i == 1 || i == 100 || i == 200 || i == 300 || i == 400)
%         subplot(1,5,count);
%         imshow(It_new);
%         count = count + 1;
%     end 
% end

rects = rect1;
hold off;

save('../results/carseqrects-wcrt.mat', 'rects');

