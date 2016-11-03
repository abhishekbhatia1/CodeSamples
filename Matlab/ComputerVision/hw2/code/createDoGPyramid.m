function [DoGPyramid, DoGLevels] = createDoGPyramid(GaussianPyramid, levels)

DoGPyramid = zeros([size(GaussianPyramid,1),size(GaussianPyramid,2),length(levels-1)]);
DoGPyramid = diff(GaussianPyramid,1,3);
DoGLevels = levels(2:length(levels));