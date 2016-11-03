function det_res = multiscale_detect(image, template, ndet)
% input:
%     image - test image.
%     template - [16 x 16x 9] matrix.
%     ndet - the number of return values.
% output:
%      det_res - [ndet x 3] matrix
%                column one is the x coordinate
%                column two is the y coordinate
%                column three is the scale, i.e. 1, 0.7 or 0.49 ..

I = image;
[x,y,score] = detect(I,template,ndet);
scale_mat = 1;
scale = 1;
for i = 1:size(x,1)-1
        scale_mat = vertcat(scale_mat,scale);
end
scale = 0.7;
I = imresize(image,scale);
while (size(I,1) > size(template,1)*8 && size(I,2) > size(template,2)*8)
    [x_new,y_new,score_new] = detect(I,template,ndet);
    x = vertcat(x,x_new/scale);
    y = vertcat(y,y_new/scale);
    score = vertcat(score,score_new);
    size(x);
    for i = 1:size(x,1)
        scale_mat = vertcat(scale_mat,scale);
    end
    scale = scale * 0.7;
    I = imresize(image,scale);
end

[scr,idx] = sort(score,'descend');
det_res = zeros(ndet,3);

% for i = 1:ndet
%     det_res(i,1) = x(idx(i));
%     det_res(i,2) = y(idx(i));
%     det_res(i,3) = scale_mat(idx(i));
% end

count = 0;
for i = 1:length(idx)
    if (count >= ndet)
        break;
    else
        x_idx = x(idx(i));
        y_idx = y(idx(i));
        flag = 0;
        for j = 1:count
            if (abs(det_res(j,2) - y_idx) < 8*size(template,1) && abs(det_res(j,1) - x_idx) < 8*size(template,2))
                flag = 1;
            end
        end
        if (flag == 0)
            count = count + 1;
            det_res(count,1) = x(idx(i));
            det_res(count,2) = y(idx(i));
            det_res(count,3) = scale_mat(idx(i));
        end
    end
end

end
