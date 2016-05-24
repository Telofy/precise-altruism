# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import logging

logging.basicConfig(
    format='%(asctime)s: %(levelname)s:'
           ' %(funcName)s (%(thread)d):'
           ' %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
