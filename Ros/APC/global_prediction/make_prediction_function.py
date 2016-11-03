#!/usr/bin/env python

import random
import csv
import numpy as np
import sys
import pdb
import copy

class GlobalPrediction():

    def __init__(self):
        self.total_accuracy = 0

        #orig_stdout = sys.stdout
        #f = file('prediction_output_function.txt', 'w')
        #sys.stdout = f
        
        self.confusion_matrix = np.zeros([38,38])
        self.item_count = np.zeros([38,1])
        
        print "Hello"
        
        for nitr in range(0,10):
            #1 take in 12 predition items
            print "--------------------------" + str(nitr + 1) + '-----------------------------'
            self.all_items = [x for x in range(1,39)]
            self.item_list = []
            self.prediction(self,12)
            
            print "item_list"
            print self.actual_item_list
            print "prediction:"
            print self.prediction
            correct = [0] * self.total_predictions
            for i in range(0,self.total_predictions):
                self.confusion_matrix[self.actual_item_list[i]-1][self.prediction[i]-1] += 1
                if(self.actual_item_list[i] - self.prediction[i] == 0):
                    correct[i] = 1
                else:
                    correct[i] = 0
            print "correct"
            print correct
            print "accuracy is : " + str(sum(correct)/(self.total_predictions*1.0)*100.0)
            self.total_accuracy = self.total_accuracy + sum(correct)/(self.total_predictions*1.0)*100.0
        
        print "Total accuracy for " + str(nitr + 1) + ' iterations is: ' + str(self.total_accuracy/(nitr+1))
        
        print "Individual Item Count: "
        print self.item_count
        
        #sys.stdout = orig_stdout
        #f.close()
        np.set_printoptions(precision=1, suppress=True,linewidth=400)
        #writer = csv.writer(open("confusion_matrix_function.txt", 'w'))
        #for i in range(0,38):
        #    print i
        #    writer.writerow(self.confusion_matrix[i])
            
    def prediction(self,numel):
            for i in range(0,numel):
                rand = random.choice(self.all_items)
                self.item_list.append(rand)
                self.all_items.remove(rand)
                self.item_count[rand-1] += 1
                
                #2 open processed table for each items
                self.cnn_processed_avg = dict()
                self.cnn_processed_med = dict()
                self.cnn_processed_std = dict()
                
                for x, item in enumerate(self.item_list):
                    lookup_value = 3*(item-1) + random.choice([0,1,2])
                    lookup_string = './predictions/raw-' + str(lookup_value) + '.out'
                    self.pred_mat = []
                    print 'opening file: ' + lookup_string + "   for item number: " + str(item)
                    with open(lookup_string, 'r') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        num_rows = 0
                        for row in reader:
                            self.pred_mat.append([float(s) for s in row])
                            num_rows += 1
                    self.pred_mat = zip(*self.pred_mat)
                    
                    if(num_rows > 1):
                        dimension = len(self.pred_mat[1])
                    else:
                        dimension = 38
                    self.avg_list = [0]*dimension
                    self.med_list = [0]*dimension
                    self.std_list = [0]*dimension
                    for i in range(0, dimension): # by item
                        temp_list = []
                        for j in range(0,len(self.pred_mat)): # down superpixel column
                            temp_list.append (self.pred_mat[j][i])
                        avg = np.mean(temp_list)
                        med = np.median(temp_list)
                        std = np.std(temp_list)
                        #print avg, med, std
            
                        self.avg_list[i] = avg
                        self.med_list[i] = med
                        self.std_list[i] = std
            
                    self.cnn_processed_avg[item] = self.avg_list
                    self.cnn_processed_med[item] = self.med_list
                    self.cnn_processed_std[item] = self.std_list
                
                partial_avg_list = np.zeros([numel,numel])
                self.item_list_copy = copy.copy(self.item_list)
                for i in range(0,numel):
                    self.full_avg_list = self.cnn_processed_avg[self.item_list[i]]
                    for j, item in enumerate(self.item_list_copy):
                        average_value = self.full_avg_list[item-1]
                        partial_avg_list[i][j] = average_value

                maxi = partial_avg_list.argmax()
                partial_avg_list[maxi%numel][maxi/numel]
            
                #3 make prediction based on max average value
                self.total_predictions = numel
                self.prediction = [0] * self.total_predictions
                self.actual_item_list = [0] * self.total_predictions
                for i in range(0,self.total_predictions):
                    maxi = partial_avg_list.argmax()
                    row = maxi/numel
                    col = maxi%numel
                    #print "maxi, max, row, col:   " + str(maxi) +",   "+ str(partial_avg_list[row][col]) + ",   " + str(row) + ",   " + str(col)
                    #prediction[row] = item_list_copy[col]
                    self.prediction[i] = self.item_list_copy[col]
                    self.actual_item_list[i] = self.item_list[row]
                    partial_avg_list[row][:] = 0
                    for k in range(0,numel):
                        partial_avg_list[k][col] = 0