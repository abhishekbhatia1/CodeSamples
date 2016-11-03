function [PrincipalCurvature] = computePrincipalCurvature(DoGPyramid)

PrincipalCurvature = zeros(size(DoGPyramid,1),size(DoGPyramid,2),size(DoGPyramid,3));

[Hx Hy] = gradient(DoGPyramid);
[Hxx Hxy] = gradient(Hx);
[Hyx Hyy] = gradient(Hy);

for i = 1:size(DoGPyramid,1)
    for j = 1:size(DoGPyramid,2)
        for k = 1:size(DoGPyramid,3)
            H = [Hxx(i,j,k),Hxy(i,j,k);Hyx(i,j,k),Hyy(i,j,k)];
            PrincipalCurvature(i,j,k) = trace(H)*trace(H)/det(H);
        end
    end
end