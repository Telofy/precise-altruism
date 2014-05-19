# -*- encoding: utf-8 -*-
import argparse
import json
import csv
from copy import copy

TEAM_SIZE = 2
RAW_FILES = ('altruism.2014-05-13.json',
             'charity.2014-05-13.json',
             'generic.2014-05-13.json')

def select(dictionary, keys):
    dict_ = copy(dictionary)
    for key in keys:
        dict_ = dict_.get(key, {})
    return key, dict_

def run():
    # python corpuscreator.py --mod 0 link_url content.title content.body
    # https://docs.python.org/dev/library/argparse.html
    parser = argparse.ArgumentParser(description='Helps us create a corpus.')
    parser.add_argument('-m', '--mod',
                        help='Modulo of choice of the team member.')
    parser.add_argument('key', nargs='+', help='Keys like content.body')
    args = parser.parse_args()
    # args.key
    data = []
    for raw_file in RAW_FILES:
        with open(raw_file) as json_file:
            data.extend(json.load(json_file)['hits']['hits'])
    # If mod is given, categorize only documents that are in the specified 'Restklasse'
    if args.mod:
        data = data[int(args.mod[0])::TEAM_SIZE]
        #print type(args.mod[0])
    # Start categorization
    with open('categorization.csv', 'a+') as csv_file:
        # Read the documents that were already categorized and are to
        # be excluded in the following categorization (also if they were skipped!)
        catreader = csv.reader(csv_file, delimiter = ';')
        done = []
        for row in catreader:
            if len(row) > 0:
                done.append(row[0])
        catwriter = csv.writer(csv_file, delimiter=';')
        # Do the categorization for uncategorized documents
        for hit in data:
            hit_data = {}
            for keys in args.key:
                the_key, value = select(hit['_source'], keys.split('.'))
                hit_data[the_key] = value
            if hit_data['link_url'] in done:
                continue
            print hit_data['title']
            print hit_data['body']
            print hit_data['title']
            # Ask for input and check if it is valid (i.e. if input \in {'y', 'n', 's'})
            valid = False
            while not valid:
                cat_ = raw_input("Is this article interesting for someone interested in charity? (y[as]/n[o]/s[kip] ")
                if cat_ == 'y':
                    catwriter.writerow([hit_data.get('link_url'), 1])
                    valid = True
                elif cat_ == 'n':
                    catwriter.writerow([hit_data.get('link_url'), 0])
                    valid = True
                elif cat_ == 's':
                    catwriter.writerow([hit_data.get('link_url'), 2])
                    valid = True
                else: print "Invalid choice, try again.\n"

if __name__ == '__main__':
    run()
