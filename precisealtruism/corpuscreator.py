import argparse
import csv
import json
import os.path
from copy import copy

TEAM_SIZE = 2

def select(dictionary, keys):
    dict_ = copy(dictionary)
    for key in keys:
        dict_ = dict_.get(key, {})
    return key, dict_

def run():
    # python corpuscreator.py --modulo 0 link_url content.title content.body
    # https://docs.python.org/dev/library/argparse.html
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
        catreader = csv.reader(csv_file, delimiter='\t')
        done = set()
        for row in catreader:
            if len(row) > 0:
                done.add(row[0])
    with open('categorization.csv', 'a+') as csv_file:
        catwriter = csv.writer(csv_file, delimiter='\t')
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
                cat_ = input('Is this article interesting for someone '
                             'interested in charity? (y[es]/n[o]/s[kip]) ')
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

if __name__ == '__main__':
    run()