# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

PIPELINE_COMPILERS = (
  'pipeline.compilers.sass.SASSCompiler',
)

PIPELINE_CSS_COMPRESSOR = None

PIPELINE_JS_COMPRESSOR = None

PIPELINE_CSS = {
    'huxley': {
        'source_filenames': (
            'css/*.css',
            'scss/*.scss'
        ),
        'output_filename': 'css/huxley.css'
    },
}

PIPELINE_JS = {
    'jquery': {
        'source_filenames': (
            'js/jquery/*.js',
        ),
        'output_filename': 'js/jquery.js'
    },
    'huxley': {
        'source_filenames': (
            'js/jquery-plugins/*.js',
            'js/core/*.js',
            'js/advisors/*.js',
            'js/chairs/*.js',
        ),
        'output_filename': 'js/huxley.js'
    }
}