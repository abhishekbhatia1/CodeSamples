function [locs,desc] = computeBrief(im, GaussianPyramid, locsDoG, k, levels, compareX, compareY)

len = size(im,1);
wid = size(im,2);
patchWidth = 9;
j = 1;
nbits = 256;
descv = zeros(1,256);

for i = 1:length(locsDoG)
    if (locsDoG(i,1)-floor(patchWidth/2)>0 && locsDoG(i,1)+floor(patchWidth/2)<=wid && ...
        locsDoG(i,2)-floor(patchWidth/2)>0 && locsDoG(i,2)+floor(patchWidth/2)<=len)
        locs(j,:) = locsDoG(i,:);
        startx = locsDoG(i,2)-floor(patchWidth/2);
        endx = locsDoG(i,2)+floor(patchWidth/2);
        starty = locsDoG(i,1)-floor(patchWidth/2);
        endy = locsDoG(i,1)+floor(patchWidth/2);
        im_new = im(startx:endx, starty:endy);
        for k = 1:nbits
            %if (im_new(compareX(k) < im_new(compareY(k))))
            if (im_new(compareX(k)) < im_new(compareY(k)))
                if (j == 1)
                    desc(1,k) = 1;
                else
                    descv(1,k) = 1;
                end
            else
                if (j == 1)
                    desc(1,k) = 0;
                else
                    descv(1,k) = 0;
                end
            end
        end
        if (j > 1)
            desc = vertcat(desc, descv);
        end
        j = j+1;
    end
end