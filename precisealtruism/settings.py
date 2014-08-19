# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

FEEDS = [
    'http://yoursiblings.org/blog/feeds/',
    'http://news.againstmalaria.com/syndication.axd?format=atom',
    'http://feeds.feedburner.com/TheGivewellBlog',
    'http://www.givedirectly.org/blog_feed.php',
    'http://www.givingwhatwecan.org/blog.xml',
    'http://80000hours.org/blog/feed.atom',
    'http://feeds.feedburner.com/TheLifeYouCanSave',
    'http://www.effective-altruism.com/feed/atom/',
    'http://www.animalcharityevaluators.org/feed/atom/',
    'http://www.kuerzr.com/feed/840ed599-007f-53ea-86ef-524ef7ff4d6f/atom.xml',
    'https://news.google.com/news/feeds?hl=en&q=charity|altruism|philanthropy&ie=UTF-8&num=10&output=atom',
]

BLOG = 'altrunews.claviger.net'
RDB_SERVER = 'sqlite:///data/database.sqlite'
MODEL_PICKLE = 'data/pipeline.pkl'
SLEEP_TIME = 5 * 60  # Seconds
LANGUAGE = 'english'
SUMMARY_LENGTH = 3
MAX_SIMILARITY = 0.8
DATA_DIR = 'data/'
STREAK_LIMIT = 1
MAX_AGE = 7  # Days

CONSUMER_KEY = None
CONSUMER_SECRET = None
OAUTH_TOKEN = None
OAUTH_SECRET = None

try:
    from .settings_override import *
except ImportError:
    pass
