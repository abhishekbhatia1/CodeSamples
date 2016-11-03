function [compareX, compareY] = makeTestPattern(patchWidth, nbits)

compX = round(normrnd(0,patchWidth/5,[nbits 2]));
compY = round(normrnd(0,patchWidth/5,[nbits 2]));

for i = 1:nbits
    if (compX(i,1)<-floor(patchWidth/2))
        compX(i,1) = -floor(patchWidth/2);
    end
    if (compX(i,1)>floor(patchWidth/2))
        compX(i,1) = floor(patchWidth/2);
    end
    if (compX(i,2)<-floor(patchWidth/2))
        compX(i,2) = -floor(patchWidth/2);
    end
    if (compX(i,2)>floor(patchWidth/2))
        compX(i,2) = floor(patchWidth/2);
    end
    if (compY(i,1)<-floor(patchWidth/2))
        compY(i,1) = -floor(patchWidth/2);
    end
    if (compY(i,1)>floor(patchWidth/2))
        compY(i,1) = floor(patchWidth/2);
    end
    if (compY(i,2)<-floor(patchWidth/2))
        compY(i,2) = -floor(patchWidth/2);
    end
    if (compY(i,2)>floor(patchWidth/2))
        compY(i,2) = floor(patchWidth/2);
    end
end

compX(:,1) = compX(:,1) + round(patchWidth/2);
compX(:,2) = compX(:,2) + round(patchWidth/2);
compY(:,1) = compY(:,1) + round(patchWidth/2);
compY(:,2) = compY(:,2) + round(patchWidth/2);

compareX = sub2ind([9 9],compX(:,1), compX(:,2));
compareY = sub2ind([9 9],compY(:,1), compY(:,2));
save('testPattern.mat','compareX','compareY');