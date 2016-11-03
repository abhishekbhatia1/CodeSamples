# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 13:15:48 2015

@author: harp
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 12:58:29 2015

@author: harp
"""
import time
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
file_loc = '/home/apark/Homework/ML_Project1/data/'
from sklearn.cross_validation import KFold
from sklearn import svm
from sklearn.feature_selection import SelectKBest
from sklearn.decomposition import PCA
import matplotlib.cm as cm

start = time.time()
print 'start time :',(start)
# Import test data and labels
#import_test = sio.loadmat(file_loc + 'Test.mat')
import_train = sio.loadmat(file_loc + 'Train.mat')

X = import_train['Xtrain']
pca = PCA(n_components=2)
pca.fit(X)
print(pca.explained_variance_ratio_) 
X = pca.transform(X)
#X = X[:, :2]
Y = import_train['Ytrain']
'''
eventsTrain = import_train['eventsTrain']
subjectsTrain = import_train['subjectsTrain']
x = import_train['x']
y = import_train['y']
z = import_train['z']
'''

y = Y.ravel()

h = .02  # step size in the mesh

# we create an instance of SVM and fit out data. We do not scale our
# data since we want to plot the support vectors
C = 1.0  # SVM regularization parameter
#svc = svm.SVC(kernel='linear', C=C).fit(X, y)
t = time.time()
print('calculating the rbf SVM classifier')
rbf_svc = svm.SVC(kernel='rbf', gamma=0.00005, C=50).fit(X, y)
print 'training the classifier took: ', (time.time() - t)
t =time.time()
#poly_svc = svm.SVC(kernel='poly', degree=3, C=C).fit(X, y)
print('calculating the linear SVM classifier')
lin_svc = svm.LinearSVC(C=C).fit(X, y)
print 'training the classifier took: ', (time.time() - t)

# create a mesh to plot in
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

# title for the plots
titles = ['SVC with RBF kernel',
          'LinearSVC (linear kernel)']
#          'SVC with RBF kernel',
#          'SVC with polynomial (degree 3) kernel']

print('plotting the outcomes')
for i, clf in enumerate((rbf_svc,lin_svc)):
    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, m_max]x[y_min, y_max].
    plt.subplot(2, 2, i + 1)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired)
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())
    plt.title(titles[i])
print "elapsed time"
print(time.time() - start)
plt.show()
