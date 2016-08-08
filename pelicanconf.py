#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Daniel Wayne Armstrong'
SITENAME = 'Circuidipity'
SITEURL = ''

TIMEZONE = 'America/Toronto'

DEFAULT_LANG = 'en'

DEFAULT_DATE_FORMAT = '%A %d %B %Y'

# Static paths will be copied without parsing their contents
STATIC_PATHS = ['images', 'extra']

# Shift the installed location of a file
EXTRA_PATH_METADATA = {
        'extra/CNAME': {'path': 'CNAME'},
        }

# Extract post date from filename
FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})'

# Sole author and don't use categories ... disable these features
AUTHOR_SAVE_AS = False
AUTHORS_SAVE_AS = False
CATEGORY_SAVE_AS = False
CATEGORIES_SAVE_AS = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# URL settings
# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
ARTICLE_URL = '{slug}.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
TAG_URL = 'tag-{slug}.html'
TAG_SAVE_AS = 'tag-{slug}.html'
TAGS_URL = 'tags.html'
TAGS_SAVE_AS = 'tags.html'
PROJECTS_URL = 'projects.html'
PROJECTS_SAVE_AS = 'projects.html'

# Contact
EMAIL_ADDR = 'daniel at circuidipity dot com'

# Plugins
PLUGIN_PATHS = ['/home/dwa/code/pelican-plugins']
PLUGINS = ['neighbors', 'tag_cloud']

# Theme
THEME = '/home/dwa/code/pelican-themes/clearwater'
WHOAMI_URL = '/theme/images/whoami.png'
MINIME_URL = '/theme/images/minime.png'
GREETING = 'Howdy!'
LICENCE_NAME = 'CC BY-NC-SA'
LICENCE_URL = 'http://creativecommons.org/licenses/by-nc-sa/4.0/'
#LICENCE_URL_IMG = 'http://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png'
COPYRIGHT = '2016'
JINJA_EXTENSIONS = ['jinja2.ext.loopcontrols']

# Social
TWITTER_URL = 'https://twitter.com/circuidipity'
GITHUB_URL = 'https://github.com/vonbrownie'

# Tag cloud
TAG_CLOUD_STEPS = 4
TAG_CLOUD_SORTING = 'alphabetically'

#DEFAULT_PAGINATION = 10
