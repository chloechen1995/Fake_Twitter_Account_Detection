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
import seaborn as sns
#%%
os.chdir("/Users/Chloechen/Desktop/tweet_analysis/data")
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
#%%
tweet_time = pd.read_csv("tweet_time_dff.csv")
tweet_time = tweet_time.drop(tweet_time.columns[[0, 1]], 1)
tweet_time['id'] = tweet_time['id'].astype(int)
#%%
user_tweets = t_analysis_ratio.merge(similarity_ratio_1, on = 'id').merge(similarity_ratio_2, on = 'id')

final_df = user_features.merge(network_features, on = 'id').merge(user_tweets, on = 'id').merge(tweet_time, on = 'id')

final_df['no_tweet'] = np.where(final_df['similarity_ratio_1'] == "None", 1, 0)
#%%
final_df = final_df.replace([np.inf, -np.inf], 1000000)
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
#os.chdir("/Users/Chloechen/Desktop/tweet_analysis/data")
#final_df.to_csv("final_df_sample.csv", sep = ",")
#%%
features_df = final_df[final_df.columns[1:-2]]

#%%
### Build Random Forest Classifier Model
X = features_df.as_matrix()
y_df = pd.DataFrame(final_df.label_model)
y_m = y_df.as_matrix()
y = pd.factorize(final_df['label_model'])[0]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

#%%
# Train the random forest classifier
clf = RandomForestClassifier()

#%%
# tuned parameters: number of trees, depth of the trees, number of features used for splitting, the minimum size of the parent node and the minimum size of the leaf node in a tree
tuned_parameters = {'n_estimators': [10, 50, 100, 150, 200], 'max_features': ['auto', 'log2'], 'n_jobs': [-1, 1, 2], 'criterion': ["gini", "entropy"]}
clf_grid = GridSearchCV(estimator=clf, param_grid=tuned_parameters, cv = 5, n_jobs = -1)
#%%
clf_grid.fit(X_train, y_train)

#%%
print "The best parameters are %s" %clf_grid.best_params_

#%%
clf_best = RandomForestClassifier(max_features = 'log2', n_estimators = 100, n_jobs = 1, criterion = 'entropy', class_weight = {0:0.1, 1:0.9})
#%%
clf_best.fit(X_train, y_train)
#%%
# Find the feature importance score
X_train_df = pd.DataFrame(X_train, columns = [features_df.columns])
feature_list = list(zip(X_train_df, clf_best.feature_importances_))

feature_df = pd.DataFrame(feature_list, columns = ["Features", "Feature_importance"])

feature_df = feature_df.sort(['Feature_importance'], ascending = False)
#%%
feature_df.round(3)
#%%
ax = sns.barplot(x = "Feature_importance", y = "Features", data = feature_df)
ax.set_xlabel("Feature_Importance")
#%%
# 10-Fold Cross Validation -- we randomly particioned the training data into 10 equal size subsamples

scores = cross_val_score(clf_best, X, y, cv = 10)
#%%
#Obtaining predictions by cross-validation
predicted = cross_val_predict(clf_best, X, y, cv = 10)
mac = metrics.accuracy_score(y, predicted)
scores_dict = {"Cross_Validation_Score_Mean": scores.mean(), "Cross_Validation_Score_Sd": scores.std(), "Metrics_Accuracy_Score": mac}

#%%
scores_dict
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

#%%
y_pred = clf_best.predict(X)
cnf_matrix = confusion_matrix(y, y_pred)
np.set_printoptions(precision = 2)

#%%
class_names = np.unique(y_df)
#%%
plt.figure()
#%%
plot_confusion_matrix(cnf_matrix, class_names)

#%%
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                      title='Normalized confusion matrix')
