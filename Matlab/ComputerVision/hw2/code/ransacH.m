function [bestH] = ransacH_new(matches, locs1, locs2, nIter, tol)

max_points = 0;
for i = 1:nIter
    %p = randperm(length(matches),4);
    p = randi(length(matches),4,1);
    for j = 1:length(p)
        p1(j,1:2) = locs1(matches(p(j),1),1:2);
        p2(j,1:2) = locs2(matches(p(j),2),1:2);
    end
    H2to1 = computeH(p1',p2');
    for j = 1:length(matches)
        point1(j,1:2) = locs1(matches(j,1),1:2);
        point1(j,3) = 1;
        point2(j,1:2) = locs2(matches(j,2),1:2);
        point2(j,3) = 1;
    end
    p_new = H2to1 * point2';
    p_new(1,:) = p_new(1,:)./p_new(3,:);
    p_new(2,:) = p_new(2,:)./p_new(3,:);
    p_new(3,:) = p_new(3,:)./p_new(3,:);
    dist = pdist2(point1,p_new');
    inliers = find(diag(dist)<tol);
    if (numel(inliers) > max_points)
        max_points = numel(inliers);
        dig = diag(dist);
        bestH = H2to1;
    end
end
jj = 1;
for j = 1:length(dig)
    if(dig(j)<tol)
        point3(jj,1:2) = locs1(matches(j,1),1:2);
        point4(jj,1:2) = locs2(matches(j,2),1:2);
        jj = jj + 1;
    end
end
bestH = computeH(point3',point4');
max_points