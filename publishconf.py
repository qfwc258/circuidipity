#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://www.circuidipity.com'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feed.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

FEED_MAX_ITEMS = 25

DELETE_OUTPUT_DIRECTORY = True
