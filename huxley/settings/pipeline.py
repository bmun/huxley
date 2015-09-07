# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from os.path import join

from .roots import PROJECT_ROOT


PIPELINE_COMPILERS = (
    'huxley.utils.pipeline.PySCSSCompiler',
    'pipeline_browserify.compiler.BrowserifyCompiler',
)

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'

PIPELINE_CSS = {
    'huxley': {
        'source_filenames': (
            'scss/core/*.scss',
            'scss/accounts/*.scss',
        ),
        'output_filename': 'css/huxley.css'
    },
}

PIPELINE_JS = {
    'huxley': {
        'source_filenames': (
            'js/huxley.browserify.js',
        ),
        'output_filename': 'js/huxley.js'
    }
}

PIPELINE_BROWSERIFY_BINARY = join(PROJECT_ROOT, 'node_modules/.bin/browserify')

PIPELINE_BROWSERIFY_ARGUMENTS = '-t babelify'

PIPELINE_UGLIFYJS_BINARY = join(PROJECT_ROOT, 'node_modules/.bin/uglifyjs')

PIPELINE_UGLIFYJS_ARGUMENTS = '--compress --mangle --screw-ie8'
