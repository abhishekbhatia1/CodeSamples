function select_patches_2()
clear all

cd('C:\Users\Abhishek Bhatia\Documents\CMU\Computer Vision\hw5\data\test1');
imfiles = dir('*.jpg');
num_pos = length(imfiles);
template_images_pos = cell(num_pos,1);
num_neg = 20*length(imfiles);
template_images_neg = cell(num_neg,1);
count = 1;
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
    j = 0;
    while(j < 20)
        j
        x_neg = randi([1 size(Itrain,2)],1,1);
        y_neg = randi([1 size(Itrain,1)],1,1);
        h_neg = 127;
        w_neg = 127;
        if ((x_neg > x && x_neg < x + w) && (y_neg > y && y_neg < y + h))
            continue;
        else
            if (y_neg + max(w_neg,h_neg) < size(Itrain,1) && x_neg + max(w_neg,h_neg) < size(Itrain,2))
                clearvars patch;
                patch = Itrain(y_neg:y_neg+h_neg,x_neg:x_neg+w_neg);
                template_images_neg{count} = patch;
                count = count + 1;
                j = j + 1;
            end
        end
    end
%     figure(2); clf;
%     figure(2); imshow(patch);
     clearvars patch;
end

cd('C:\Users\Abhishek Bhatia\Documents\CMU\Computer Vision\hw5\code');

save('template_images_pos.mat','template_images_pos')
save('template_images_neg.mat','template_images_neg')

end