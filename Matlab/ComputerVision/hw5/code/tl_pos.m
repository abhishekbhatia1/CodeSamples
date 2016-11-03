function template = tl_pos(template_images_pos)
% input:
%     template_images_pos - a cell array, each one contains [16 x 16 x 9] matrix
% output:
%     template - [16 x 16 x 9] matrix

template = zeros(16,16,9);
num_pos = length(template_images_pos);
for i = 1:num_pos
    patch = template_images_pos{i};
    template = template + hog(patch);
end
template = template/num_pos;
end