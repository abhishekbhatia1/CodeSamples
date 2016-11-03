function [u, v] = LucasKanadeICA(It, It1, rect)
It = im2double(It);
It1 = im2double(It1);
x_begin = rect(1);
x_end = rect(3);
y_begin = rect(2);
y_end = rect(4);
width = x_end - x_begin + 1;
height = y_end - y_begin + 1;
threshold = 0.005;
p = [0;0];
del_p = [100;100];
del_Wp = [1 0; 0 1];
[X,Y] = meshgrid(x_begin:x_end,y_begin:y_end);
WIt = interp2(It,X,Y);
[del_Tx,del_Ty] = imgradientxy(WIt);
del_Tx_rs = del_Tx(:);
del_Ty_rs = del_Ty(:);
del_T = horzcat(del_Tx_rs,del_Ty_rs);
sdi = del_T*del_Wp;
Hes = sdi'*sdi;
while (abs(del_p(1)) > threshold || abs(del_p(2)) > threshold)
    WIt1 = interp2(It1,X+p(1),Y+p(2));
    error = WIt1 - WIt;
    error_rs = error(:);
    del_p = inv(Hes)*sdi'*error_rs;
    p = p - del_p;
end
u = p(1);
v = p(2);
end 