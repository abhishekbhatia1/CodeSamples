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
from mpl_toolkits.mplot3d import Axes3D
from sklearn import preprocessing

# Import test data and labels
import_test = sio.loadmat(file_loc + 'data/Test.mat')
import_train = sio.loadmat(file_loc + 'data/Train.mat')


Ytrain = import_train['Ytrain']
eventsTrain = import_train['eventsTrain']
subjectsTrain = import_train['subjectsTrain']
x = import_train['x']
y = import_train['y']
z = import_train['z']

Xtrain = import_train['Xtrain']

scaler = preprocessing.StandardScaler().fit(Xtrain)
Xtrain = scaler.transform(Xtrain)


'''
Xtrain = np.zeros((501,5904))
Xtrain[:,0:5903] = import_train['Xtrain']
Xtrain[:,5903:5904] = import_train['eventsTrain']/1000.0
'''


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

index_0 = np.where(Ytrain==0)[0]
index_1 = np.where(Ytrain==1)[0]
index_3 = np.where(Ytrain==3)[0]
index_n0 = np.concatenate((index_1, index_3))
index_n1 = np.concatenate((index_0, index_3))
index_n3 = np.concatenate((index_1, index_0))


# Brain plots
voxel_global_avg = np.zeros((5903,3))
voxel_avg = np.zeros((5903,3))
color_val = ['r','g','b']
vals = [0,1,3]



# get averages for each voxel
for j in range(0,3):
    for i in range(0,5903):
        voxel_global_avg[i,0] = Xtrain[index_n0,i].mean()
        voxel_global_avg[i,1] = Xtrain[index_n1,i].mean()
        voxel_global_avg[i,2] = Xtrain[index_n3,i].mean()
        
# get averages of ech voxel by label
for j in range(0,3):
    print j
    index = np.where(Ytrain==vals[j])[0]
    print index
    for i in range(0,5903):
        voxel_avg[i,j] = Xtrain[index,i].mean()
      
thresh = [.03,.12,.6]
voxel_diff = voxel_avg - voxel_global_avg
significant_voxels = np.zeros((5903,3))

for j in range(0,3):
    for i in range(0,5903):
        if(voxel_diff[i,j] > thresh[j]):
            significant_voxels[i,j] = 1
            
print significant_voxels
'''
fig = plt.figure()
plt.hold('on')

ax = fig.add_subplot(221,projection='3d')
ax.scatter(x,y,z)
plt.title('all voxels')

subplot_val=[222,223,224]
titles = ['class 0 +', 'class 1 +', 'class 3 +']
# see if mean for label exceed threshold then plot
for j in range(0,3):
    ax = fig.add_subplot(subplot_val[j],projection='3d')
    plt.title(titles[j])
    for i in range(0,5903):
        if( voxel_diff[i,j] > thresh[j]):
            ax.scatter(x[i],y[i],z[i],c=color_val[j])


fig = plt.figure()
plt.hold('on')
ax = fig.add_subplot(111,projection='3d')
plt.title('positive activation')

for j in range(0,3):
    for i in range(0,5903):
        if( voxel_diff[i,j] > thresh[j]):
            ax.scatter(x[i],y[i],z[i],c=color_val[j])



class0_diff = voxel_diff[:,0]
class1_diff = voxel_diff[:,1]
class3_diff = voxel_diff[:,2]
np.sort(class0_diff)
np.sort(class1_diff)
np.sort(class3_diff)
print 'class 0 highest diffs 10 voxels', class0_diff[1:10]
print 'class 1 highest diffs 10 voxels', class1_diff[1:10]
print 'class 3 highest diffs 10 voxels', class3_diff[1:10]

'''
# now look at low activations

fig = plt.figure()
plt.hold('on')

ax = fig.add_subplot(221,projection='3d')
ax.scatter(x,y,z)
plt.title('all voxels')

neg_thresh = [-.65, -.3, 0]

subplot_val=[222,223,224]
titles = ['class 0 -', 'class 1 -', 'class 3 -']
# see if mean for label exceed threshold then plot
for j in range(0,3):
    ax = fig.add_subplot(subplot_val[j],projection='3d')
    plt.title(titles[j])
    for i in range(0,5903):
        if( voxel_diff[i,j] < neg_thresh[j]):
            ax.scatter(x[i],y[i],z[i],c=color_val[j])


fig = plt.figure()
plt.hold('on')
ax = fig.add_subplot(111,projection='3d')
plt.title('negative activation')

for j in range(0,3):
    for i in range(0,5903):
        if( voxel_diff[i,j] < neg_thresh[j]):
            ax.scatter(x[i],y[i],z[i],c=color_val[j])


plt.show()

'''
# try another visualization
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
for i in range(0,5903):
    max_val = voxel_avg[i,:].max()
    if( voxel_avg[i,0] == max_val):
        ax.scatter(x[i],y[i],z[i],c=color_val[0])
    elif( voxel_avg[i,1] == max_val):
        ax.scatter(x[i],y[i],z[i],c=color_val[1])
    elif( voxel_avg[i,2] == max_val):
        ax.scatter(x[i],y[i],z[i],c=color_val[2])
plt.show()
'''