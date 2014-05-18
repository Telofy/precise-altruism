# -*- encoding: utf-8 -*-
import argparse
import json
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
    parser.add_argument('-m', '--mod', nargs='+',
                        help='Modulo of choice of the team member.')
    parser.add_argument('key', nargs='+', help='Keys like content.body')
    args = parser.parse_args()
    # args.key
    data = []
    for raw_file in RAW_FILES:
        with open(raw_file) as json_file:
            data.extend(json.load(json_file)['hits']['hits'])
    categorization = {}
    for hit in data:
	hit_data = {}
	for keys in args.key:
	    the_key, value = select(hit['_source'], keys.split('.'))
	    hit_data[the_key] = value
	print hit_data['body']
	print hit_data['title']
	cat_ = raw_input("0 or 1? ")
	categorization[hit_data.get('link_url')] = int(cat_)
if __name__ == '__main__':
    run()
