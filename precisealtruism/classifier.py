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
               SGDClassifier(), AdaBoostClassifier(),
               svm.SVC(), svm.NuSVC(), svm.LinearSVC()]
for classifier in classifiers:
    start = time()
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(stop_words='english')),
        ('densifier', Densifier()),
        ('classifier', classifier)])
    print(pipeline.named_steps['vectorizer'])
    print(pipeline.named_steps['classifier'])
    # https://github.com/scikit-learn/scikit-learn/issues/1837
    precisions = cross_validation.cross_val_score(
        pipeline, documents, labels, cv=10, scoring='precision')
    precision, precision_std = precisions.mean(), precisions.std() * 2
    print('Precision: {:.2} ± {:.2}'.format(precision, precision_std))
    recalls = cross_validation.cross_val_score(
        pipeline, documents, labels, cv=10, scoring='recall')
    recall, recall_std = recalls.mean(), recalls.std() * 2
    print('Recall: {:.2} ± {:.2}'.format(recall, recall_std))
    f1_score = 2 * ((precision * recall) /
                    (precision + recall))
    f1_score_std = 2 * ((precision_std * recall_std) /
                        (precision_std + recall_std))  # Amidoinitrite?
    print('F1 score: {:.2} ± {:.2}'.format(f1_score, f1_score_std))
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
