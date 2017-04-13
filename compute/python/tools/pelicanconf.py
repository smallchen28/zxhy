#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# basic config
SITENAME = u'生命不息，折腾不止。'
SITEURL = 'http://10.43.174.141:8000'
PATH = 'content'
DELETE_OUTPUT_DIRECTORY = True
USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = u'未分类'
TYPOGRIFY = True
STATIC_PATHS = ['images']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


# Pagination config
DEFAULT_PAGINATION = 8

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True


# date and time config
TIMEZONE = 'Asia/Shanghai'
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_DATE = 'fs'  # use filesystem's mtime
DEFAULT_LANG = u'zh_CN'

# metadata config
AUTHOR = u'liuyx'

# themes config
THEME ='themes/voidy-bootstrap/'
SITESUBTITLE ='我的足迹.'
SITETAG = ""
STYLESHEET_FILES = ("pygment.css", "voidybootstrap.css",)

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('QQ', '#'),
          ('FACEBOOK', '#'),)

CUSTOM_ARTICLE_FOOTERS = ("taglist.html", "sharing.html", )
CUSTOM_SCRIPTS_ARTICLE = "sharing_scripts.html"
SIDEBAR = "sidebar.html"
