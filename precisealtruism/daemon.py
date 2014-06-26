# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import requests
import feedparser
from collections import defaultdict
from copy import copy
from time import sleep
from itertools import cycle
from sqlalchemy.sql import or_
from readability import Document
from .classifier import pipeline
from .models import Entry, Session
from .logger import logger
from . import settings

session = Session()


class UnchangedException(Exception):
    pass


class AltruismSource(object):

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
                published=entry.published,
                url=entry.link,
                source=url,
                title=entry.title,
                content=entry.content))

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
            url, timeout=10, headers=headers)
        response.raise_for_status()
        self.headers[url] = response.headers
        if response.status_code == 304:
            raise UnchangedException
        return response

    def clean():
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
        return self

    def nub(self):
        self.entries = []
        for entry in self.feed.entries:
            if not session.query(Entry).filter(
                    or_(Entry.uid == entry.id, Entry.url == entry.url)).count():
                self.entries.append(entry)
        return self

    def complement(self):
        for entry in self.entries:
            if len(entry.content.split(' ')) < 100:
                response = requests.get(self.url)
                document = Document(response.content, url=response.url)



    def classify(self):
        for entry in self.entries:
            entry.classification = pipeline.predict(entry.content)
        return self


def run():
    for url in cycle(feeds):
        entries = AltruismSource(url).clean().nub().classify().entries
        session.add_all(entries)
        session.commit()  # So entries aren’t posted
                          # indefinitely if saving fails
        for entry in entries:
            # TODO: Post to Tumblr
            print('{}: <url><loc>{}</loc><lastmod>{}</lastmod></url>'.format(
                entry.classification, entry.url, entry.updated.isoformat()))
        sleep(settings.SLEEP_TIME)
