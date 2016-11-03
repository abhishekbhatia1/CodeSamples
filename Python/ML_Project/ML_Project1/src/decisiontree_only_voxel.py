# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 16:52:05 2015

@author: harp
"""

import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
file_loc = '/home/apark/Homework/ML_Project1/data/'
from sklearn.cross_validation import KFold
from sklearn import svm
from sklearn.feature_selection import SelectKBest
from sklearn.decomposition import PCA, KernelPCA
from sklearn import cross_validation
from sklearn.cross_validation import StratifiedKFold
from sklearn import tree
import matplotlib.cm as cm

# Import test data and labels
import_test = sio.loadmat(file_loc + 'Test.mat')
import_train = sio.loadmat(file_loc + 'Train.mat')

Y_train = import_train['Ytrain']
X_train = import_train['Xtrain']
X_test = import_test['Xtest']

#Standardization
from sklearn import preprocessing
scaler = preprocessing.StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


Y_kf = Y_train.ravel()
k_fold = StratifiedKFold(Y_kf, n_folds=5)
print(k_fold)

for train, test in k_fold:
    X = X_train[train]
    Y = Y_train[train]
    X_test = X_train[test]
    Y_test = Y_train[test]    
    y = Y.ravel()
    
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X,y)

    z = clf.score(X_test, Y_test)

    print"decision tree accuracy",z
    
    
# create final classifier for test data
clf = clf.fit(X_train,Y_train)
Y_test = clf.predict(X_test)

Y_testing = np.zeros((len(Y_test),3))
for i in range (0,len(Y_test)):
    if (Y_test[i] == 0):
        Y_testing[i,0] = 1
    elif(Y_test[i] == 1):
        Y_testing[i,1] = 1
    elif(Y_test[i] == 3):
        Y_testing[i,2] = 1
        
np.savetxt('prediction.csv',Y_testing,fmt='%.2d',delimiter=',')
print 'printed prediction.csv to file'

                
