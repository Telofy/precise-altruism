# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

FEEDS = [
    'https://news.google.com/news/feeds?hl=en&q=charity|altruism|philanthropy&ie=UTF-8&num=10&output=atom',
    'http://feeds.feedburner.com/TheGivewellBlog',
    'http://80000hours.org/blog/feed.atom',
    'http://www.effective-altruism.com/feed/atom/',
]
RDB_SERVER = 'sqlite:///data/database.sqlite'
SLEEP_TIME = 5 * 60
