#!/usr/bin/env python

import random
import csv
import numpy as np
import sys
import pdb
import copy

def bin_pred(prediction, old_prediction, active_bins, bin_list):    
    if (len(old_prediction) == 0):
        bin_list.append(active_bins[0])
    else:
        flag = 0
        for i in range(0,len(old_prediction)):
            if (abs(old_prediction[i] - prediction[i]) > 0):
                bin_list.append(bin_list[i])
                flag = 1
                break
        if (flag == 0):
            bin_list.append(active_bins[len(prediction)%len(active_bins) - 1])
    
    return bin_list

def pred(numel,full_item_list, pred_mat_combined):
        
    #2 open processed table for each items
    cnn_processed_avg = dict()
    cnn_processed_med = dict()
    cnn_processed_std = dict()
    
    item_list = []
    for i in range(0,numel):
        item = full_item_list[i]
        item_list.append(item)
        pred_mat = pred_mat_combined[item]
        
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

            avg_list[i] = avg
            med_list[i] = med
            std_list[i] = std

        cnn_processed_avg[item] = avg_list
        cnn_processed_med[item] = med_list
        cnn_processed_std[item] = std_list
    
    partial_avg_list = np.zeros([12,12])
    item_list_copy = copy.copy(full_item_list)
    for i in range(0,numel):
        full_avg_list = cnn_processed_avg[full_item_list[i]]
        for j, item in enumerate(item_list_copy):
            average_value = full_avg_list[item-1]
            partial_avg_list[i][j] = average_value

    maxi = partial_avg_list.argmax()
    partial_avg_list[maxi%12][maxi/12]

    #3 make prediction based on max average value
    total_predictions = numel
    prediction = [0] * total_predictions
    actual_item_list = [0] * total_predictions
    for i in range(0,total_predictions):
        maxi = partial_avg_list.argmax()
        row = maxi/12
        col = maxi%12
        #print "maxi, max, row, col:   " + str(maxi) +",   "+ str(partial_avg_list[row][col]) + ",   " + str(row) + ",   " + str(col)
        #prediction[row] = item_list_copy[col]
        #prediction[i] = item_list_copy[col]
        #actual_item_list[i] = item_list[row]
        prediction[row] = item_list_copy[col]
        actual_item_list[row] = item_list[row]
        partial_avg_list[row][:] = 0
        for k in range(0,12):
            partial_avg_list[k][col] = 0
            
    return prediction, actual_item_list, total_predictions

if __name__ == '__main__':
    total_accuracy = 0
    total_bin_accuracy = 0

    orig_stdout = sys.stdout
    f = file('global_prediction_output.txt', 'w')
    sys.stdout = f
    
    confusion_matrix = np.zeros([38,38])
    item_count = np.zeros([38,1])
    num_itr = 1
    numel = 12
    
    for nitr in range(0,num_itr):
        #1 take in 12 predition items
        print "--------------------------" + str(nitr + 1) + '-----------------------------'
        all_items = [x for x in range(1,39)]
        full_item_list = []
        old_prediction = []
        bin_list = []
        active_bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        
        for i in range(0,12):
            rand = random.choice(all_items)
            full_item_list.append(rand)
            all_items.remove(rand)
            item_count[rand-1] += 1
            
        for j in range(1,13):
            numel = j
            item_list = []
            for i in range(0,numel):
                item_list.append(full_item_list[i])
            
            #pred_mat_combined = []
            pred_mat_combined = dict()
            for x, item in enumerate(item_list):
                lookup_value = 3*(item-1) #+ random.choice([0,1,2])
                lookup_string = './predictions/raw-' + str(lookup_value) + '.out'
                pred_mat = []
                #print 'opening file: ' + lookup_string + "   for item number: " + str(item)
                with open(lookup_string, 'r') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    num_rows = 0
                    for row in reader:
                        pred_mat.append([float(s) for s in row])
                        num_rows += 1
                pred_mat = zip(*pred_mat)
                #pred_mat_combined.append(pred_mat)
                pred_mat_combined[item] = pred_mat
                        
            prediction, actual_item_list, total_predictions = pred(numel, full_item_list, pred_mat_combined)
            bin_list = bin_pred(prediction, old_prediction, active_bins, bin_list)
            old_prediction = prediction
            
            if (j == 12):
                print "Full item_list"
                print full_item_list
                #print "item_list"
                #print actual_item_list
                print "prediction:"
                print prediction
                print "Bin List: "
                print bin_list
            correct = [0] * total_predictions
            for i in range(0,total_predictions):
                confusion_matrix[actual_item_list[i]-1][prediction[i]-1] += 1
                if (actual_item_list[i] - prediction[i] == 0):
                    correct[i] = 1
                else:
                    correct[i] = 0
            if (j == 12):
                print "correct"
                print correct
                print "accuracy is : " + str(sum(correct)/(total_predictions*1.0)*100.0)
        
        correct_bin = [0] * total_predictions
        for i in range(0,total_predictions):
            item_num = full_item_list[i]
            bin_actual = bin_list[i]
            item_ind_in_pred = prediction.index(item_num)
            bin_predicted = bin_list[item_ind_in_pred]
            if (bin_actual - bin_predicted == 0):
                correct_bin[i] = 1
            else:
                correct_bin[i] = 0
        print "bin accuracy is : " + str(sum(correct_bin)/(total_predictions*1.0)*100.0)
        total_bin_accuracy = total_bin_accuracy + sum(correct_bin)/(total_predictions*1.0)*100.0
        
        total_accuracy = total_accuracy + sum(correct)/(total_predictions*1.0)*100.0
        
    print "---------------------------------------------------------------------------------------"
    print "Total accuracy for " + str(nitr + 1) + ' iterations is: ' + str(total_accuracy/(nitr+1))
    print "---------------------------------------------------------------------------------------"
    print "Total bin accuracy for " + str(nitr + 1) + ' iterations is: ' + str(total_bin_accuracy/(nitr+1))
    
    
    #print "Individual Item Count: "
    #print item_count
    
    sys.stdout = orig_stdout
    f.close()
    np.set_printoptions(precision=1, suppress=True,linewidth=400)
    writer = csv.writer(open("confusion_matrix_function.txt", 'w'))
    for i in range(0,38):
        writer.writerow(confusion_matrix[i])
