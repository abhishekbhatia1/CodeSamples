% Problem 1: Image Alignment

%% 1. Load images (all 3 channels)
red = load('red.mat');
green = load('green.mat');
blue = load('blue.mat');
a = red.red;
n_a = norm(double(a));
b = green.green;
n_b = norm(double(b));
c = blue.blue;
n_c = norm(double(c));
% Red channel as 'red'
% Green channel as 'green'
% Blue channel as 'blue'

%% 2. Find best alignment
% Hint: Lookup the 'circshift' function
max_a = inf;
max_c = inf;
for i = -30:30
    for j = -30:30
        a_dis = circshift(a,[i,j]);
        %SSD
        s = sumsqr(b - a_dis);
        %NCC
        %s = normxcorr2(a_dis(:,:),b(:,:));
        %s = dot(double(b/n_b), double(a_dis/n_a),1);
        %s = sum(s);
        if (s < max_a)
            max_a = s;
            i_a = i;
            j_a = j;
        end
    end
end

for i = -30:30
    for j = -30:30
        c_dis = circshift(c,[i,j]);
        %SSD
        s = sumsqr(b - c_dis);
        %NCC
        %s = normxcorr2(c_dis(:,:),b(:,:));
        %s = dot(double(b/n_b), double(c_dis/n_c),1);
        %s = sum(s);
        if (s < max_c)
            max_c = s;
            i_c = i;
            j_c = j;
        end
    end
end

a = circshift(a,[i_a,j_a]);
c = circshift(c,[i_c,j_c]);

rgbResult = alignChannels(a, b, c);

%% 3. Save result to rgb_output.jpg (IN THE "results" folder)
