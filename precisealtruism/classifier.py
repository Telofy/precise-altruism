# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import json
from random import random
from time import time
from sklearn import cross_validation, svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.pipeline import Pipeline

DATADIR = 'data/'


class Densifier(object):
    def fit(self, X, y=None):
        pass
    def fit_transform(self, X, y=None):
        return self.transform(X)
    def transform(self, X, y=None):
        return X.toarray()


def preprocess(item):
    return item['_source']['content']['body_cleaned']


tuples = []
for cat in (True, False):
    with open(DATADIR + 'altruism.{}.json'.format(cat)) as json_file:
        tuples.extend((preprocess(item), cat)
                      for item in json.load(json_file))
documents, labels = zip(*sorted(tuples, key=lambda x: random()))

classifiers = [RandomForestClassifier(), LogisticRegression(),
               SGDClassifier(), AdaBoostClassifier(),
               svm.SVC(), svm.NuSVC(), svm.LinearSVC()]
for classifier in classifiers:
    start = time()
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(stop_words='english')),
        ('densifier', Densifier()),
        ('classifier', classifier)])
    # https://github.com/scikit-learn/scikit-learn/issues/1837
    precisions = cross_validation.cross_val_score(
        pipeline, documents, labels, cv=10, scoring='precision')
    recalls = cross_validation.cross_val_score(
        pipeline, documents, labels, cv=10, scoring='recall')
    precision, precision_std = precisions.mean(), precisions.std() * 2
    recall, recall_std = recalls.mean(), recalls.std() * 2
    f1_score = 2 * ((precision * recall) /
                    (precision + recall))
    f1_score_std = 2 * ((precision_std * recall_std) /
                        (precision_std + recall_std))  # Amidoinitrite?
    print(('{}\nPrecision: {:.2} ± {:.2}\n'
               'Recall: {:.2} ± {:.2}\n'
               'F1 score: {:.2} ± {:.2}').format(
        classifier, precision, precision_std,
        recall, recall_std, f1_score, f1_score_std))
    print('Time: {:.2f} s\n'.format(time() - start))

# Old stuff, for reference, then to be deleted.
#
#cutoff = int(len(documents) / (10/8))
#train_documents = documents[:cutoff]
#train_labels = labels[:cutoff]
#test_documents = documents[cutoff:]
#test_labels = labels[cutoff:]
#
#classifier = LogisticRegression()
#vectorizer = TfidfVectorizer()
#pipeline = Pipeline([
#    ('vectorizer', vectorizer),
#    ('classifier', classifier)])
#
#train_feature_matrix = vectorizer.fit_transform(train_documents, train_labels)
#classifier.fit(train_feature_matrix, train_labels)
#
#test_feature_matrix = vectorizer.transform(test_documents)
#labels = classifier.predict(test_feature_matrix)
#
#print(test_labels)
#print(list(labels))
