clear all
load(fullfile('..','data','sylvseq.mat'));
load(fullfile('..','data','sylvbases.mat'));
% load(fullfile('..','data','bookSequence.mat'));
% load(fullfile('..','data','bookBases.mat'));

rect1(1,:) = [102; 62; 156; 108];
rect2(1,:) = [102; 62; 156; 108];
% rect1(1,:) = [247;102;285;161];
% rect2(1,:) = [247;102;285;161];

%rect = []
figure(2);
hold on;

%for i=1:length(frames)-1
for i=1:size(frames,3)-1
    It=frames(:,:,i);
    It1=frames(:,:,i+1);
    It_new = insertShape(It,'rectangle',[rect1(i,1),rect1(i,2),rect1(i,3)-rect1(i,1),rect1(i,4)-rect1(i,2)], ...
         'Color','yellow','LineWidth',2);
    It_new = insertShape(It_new,'rectangle',[rect2(i,1),rect2(i,2),rect2(i,3)-rect2(i,1),rect2(i,4)-rect2(i,2)], ...
         'Color','green','LineWidth',3);
    imshow(It_new);
    [u1,v1] = LucasKanade(It,It1,rect1(i,:));
    [u2,v2] = LucasKanadeBasis(It,It1,rect2(i,:),bases);
    rect1(i+1,:)=  rect1(i,:) + round([u1,v1,u1,v1]);
    rect2(i+1,:)=  rect2(i,:) + round([u2,v2,u2,v2]);
end

% count = 1;
% for i=1:size(frames,3)-1
%     It=frames(:,:,i);
%     It1=frames(:,:,i+1);
%     It_new = insertShape(It,'rectangle',[rect1(i,1),rect1(i,2),rect1(i,3)-rect1(i,1),rect1(i,4)-rect1(i,2)], ...
%          'Color','green','LineWidth',2);
%     It_new = insertShape(It_new,'rectangle',[rect2(i,1),rect2(i,2),rect2(i,3)-rect2(i,1),rect2(i,4)-rect2(i,2)], ...
%          'Color','yellow','LineWidth',3);
%     %if (i == 1 || i == 100 || i == 300 || i == 350 || i == 400)
%     if (i == 1 || i == 50 || i == 100 || i == 150 || i == 200)
%         subplot(1,5,count);
%         imshow(It_new);
%         count = count + 1;
%     end
%     [u1,v1] = LucasKanade(It,It1,rect1(i,:));
%     [u2,v2] = LucasKanadeBasis(It,It1,rect2(i,:),bases);
%     rect1(i+1,:)=  rect1(i,:) + round([u1,v1,u1,v1]);
%     rect2(i+1,:)=  rect2(i,:) + round([u2,v2,u2,v2]);
% end

rects = rect2;
save('../results/sylvseqrects.mat', 'rects');
hold off;