# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import json
import re
from random import random
from time import time
from sklearn import cross_validation
from sklearn.svm import SVC, NuSVC, LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from Stemmer import Stemmer

DATADIR = 'data/'
METRIC = 'f1'

stemmer = Stemmer('english')
word_re = re.compile(r'(?u)\b\w\w+\b', flags=re.UNICODE)


class Densifier(object):
    def fit(self, X, y=None):
        pass
    def fit_transform(self, X, y=None):
        return self.transform(X)
    def transform(self, X, y=None):
        return X.toarray()


def preprocess(item):
    return item['_source']['content']['body_cleaned']

def tokenize(document):
    return stemmer.stemWords(word_re.findall(document))

def load_corpus(datadir):
    tuples = []
    for cat in (True, False):
        with open(datadir + 'altruism.{}.json'.format(cat)) as json_file:
            tuples.extend((preprocess(item), cat)
                          for item in json.load(json_file))
    return zip(*sorted(tuples, key=lambda x: random()))

#Get development set for grid search:
X_dev, X_test, Y_dev, Y_test = train_test_split(data, labels, test_size=0.5)
'''
params = [
         {
          'classifier__n_estimators': (7,10,15),
          'classifier__min_samples_leaf': (1,3,5),
          'classifier__max_depth': (None, 15),
          'classifer__criterion': ("gini", "entropy")
         },
         {
          'classifier__max_features': (None, "auto")
          'classifier__min_samples_leaf': (1,3,5)
          'classifier__max_depth': (None, 15)
         },
         {
          'classifier__n_estimators': (40,50,60)
          'classifier__learning_rate': (0.5,1.)
         },
         {
          'classifier__C': (0.8, 1., 3., 10.)
         },
         {
          'classifier__loss': ('log', 'squared_loss')
          'classifier__penalty': ('l2', 'elasticnet')
          'classifier__alpha': (0.0001, 0.001, 0.1)
          'classifier__eta0': (0.001, 0.01, 0.1)
         },
         {
          'classifier__C': (1., 3., 10.)
          'classifier__kernel': ('rbf', 'poly')
          'classifier__gamma': (0.0, 0.001)
         },
         {
          'classifier__nu': (0.3, 0.5, 0.8)
          'classifier__C': (1., 3., 10.)
          'classifier__kernel': ('rbf', 'poly')
          'classifier__gamma': (0.0, 0.001)
         },
         {
          LINEAR SVM
         },
         {
          K-NN
         },
         {
          'classifier__n_estimators': (40,50,60)
          'classifier__learning_rate': (0.5,1.)
         }
        ]
''' 

def crossvalidate(classifiers, documents, labels):
    i = 0
    for classifier in classifiers:
        #perform gridsearch, s.t. classifier uses optimal params
        #classifier = GridSearchCV(classifier, params[i], cv = 5)
        start = time()
        pipeline = Pipeline([
            ('vectorizer', TfidfVectorizer(stop_words='english')),
            ('densifier', Densifier()),
            ('classifier', classifier)])
        print(pipeline.named_steps['vectorizer'])
        print(pipeline.named_steps['classifier'])
        scores = cross_validation.cross_val_score(
            pipeline, documents, labels, cv=10, scoring='f1')
        score, score_std = scores.mean(), scores.std() * 2
        print('{}: {:.2} ± {:.2}'.format(METRIC.capitalize(), score, score_std))
        print('Time: {:.2f} s\n'.format(time() - start))
        i = i+1
def run():
    documents, labels = load_corpus(DATADIR)
    classifiers = [RandomForestClassifier(), DecisionTreeClassifier(),
                   LogisticRegression(), SGDClassifier(shuffle=True),
                   GaussianNB(), SVC(), NuSVC(), LinearSVC(),
                   KNeighborsClassifier(), AdaBoostClassifier()]
    crossvalidate(classifiers, documents, labels)
