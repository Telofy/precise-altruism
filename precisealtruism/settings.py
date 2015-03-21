# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

FEEDS = [
    'http://yoursiblings.org/blog/feeds/',
    'http://claviger.net/feeds/all.atom',
    'https://www.againstmalaria.com/News.ashx',
    'http://feeds.feedburner.com/TheGivewellBlog',
    'http://www.givewell.org/rss.xml',
    'http://www.givedirectly.org/blog_feed.php',
    'http://www.givingwhatwecan.org/blog.xml',
    'http://www.charityscience.com/1/feed',
    'http://80000hours.org/blog/feed.atom',
    'http://davidroodman.com/feed/atom/',
    'http://feeds.feedburner.com/TheLifeYouCanSave',
    'http://effective-altruism.com/.rss',
    'http://www.animalcharityevaluators.org/feed/atom/',
    'http://www.povertyactionlab.org/news.xml',
    'http://www.povertyactionlab.org/evaluations.xml',
    'http://www.povertyactionlab.org/publications.xml',
    'http://www.cgdev.org/cgd/feed',
    'http://sentience.ch/en/feed/',
    'http://globalprioritiesproject.org/feed/atom/',
    'http://www.gatesnotes.com/rss',
    'http://www.evidenceaction.org/blog-full/?format=rss',
    'http://www.who.int/feeds/entity/mediacentre/news/en/rss.xml',
    'http://reg-charity.org/feed/atom/',
    'http://www.goodventures.org/feeds/all',
    'http://www.poverty-action.org/blog/feed/atom',
    'http://veganoutreach.org/feed/atom/',
    'http://www.fhi.ox.ac.uk/news-archive/feed/atom/',
    'http://www.animalequality.net/rss.xml',
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
