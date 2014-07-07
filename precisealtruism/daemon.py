# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import json
import re
import sys
import requests
import feedparser
from collections import defaultdict
from copy import copy
from datetime import datetime, timedelta
from HTMLParser import HTMLParser
from itertools import cycle
from time import sleep
from urlparse import urlparse, urlunparse, parse_qs
from bs4 import BeautifulSoup
from readability import Document
from slugify import slugify
from sumy.parsers.html import HtmlParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words
from tumblpy import Tumblpy, TumblpyAuthError
from .classifier import pipeline
from .models import Entry, Session
from .logger import logger
from .utils import stem, lemmatized_tokens, stemmed_tokens
from . import settings

session = Session()
unescape = HTMLParser().unescape
tumblr = Tumblpy(settings.CONSUMER_KEY, settings.CONSUMER_SECRET,
                 settings.OAUTH_TOKEN, settings.OAUTH_SECRET)

# Summarization
tokenizer = Tokenizer(settings.LANGUAGE)
summarizer = LsaSummarizer(stem)
stop_words = set(get_stop_words(settings.LANGUAGE))
stop_words_stemmed = set(map(stem, stop_words))
summarizer.stop_words = stop_words

def summarize(entry, count):
    clean = lambda sentence: re.sub(r' (?:[;,:.!?])', '', unicode(sentence))
    parser = HtmlParser.from_string(entry.content, entry.url, tokenizer)
    sentences = map(clean, summarizer(parser.document, count))
    return '<ul>{}</ul>'.format(''.join(
        '<li>{}</li>'.format(sentence) for sentence in sentences))

def content_lemmas(string):
    return set(lemmatized_tokens(string)) - stop_words

def content_stems(string):
    return set(stemmed_tokens(string)) - stop_words_stemmed

def similarity(title0, title1):
    set0 = content_stems(title0)
    set1 = content_stems(title1)
    return len(set0 & set1) / len(set0 | set1)

def update(attribute):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self_ = copy(self)
            setattr(self_, attribute, result)
            return self_
        return wrapper
    return decorator


class UnchangedException(Exception):
    pass


class Source(object):

    headers = defaultdict(dict)

    def __init__(self, url):
        self.url = url
        self.response = self._fetch()
        self.feed = feedparser.parse(self.response.content)
        self.entries = []
        for entry in self.feed.entries:
            self.entries.append(Entry(
                uid=entry.id,
                updated=entry.updated,
                url=entry.link,
                source=url,
                title=unescape(entry.title),
                content=self._extract_content(entry)))

    @staticmethod
    def _extract_content(entry):
        if entry.get('content'):
            return entry['content'][0]['value']
        return entry['summary']

    def _fetch(self):
        # Friendly headers
        headers = {
            'if-modified-since':
                self.headers[self.url].get('last-modified'),
            'if-none-match':
                self.headers[self.url].get('etag')}
        # Retrieval
        logger.info('Requesting %s', self.url)
        response = requests.get(
            self.url, timeout=10, headers=headers)
        response.raise_for_status()
        self.headers[self.url] = response.headers
        if response.status_code == 304:
            raise UnchangedException
        return response

    @update('entries')
    def clean(self):
        for entry in self.entries:
            parsed_url = urlparse(entry.url)
            # Remove fragment
            cleaned_url = urlunparse(parsed_url[:-1] + ('',))
            # Degoogling
            if 'news.google.' in parsed_url.hostname:
                parsed_qs = parse_qs(parsed_url.query)
                cleaned_url = parsed_qs['url'][0]
                entry.content = ''
            entry.url = cleaned_url
            yield entry

    @update('entries')
    def since(self, date):
        for entry in self.entries:
            if entry.updated > date:
                yield entry

    @update('entries')
    def nub(self):
        old_entries = session.query(Entry) \
            .filter(Entry.classification==True) \
            .order_by(Entry.fetched.desc())[:50]
        for entry in self.entries:
            if not session.query(Entry).filter_by(uid=entry.uid).count():
                for old_entry in old_entries:
                    if similarity(entry.title, old_entry.title) \
                            > settings.MAX_SIMILARITY:
                        logger.info('Too similar: %s and %s (%s and %s)',
                                    entry.url, old_entry.url,
                                    entry.title, old_entry.title)
                        break
                else:  # No break
                    yield entry

    @update('entries')
    def complement(self):
        for entry in self.entries:
            response = requests.get(entry.url, timeout=10)
            document = Document(response.content, url=response.url)
            # Image extraction first
            document._html()  # Trigger parsing
            images = document.html.xpath(
                '//meta[@property="og:image"]/@content')
            images += document.html.xpath(
                '//meta[@name="twitter:image:src"]/@content')
            # Content extraction second
            entry.url = response.url
            entry.image = (images or [''])[0]
            entry.title = document.short_title()
            entry.content = document.summary()
            yield entry

    @update('entries')
    def classify(self):
        for entry in self.entries:
            content_cleaned = '{}\n{}'.format(
                entry.title, BeautifulSoup(entry.content).get_text())
            entry.classification = pipeline.predict([content_cleaned])[0]
            # This way I can feed these directly into Ferret for possible
            # manual classification later on.
            print('{}: <url><loc>{}</loc><lastmod>{}</lastmod></url>'.format(
                entry.classification, entry.url, entry.updated.isoformat()))
            sys.stdout.flush()
            yield entry


def run():
    for url in cycle(settings.FEEDS):
        try:
            tumblr.get('followers', settings.BLOG)
        except TumblpyAuthError:
            # The API always raises 401 Not Authorized on errors.
            # This should always work on our own Tumblrs and helps
            # distinguish authorization errors from other errors.
            logger.error('Error connecting to %s', settings.BLOG, exc_info=True)
            logger.info('Sleeping for %s s', settings.SLEEP_TIME)
            sleep(settings.SLEEP_TIME)
            continue
        try:
            min_date = datetime.utcnow() - timedelta(days=settings.MAX_AGE)
            # Nubbing twice because title might change
            source = Source(url).clean().since(min_date).nub() \
                .complement().nub().classify()
        except UnchangedException:
            logger.info('Feed unchanged')
            logger.info('Sleeping for %s s', settings.SLEEP_TIME)
            sleep(settings.SLEEP_TIME)
            continue
        entries = list(source.entries)
        session.add_all(entries)
        session.commit()  # So entries aren’t posted
                          # indefinitely if saving fails
        # So not to spam Tumblr when a new feed is added
        relevant_entries = [entry for entry in entries
                            if entry.classification][:settings.STREAK_LIMIT]
        for entry in relevant_entries:
            description = summarize(entry, settings.SUMMARY_LENGTH)
            if entry.image:
                image = ('<img src="{}" alt="{}"'
                         ' style="width: 150px; float: right;" />').format(
                            entry.image, entry.title)
                description = '{}\n{}'.format(image, description)
            params = {
                'slug': slugify(entry.title, to_lower=True),
                'tags': ','.join(
                    set(['altruism', 'charity', 'philanthropy'])
                    | content_lemmas(entry.title)),
                'type': 'link',
                'url': entry.url,
                'source_url': entry.url,
                'title': unescape(entry.title),
                'tweet': '{}\n[URL]'.format(
                    unescape(entry.title)),
                'description': description}
            try:
                post = tumblr.post('post', settings.BLOG, params=params)
            except TumblpyAuthError:  # 401 Not Authorized includes deleted
                logger.error('Error for %s:', entry.url, exc_info=True)
            else:
                logger.info('Posted %s as %s', entry.url, post['id'])
        logger.info('Sleeping for %s s', settings.SLEEP_TIME)
        sleep(settings.SLEEP_TIME)
