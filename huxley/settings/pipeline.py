# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from os.path import join

from .roots import JS_ROOT, PROJECT_ROOT


PIPELINE = {
    'COMPILERS': (
        'huxley.utils.pipeline.PySCSSCompiler',
        'huxley.utils.pipeline.BrowserifyCompiler',
    ),

    'CSS_COMPRESSOR': 'pipeline.compressors.cssmin.CSSMinCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.uglifyjs.UglifyJSCompressor',

    'STYLESHEETS': {
        'huxley': {
            'source_filenames': (
                'scss/core/*.scss',
                'scss/accounts/*.scss',
            ),
            'output_filename': 'css/huxley.css',
        },
    },

    'JAVASCRIPT': {
        'huxley': {
            'source_filenames': (
                'js/huxley.browserify.js',
            ),
            'output_filename': 'js/huxley.js',
        },
    },

    'UGLIFYJS_BINARY': join(PROJECT_ROOT, 'node_modules/.bin/uglifyjs'),
    'UGLIFYJS_ARGUMENTS': '--compress --mangle --screw-ie8',

    'BROWSERIFY_BINARY': join(PROJECT_ROOT, 'node_modules/.bin/browserify'),
    'BROWSERIFY_ARGUMENTS': '-t babelify -t [detachkify -relativeTo %s]' % JS_ROOT,
}
