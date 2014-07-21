# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from .utils import Densifier, stemmed_tokens, load_corpus
from . import settings

word_re = re.compile(r'(?u)\b\w\w+\b', flags=re.UNICODE)

documents, labels = load_corpus(settings.DATA_DIR)
pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer(
        stop_words=settings.LANGUAGE,
        tokenizer=stemmed_tokens,
        ngram_range=(1, 2))),
    ('densifier', Densifier()),
    ('scaler', StandardScaler()),
    ('classifier', SGDClassifier(
        loss='perceptron',
        penalty='elasticnet',
        n_iter=20,
        alpha=0.001,
        shuffle=True))])
pipeline.fit_transform(documents, labels)
