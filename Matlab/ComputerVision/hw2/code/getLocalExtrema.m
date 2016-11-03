function [locsDoG] = getLocalExtrema(DoGPyramid, DoGLevels, PrincipalCurvature,th_contrast, th_r)

ii = 1;
regmax = imregionalmax(DoGPyramid);
regmin = imregionalmin(DoGPyramid);

for i = 1:size(DoGPyramid,1)
    for j = 1:size(DoGPyramid,2)
        for k = 1:size(DoGPyramid,3)
            if (regmax(i,j,k))
                locs(ii,1) = j;
                locs(ii,2) = i;
                locs(ii,3) = DoGLevels(k);
                locs(ii,4) = k;
                ii = ii + 1;
            end
            if (regmin(i,j,k))
                locs(ii,1) = j;
                locs(ii,2) = i;
                locs(ii,3) = DoGLevels(k);
                locs(ii,4) = k;
                ii = ii + 1;
            end
        end
    end
end

locs;

ii = 1;
for i = 1:size(locs,1)
    %for j = 1:size(locs,2)
        %for k = 1:size(locs,3)
            if (abs(DoGPyramid(locs(i,2),locs(i,1),locs(i,4))) > th_contrast && ...
               (PrincipalCurvature(locs(i,2),locs(i,1),locs(i,4)) > 0 && ...
               PrincipalCurvature(locs(i,2),locs(i,1),locs(i,4)) < th_r))
                locsDoG(ii,1) = locs(i,1);
                locsDoG(ii,2) = locs(i,2);
                locsDoG(ii,3) = locs(i,3);
                ii = ii + 1;
            end
        %end
    %end
end