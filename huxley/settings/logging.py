# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s: %(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'database': {
            'level': 'DEBUG',
            'class': 'huxley.logging.handlers.DatabaseHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'loggers': {
        'huxley': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'huxley.server': {
            'handlers': ['database', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'huxley.db': {
            'handlers': ['database'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
