function [filterBank,dictionary] = getFilterBankAndDictionary(train_imagenames)

alpha = 150;
k_words = 300;
count = 1;
for i = 1:length(train_imagenames)
%for i = 1:2
        I = imread(train_imagenames{i});
        if (length(size(I)) == 2)
            I = repmat(I,[1 1 3]);
        end
%         if (size(I,1) >= alpha && size(I,2) >= alpha)
%             rp_r = randperm(size(I,1),alpha);
%             rp_c = randperm(size(I,2),alpha);
%             size_min = alpha;
%         else
%             if (size(I,1) < size(I,2))
%                 size_min = size(I,1);
%             else
%                 size_min = size(I,2);
%             end
%             rp_r = randperm(size_min,size_min);
%             rp_c = randperm(size_min,size_min);
%         end
%         for j = 1:size_min
%             I_new(j,1,:) = I(rp_r(j),rp_c(j),:);
%         end
        filterBank = createFilterBank();
        %filterResponses = zeros(size(doubleI,1), size(doubleI,2), length(filterBank)*3);
        %kmeans_input = zeros(150*length(train_imagenames),60);
        %filterResponses{i} = extractFilterResponses(I_new, filterBank);
        filterResponses = extractFilterResponses(I, filterBank);
        if (size(I,1) >= alpha && size(I,2) >= alpha)
            rp_r = randperm(size(I,1),alpha);
            rp_c = randperm(size(I,2),alpha);
            size_min = alpha;
        else
            if (size(I,1) < size(I,2))
                size_min = size(I,1);
            else
                size_min = size(I,2);
            end
            rp_r = randperm(size_min,size_min);
            rp_c = randperm(size_min,size_min);
        end
        I_new = zeros(size_min,1,60);
        for j = 1:size_min
            I_new(j,1,:) = filterResponses(rp_r(j),rp_c(j),:);
        end
        %for j = 1:size_min
            %kmeans_input(count,:) = filterResponses{i}(j,1,:);
            %if (i == 1)
                %kmeans_input(count:count+size(filterResponses{i},1)-1,:) = filterResponses{i}(:,1,:);
                kmeans_input(count:count+size_min-1,:) = I_new(:,1,:);
            %else
            %    kmeans_input = [kmeans_input,filterResponses{i}(:,1,:)];
            %end
            %count = count + size(filterResponses{i},1);
            count = count + size_min;
            size_min;
            count;
        %end
        %kmeans_input = [kmeans_input,filterResponses{i}];
end
[~,dictionary] = kmeans(kmeans_input,k_words,'EmptyAction','drop');
count
size(kmeans_input)
size(dictionary)
dictionary = dictionary';