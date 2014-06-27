# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import logging

NAME = 'precisealtruism'
LEVEL = logging.INFO

logger = logging.getLogger(NAME)
logger.setLevel(LEVEL)
logger.root.handlers[0].setFormatter(logging.Formatter(
    '%(asctime)s: %(levelname)s: %(funcName)s (%(thread)d): %(message)s'))

logger.root.setLevel(logging.WARNING)  # Readability fix
