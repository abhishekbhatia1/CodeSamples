import random
import csv
import numpy as np
import sys
import pdb

total_accuracy = 0

orig_stdout = sys.stdout
f = file('prediction_output.txt', 'w')
sys.stdout = f

confusion_matrix = np.zeros([38,38])
item_count = np.zeros([38,1])

for nitr in range(0,10000):

    #1 take in 12 predition items
    print "--------------------------" + str(nitr + 1) + '-----------------------------'
    all_items = [x for x in range(1,39)]
    item_list = []
    for i in range(0,12):
        rand = random.choice(all_items)
        item_list.append(rand)
        all_items.remove(rand)
        item_count[rand-1] += 1
    #print item_list
    #item_list = [1,2,3,4,5,6,7,8,9,10,11,12]

    #2 open processed table for each items
    cnn_processed_avg = dict()
    cnn_processed_med = dict()
    cnn_processed_std = dict()

    for x, item in enumerate(item_list):
        lookup_value = 3*(item-1) + random.choice([0,1,2])
        lookup_string = './predictions/raw-' + str(lookup_value) + '.out'
        #print lookup_string
        #lookup_string = './predictions/image-' + str(lookup_value) + 'out'
        #lookup_string = 'image-1processed'
        pred_mat = []
        print 'opening file: ' + lookup_string + "   for item number: " + str(item)
        with open(lookup_string, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            num_rows = 0
            for row in reader:
                pred_mat.append([float(s) for s in row])
                num_rows += 1
        pred_mat = zip(*pred_mat)
        #print pred_mat
        #pred_mat = np.transpose(pred_mat)
        if(num_rows > 1):
            dimension = len(pred_mat[1])
        else:
            dimension = 38
        avg_list = [0]*dimension
        med_list = [0]*dimension
        std_list = [0]*dimension
        for i in range(0, dimension): # by item
            temp_list = []
            for j in range(0,len(pred_mat)): # down superpixel column
                temp_list.append (pred_mat[j][i])
            avg = np.mean(temp_list)
            med = np.median(temp_list)
            std = np.std(temp_list)
            #print avg, med, std

            avg_list[i] = avg
            med_list[i] = med
            std_list[i] = std

        cnn_processed_avg[item] = avg_list
        cnn_processed_med[item] = med_list
        cnn_processed_std[item] = std_list

    partial_avg_list = np.zeros([12,12])
    item_list_copy = item_list
    for i in range(0,12):
        full_avg_list = cnn_processed_avg[item_list[i]]
        for j, item in enumerate(item_list_copy):
            average_value = full_avg_list[item-1]
            partial_avg_list[i][j] = average_value
        partial_avg_list[i][:] = partial_avg_list[i][:]/sum(partial_avg_list[i][:])
        #print partial_avg_list.shape
        #max_index = ma
    #print partial_avg_list

    maxi = partial_avg_list.argmax()
    partial_avg_list[maxi%12][maxi/12]

    #3 make prediction based on max average value
    prediction = [0] * 12
    for i in range(0,12):
        maxi = partial_avg_list.argmax()
        row = maxi/12
        col = maxi%12
        #print "maxi, max, row, col:   " + str(maxi) +",   "+ str(partial_avg_list[row][col]) + ",   " + str(row) + ",   " + str(col)
        prediction[row] = item_list_copy[col]
        partial_avg_list[row][:] = 0
        for k in range(0,12):
            partial_avg_list[k][col] = 0

        #print partial_avg_list
        for j in range(0,12):
            thissum = sum(partial_avg_list[j][:])
            if(thissum != 0):
                partial_avg_list[j][:] = partial_avg_list[j][:]/thissum

    print "item_list"
    print item_list
    print "prediction:"
    print prediction
    correct = [0] *12
    for i in range(0,12):
    	confusion_matrix[item_list[i]-1][prediction[i]-1] += 1
        if(item_list[i] - prediction[i] == 0):
            correct[i] = 1
        else:
            correct[i] = 0
    print "correct"
    print correct
    print "accuracy is : " + str(sum(correct)/12.0*100.0)
    total_accuracy = total_accuracy + sum(correct)/12.0*100.0

print "Total accuracy for " + str(nitr + 1) + ' iterations is: ' + str(total_accuracy/nitr)

print "Individual Item Count: "
print item_count

sys.stdout = orig_stdout
f.close()
np.set_printoptions(precision=1, suppress=True,linewidth=400)
writer = csv.writer(open("confusion_matrix.txt", 'w'))
for i in range(0,38):
	print i
	writer.writerow(confusion_matrix[i])
	#writer.writerow(' ')