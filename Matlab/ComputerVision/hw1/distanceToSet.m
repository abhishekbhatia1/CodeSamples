function [histInter] = distanceToSet(wordHist, histograms)

histo = bsxfun(@min,wordHist,histograms);
histInter = sum(histo);