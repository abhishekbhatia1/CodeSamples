function template = tl_lda(template_images_pos, template_images_neg, lambda)
% input:
%     template_images_pos - a cell array, each one contains [16 x 16 x 9] matrix
%     template_images_neg - a cell array, each one contains [16 x 16 x 9] matrix
%     lambda - parameter for lda
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

clearvars patch;
cov = zeros(16,16,9);
cov_temp = zeros(16,16,9);
num_neg = length(template_images_neg);
for i = 1:num_neg
    patch = template_images_neg{i};
    hog_patch = hog(patch);
    for j = 1:size(hog_patch,3)
        cov_temp(:,:,j) = 1/num_neg * (hog_patch(:,:,j) - template_neg(:,:,j)) ...
                     * (hog_patch(:,:,j) - template_neg(:,:,j))';
    end
    cov = cov + cov_temp;
end

Id = eye(16,16);
inv_cov = zeros(16,16,9);
for i = 1:size(cov,3)
    inv_cov(:,:,i) = inv(cov(:,:,i) + lambda*Id);
    template(:,:,i) = inv_cov(:,:,i) * (template_pos(:,:,i) - template_neg(:,:,i));
end

end