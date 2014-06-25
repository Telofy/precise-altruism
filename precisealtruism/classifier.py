# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import json
import re
from random import random
from time import time
from sklearn import cross_validation, svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
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

tuples = []
for cat in (True, False):
    with open(DATADIR + 'altruism.{}.json'.format(cat)) as json_file:
        tuples.extend((preprocess(item), cat)
                      for item in json.load(json_file))
documents, labels = zip(*sorted(tuples, key=lambda x: random()))

classifiers = [RandomForestClassifier(), LogisticRegression(),
               SGDClassifier(shuffle=True), AdaBoostClassifier(),
               svm.SVC(), svm.NuSVC(), svm.LinearSVC()]
for classifier in classifiers:
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
