function [x,y,score,CC] = detection(I,template,ndet)
%
% return top ndet detections found by applying template to the given image.
%   x,y should contain the coordinates of the detections in the image
%   score should contain the scores of the detections
%

ohist = hog(I);
n_or = size(ohist,3);
CC = zeros(size(ohist,1),size(ohist,2));

for i = 1:n_or
    CC = CC + imfilter(ohist(:,:,i), template(:,:,i));
end

[scr,idx] = sort(CC(:),'descend');
scr;
x = zeros(ndet,1);
y = zeros(ndet,1);
score = zeros(ndet,1);
count = 0;


for i = 1:length(idx)
    if (count >= ndet)
        break;
    else
        [yb,xb] = ind2sub(size(CC),idx(i));
        %[yp,xp] = [8*yb,8*xb];
        yp = 8*yb;
        xp = 8*xb;
        flag = 0;
        for j = 1:count
            if (abs(y(j) - yp) < 8*size(template,1) && abs(x(j) - xp) < 8*size(template,2))
                flag = 1;
            end
        end
        if (flag == 0)
            count = count + 1;
            x(count) = xp;
            y(count) = yp;
            score(count) = scr(i);
        end
    end
end
end