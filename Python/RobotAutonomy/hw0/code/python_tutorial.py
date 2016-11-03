#!/usr/bin/env python
import numpy as np
import operator as op

def print_list(l):
    print l

def sort_manual(shops):

    # TODO: Here implement manual sorting using loops

    shops_sorted = []
    for key,value in shops.iteritems():
        shops_sorted.append([key,value])
        
    index = len(shops_sorted)

    for i in range(0, (len(shops_sorted))):
        for j in range(0, (len(shops_sorted))):
            if(shops_sorted[i][1] > shops_sorted[j][1]):
                temp = shops_sorted[i]
                shops_sorted[i] = shops_sorted[j]
                shops_sorted[j] = temp
    print 'Manual sorting result: '
    print shops_sorted

def sort_python(shops):
    
    #TODO: Here implement sorting using python's built in sorting functions
    
    shops_sorted = {}
    shops_sorted = sorted(shops.items(), key=op.itemgetter(1), reverse=True)
        
    print 'Python sorting result: '
    print_list(shops_sorted)

def sort_numpy(shops):
    
    # TODO: Here implement sorting using numpy's built-in sorting function
    
    shops_sorted = []
    sorted_values = np.sort(shops.values())
    
    sorted_values = sorted_values[::-1]
    
    for values in sorted_values:
        for key in shops:
            if (values == shops[key]):
                shops_sorted.append([key,shops[key]])

    print 'Numpy sorting result: '
    print_list(shops_sorted)

def main():

    shops = {}
    shops['21st Street'] = 0.9
    shops['Voluto'] = 0.6
    shops['Coffee Tree'] = 0.45
    shops['Tazza D\' Oro'] = 0.75
    shops['Espresso a Mano'] = 0.95
    shops['Crazy Mocha'] = 0.35
    shops['Commonplace'] = 0.5
    
    print 'Shops dictionary: '
    print_list(shops)
    sort_manual(shops)
    sort_python(shops)
    sort_numpy(shops)
    

if __name__ == "__main__":
    main()
