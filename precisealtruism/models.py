# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import re
import dateutil
import six
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Boolean, DateTime, Integer, Unicode
from . import settings

engine = create_engine(settings.RDB_SERVER)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)
    uid = Column(Unicode, unique=True, index=True,
        default=lambda context: context.current_parameters['url'])
    fetched = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)
    published = Column(DateTime, nullable=True)
    url = Column(Unicode, unique=True, index=True)
    source = Column(Unicode)
    title = Column(Unicode, default='')
    content = Column(Unicode, default='')
    classification = Column(Boolean, nullable=True)

    def __init__(self, **kwargs):
        # TODO: If I have a lot of time one day, I need to move this stuff
        # to a feedparser fork.
        if isinstance(kwargs.get('updated'), six.string_types):
            kwargs['updated'] = dateutil.parse(kwargs['updated'])
        if isinstance(kwargs.get('published'), six.string_types):
            kwargs['published'] = dateutil.parse(kwargs['published'])

    def __repr__(self):
        return '<Entry({}: {})>'.format(self.url, self.classification)
