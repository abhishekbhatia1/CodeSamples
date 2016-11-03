function [ F ] = eightpoint_ransac( pts1, pts2, M )
% eightpoint:
%   pts1 - Nx2 matrix of (x,y) coordinates
%   pts2 - Nx2 matrix of (x,y) coordinates
%   M    - max (imwidth, imheight)

% Q2.1 - Todo:
%     Implement the eightpoint algorithm
%     Generate a matrix F from some '../data/some_corresp.mat'
%     Save F, M, pts1, pts2 to q2_1.mat

%     Write F and display the output of displayEpipolarF in your writeup
max_points = 0;
nIter = 2000;
tol = 20;
for i = 1:nIter
    p = randi(length(pts1),8,1);
    for j = 1:length(p)
        p1(j) = pts1(p(j));
        p2(j) = pts2(p(j));
    end
    F = computeF(p1,p2,max(pts1(1,:), pts1(2,:)))
    for j = 1:length(pts1)
        point1(j,1:2) = pts1(j,1:2);
        point1(j,3) = 1;
        point2(j,1:2) = pts2(j,1:2);
        point2(j,3) = 1;
    end
    p_new = F * point2';
    p_new(1,:) = p_new(1,:)./p_new(3,:);
    p_new(2,:) = p_new(2,:)./p_new(3,:);
    p_new(3,:) = p_new(3,:)./p_new(3,:);
    dist = pdist2(point1,p_new');
    inliers = find(diag(dist)<tol);
    if (numel(inliers) > max_points)
        max_points = numel(inliers)
        dig = diag(dist);
        bestF = F;
    end
end
jj = 1;
for j = 1:length(dig)
    if(dig(j)<tol)
        point3(jj) = pts1(j);
        point4(jj) = pts2(j);
        jj = jj + 1;
    end
end
bestF = computeF(point3,point4,max(pts1(1,:), pts1(2,:)))
max_points
end