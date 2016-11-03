# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 09:29:12 2015

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
# Import test data and labels
import_test = sio.loadmat(file_loc + 'data/Test.mat')
import_train = sio.loadmat(file_loc + 'data/Train.mat')

Xtrain = import_train['Xtrain']
Ytrain = import_train['Ytrain']
eventsTrain = import_train['eventsTrain']
subjectsTrain = import_train['subjectsTrain']
x = import_train['x']
y = import_train['y']
z = import_train['z']



# PCA
'''
from sklearn.decomposition import PCA
pca = PCA(n_components = 10)
pca.fit(Xtrain)
print(pca.explained_variance_ratio_)
Xtrain_pca = pca.transform(Xtrain)
print( " Xtrain_pca share: ", Xtrain_pca.shape)
'''
from sklearn.decomposition import KernelPCA
kpca = KernelPCA(kernel="rbf", degree=5, gamma=10)
Xtrain_pca = kpca.fit_transform(Xtrain)
print( " Xtrain Kernel PCA share: ", Xtrain_pca.shape)


# plot principal components
index_0 = np.where(Ytrain==0)[0]
index_1 = np.where(Ytrain==1)[0]
index_3 = np.where(Ytrain==3)[0]

plt.figure()
plt.hold('on')
plt.scatter(Xtrain_pca[index_0,:1],Xtrain_pca[index_0,1:2], color="r")
plt.scatter(Xtrain_pca[index_1,:1],Xtrain_pca[index_1,1:2], color="g")
plt.scatter(Xtrain_pca[index_3,:1],Xtrain_pca[index_3,1:2], color="b")
plt.legend(("0", "1","3"))
plt.title("PCA of 2 largest components")


# plot PCA per subject by label
plt.figure()
for i in range(min(subjectsTrain),max(subjectsTrain)):
    p_index_0 = [];
    p_index_1 = [];
    p_index_3 = [];
    for j in range(0,len(Ytrain)):
        if(subjectsTrain[j] == i):
            if( Ytrain[j] == 0):
                p_index_0.append(j)
            elif(Ytrain[j] == 1):
                p_index_1.append(j)
            elif(Ytrain[j] == 3):
                p_index_3.append(j)
                
    plt.subplot(5,6,i)
    plt.title("subject number: " + str(i))
    
    plt.scatter(Xtrain_pca[p_index_0,:1],Xtrain_pca[p_index_0,1:2], color="r")
    plt.scatter(Xtrain_pca[p_index_1,:1],Xtrain_pca[p_index_1,1:2], color="g")
    plt.scatter(Xtrain_pca[p_index_3,:1],Xtrain_pca[p_index_3,1:2], color="b")
    

# plot PCA per subject by time
plt.figure()
for i in range(min(subjectsTrain),max(subjectsTrain)):
    p_index_0 = [];
    p_index_1 = [];
    p_index_3 = [];
    for j in range(0,len(Ytrain)):
        if(subjectsTrain[j] == i):
            if( Ytrain[j] == 0):
                p_index_0.append(j)
            elif(Ytrain[j] == 1):
                p_index_1.append(j)
            elif(Ytrain[j] == 3):
                p_index_3.append(j)
    #print eventsTrain[p_index_0,:]
    #print max(eventsTrain)
    #print eventsTrain[p_index_0,:]/float(max(eventsTrain))
    color_array_0 = eventsTrain[p_index_0]/float(max(eventsTrain))
    color_array_1 = eventsTrain[p_index_1]/float(max(eventsTrain))
    color_array_3 = eventsTrain[p_index_3]/float(max(eventsTrain))
    plt.subplot(5,6,i)
    plt.title("subject number: " + str(i))
    plt.gray()
    plt.scatter(Xtrain_pca[p_index_0,:1],Xtrain_pca[p_index_0,1:2], c=color_array_0 )
    plt.scatter(Xtrain_pca[p_index_1,:1],Xtrain_pca[p_index_1,1:2], c=color_array_1 )
    plt.scatter(Xtrain_pca[p_index_3,:1],Xtrain_pca[p_index_3,1:2], c=color_array_3 )


plt.show()
    
#plt.plot()

'''
kf = KFold(len(Y),n_folds = 5)
for train_index,test_index in kf:
    #print( "Train: ", train_index, "  Test: ", test_index)
    X_train, X_test = Xtrain_pca[train_index], Xtrain_pca[test_index]
    Y_train, Y_test = Y[train_index], Y[test_index]
    print("X_train shape: ", X_train.shape)
    clf = svm.SVC()
    clf.fit(X_train, Y_train)
    Y_predict = clf.predict(X_test)
    right = 0
    for i in range(0,len(Y_test)):
        if(abs(Y_predict[i] - Y_train[i]) < 1):
            right +=1
            print("correct label")
    performance = float(right)/float(len(Y_train))
    print("performance of : ", performance)

      '''      