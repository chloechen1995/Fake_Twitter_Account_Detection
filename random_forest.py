#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 07:53:04 2017

@author: Chloechen
"""

# Reference: https://chrisalbon.com/machine-learning/random_forest_classifier_example_scikit.html
# Reference: Scikit Learn Website
#%%
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import itertools
#%%
os.chdir("/Users/Chloechen/Desktop/tweet_analysis")
user_features = pd.read_csv("sample_feature_guanyu.csv")
user_features['id'] = user_features['id'].astype(int)
user_features = user_features.drop('Unnamed: 0', 1)
network_features = pd.read_csv("sample_data_rachel.csv")
network_features = network_features.rename(columns = {'Unnamed: 0': 'id'})
network_features['id'] = network_features['id'].astype(int)
t_analysis_ratio = pd.read_csv("t_analysis_ratio.csv")
t_analysis_ratio = t_analysis_ratio.drop('Unnamed: 0', 1)
t_analysis_ratio['id'] = t_analysis_ratio['id'].astype(int)
similarity_ratio_1 = pd.read_csv("similarity_ratio_1.csv")
similarity_ratio_1 = similarity_ratio_1.drop('Unnamed: 0', 1)
similarity_ratio_1['id'] = similarity_ratio_1['id'].astype(int)
similarity_ratio_2 = pd.read_csv("similarity_ratio_2.csv")
similarity_ratio_2 = similarity_ratio_2.drop('Unnamed: 0', 1)
similarity_ratio_2['id'] = similarity_ratio_2['id'].astype(int)

user_tweets = t_analysis_ratio.merge(similarity_ratio_1, on = 'id').merge(similarity_ratio_2, on = 'id')

final_df = user_features.merge(network_features, on = 'id').merge(user_tweets, on = 'id')

final_df['no_tweet'] = np.where(final_df['similarity_ratio_1'] == "None", 1, 0)
#%%
final_df = final_df.replace([np.inf, -np.inf], np.nan)
final_df = final_df.replace({'No tweets': -1}, regex = True)
final_df = final_df.replace({'None': -1}, regex = True)
final_df = final_df.fillna(-1)

#%%
final_df[['tweet_rate', 'mobile_ratio', 'website_ratio', 'third_ratio', 'other_ratio', 'url_ratio', 'url_unique_ratio', 'hashtag_ratio', 'username_ratio', 'username_unique_ratio', 'similarity_ratio_1', 'similarity_ratio_2']] = final_df[['tweet_rate', 'mobile_ratio', 'website_ratio', 'third_ratio', 'other_ratio', 'url_ratio', 'url_unique_ratio', 'hashtag_ratio', 'username_ratio', 'username_unique_ratio', 'similarity_ratio_1', 'similarity_ratio_2']].astype(float)
#%%
cols = list(final_df.columns.values)
cols.pop(cols.index('label'))
final_df = final_df[cols+ ['label']]
final_df['label_model'] = np.where(final_df['label'] == 'genuine', 'Genuine', 'Fake')
#%%
features_df = final_df[final_df.columns[1:-2]]

#%%
### Build Random Forest Classifier Model
X = features_df.as_matrix()
y_df = pd.DataFrame(final_df.label)
y_m = y_df.as_matrix()
y = pd.factorize(final_df['label'])[0]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

#%%
# Train the random forest classifier
clf = RandomForestClassifier(n_jobs = 2, n_estimators = 100)
clf.fit(X_train, y_train)

#%%
clf.predict(X_test)

#%%
# Find the feature importance score
X_train_df = pd.DataFrame(X_train, columns = [features_df.columns])
feature_list = list(zip(X_train_df, clf.feature_importances_))

feature_df = pd.DataFrame(feature_list, columns = ["Features", "Feature_importance"])

feature_df.sort(['Feature_importance'], ascending = False)

#%%
# 10-Fold Cross Validation -- we randomly particioned the training data into 10 equal size subsamples

scores = cross_val_score(clf, X, y, cv = 10)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
#%%
#Obtaining predictions by cross-validation
predicted = cross_val_predict(clf, X, y, cv = 10)
metrics.accuracy_score(y, predicted)

#%%

# Since we find that some features do not contribute in predicting the label of an account, we will eliminate those from our model
new_feature = feature_df[feature_df['Feature_importance'] > 0]

#%%
new_feature_df = features_df[new_feature['Features']]

#%%
X_new = new_feature_df.as_matrix()
y_df = pd.DataFrame(final_df.label)
y_m = y_df.as_matrix()
y = pd.factorize(final_df['label'])[0]
X_train_new, X_test_new, y_train_new, y_test_new = train_test_split(X_new, y, test_size = 0.3, random_state = 0)

#%%
# Train the random forest classifier
clf_new = RandomForestClassifier(n_jobs = 2, n_estimators = 100)
clf_new.fit(X_train_new, y_train_new)

#%%
clf_new.predict(X_test_new)

#%%
# 10-Fold Cross Validation -- we randomly particioned the training data into 10 equal size subsamples

scores_new = cross_val_score(clf_new, X_new, y, cv = 10)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores_new.mean(), scores_new.std() * 2))
#%%
#Obtaining predictions by cross-validation
predicted_new = cross_val_predict(clf_new, X_new, y, cv = 10)
metrics.accuracy_score(y, predicted_new)

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
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

#%%
y_pred = clf.predict(X)
cnf_matrix = confusion_matrix(y, y_pred)
np.set_printoptions(precision = 2)

#%%
class_names = np.unique(y_df)
#%%
plt.figure()
#%%
plot_confusion_matrix(cnf_matrix, class_names)

#%%
# How to make the plot look better?
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                      title='Normalized confusion matrix')
#%%
# tuned parameters: number of trees, depth of the trees, number of features used for splitting, the minimum size of the parent node and the minimum size of the leaf node in a tree
tuned_parameters = {'n_estimators': [10, 50, 100, 150], 'max_features': ['auto', 'log2']}
clf_grid = GridSearchCV(estimator=clf, param_grid=tuned_parameters, cv = 5)
#%%
clf_grid.fit(X, y)
#%%
print clf_grid.best_params_

#%%
sorted(clf_grid.cv_results_.keys())