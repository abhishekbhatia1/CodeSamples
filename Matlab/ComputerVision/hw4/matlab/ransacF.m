function [ F ] = ransacF( pts1, pts2, M )
% ransacF:
%   pts1 - Nx2 matrix of (x,y) coordinates
%   pts2 - Nx2 matrix of (x,y) coordinates
%   M    - max (imwidth, imheight)

% Q2.X - Extra Credit:
%     Implement RANSAC
%     Generate a matrix F from some '../data/some_corresp_noisy.mat'
%          - using sevenpoint
%          - using ransac

%     In your writeup, describe your algorith, how you determined which
%     points are inliers, and any other optimizations you made
max_points = 0;
nIter = 100;
tol = .01;
for i = 1:nIter
    p = randi(length(pts1),7,1);
    for j = 1:length(p)
        p1(j,1:2) = pts1(p(j),1:2);
        p2(j,1:2) = pts2(p(j),1:2);
    end
    F_i = sevenpoint(p1,p2,M);
    for i_f = 1:size(F_i,3)
        for j = 1:length(pts1)
            point1(j,1:2) = pts1(j,1:2);
            point1(j,3) = 1;
            point2(j,1:2) = pts2(j,1:2);
            point2(j,3) = 1;
        end
        dist = abs(point1 * F_i(:,:,i_f) * point2');
        inliers = find(diag(dist)<tol);
        if (numel(inliers) > max_points)
            max_points = numel(inliers);
            dig = diag(dist);
            bestF = F_i(:,:,i_f);
        end
    end
end
jj = 1;
for j = 1:length(dig)
    if(dig(j)<tol)
        point3(jj,1:2) = pts1(j,1:2);
        point4(jj,1:2) = pts2(j,1:2);
        jj = jj + 1;
    end
end
bestF = sevenpoint(point3,point4,M);
F = bestF;
max_points;
end