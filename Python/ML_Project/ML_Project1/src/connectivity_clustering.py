# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 23:37:10 2015

@author: apark
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
from sklearn import cluster
from sklearn.cross_validation import KFold
from sklearn import svm
from sklearn.feature_selection import SelectKBest
from sklearn.decomposition import PCA
from sklearn import cross_validation
from sklearn.cross_validation import StratifiedKFold
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import Pipeline, FeatureUnion
import matplotlib.cm as cm
from sklearn.cluster import MiniBatchKMeans

# Import test data and labels
import_test = sio.loadmat(file_loc + 'data/Test.mat')
import_train = sio.loadmat(file_loc + 'data/Train.mat')
Ytrain = import_train['Ytrain']
eventsTrain = import_train['eventsTrain']
subjectsTrain = import_train['subjectsTrain']
X_testing = import_test['Xtest']
x = import_train['x']
y = import_train['y']
z = import_train['z']
xyz = np.zeros((5903,3))
xyz[:,0] = x[:,0]
xyz[:,1] = y[:,0]
xyz[:,2] = z[:,0]

Xtrain = import_train['Xtrain']
scaler = preprocessing.StandardScaler().fit(Xtrain)
Xtrain = scaler.transform(Xtrain)


from sklearn.neighbors import kneighbors_graph, BallTree
from sklearn.feature_extraction.image import grid_to_graph
xyz_balltree = BallTree(xyz)
print xyz_balltree
print xyz_balltree.query_radius(xyz[0], r = .04)



#connectivity = kneighbors_graph(xyz_balltree, 2, include_self=True,mode='connectivity')
#connectivity = grid_to_graph(n_x =x, n_y = y, n_z = z )
#agglo = cluster.FeatureAgglomeration(n_clusters = 590)
#agglo.fit(Xtrain)
#Xtrain_reduced = agglo.transform(Xtrain)


'''

#k_fold = cross_validation.KFold(len(X_train), 5)
Y_kf = Ytrain.ravel()
k_fold = StratifiedKFold(Y_kf, n_folds=10)

for train, test in k_fold:
    X = Xtrain[train]
    Y = Ytrain[train]
    X_test = Xtrain[test]
    Y_test = Ytrain[test]    
    y = Y.ravel()

    n_clusters = 5


    kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=1)
    kmeans.fit(X,Y)
    z = kmeans.score(X_test, Y_test)
    print 'kmeans accuracy', z  

kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=1)
kmeans.fit(Xtrain,Ytrain)
Y_test = kmeans.predict(X_testing)
Y_testing = np.zeros((len(Y_test),3))
for i in range (0,len(Y_test)):
    if (Y_test[i] == 0):
        Y_testing[i,0] = 1
    elif(Y_test[i] == 1):
        Y_testing[i,1] = 1
    elif(Y_test[i] == 3):
        Y_testing[i,2] = 1
        
#print(Y_testing)

np.savetxt('prediction.csv', Y_testing, fmt='%.1d',delimiter=',')

'''