function template = tl_pos_neg(template_images_pos, template_images_neg)
% input:
%     template_images_pos - a cell array, each one contains [16 x 16 x 9] matrix
%     template_images_neg - a cell array, each one contains [16 x 16 x 9] matrix
% output:
%     template - [16 x 16 x 9] matrix 

template_pos = zeros(16,16,9);
num_pos = length(template_images_pos);
for i = 1:num_pos
    patch = template_images_pos{i};
    template_pos = template_pos + hog(patch);
end
template_pos = template_pos/num_pos;

clearvars patch;
template_neg = zeros(16,16,9);
num_neg = length(template_images_neg);
for i = 1:num_neg
    patch = template_images_neg{i};
    template_neg = template_neg + hog(patch);
end
template_neg = template_neg/num_neg;

template = template_pos - template_neg;

end