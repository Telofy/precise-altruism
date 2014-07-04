# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import argparse
import csv
import json
import os.path
import six
from copy import copy
from six.moves import input

TEAM_SIZE = 2
SEPARATOR = '\t' if six.PY3 else b'\t'

def select(dictionary, keys):
    dict_ = copy(dictionary)
    for key in keys:
        dict_ = dict_.get(key, {})
    return key, dict_

def find_item(iterable, key, value):
    for item in iterable:
        try:
            if key(item) == value:
                return item
        except KeyError:
            pass
    raise KeyError('No item with key(item) == {!r}'.format(value))

def corpus_generation():
    parser = argparse.ArgumentParser(description='Actually creates a corpus.')
    parser.add_argument('datadir',
                        help='Directory for source and target files.')
    args = parser.parse_args()
    with open('categorization.csv') as csv_file:
        catreader = csv.reader(csv_file, delimiter=SEPARATOR)
        altruism = {True: [], False: []}
        sources = {}
        for row in catreader:
            url, cat, src, _ = row
            cat = {'True': True, 'False': False}.get(cat)
            if cat is None:
                continue
            try:
                source = sources[src]
            except KeyError:
                with open(os.path.join(args.datadir, row[2])) as json_file:
                    source = json.load(json_file)['hits']['hits']
                    sources[src] = source
            altruism[cat].append(find_item(
                source, lambda item: item['_source']['link_url'], url))
    for cat, items in altruism.items():
        print('{} items in category {}'.format(len(items), cat))
        filename = 'altruism.{}.json'.format(cat)
        with open(os.path.join(args.datadir, filename), 'w') as json_file:
            json.dump(items, json_file, indent=4)

def manual_classification():
    parser = argparse.ArgumentParser(description='Helps us create a corpus.')
    parser.add_argument('-m', '--modulo', type=int,
                        help='Modulo of choice of the team member.')
    parser.add_argument('-f', '--file',
                        help='Source file.')
    parser.add_argument('key', nargs='+', help='Keys like content.body')
    args = parser.parse_args()
    filename = os.path.basename(args.file)
    # args.key
    with open(args.file) as json_file:
        data = json.load(json_file)['hits']['hits']
    # If modulo is given, categorize only documents that are in the specified 'Restklasse'
    if args.modulo:
        data = data[int(args.modulo)::TEAM_SIZE]
        #print type(args.modulo)
    # Start categorization
    with open('categorization.csv', 'r') as csv_file:
        # Read the documents that were already categorized and are to
        # be excluded in the following categorization (also if they were skipped!)
        catreader = csv.reader(csv_file, delimiter=SEPARATOR)
        done = set()
        for row in catreader:
            if len(row) > 0:
                done.add(row[0])
    with open('categorization.csv', 'a+') as csv_file:
        catwriter = csv.writer(csv_file, delimiter=SEPARATOR)
        # Do the categorization for uncategorized documents
        for hit in data:
            link_url = hit['_source']['link_url']
            hit_data = []
            for keys in args.key:
                the_key, value = select(hit['_source'], keys.split('.'))
                hit_data.append((the_key, value))  # To maintain the order
            if link_url in done:
                continue
            print('\n------------------------------- '
                  'begin document'
                  ' -------------------------------\n')
            for key, value in hit_data:
                print(key + ':', value)
                print('\n')
            print('\n------------------------------- '
                  'end document'
                  ' -------------------------------\n')
            # Ask for input and check if it is valid (i.e. if input \in {'y', 'n', 's'})
            valid = False
            while not valid:
                cat_ = input('Is this article interesting for our'
                             ' envisioned reader? (y[es]/n[o]/s[kip]) ')
                if cat_ == 'y':
                    catwriter.writerow([link_url, True, filename, args.modulo])
                    valid = True
                elif cat_ == 'n':
                    catwriter.writerow([link_url, False, filename, args.modulo])
                    valid = True
                elif cat_ == 's':
                    catwriter.writerow([link_url, None, filename, args.modulo])
                    valid = True
                else: print('Invalid choice, try again.\n')
