function M = LucasKanadeAffine(It, It1)
It = im2double(It);
It1 = im2double(It1);
x_begin = 1;
x_end = size(It,2);
y_begin = 1;
y_end = size(It,1);
width = x_end - x_begin + 1;
height = y_end - y_begin + 1;
threshold = 0.005;
p = [0;0;0;0;0;0];
del_p = [100;100;100;100;100;100];
[X,Y] = meshgrid(x_begin:x_end,y_begin:y_end);
M = [1+p(1) p(2) p(3); p(4) 1+p(5) p(6)];
TF = affine2d(M');
WIt = imwarp(It,TF);
[del_Tx,del_Ty] = imgradientxy(WIt);
del_Tx_rs = del_Tx(:);
del_Ty_rs = del_Ty(:);
X_rs = X(:);
Y_rs = Y(:);
sdi = [del_Tx_rs.*X_rs del_Tx_rs.*Y_rs del_Tx_rs del_Ty_rs.*X_rs del_Ty_rs.*Y_rs del_Ty_rs];
Hes = sdi'*sdi;
while (abs(del_p) > threshold)
    WIt1 = imwarp(It1,TF);
    error = WIt1 - WIt;
    error_rs = error(:);
    del_p = inv(Hes)*sdi'*error_rs;
    p = p + del_p;
    M = [1+p(1) p(2) p(3); p(4) 1+p(5) p(6)];
    TF = affine2d(M');
end
end