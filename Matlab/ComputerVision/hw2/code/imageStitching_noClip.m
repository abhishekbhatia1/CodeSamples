function [panoImg] = imageStitching_noClip_new(img1, img2, H2to1)

pano_width = 1280;

q = [1 1 1; size(img2,2) 1 1; 1 size(img2,1) 1; size(img2,2) size(img2,1) 1;]'
%q = [1 1 1; size(img2,1) 1 1; 1 size(img2,2) 1; size(img2,1) size(img2,2) 1;]'

p = H2to1*q;
p(1,:) = p(1,:)./p(3,:);
p(2,:) = p(2,:)./p(3,:);
p(3,:) = p(3,:)./p(3,:);
p = round(p)

y_min = min(p(2,:))
if (y_min < 0)
    p(2,:) = p(2,:) + abs(y_min) + 5;
end
p

if(y_min < 0)
    out_size(1) = max(p(2,4),p(2,3)) + 10;
    out_size(2) = max(p(1,2),p(1,4)) + 15;
    pano_height = round((out_size(1)/out_size(2))*pano_width);
    s = pano_height/out_size(1);
    out_size(1) = pano_height;
    out_size(2) = pano_width;
else
    out_size(1) = max(max(p(2,:)),size(img1,1)) + 10;
    out_size(2) = max(max(p(1,:)),size(img1,2)) + 10;
    pano_height = round((out_size(1)/out_size(2))*pano_width);
    s = pano_height/out_size(1);
    out_size(1) = pano_height;
    out_size(2) = pano_width;
end

%M1 = [1 0 5; 0 1 p(2,1); 0 0 1]
if (y_min < 0)
    M1 = [s 0 s*5; 0 s s*(abs(y_min)+5); 0 0 1];
else
    M1 = [s 0 s*5; 0 s s*5; 0 0 1];
end

warp_img1 = warpH(img1, M1, out_size);
warp_img2 = warpH(img2, M1*H2to1, out_size);

warp_img1 = im2double(warp_img1);
warp_img2 = im2double(warp_img2);

panoImg = max(warp_img1,warp_img2);
%panoImg = warp_img1;