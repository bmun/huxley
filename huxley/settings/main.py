# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from os.path import dirname

HUXLEY_ROOT = dirname(dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (('BMUN Tech Officer', 'tech@bmun.org'))
ADMIN_SECRET = 'OVERRIDE THIS IN PRODUCTION'
SECRET_KEY = '+42lz(cp=6t#dzpkah^chn760l)rmu$p&f-#7ggsde2l3%fm-i'
MANAGERS = ADMINS

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '%s/huxley.db' % HUXLEY_ROOT, # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

ROOT_URLCONF = 'huxley.urls'

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False

MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATIC_ROOT = '%s/static/' % HUXLEY_ROOT
STATIC_URL = '/static/'

STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'huxley.core.context_processors.conference',
    'huxley.core.context_processors.user_type',
    'huxley.core.context_processors.default_path',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    '%s/templates/' % HUXLEY_ROOT,
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'huxley.core.middleware.LatestConferenceMiddleware',
    'huxley.accounts.middleware.EnforceUserTypeMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'huxley.accounts.backends.LoginAsUserBackend'
)

AUTH_USER_MODEL = 'accounts.HuxleyUser'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'huxley.core',
    'huxley.accounts',
    'huxley.advisors',
    'huxley.chairs',
    'pipeline',
    'south',
)
