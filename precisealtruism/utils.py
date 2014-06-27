# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import json
import re
from random import random
from Stemmer import Stemmer


class Densifier(object):

    def fit(self, X, y=None):
        pass

    def fit_transform(self, X, y=None):
        return self.transform(X)

    def transform(self, X, y=None):
        return X.toarray()

    def get_params(self, *args, **kwargs):
        return {}


stemmer = Stemmer('english')
word_re = re.compile(r'(?u)\b\w\w+\b', flags=re.UNICODE)

def tokenize(document):
    return stemmer.stemWords(word_re.findall(document))

def preprocess(item):
    return item['_source']['content']['body_cleaned']

def load_corpus(datadir):
    tuples = []
    for cat in (True, False):
        with open(datadir + 'altruism.{}.json'.format(cat)) as json_file:
            tuples.extend((preprocess(item), cat)
                          for item in json.load(json_file))
    return zip(*sorted(tuples, key=lambda x: random()))
