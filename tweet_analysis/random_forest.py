#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 10:28:27 2017

@author: Chloechen
"""
### This script builds a random forest model for the sample dataset

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import itertools
import seaborn as sns
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint as sp_randint
import os
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
os.chdir("/Users/Chloechen/Desktop/tweet_analysis/data")
#%%
def random_forest(dataset):
    """
    find the optimal parameters from RandomSearchCV and fit it on the training dataset
    
    Argument: dataset (1~4)
    
    Return: Random_search result and feature importance dataframe
    """
    final_df = pd.read_csv("final_df_sample_" + str(dataset) + ".csv")
    features_df = final_df[final_df.columns[1:-2]]
    X = features_df.as_matrix()
    y = pd.factorize(final_df['label_model'])[0]
    y_df = pd.DataFrame(final_df.label_model)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
    clf = RandomForestClassifier(oob_score = True, n_jobs = -1)
    param_dist = {'max_features': ['auto', 'log2'],
              "n_estimators": sp_randint(10, 200),
              "min_samples_leaf": sp_randint(50, 200),
              "criterion": ["gini", "entropy"],
              'random_state': sp_randint(0, 20),
              'class_weight': [{0: 10}, {0: 20}]
              }

	# run randomized search
    n_iter_search = 30
    random_search = RandomizedSearchCV(clf, param_distributions=param_dist,
	                                   n_iter=n_iter_search, cv = 5)
    ran_search = random_search.fit(X_train, y_train)
    clf_best = ran_search.best_estimator_
    clf_best.fit(X_train, y_train)
    predicted = cross_val_predict(clf_best, X_train, y_train, cv = 5)
    y_pred = clf_best.predict(X_test)
    mac = metrics.accuracy_score(y_train, predicted)
    X_train_df = pd.DataFrame(X_train, columns = [features_df.columns])
    feature_list = list(zip(X_train_df, clf_best.feature_importances_))
    feature_df = pd.DataFrame(feature_list, columns = ["Features", "Feature_importance"])
    feature_df = feature_df.sort_values(['Feature_importance'], ascending = False)
    feature_df = feature_df.round(3)
    return y_df, y_test, y_pred, mac, ran_search, feature_df

#%%
def report(ran_search, n_top=3):
    """
    prints out the first three best parameters with the corresponding validation scores
    
    Argument: ran_search result
    
    Return: print the top three parameters results and the scores
    
    """
    results = ran_search.cv_results_
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
def plot_features(dataset):
    """
    create feature importance barplot
    
    Argument: dataset (1~4)
    
    Return: feature importance barplot
    """
    y_df, y_test, y_pred, mac, ran_search, feature_df = random_forest(dataset)
    ax = sns.barplot(x = "Feature_importance", y = "Features", data = feature_df)
    sns.plt.suptitle('Feature Importance Barplot for Sample Dataset_' + str(dataset))
    ax.set_xlabel("Feature_Importance")


#%%
### Use Reference in Scikit Learn
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

#%%
def create_confusion_matrix(y_test, y_pred, y_df, dataset):
    """
    create regular and normalized confusion matrix
    
    Argument: dataset
    
    Return: regular and normalized confusion matrix
    """

    cnf_matrix = confusion_matrix(y_test, y_pred)
    np.set_printoptions(precision = 2)
    class_names = np.unique(y_df)
    plt.figure()
    plot_confusion_matrix(cnf_matrix, class_names, title='Confusion matrix for Sample Dataset_' + str(dataset))
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                      title='Normalized confusion matrix for Sample Dataset_' + str(dataset))

#%%
# dataset = the number in the final_df name
dataset = 1
#%%
y_df, y_test, y_pred, mac, ran_search, feature_df = random_forest(dataset)

#%%
# print out the accuracy score
mac
#%%
report(ran_search, n_top=3)

#%%
plot_features(dataset)

#%%
create_confusion_matrix(y_test, y_pred, y_df, dataset)

