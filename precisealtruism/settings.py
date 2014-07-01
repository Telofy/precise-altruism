# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

FEEDS = [
    'http://feeds.feedburner.com/TheGivewellBlog',
    'http://www.givingwhatwecan.org/blog.xml',
    'http://80000hours.org/blog/feed.atom',
    'http://feeds.feedburner.com/TheLifeYouCanSave',
    'http://www.effective-altruism.com/feed/atom/',
    'http://www.animalcharityevaluators.org/feed/atom/',
    'http://www.kuerzr.com/feed/840ed599-007f-53ea-86ef-524ef7ff4d6f/atom.xml',
    'https://news.google.com/news/feeds?hl=en&q=charity|altruism|philanthropy&ie=UTF-8&num=10&output=atom',
]

BLOG = 'altrunews.tumblr.com'
RDB_SERVER = 'sqlite:///data/database.sqlite'
SLEEP_TIME = 5 * 60
LANGUAGE = 'english'
SUMMARY_LENGTH = 5
MAX_SIMILARITY = 0.9
DATA_DIR = 'data/'
STREAK_LIMIT = 1

CONSUMER_KEY = None
CONSUMER_SECRET = None
OAUTH_TOKEN = None
OAUTH_SECRET = None

try:
    from .settings_override import *
except ImportError:
    pass
