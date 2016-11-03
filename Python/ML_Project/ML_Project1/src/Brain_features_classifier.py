# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 22:40:08 2015

@author: harp
"""

import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
file_loc = '/home/apark/Homework/ML_Project1/'
from sklearn.cross_validation import KFold
from sklearn import svm
from sklearn.feature_selection import SelectKBest
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
from sklearn import preprocessing
from sklearn import tree
from sklearn.cross_validation import StratifiedKFold
from sklearn.naive_bayes import GaussianNB

# Import test data and labels
import_test = sio.loadmat(file_loc + 'data/Test.mat')
import_train = sio.loadmat(file_loc + 'data/Train.mat')
Ytrain = import_train['Ytrain']
eventsTrain = import_train['eventsTrain']
subjectsTrain = import_train['subjectsTrain']
Xtest = import_test['Xtest']
x = import_train['x']
y = import_train['y']
z = import_train['z']

Xtrain = import_train['Xtrain']
scaler = preprocessing.StandardScaler().fit(Xtrain)
Xtrain = scaler.transform(Xtrain)

index_0 = np.where(Ytrain==0)[0]
index_1 = np.where(Ytrain==1)[0]
index_3 = np.where(Ytrain==3)[0]
index_n0 = np.concatenate((index_1, index_3))
index_n1 = np.concatenate((index_0, index_3))
index_n3 = np.concatenate((index_1, index_0))


voxel_global_avg = np.zeros((5903,3))
voxel_avg = np.zeros((5903,3))
# get averages for each voxel
for j in range(0,3):
    for i in range(0,5903):
        voxel_global_avg[i,0] = Xtrain[index_n0,i].mean()
        voxel_global_avg[i,1] = Xtrain[index_n1,i].mean()
        voxel_global_avg[i,2] = Xtrain[index_n3,i].mean()
vals = [0,1,3]
# get averages of ech voxel by label
for j in range(0,3):
    index = np.where(Ytrain==vals[j])[0]
    for i in range(0,5903):
        voxel_avg[i,j] = Xtrain[index,i].mean()
        
# get truth matrix of positive clusters   
pos_thresh = [.62,.32,.62] # [.6,.3,.6] reference values
voxel_diff = abs(voxel_avg - voxel_global_avg)
positive_clusters = np.zeros((5903,3))
negative_clusters = np.zeros((5903,3))
for j in range(0,3):
    for i in range(0,5903):
        if(voxel_diff[i,j] > pos_thresh[j]):
            positive_clusters[i,j] = 1
            
# get truth matrix of negative clusters
neg_thresh = [-.7, -.35, 0] # [-.65, -.3, 0] reference values
for j in range(0,3):
    for i in range(0,5903):
        if( voxel_diff[i,j] < neg_thresh[j]):
            negative_clusters[i,j] = 1

clusters = np.zeros((501,6))
clusters[:,0]= np.dot(Xtrain,positive_clusters[:,0])
clusters[:,1]= np.dot(Xtrain,positive_clusters[:,1])
clusters[:,2]= np.dot(Xtrain,positive_clusters[:,2])
clusters[:,3]= np.dot(Xtrain,negative_clusters[:,0])
clusters[:,4]= np.dot(Xtrain,negative_clusters[:,1])
clusters[:,5]= np.dot(Xtrain,negative_clusters[:,2])

Clusterstrain = clusters

clusters = np.zeros((1001,6))
clusters[:,0]= np.dot(Xtest,positive_clusters[:,0])
clusters[:,1]= np.dot(Xtest,positive_clusters[:,1])
clusters[:,2]= np.dot(Xtest,positive_clusters[:,2])
clusters[:,3]= np.dot(Xtest,negative_clusters[:,0])
clusters[:,4]= np.dot(Xtest,negative_clusters[:,1])
clusters[:,5]= np.dot(Xtest,negative_clusters[:,2])

Clusterstest = clusters
'''
Y_kf = Ytrain.ravel()
k_fold = StratifiedKFold(Y_kf, n_folds=5)
print(k_fold)

for train, test in k_fold:
    X = Xtrain[train]
    Y = Ytrain[train]
    X_test = Xtrain[test]
    Y_test = Ytrain[test]    
    y = Y.ravel()
    
    cX = Clusterstrain[train]
    cY = Ytrain[train]
    cX_test = Clusterstrain[test]
    cY_test = Ytrain[test]
    cy = cY.ravel()
    
    NBclf = GaussianNB().fit(cX,cy)
    DTclf = tree.DecisionTreeClassifier().fit(cX,cy)
    lin_svc = svm.LinearSVC(C=1.0).fit(X, y)
    rbf_svc = svm.SVC(kernel='rbf', gamma=0.0001, C=10, probability=True).fit(X, y)
    
    for i, clf in enumerate((rbf_svc,lin_svc)):
        z = clf.score(X_test, Y_test)
        if clf == rbf_svc :
            print("RBF",z)
        else:
            print("Linear",z)
    for i, clf in enumerate((NBclf, DTclf))  :      
        z = clf.score(cX_test, cY_test)
        if clf == NBclf:
            print"naive bayes accuracy",z
        else:
            print "decision tree accuracy", z
    
'''
# create final classifier for test data
y = Ytrain.ravel()
NBclf = GaussianNB().fit(Clusterstrain,y)
Y_test_0 = NBclf.predict(Clusterstest)

lin_svc = svm.LinearSVC(C=1.0).fit(Xtrain, y)
Y_test_1 = lin_svc.predict(Xtest)

rbf_svc = svm.SVC(kernel='rbf', gamma=0.0001, C=10, probability=True).fit(Xtrain, y)
Y_test_2 = rbf_svc.predict(Xtest)

Y_testing = np.zeros((len(Y_test_0),3))
for i in range (0,len(Y_test_0)):
    if ((Y_test_0[i] == 0 and Y_test_1[i] == 0) or
        (Y_test_1[i] == 0 and Y_test_2[i] == 0) or
        (Y_test_0[i] == 0 and Y_test_2[i] == 0) ):
        Y_testing[i,0] = 1
    elif((Y_test_0[i] == 1 and Y_test_1[i] == 1) or
         (Y_test_1[i] == 1 and Y_test_2[i] == 1) or
         (Y_test_0[i] == 1 and Y_test_2[i] == 1) ):
        Y_testing[i,1] = 1
    elif((Y_test_0[i] == 3 and Y_test_1[i] == 3) or
         (Y_test_1[i] == 3 and Y_test_2[i] == 3) or
         (Y_test_0[i] == 3 and Y_test_2[i] == 3) ):
        Y_testing[i,2] = 1
    else:
        print 'agreement not found'
        Y_testing[i,2] = 1
        
np.savetxt('prediction.csv',Y_testing,fmt='%.2d',delimiter=',')
print 'printed prediction.csv to file'



