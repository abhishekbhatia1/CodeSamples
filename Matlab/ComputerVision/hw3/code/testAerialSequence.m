clear all;
load(fullfile('..','data','aerialseq.mat'));
figure(1);
hold on;

for i=1:size(frames,3)-1
    It=frames(:,:,i);
    It1=frames(:,:,i+1);
    mask = SubtractDominantMotion(It, It1);
    im = imfuse(mask,frames(:,:,i));
    imshow(im);
end

% count = 1;
% for i=1:size(frames,3)-1
%     It=frames(:,:,i);
%     It1=frames(:,:,i+1);
%     mask = SubtractDominantMotion(It, It1);
%     im = imfuse(mask,frames(:,:,i));
%     if (i == 30 || i == 60 || i == 90 || i == 120)
%         subplot(1,4,count);
%         imshow(im);
%         count = count + 1;
%     end
% end

hold off;
% save(fullfile('..','results','aerialseqrects.mat','rects'));
