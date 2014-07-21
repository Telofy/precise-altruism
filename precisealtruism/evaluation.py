# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import json
from random import random
from time import time
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC, NuSVC, LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from Stemmer import Stemmer
from .utils import Densifier, stemmed_tokens, load_corpus
from . import settings

METRIC = 'f1'

def crossvalidate(pipelines, documents, labels):
    for pipeline, parameters in pipelines:
        grid_search = GridSearchCV(
            pipeline, parameters, n_jobs=-1, verbose=1, cv=5, scoring='f1')
        grid_search.fit(documents, labels)
        for item in sorted(grid_search.grid_scores_,
                           key=lambda item: -item.mean_validation_score)[:10]:
            print(item)
        print('Best score: {:.3f}'.format(grid_search.best_score_))
        print('Best parameters set:')
        best_parameters = grid_search.best_estimator_.get_params()
        for param_name in sorted(parameters.keys()):
            print('\t{}: {!r}'.format(param_name, best_parameters[param_name]))


def run():
    documents, labels = load_corpus(settings.DATA_DIR)
    vectorizers = [(TfidfVectorizer(),
                    {'stop_words': (settings.LANGUAGE,),
                     'ngram_range': ((1, 2),),  # Removed (1, 1)
                     'tokenizer': (stemmed_tokens,)})]
    classifiers = [(SGDClassifier(),
                    {'loss': ('log', 'hinge', 'modified_huber',
                              'perceptron'),  # Removed loss², hinge²
                     'penalty': ('l2', 'elasticnet'),  # Removed l1
                     'alpha': (0.00001, 0.0001, 0.001),
                     'n_iter': (5, 50, 100, 250),
                     'shuffle': (True,)}),
                   #(RandomForestClassifier(),
                   # {'n_estimators': (7, 10, 15),
                   #  'min_samples_leaf': (1, 3, 5),
                   #  'max_depth': (None, 15),
                   #  'criterion': ('gini', 'entropy')}),
                   #(DecisionTreeClassifier(),
                   # {'max_features': (None, 'auto'),
                   #  'min_samples_leaf': (1, 3, 5),
                   #  'max_depth': (None, 15)}),
                   (LogisticRegression(),
                    {'C': (0.8, 1., 3., 10.)}),
                   #(GaussianNB(), {}),
                   #(SVC(),
                   # {'C': (1., 3., 10.),
                   #  'kernel': (b'rbf', b'poly'),
                   #  'gamma': (0.0, 0.001)}),
                   (NuSVC(),
                    {'nu': (0.3, 0.5, 0.8),
                     'kernel': (b'rbf', b'poly'),
                     'gamma': (0.0, 0.001)}),
                   (LinearSVC(),
                    {'C': (0.8, 1., 3., 10, 15)}),
                   #(KNeighborsClassifier(),
                   # {'n_neighbors': (3, 5, 7, 9, 11)}),
                   #(AdaBoostClassifier(),
                   # {'n_estimators': (40, 50, 60),
                   #  'learning_rate': (0.5, 1.)})
    ]
    pipelines = [(Pipeline([('vectorizer', vectorizer),
                            ('densifier', Densifier()),
                            ('scaler', StandardScaler()),
                            ('classifier', classifier)]),
                  dict([('vectorizer__' + key, value)
                        for key, value in params_v.items()] +
                       [('classifier__' + key, value)
                        for key, value in params_c.items()]))
                 for vectorizer, params_v in vectorizers
                 for classifier, params_c in classifiers]
    crossvalidate(pipelines, documents, labels)
