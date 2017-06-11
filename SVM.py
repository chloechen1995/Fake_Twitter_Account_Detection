#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 19:42:45 2017

@author: Rachel
"""
import os 
os.chdir('/Users/Rachel/Desktop/STA 160')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import GridSearchCV, KFold, train_test_split, learning_curve
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import itertools
#%%
data = pd.read_csv('final_df_sample_2.csv', index_col = 0)
X = np.array(data.iloc[:,:-2])
y = np.array(data['label_model'])
#%%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 5)
#%%
def report(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")
#%%
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="orange" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
#%%---------- Linear SVM ----------
lin_SVC = LinearSVC(dual = False)
param_grid = dict(C=np.logspace(-2,3,6), penalty = ['l1', 'l2'], class_weight = [{'Fake': 3}, {'Fake': 5}, {'Fake': 7}, {'Fake': 9}])
cv = KFold(n_splits=5, random_state = 5)
grid = GridSearchCV(lin_SVC, param_grid=param_grid, cv=cv, n_jobs = 4)
grid.fit(X_train, y_train)
report(grid.cv_results_)
#%%
lin_SVC = LinearSVC(C = 10, dual = False, penalty = 'l1', class_weight = {'Fake': 3})
lin_SVC.fit(X_train, y_train)
predict = lin_SVC.predict(X_test)
accuracy_score(y_test, predict)
#%%
cnf_matrix = confusion_matrix(y_test, predict)
class_names = np.unique(y_test)
plt.figure()
plot_confusion_matrix(cnf_matrix, class_names)
plt.savefig('linear_svc_confm_1.png')

plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                      title='Normalized confusion matrix')
plt.savefig('linear_svc_confm_2.png')
#%%---------- rbf SVM ----------
SVC_rbf = SVC(kernel = 'rbf')
C_range = np.logspace(-2,3,6)
gamma_range = np.logspace(-3, 2, 6)
class_weight = [{'Fake': 3}, {'Fake': 5}, {'Fake': 7}, {'Fake': 9}]
param_grid = dict(gamma=gamma_range, C=C_range, class_weight=class_weight)
cv = KFold(n_splits=5, random_state = 5)
grid = GridSearchCV(SVC_rbf, param_grid=param_grid, cv=cv, n_jobs = 4)
grid.fit(X_train, y_train)
report(grid.cv_results_)
#%%
