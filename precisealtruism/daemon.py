# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import json
import re
import requests
import feedparser
from collections import defaultdict
from copy import copy
from HTMLParser import HTMLParser
from itertools import cycle
from time import sleep
from urlparse import urlparse, urlunparse, parse_qs
from bs4 import BeautifulSoup
from readability import Document
from slugify import slugify
from sumy.parsers.html import HtmlParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words
from tumblpy import Tumblpy, TumblpyAuthError
from .classifier import pipeline
from .models import Entry, Session
from .logger import logger
from . import settings

session = Session()
unescape = HTMLParser().unescape
tumblr = Tumblpy(settings.CONSUMER_KEY, settings.CONSUMER_SECRET,
                 settings.OAUTH_TOKEN, settings.OAUTH_SECRET)

# Summarization
tokenizer = Tokenizer(settings.LANGUAGE)
stemmer = Stemmer(settings.LANGUAGE)  # Probably slower than ours
summarizer = LsaSummarizer(stemmer)
summarizer.stop_words = get_stop_words(settings.LANGUAGE)

def summarize(entry, count):
    clean = lambda sentence: re.sub(r' (?:[;,:.!?])', '', unicode(sentence))
    parser = HtmlParser.from_string(entry.content, entry.url, tokenizer)
    sentences = map(clean, summarizer(parser.document, count))
    return '<ul>{}</ul>'.format(''.join(
        '<li>{}</li>'.format(sentence) for sentence in sentences))

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
        if entry['content']:
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
    def nub(self):
        for entry in self.entries:
            if not session.query(Entry).filter_by(uid=entry.uid).count():
                yield entry

    @update('entries')
    def complement(self):
        for entry in self.entries:
            if len(entry.content) < 1000:
                response = requests.get(entry.url, timeout=10)
                document = Document(response.content, url=response.url)
                entry.content = document.summary()
                entry.title = document.short_title()
            yield entry

    @update('entries')
    def classify(self):
        for entry in self.entries:
            content_cleaned = BeautifulSoup(entry.content).get_text()
            entry.classification = pipeline.predict([content_cleaned])[0]
            yield entry


def run():
    for url in cycle(settings.FEEDS):
        try:
            tumblr.get('followers', settings.BLOG)
        except TumblpyAuthError:
            # The API always raises 401 Not Authorized on errors.
            # This should always work on our own Tumblrs and helps
            # distinguish authorization errors from other errors.
            logger.error('Error connecting to %s', self.blog, exc_info=True)
            sleep(settings.SLEEP_TIME)
            continue
        try:
            source = Source(url).clean().nub().complement().classify()
        except UnchangedException:
            sleep(settings.SLEEP_TIME)
            continue
        entries = list(source.entries)
        session.add_all(entries)
        session.commit()  # So entries aren’t posted
                          # indefinitely if saving fails
        # So not to spam Tumblr when a new feed is added
        relevant_entries = [entry for entry in entries
                            if entry.classification][:3]
        for entry in relevant_entries:
            params = {
                'slug': slugify(entry.title, to_lower=True),
                'tags': 'charity,altruism',  # Needs more fance
                'type': 'link',
                'url': entry.url,
                'source_url': entry.url,
                'title': unescape(entry.title),
                'description': summarize(entry, settings.SUMMARY_LENGTH)}
            try:
                post = tumblr.post('post', settings.BLOG, params=params)
            except TumblpyAuthError:  # 401 Not Authorized includes deleted
                logger.error('Error for %s:', entry.url, exc_info=True)
            else:
                logger.info('Posted %s as %s', entry.url, post['id'])
            # This way I can feed these directly into Ferret for possible
            # manual classification later on.
            print('{}: <url><loc>{}</loc><lastmod>{}</lastmod></url>'.format(
                entry.classification, entry.url, entry.updated.isoformat()))
        logger.info('Sleeping for %s s', settings.SLEEP_TIME)
        sleep(settings.SLEEP_TIME)
