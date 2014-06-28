# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

FEEDS = [
    'http://feeds.feedburner.com/TheGivewellBlog',
    'https://news.google.com/news/feeds?hl=en&q=charity|altruism|philanthropy&ie=UTF-8&num=10&output=atom',
    'http://80000hours.org/blog/feed.atom',
    'http://www.effective-altruism.com/feed/atom/',
]

BLOG = 'altrunews.tumblr.com'
RDB_SERVER = 'sqlite:///data/database.sqlite'
SLEEP_TIME = 5 * 60
LANGUAGE = 'english'
SUMMARY_LENGTH = 5
DATA_DIR = 'data/'

CONSUMER_KEY = None
CONSUMER_SECRET = None
OAUTH_TOKEN = None
OAUTH_SECRET = None

try:
    from .settings_override import *
except ImportError:
    pass
