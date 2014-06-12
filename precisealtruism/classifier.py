import json
from random import random
from sklearn.cross_validation import ShuffleSplit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

DATADIR = 'data/'

def preprocess(item):
    return item['_source']['content']['body_cleaned']

tuples = []
for cat in (True, False):
    with open(DATADIR + 'altruism.{}.json'.format(cat)) as json_file:
        tuples.extend((preprocess(item), cat)
                      for item in json.load(json_file))
documents, labels = zip(*sorted(tuples, key=lambda x: random()))

train_documents = [doc for i, doc in enumerate(documents) if i % 10 <= 8]
train_labels = [label for i, label in enumerate(labels) if i % 10 <= 8]
test_documents = [doc for i, doc in enumerate(documents) if i % 10 > 8]
test_labels = [label for i, label in enumerate(labels) if i % 10 > 8]

classifier = LogisticRegression()
vectorizer = TfidfVectorizer()
pipeline = Pipeline([
    ('vectorizer', vectorizer),
    ('classifier', classifier)])

train_feature_matrix = vectorizer.fit_transform(train_documents, train_labels)
classifier.fit(train_feature_matrix, train_labels)

test_feature_matrix = vectorizer.transform(test_documents)
labels = classifier.predict(test_feature_matrix)

print(test_labels)
print(list(labels))

#classifier = LogisticRegression(...)
#vectorizer = TfidfVectorizer(...)
#documents = [...] of length n
#labels [...] of length n      e.g., [0, 0, 1, 0, 1]
#split documents and labels in train_documents, test_documents, train_labels, test_labels
#vectorizer.fit(train_documents, train_labels)
#feature_matrix = vectorizer.transform(test_documents)
#classifier.fit(feature_matrix, train_labels)
#labels = classifier.predict(test_documents)
#labels = [0, 1, 1, 0, ...]
