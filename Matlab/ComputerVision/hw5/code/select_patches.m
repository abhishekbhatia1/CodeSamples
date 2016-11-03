function select_patches()
clear all

cd('C:\Users\Abhishek Bhatia\Documents\CMU\Computer Vision\hw5\data');
imfiles = dir('*.jpg');
num_pos = length(imfiles);
template_images_pos = cell(num_pos,1);
for i = 1:num_pos
    Itrain = im2double(rgb2gray(imread(imfiles(i).name)));
    figure(1); clf;
    imshow(Itrain);
    a = round(getrect);
    x = a(1)
    y = a(2) 
    w = a(3); 
    h = a(4);
    if (y + max(w,h) < size(Itrain,1) && x + max(w,h) < size(Itrain,2))
        w = max(w,h)
        h = w
    else
        w = min(w,h)
        h = w
    end
    patch = Itrain(y:y+h,x:x+w);
    patch = imresize(patch, [128 128]);
    template_images_pos{i} = patch;
    figure(2); clf;
    figure(2); imshow(patch);
    clearvars patch;
end

cd('C:\Users\Abhishek Bhatia\Documents\CMU\Computer Vision\hw5\data');
imfiles = dir('*.jpg');
num_neg = length(imfiles);
template_images_neg = cell(num_neg,1);
for i = 1:num_neg
    Itrain = im2double(rgb2gray(imread(imfiles(i).name)));
    figure(1); clf;
    imshow(Itrain);
    a = round(getrect);
    x = a(1); 
    y = a(2); 
    w = a(3); 
    h = a(4);
    if (y + max(w,h) < size(Itrain,1) && x + max(w,h) < size(Itrain,2))
        w = max(w,h);
        h = w;
    else
        w = min(w,h);
        h = w;
    end
    patch = Itrain(y:y+h,x:x+w);
    patch = imresize(patch, [128 128]);
    template_images_neg{i} = patch;
    figure(2); clf;
    figure(2); imshow(patch);
    clearvars patch;
end
cd('C:\Users\Abhishek Bhatia\Documents\CMU\Computer Vision\hw5\code');

save('template_images_pos.mat','template_images_pos')
save('template_images_neg.mat','template_images_neg')

end