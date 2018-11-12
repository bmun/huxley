# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from .roots import HUXLEY_ROOT
import sys

DEBUG = True

DATA_UPLOAD_MAX_NUMBER_FIELDS = 3000

# IMPORTANT: Override this in local settings!
SECRET_KEY = '+42lz(cp=6t#dzpkah^chn760l)rmu$p&f-#7ggsde2l3%fm-i'

ADMINS = (('BMUN Tech Officer', 'tech@bmun.org'))
ADMIN_SECRET = 'OVERRIDE THIS IN PRODUCTION'

SITE_ID = 1

# True only when testing is run from command line
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

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
USE_I18N = False

EMAIL_BACKEND = 'huxley.logging.mail.DevLoggingEmailBackend'

STATIC_ROOT = '%s/static/' % HUXLEY_ROOT
STATIC_URL = '/static/'

STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        '%s/templates/' % HUXLEY_ROOT,
    ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.static',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'huxley.logging.middleware.LoggingMiddleware',
    'huxley.logging.middleware.ExceptionLoggerMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'huxley.accounts.backends.LoginAsUserBackend'
)

AUTH_USER_MODEL = 'accounts.User'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'huxley.core',
    'huxley.api',
    'huxley.accounts',
    'huxley.www',
    'huxley.logging',
)
