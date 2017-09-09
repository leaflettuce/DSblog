#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals


AUTHOR = u'Andrew Trick'

SITENAME = u'Andrew Trick'
SITEURL = 'http://localhost:8000'
BANNER_SUBTITLE = u"Projects and explorations into the subjects of data science."


PATH = 'content'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll

LINKS = None

#(('Home','/index.html'),
#('About','/pages/about.md'),)

# Social widget
SOCIAL = (('email','mailto:andyjtrick@gmail.com', 'envelope-o'),
		('linkedin', 'https://www.linkedin.com/in/andrew-trick-916011134'),
        ('github', 'https://github.com/leaflettuce'),
		('kaggle', 'https://www.kaggle.com/leaflettuce', 'database'),
		('instagram', 'https://www.instagram.com/andyjtrick/'),
		('meetup', 'https://www.meetup.com/members/13019733/', 'meetup'),
        )

		  
DEFAULT_PAGINATION = 6

SUMMARY_MAX_LENGTH = 500

DEFAULT_DATE = 'fs'

PYGMENTS_STYLE = 'friendly'

STATIC_PATHS = ['img', 'css', 'js', 'extra/custom.css', 'data', 'extra/tdwp_shows.css', 'extra/names_search.css']

THEME = 'pelican-bootstrap3'

DELETE_OUTPUT_DIRECTORY = True

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
DISPLAY_CATEGORIES_ON_SIDEBAR       = True

MARKUP = ('md', 'ipynb')

PLUGIN_PATHS = ['./plugins']

PLUGINS = ['ipynb.markup', 'assets', 'i18n_subsites', 'tag_cloud', 'pelican_javascript', 'pelican_dynamic']

#JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
#I18N_SUBSITES = {}

BOOTSTRAP_THEME = 'journal'

#SITELOGO = 'img/profile_book_square.png'
#ABOUT_ME = 'Touring and playing music with TDWP. Student in data science.'
#AVATAR = 'img/profile_book_square.png'

DISPLAY_CATEGORIES_ON_MENU = False

DISPLAY_TAGS_ON_SIDEBAR = True
TAG_CLOUD_MAX_ITEMS = 10
DIRECT_TEMPLATES = ('index', 'categories', 'authors', 'archives', 'search')
#BOOTSTRAP_NAVBAR_INVERSE = True
BANNER = 'img/banner.jpg'

YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
SHOW_ARTICLE_CATEGORY = True
#FAVICON = 'images/favicon.png'

#DISPLAY_ARTICLE_INFO_ON_INDEX = True

#DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
RECENT_POST_COUNT = 3

FEED_USE_SUMMARY = True
#DISABLE_SIDEBAR_TITLE_ICONS = True

DISPLAY_TAGS_INLINE = False

CUSTOM_CSS = 'static/custom.css'
EXTRA_PATH_METADATA = {'extra/custom.css':{'path':'static/custom.css'},
						'extra/tdwp_shows.css':{'path':'static/tdwp_shows.css'},
						'extra/names_search.css':{'path':'static/names_search.css'}}