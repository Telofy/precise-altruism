# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import json
import re
from random import random
from Stemmer import Stemmer
from nltk.stem.wordnet import WordNetLemmatizer
from . import settings


class Densifier(object):

    def fit(self, X, y=None):
        pass

    def fit_transform(self, X, y=None):
        return self.transform(X)

    def transform(self, X, y=None):
        return X.toarray()

    def get_params(self, *args, **kwargs):
        return {}


word_re = re.compile(r'(?u)\b\w\w+\b', flags=re.UNICODE)
stemmer = Stemmer(settings.LANGUAGE)
lemmatizer = WordNetLemmatizer()

tokenize = word_re.findall
stem = stemmer.stemWord
stem_all = stemmer.stemWords
lemmatize = lemmatizer.lemmatize

def stemmed_tokens(document):
    return stem_all(tokenize(document.lower()))

def lemmatized_tokens(document):
    return map(lemmatize, tokenize(document.lower()))

def preprocess(item):
    return '{}\n{}'.format(
        item['_source']['content']['title'],
        item['_source']['content']['body_cleaned'])

def load_corpus(datadir):
    tuples = []
    for cat in (True, False):
        with open(datadir + 'altruism.{}.json'.format(cat)) as json_file:
            tuples.extend((preprocess(item), cat)
                          for item in json.load(json_file))
    return zip(*sorted(tuples, key=lambda x: random()))
