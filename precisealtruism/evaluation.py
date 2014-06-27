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
from Stemmer import Stemmer
from .utils import Densifier, tokenize, load_corpus

DATADIR = 'data/'
METRIC = 'f1'

def crossvalidate(pipelines, documents, labels):
    for pipeline, parameters in pipelines:
        start = time()
        grid_search = GridSearchCV(
            pipeline, parameters, n_jobs=-1, verbose=1, cv=10, scoring='f1')
        grid_search.fit(documents, labels)
        print('Best score: {:.3f}'.format(grid_search.best_score_))
        print('Best parameters set:')
        best_parameters = grid_search.best_estimator_.get_params()
        for param_name in sorted(parameters.keys()):
            print('\t{}: {!r}'.format(param_name, best_parameters[param_name]))
        print('Time: {:.2f} s\n'.format(time() - start))

def run():
    documents, labels = load_corpus(DATADIR)
    vectorizers = [(TfidfVectorizer(), {'stop_words': (None, 'english'),
                                        'tokenizer': (tokenize,)})]
    classifiers = [(RandomForestClassifier(), {}),
                   (DecisionTreeClassifier(), {}),
                   (LogisticRegression(), {}),
                   (SGDClassifier(), {'penalty': ('l2', 'elasticnet'),
                                      'shuffle': (True,)}),
                   (GaussianNB(), {}),
                   (SVC(), {}),
                   (NuSVC(), {}),
                   (LinearSVC(), {}),
                   (KNeighborsClassifier(), {}),
                   (AdaBoostClassifier(), {})]
    pipelines = [(Pipeline([('vectorizer', vectorizer),
                            ('densifier', Densifier()),
                            ('classifier', classifier)]),
                  dict([('vectorizer__' + key, value)
                        for key, value in params_v.items()] +
                       [('classifier__' + key, value)
                        for key, value in params_c.items()]))
                 for vectorizer, params_v in vectorizers
                 for classifier, params_c in classifiers]
    crossvalidate(pipelines, documents, labels)
