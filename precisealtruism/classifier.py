# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from .utils import Densifier, tokenize, load_corpus

DATADIR = 'data/'

word_re = re.compile(r'(?u)\b\w\w+\b', flags=re.UNICODE)

documents, labels = load_corpus(DATADIR)
pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer(stop_words='english', tokenizer=tokenize)),
    ('densifier', Densifier()),
    ('classifier', SGDClassifier())])
pipeline.fit_transform(documents, labels)
