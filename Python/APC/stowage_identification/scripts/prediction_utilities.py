import random
import csv
import numpy as np
import sys
import IPython
ordered_belief_list = np.zeros([12,1])


def stowage_local_prediction(unordered_item_list, prediction, num):
    n_items,n_superpixels = prediction.shape
    print n_superpixels
    full_avg_list = np.zeros([n_items,1])
    for i in range(0,n_items):
        #print str(i)
        total = 0
        for j in range(0,n_superpixels):
            total += prediction[i][j]
        full_avg_list[i] = float(total) / float(n_superpixels)
    #print "full avg list: -----------------"
    #print full_avg_list
    # remove items not in the 12 item list
    partial_avg_list = np.zeros([12,1])
    for i, item in enumerate(unordered_item_list):
        partial_avg_list[i] = full_avg_list[item - 1]

    # renormalize probability
    partial_avg_list = partial_avg_list/sum(partial_avg_list)
    
    print "\n-----Normalized partial_avg_list------"
    print partial_avg_list

    maxi = partial_avg_list.argmax()
    local_prediction = partial_avg_list[maxi]
    ordered_belief_list[num] = unordered_item_list[maxi]
    return unordered_item_list[maxi], local_prediction


def stowage_global_prediction(unordered_item_list, prediction_dict,  ground_truth=[]):
    
    if ground_truth: # Nice to have, likely will not implement
        doGroundTruth = True
    else:
        doGroundTruth = False

    #if len(unordered_item_list != 12):
    #    print "item list needs to contain 12 elements"
    #    return []
    confusion_matrix = np.zeros([38,38])
    item_count = np.zeros([38,1])


    #1 take in 12 predition items
    #item_list = [1,2,3,4,5,6,7,8,9,10,11,12]
    item_list = unordered_item_list
    #2 open processed table for each items
    cnn_processed_avg = dict()
    cnn_processed_med = dict()
    cnn_processed_std = dict()
    n_dictionary = 38
    n_items = len(unordered_item_list)
    n_images = len(prediction_dict)
    #rint 'n_items', n_items, 'n_images', n_images
    avg_list = [0]*n_dictionary
    med_list = [0]*n_dictionary
    std_list = [0]*n_dictionary
    for x in range(0,n_images):
        #print 'l67 x', x
        prediction = prediction_dict[x]
        n_dictionary, n_superpixels = prediction.shape
        #print n_dictionary, n_superpixels, "dict sps"
        for i in range(0,n_items):
            #print str(i)
            temp_list = []
            for j in range(0,n_superpixels):
                temp_list.append (prediction[i][j])
            avg = np.mean(temp_list)
            med = np.median(temp_list)
            std = np.std(temp_list)
            print avg, med, std, i
            avg_list[i] = avg
            med_list[i] = med
            std_list[i] = std

        cnn_processed_avg[x] = avg_list
        cnn_processed_med[x] = med_list
        cnn_processed_std[x] = std_list

        # END TODO

    partial_avg_list = np.zeros([n_images,n_items])
    item_list_copy = item_list
    for i in range(0,n_images):
        full_avg_list = cnn_processed_avg[i]
        for j, item in enumerate(item_list_copy):
            average_value = full_avg_list[item-1]
            partial_avg_list[i][j] = average_value
        partial_avg_list[i][:] = partial_avg_list[i][:]/sum(partial_avg_list[i][:])
            #print partial_avg_list.shape
            #max_index = ma
        #print partial_avg_list

    maxi = partial_avg_list.argmax()
    partial_avg_list[maxi%n_images][maxi/n_items]

    #3 make prediction based on max average value
    prediction = [0] * n_images
    for i in range(0,n_images):
        maxi = partial_avg_list.argmax()
        row = maxi/n_items
        col = maxi%n_items
        #print "maxi, max, row, col:   " + str(maxi) +",   "+ str(partial_avg_list[row][col]) + ",   " + str(row) + ",   " + str(col)
        prediction[row] = item_list_copy[col]
        partial_avg_list[row][:] = 0
        for k in range(0,n_images):
            partial_avg_list[k][col] = 0

        #print partial_avg_list
        for j in range(0,n_images):
            thissum = sum(partial_avg_list[j][:])
            if(thissum != 0):
                partial_avg_list[j][:] = partial_avg_list[j][:]/thissum

    return prediction

    print "prediction:"
    print prediction
    if doGroundTruth:
        correct = [0] *n_items
        for i in range(0,items):
            confusion_matrix[item_list[i]-1][prediction[i]-1] += 1
            if(item_list[i] - prediction[i] == 0):
                correct[i] = 1
            else:
                correct[i] = 0
        print "correct"
        print correct
        print "accuracy is : " + str(sum(correct)/n_items*100.0)