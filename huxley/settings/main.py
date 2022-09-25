# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import os
import sys
from .roots import HUXLEY_ROOT

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(n(p(m6@(9&y-m+6k@ca%y2f3u%7+gzqctb5x&5@0c3653a1jg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMINS = (('BMUN Tech Officer', 'tech@bmun.org'))
ADMIN_SECRET = 'OVERRIDE THIS IN PRODUCTION'

SITE_ID = 1

# True only when testing is run from command line
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'huxley.core',
    'huxley.api',
    'huxley.accounts',
    'huxley.www',
    'huxley.logging',
    'django_celery_results',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'huxley.logging.middleware.LoggingMiddleware',
    'huxley.logging.middleware.ExceptionLoggerMiddleware',
]

ROOT_URLCONF = 'huxley.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            '%s/templates/' % HUXLEY_ROOT,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'huxley.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'huxley.accounts.backends.LoginAsUserBackend'
)

AUTH_USER_MODEL = 'accounts.User'


EMAIL_BACKEND = 'huxley.logging.mail.DevLoggingEmailBackend'


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = '%s/static/' % HUXLEY_ROOT
STATIC_URL = '/static/'

# Google Sheets integration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'huxley/service.json'
SHEET_ID = None

# Smartwaiver integration
SMARTWAIVER_API_KEY = None

# Celery Configuration Options
CELERY_RESULT_BACKEND = 'django-db'

# Intuit Keys
CLIENT_ID = "AB6M8vUqtDAsPaooTFWYk81NztxLFyRQR2ms6B8IL3hkwBttp6"
CLIENT_SECRET = "EjKoGCduPuNfgNxRw4jN1GQkTpO3vsd8CigRIxet"
REFRESH_TOKEN = "AB11672268887ziHd3PUdT3wPTInEzvAbMXLSbEPj9rNzlJS0s"
REALM_ID = "1404322785"
ACCESS_TOKEN = "eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..2_ehM6_w3D_C0w2idJ8_lw.79ayeD1bHQw1kMIvCgrrov0Vfb5rUYOOmiDf7ibF6EblAY0LxXmvScevkV4gpbqzT5c0P05VU0-8fPGRbiiCCB7XD6cIUktCh6VGpvd8ZtWLfOwX8zfkY-cn6l6sm_3w1nysuPgdgzuMpCJOHVsyc5MzMJYLQ4-vCjigpB5wK2vKnrTbTcWWXcJSMUAeZ7n_nXNV-ewPNgi8AnHT-0fOkJh_l7oQlSPlCLzWpRmzoCXtw7bQ4RxG30P-TAucZ_SmjQWv_WCtAHGpAs7lRhU5LAORcrq8pIyeXgJj6RgqPXjOIsl1JvTWaQ-9o0Is65NIlHWH1Iy0oBKe-VHZBQu_I7LP61lnihNT_qm0BRMuxTa_8BtcJbVD8BE04pojPC6Wxf52cWX3DB05yvvPnF9sGa_fQ7IE2iU36-mRW6sMrfyRBxTTkdvvD_yDSpfw72wNiqgUyqp_Qfl67uGNcLh4e88sRmfAlYLu-2G72rl-_I36MEM1oquEon4u17q8713XNUV1RNNrPwlWtmjMRlCRpbdH07WuEOKe_3bcu1OPISW3MAUzpb3ajbPwiiy24R3nenitQmHluUtGst8vINQj5L_frR9Lqkmt02Iu3-TRZyENni4Cf9glXWFxlJL2buFDjtOssLGWD4QfHY1fXw2-teJfUADdqMAg_sWTDgX5V3Q_cLnuXq_tzyzJFW4Byk0vGSeBSAwc1WQM44S89AdaXuUKWTy2MChNV0BJx3Y47VI.DUrt1Ps1-qQVpy5XswejGg"
